"""Persistent capture schedules and local-time occurrence calculation."""
from __future__ import annotations

import json
import math
import os
import re
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4
from zoneinfo import ZoneInfo

from astral import Observer
from astral.sun import sunset
from croniter import CroniterBadDateError, croniter

HISTORY_LIMIT = 100
CRON_LOOKBACK = timedelta(minutes=90)


def validate_cron(value: Any) -> str:
    """Validate deterministic, standard five-field cron expressions."""
    if not isinstance(value, str) or len(value) > 120:
        raise ValueError("Cron expression must contain five fields")
    expression = " ".join(value.split()).lower()
    fields = expression.split(" ")
    if len(fields) != 5:
        raise ValueError("Cron expression must contain five fields: minute hour day month weekday")
    for index, field in enumerate(fields):
        names = r"jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec" if index == 3 else (
            r"mon|tue|wed|thu|fri|sat|sun" if index == 4 else r"(?!)"
        )
        stripped = re.sub(names, "", field)
        if not stripped or re.search(r"[^0-9*,/\-]", stripped):
            # A name-only month or weekday is valid; arbitrary letters are not.
            if stripped or not re.fullmatch(names, field):
                raise ValueError("Cron supports numbers, names, *, ranges, lists and steps")
    if not croniter.is_valid(expression):
        raise ValueError("Invalid cron expression")
    try:
        croniter(expression, datetime(2024, 1, 1), max_years_between_matches=50).get_next(datetime)
    except (ValueError, CroniterBadDateError) as err:
        raise ValueError("Cron expression has no matching date") from err
    return expression


def local_zone():
    name = os.environ.get("TZ", "").lstrip(":")
    if name:
        return ZoneInfo(name)
    try:
        path = Path("/etc/localtime").resolve()
        return ZoneInfo(str(path).split("/zoneinfo/", 1)[1])
    except (IndexError, OSError):
        return datetime.now().astimezone().tzinfo


def now_local() -> datetime:
    return datetime.now(timezone.utc).astimezone(local_zone())


def validate_schedule(data: dict[str, Any], camera_exists: bool) -> dict[str, Any]:
    if not isinstance(data, dict) or not camera_exists:
        raise ValueError("Camera not found")
    name = str(data.get("name", "")).strip()
    if not name or len(name) > 100:
        raise ValueError("Name must be 1 to 100 characters")
    mode = data.get("mode")
    if mode not in ("photo", "video", "timelapse"):
        raise ValueError("Invalid capture mode")
    repeat = data.get("repeat")
    if repeat not in ("once", "daily", "weekly", "cron"):
        raise ValueError("Invalid repeat rule")
    weekdays = data.get("weekdays", [])
    if not isinstance(weekdays, list) or any(type(x) is not int or x not in range(7) for x in weekdays):
        raise ValueError("Invalid weekdays")
    weekdays = sorted(set(weekdays))
    if repeat == "weekly" and not weekdays:
        raise ValueError("Choose at least one weekday")
    day = data.get("date", "")
    if repeat == "once":
        try:
            date.fromisoformat(day)
        except (TypeError, ValueError):
            raise ValueError("Invalid date") from None
    trigger = "cron" if repeat == "cron" else data.get("trigger")
    if trigger not in ("fixed", "sunset", "cron") or (repeat != "cron" and trigger == "cron"):
        raise ValueError("Invalid trigger")
    cron_expression = validate_cron(data.get("cron_expression")) if trigger == "cron" else None
    clock = data.get("time", "")
    latitude = longitude = offset = None
    if trigger == "fixed":
        try:
            if len(clock) != 5 or clock[2] != ":":
                raise ValueError
            time.fromisoformat(clock)
        except (TypeError, ValueError):
            raise ValueError("Time must be HH:MM") from None
    elif trigger == "sunset":
        try:
            latitude, longitude = float(data["latitude"]), float(data["longitude"])
            offset = int(data.get("offset_minutes", 0))
        except (KeyError, TypeError, ValueError, OverflowError):
            raise ValueError("Invalid location or sunset offset") from None
        if not (math.isfinite(latitude) and math.isfinite(longitude) and -90 <= latitude <= 90 and -180 <= longitude <= 180 and -720 <= offset <= 720):
            raise ValueError("Invalid location or sunset offset")
    preset = str(data.get("preset", ""))
    if not preset.isdecimal():
        raise ValueError("Choose a camera preset")
    settings = data.get("settings", {})
    if not isinstance(settings, dict) or len(settings) > 100:
        raise ValueError("Invalid settings")
    if any(not str(k).isdecimal() or not str(v).isdecimal() for k, v in settings.items()):
        raise ValueError("Invalid setting IDs or options")
    duration = None
    if mode != "photo":
        try:
            duration = int(data.get("duration_seconds"))
        except (TypeError, ValueError):
            raise ValueError("Duration is required") from None
        if not 1 <= duration <= 86400:
            raise ValueError("Duration must be between 1 second and 24 hours")
    return {"name": name, "camera_id": str(data["camera_id"]), "mode": mode,
            "repeat": repeat, "weekdays": weekdays, "date": day if repeat == "once" else None,
            "trigger": trigger, "time": clock if trigger == "fixed" else None, "cron_expression": cron_expression,
            "latitude": latitude, "longitude": longitude, "offset_minutes": offset,
            "preset": preset, "preset_identity": str(data.get("preset_identity", "")),
            "settings": {str(k): str(v) for k, v in settings.items()},
            "duration_seconds": duration, "enabled": bool(data.get("enabled", True))}


def occurrence(schedule: dict[str, Any], day: date, zone=None) -> datetime | None:
    """Return aware event time; None means no sunset or invalid local wall time."""
    zone = zone or local_zone()
    if schedule["trigger"] == "sunset":
        try:
            solar_time = sunset(Observer(schedule["latitude"], schedule["longitude"]), day, tzinfo=zone)
            return (solar_time.astimezone(timezone.utc) + timedelta(minutes=schedule["offset_minutes"])).astimezone(zone)
        except ValueError:
            return None
    wall = datetime.combine(day, time.fromisoformat(schedule["time"]))
    value = wall.replace(tzinfo=zone, fold=0)
    if value.astimezone(timezone.utc).astimezone(zone).replace(tzinfo=None) != wall:
        return None
    return value


def matches(schedule: dict[str, Any], day: date) -> bool:
    if schedule["repeat"] == "once":
        return schedule["date"] == day.isoformat()
    return schedule["repeat"] == "daily" or day.weekday() in schedule["weekdays"]


def next_occurrence(schedule: dict[str, Any], after: datetime) -> tuple[date, datetime | None] | None:
    zone = local_zone()
    if schedule["repeat"] == "cron":
        return _next_cron_occurrence(schedule, zone)
    processed = set(schedule.get("processed_dates", []))
    created = datetime.fromisoformat(schedule["created_at"])
    start = (created.astimezone(zone) - timedelta(days=1)).date()
    if processed:
        start = max(start, date.fromisoformat(max(processed)) + timedelta(days=1))
    # Bound recovery work after a very long outage; history itself is bounded too.
    start = max(start, after.astimezone(zone).date() - timedelta(days=370))
    days = ([date.fromisoformat(schedule["date"])] if schedule["repeat"] == "once"
            else (start + timedelta(days=n) for n in range(741)))
    for day in days:
        if not matches(schedule, day) or day.isoformat() in processed:
            continue
        target = occurrence(schedule, day, zone)
        # Treat missing solar events as an event at the end of the local day.
        marker = target or datetime.combine(day, time(23, 59), tzinfo=zone)
        if marker <= created:
            continue
        return day, target
    return None


def _cron_base(schedule: dict[str, Any]) -> datetime:
    created = datetime.fromisoformat(schedule["created_at"])
    cursor = schedule.get("cron_cursor")
    if cursor:
        last = datetime.fromisoformat(cursor)
        if last.timestamp() > created.timestamp():
            return last
    return created


def _valid_cron_time(wall: datetime, zone: Any) -> datetime | None:
    candidate = wall.replace(tzinfo=zone, fold=0)
    if candidate.astimezone(timezone.utc).astimezone(zone).replace(tzinfo=None) != wall:
        return None
    return candidate


def _next_cron_occurrence(schedule: dict[str, Any], zone: Any) -> tuple[date, datetime] | None:
    base = _cron_base(schedule)
    iterator = croniter(schedule["cron_expression"], base.astimezone(zone).replace(tzinfo=None),
                        max_years_between_matches=50)
    try:
        for _ in range(2881):
            wall = iterator.get_next(datetime)
            candidate = _valid_cron_time(wall, zone)
            if candidate and candidate.timestamp() > base.timestamp():
                return candidate.date(), candidate
    except CroniterBadDateError:
        return None
    return None


def cron_missed_before(schedule: dict[str, Any], before: datetime) -> datetime | None:
    """Find the last missed occurrence before a cutoff, for bounded outage recovery."""
    zone = local_zone()
    base = _cron_base(schedule)
    if base.timestamp() >= before.timestamp():
        return None
    iterator = croniter(schedule["cron_expression"], before.astimezone(zone).replace(tzinfo=None),
                        max_years_between_matches=50)
    try:
        for _ in range(2881):
            wall = iterator.get_prev(datetime)
            candidate = _valid_cron_time(wall, zone)
            if candidate and base.timestamp() < candidate.timestamp() < before.timestamp():
                return candidate
            if candidate and candidate.timestamp() <= base.timestamp():
                return None
    except CroniterBadDateError:
        return None
    return None


class ScheduleStore:
    """Single-process atomic JSON store, separate from camera credentials."""
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = json.loads(path.read_text()) if path.exists() else {"schedules": [], "history": []}
        self.data.setdefault("wake_guards", {})

    def save(self):
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))
        os.replace(temporary, self.path)

    def get(self, schedule_id):
        return next((s for s in self.data["schedules"] if s["id"] == schedule_id), None)

    def create(self, values):
        item = {**values, "id": uuid4().hex, "created_at": now_local().isoformat(), "processed_dates": []}
        self.data["schedules"].append(item)
        self.save()
        return item

    def update(self, item, values):
        item.update(values)
        item["created_at"] = now_local().isoformat()
        item["processed_dates"] = []
        item.pop("cron_cursor", None)
        self.save()
        return item

    def history(self, item, day, target, status, error=None):
        record = {"id": uuid4().hex, "schedule_id": item["id"], "camera_id": item["camera_id"],
                  "mode": item["mode"], "occurrence_date": day.isoformat(),
                  "scheduled_at": target.isoformat() if target else None,
                  "started_at": None, "finished_at": None if status == "preparing" else now_local().isoformat(), "status": status, "error": error,
                  "shutter_sent": False}
        if item["repeat"] == "cron":
            if target is None:
                raise ValueError("Cron occurrence must have a scheduled time")
            item["cron_cursor"] = target.isoformat()
        else:
            item.setdefault("processed_dates", []).append(day.isoformat())
            item["processed_dates"] = item["processed_dates"][-400:]
        if item["repeat"] == "once":
            item["enabled"] = False
        self.data["history"].append(record)
        # Retain in-progress entries even when history is full.
        active = [r for r in self.data["history"] if r["status"] in ("preparing", "capturing")]
        done = [r for r in self.data["history"] if r["status"] not in ("preparing", "capturing")]
        self.data["history"] = done[-HISTORY_LIMIT:] + active
        self.save()
        return record
