import { CONSOLE_STYLES } from "./opengopro-console-styles.js";

const I18N = {
  en: {
    "action.add_camera": "Add camera",
    "action.apply": "Apply",
    "action.cancel": "Cancel",
    "action.close": "Close",
    "action.configure_cohn": "Configure COHN",
    "action.refresh": "Refresh list",
    "action.scan_ble": "Scan BLE",
    "action.scan_wifi": "Scan Wi-Fi",
    "action.settings": "Settings",
    "action.start": "Start",
    "action.stop": "Stop",
    "action.restart": "Restart",
    "action.wake": "Wake",
    "action.sleep": "Sleep",
    "capture.capturing": "Capturing",
    "capture.lapse_running": "Lapse running",
    "capture.recording": "Recording",
    "capture.ready": "Ready",
    "capture.start_lapse": "Start lapse",
    "capture.start_recording": "Start recording",
    "capture.stop_capture": "Stop capture",
    "capture.stop_lapse": "Stop lapse",
    "capture.stop_recording": "Stop recording",
    "capture.take_photo": "Take photo",
    "empty.camera_settings": "Select a camera to show writable OpenGoPro settings.",
    "empty.cameras": "No cameras",
    "empty.media": "Refresh to show camera media. In Home Assistant, files are also exposed through Media Browser.",
    "empty.no_presets": "No presets",
    "empty.preset_status": "Camera Preset Status has not been loaded. Confirm the current preset before writing parameters.",
    "empty.provision": "Scan BLE and choose a camera, or enter the BLE address manually.",
    "empty.provision_progress": "Provisioning progress appears here in real time.",
    "empty.settings_unmatched": "The current preset did not match built-in setting controls. Use the setting:value entries on the preset card; this mapping can be expanded later.",
    "error.mpegts_unsupported": "This browser does not support mpegts.js/MSE live playback",
    "error.need_ble": "Scan and select a GoPro first, or enter the BLE address manually",
    "error.need_ble_scan": "Select a GoPro from the BLE scan list first, or enter the BLE address manually",
    "error.need_wifi": "Home Wi-Fi SSID and password are required",
    "error.state_failed": "State read failed",
    "form.ble_address": "BLE address",
    "form.camera_name": "Name",
    "form.wifi_password": "Home Wi-Fi password",
    "form.wifi_ssid": "Wi-Fi SSID",
    "hint.no_camera": "No camera selected. In standalone mode, scan BLE first and configure HERO12 COHN.",
    "log.idle": "Waiting for action",
    "metric.battery": "Battery",
    "metric.connection": "Connection",
    "metric.mode": "Mode",
    "metric.recording": "Recording",
    "metric.remaining": "Remaining",
    "metric.sd": "SD card",
    "mode.photo": "Photo",
    "mode.timelapse": "Lapse",
    "mode.video": "Video",
    "modal.provision_description": "Configure HERO12 COHN over BLE and save LAN HTTPS connection details.",
    "modal.provision_title": "Add GoPro camera",
    "modal.settings_description": "{mode} presets and active-preset parameters.",
    "modal.settings_title": "Camera settings",
    "panel.cameras": "Cameras",
    "panel.log": "Log",
    "panel.media": "Media",
    "panel.presets": "Presets",
    "panel.current_preset": "Current preset",
    "panel.preview": "Preview",
    "panel.power": "Power",
    "placeholder.ssid": "Choose a scanned SSID, or type a hidden network",
    "power.checking": "Checking camera state",
    "power.off": "Camera is offline or sleeping",
    "power.on": "Camera online",
    "power.standby": "Camera is in low-power BLE standby and can be woken",
    "power.unknown": "Camera state unknown",
    "preview.offline_title": "Preview offline",
    "preview.offline_body": "Select a camera before starting preview.",
    "preview.reserved_title": "Preview unavailable",
    "preview.reserved_body": "This adapter does not expose a preview stream.",
    "preview.standby_title": "Preview standby",
    "preview.standby_body": "Start preview to show the live feed.",
    "run.configure_cohn": "Configure COHN",
    "run.configure_cohn_busy": "Configuring COHN...",
    "run.load_media": "Load media",
    "run.refresh": "Refresh",
    "run.refreshed": "Refreshed",
    "run.scan_ble": "Scan BLE",
    "run.scan_wifi": "Scan Wi-Fi",
    "setting.current": "Current: {value}",
    "setting.output": "Output",
    "setting.photo": "Photo settings",
    "setting.lapse": "Lapse settings",
    "setting.lens": "Lens",
    "setting.mode": "Mode",
    "setting.res": "Res",
    "setting.video": "Video settings",
    "stage.ble_connect": "Connect BLE",
    "stage.clear_certificate": "Clear old COHN certificate",
    "stage.cohn_status_done": "LAN address received {address}",
    "stage.connect_wifi": "Write Wi-Fi credentials and connect",
    "stage.connect_wifi_done": "Camera connected to Wi-Fi",
    "stage.create_certificate": "Create COHN certificate",
    "stage.done": "Provisioning complete",
    "stage.error": "Provisioning failed",
    "stage.failed": "Provisioning failed",
    "stage.get_certificate": "Read COHN certificate",
    "stage.resolve_ble": "Find BLE device",
    "stage.scan_wifi": "Scan Wi-Fi visible to the camera",
    "stage.scan_wifi_done": "Found {count} access points",
    "stage.set_datetime": "Sync camera time",
    "stage.start": "Start provisioning",
    "stage.wait_cohn_status": "Wait for LAN connection details",
    "status.idle": "idle",
    "status.recording": "recording",
    "title": "GoPro Control",
    "unknown": "unknown",
    "wifi.bars": "{count} bars",
    "wifi.configured": "saved",
    "wifi.current": "current",
    "wifi.summary": "Scanned {count} SSIDs",
  },
  "zh-Hans": {
    "action.add_camera": "添加相机",
    "action.apply": "应用",
    "action.cancel": "取消",
    "action.close": "关闭",
    "action.configure_cohn": "配置 COHN",
    "action.refresh": "刷新列表",
    "action.scan_ble": "扫描 BLE",
    "action.scan_wifi": "扫描 Wi-Fi",
    "action.settings": "设置",
    "action.start": "启动",
    "action.stop": "停止",
    "action.restart": "重启",
    "action.wake": "唤醒",
    "action.sleep": "休眠",
    "capture.capturing": "拍摄中",
    "capture.lapse_running": "延时拍摄中",
    "capture.recording": "录制中",
    "capture.ready": "就绪",
    "capture.start_lapse": "开始延时",
    "capture.start_recording": "开始录制",
    "capture.stop_capture": "停止拍摄",
    "capture.stop_lapse": "停止延时",
    "capture.stop_recording": "停止录制",
    "capture.take_photo": "拍照",
    "empty.camera_settings": "选择相机后显示可写入的 OpenGoPro 设置。",
    "empty.cameras": "暂无相机",
    "empty.media": "刷新后显示相机媒体。HA 模式下也会同步暴露到 Media Browser。",
    "empty.no_presets": "暂无 preset",
    "empty.preset_status": "未读取到相机 Preset Status。参数写入前建议先确认当前相机 preset。",
    "empty.provision": "点击扫描 BLE 后选择相机，或手动填写 BLE 地址。",
    "empty.provision_progress": "配置过程会实时显示在这里。",
    "empty.settings_unmatched": "当前 preset 没有匹配到内置设置控件。请查看 preset 卡片里的 setting:value，后续可继续扩充映射。",
    "error.mpegts_unsupported": "当前浏览器不支持 mpegts.js/MSE Live Playback",
    "error.need_ble": "请先扫描并选择 GoPro，或手动填写 BLE 地址",
    "error.need_ble_scan": "请先从 BLE 扫描列表选择 GoPro，或手动填写 BLE 地址",
    "error.need_wifi": "家庭 Wi-Fi SSID 和密码是必填字段",
    "error.state_failed": "状态读取失败",
    "form.ble_address": "BLE 地址",
    "form.camera_name": "名称",
    "form.wifi_password": "家庭 Wi-Fi 密码",
    "form.wifi_ssid": "Wi-Fi SSID",
    "hint.no_camera": "还没有选择相机。standalone 模式可以先扫描 BLE 并配置 HERO12 COHN。",
    "log.idle": "等待操作",
    "metric.battery": "电量",
    "metric.connection": "连接",
    "metric.mode": "模式",
    "metric.recording": "录制",
    "metric.remaining": "剩余",
    "metric.sd": "SD 卡",
    "mode.photo": "照片",
    "mode.timelapse": "延时",
    "mode.video": "视频",
    "modal.provision_description": "通过 BLE 为 HERO12 配置 COHN，并保存局域网 HTTPS 连接信息。",
    "modal.provision_title": "添加 GoPro 相机",
    "modal.settings_description": "{mode} preset 和当前 preset 参数。",
    "modal.settings_title": "相机设置",
    "panel.cameras": "相机列表",
    "panel.log": "日志",
    "panel.media": "媒体",
    "panel.presets": "Presets",
    "panel.current_preset": "当前 Preset",
    "panel.preview": "预览",
    "panel.power": "电源",
    "placeholder.ssid": "选择扫描到的 SSID，隐藏网络可手动输入",
    "power.checking": "正在检测相机状态",
    "power.off": "相机离线或已休眠",
    "power.on": "相机在线",
    "power.standby": "相机低功耗 BLE 可发现，等待唤醒",
    "power.unknown": "相机状态未知",
    "preview.offline_title": "预览离线",
    "preview.offline_body": "选择相机后可以启动预览。",
    "preview.reserved_title": "预览不可用",
    "preview.reserved_body": "当前 adapter 没有暴露预览流。",
    "preview.standby_title": "预览待机",
    "preview.standby_body": "点击启动预览后显示实时画面。",
    "run.configure_cohn": "配置 COHN",
    "run.configure_cohn_busy": "配置 COHN...",
    "run.load_media": "读取媒体",
    "run.refresh": "刷新",
    "run.refreshed": "已刷新",
    "run.scan_ble": "扫描 BLE",
    "run.scan_wifi": "扫描 Wi-Fi",
    "setting.current": "当前: {value}",
    "setting.output": "输出",
    "setting.photo": "照片设置",
    "setting.lapse": "延时设置",
    "setting.lens": "镜头",
    "setting.mode": "模式",
    "setting.res": "分辨率",
    "setting.video": "视频设置",
    "stage.ble_connect": "连接 BLE",
    "stage.clear_certificate": "清理旧 COHN 证书",
    "stage.cohn_status_done": "获取到局域网地址 {address}",
    "stage.connect_wifi": "写入 Wi-Fi 凭据并连接",
    "stage.connect_wifi_done": "相机已连接 Wi-Fi",
    "stage.create_certificate": "创建 COHN 证书",
    "stage.done": "配置完成",
    "stage.error": "配置失败",
    "stage.failed": "配置失败",
    "stage.get_certificate": "读取 COHN 证书",
    "stage.resolve_ble": "查找 BLE 设备",
    "stage.scan_wifi": "扫描相机可见的 Wi-Fi",
    "stage.scan_wifi_done": "已发现 {count} 个接入点",
    "stage.set_datetime": "同步相机时间",
    "stage.start": "开始配置",
    "stage.wait_cohn_status": "等待局域网连接信息",
    "status.idle": "空闲",
    "status.recording": "录制中",
    "title": "GoPro 控制台",
    "unknown": "未知",
    "wifi.bars": "{count} 格",
    "wifi.configured": "已保存",
    "wifi.current": "当前连接",
    "wifi.summary": "已扫描到 {count} 个 SSID",
  },
};

function normalizeLocale(locale) {
  const value = String(locale || "").replace("_", "-").toLowerCase();
  if (value.startsWith("zh")) return "zh-Hans";
  return "en";
}

const SETTING_GROUPS = [
  {
    title: "Video",
    description: "Resolution, frame cadence and capture shape.",
    settings: [
      {
        id: "2",
        label: "Resolution",
        options: [
          ["100", "5.3K"],
          ["1", "4K"],
          ["4", "2.7K"],
          ["9", "1080"],
          ["107", "5.3K 8:7"],
          ["108", "4K 8:7"],
          ["109", "4K 9:16"],
        ],
      },
      {
        id: "3",
        label: "FPS",
        options: [
          ["10", "24"],
          ["8", "30"],
          ["5", "60"],
          ["1", "120"],
          ["0", "240"],
        ],
      },
      {
        id: "108",
        label: "Aspect",
        options: [
          ["1", "16:9"],
          ["0", "4:3"],
          ["3", "8:7"],
          ["4", "9:16"],
          ["5", "21:9"],
          ["6", "1:1"],
        ],
      },
      {
        id: "121",
        label: "Lens",
        options: [
          ["0", "Wide"],
          ["4", "Linear"],
          ["3", "SuperView"],
          ["8", "Linear + Horizon Leveling"],
          ["9", "HyperView"],
          ["10", "Linear + Horizon Lock"],
          ["13", "Ultra Wide"],
          ["104", "Ultra HyperView"],
        ],
      },
    ],
  },
  {
    title: "Stabilization",
    description: "Motion smoothing, horizon handling and lens mods.",
    settings: [
      {
        id: "135",
        label: "HyperSmooth",
        options: [
          ["0", "Off"],
          ["1", "Low"],
          ["2", "High"],
          ["3", "Boost"],
          ["4", "Auto Boost"],
          ["100", "Standard"],
        ],
      },
      {
        id: "150",
        label: "Horizon",
        options: [
          ["0", "Off"],
          ["2", "Locked"],
        ],
      },
      {
        id: "162",
        label: "Max Lens",
        options: [
          ["0", "Off"],
          ["1", "On"],
        ],
      },
      {
        id: "189",
        label: "Lens Mod",
        options: [
          ["0", "None"],
          ["1", "Max Lens 1.0"],
          ["2", "Max Lens 2.0"],
          ["3", "Max Lens 2.5"],
          ["4", "Macro"],
          ["10", "Standard Lens"],
          ["100", "Auto Detect"],
        ],
      },
    ],
  },
  {
    title: "Quality",
    description: "Compression, bit depth and camera processing profile.",
    settings: [
      {
        id: "182",
        label: "Bit Rate",
        options: [
          ["0", "Standard"],
          ["1", "High"],
          ["2", "Max"],
        ],
      },
      {
        id: "183",
        label: "Bit Depth",
        options: [
          ["0", "8-Bit"],
          ["2", "10-Bit"],
        ],
      },
      {
        id: "184",
        label: "Profile",
        options: [
          ["0", "Standard"],
          ["1", "HDR"],
          ["2", "Log"],
          ["101", "HLG HDR"],
        ],
      },
      {
        id: "180",
        label: "System Video",
        options: [
          ["0", "Highest Quality"],
          ["101", "Extended Battery"],
          ["102", "Longest Battery"],
          ["111", "Standard Quality"],
          ["112", "Basic Quality"],
        ],
      },
    ],
  },
  {
    title: "Capture",
    description: "Duration, hindsight and camera behavior.",
    settings: [
      {
        id: "156",
        label: "Video Duration",
        options: [
          ["100", "No Limit"],
          ["10", "5 Seconds"],
          ["1", "15 Seconds"],
          ["3", "1 Minute"],
          ["4", "5 Minutes"],
          ["7", "1 Hour"],
        ],
      },
      {
        id: "167",
        label: "HindSight",
        options: [
          ["4", "Off"],
          ["2", "15 Seconds"],
          ["3", "30 Seconds"],
        ],
      },
      {
        id: "134",
        label: "Anti-Flicker",
        options: [
          ["2", "60Hz"],
          ["3", "50Hz"],
          ["0", "NTSC"],
          ["1", "PAL"],
        ],
      },
      {
        id: "59",
        label: "Auto Power Down",
        options: [
          ["0", "Never"],
          ["1", "1 Min"],
          ["4", "5 Min"],
          ["6", "15 Min"],
          ["7", "30 Min"],
        ],
      },
    ],
  },
  {
    title: "Photo / Lapse",
    description: "Still capture, lapse modes and intervals.",
    settings: [
      {
        id: "122",
        label: "Photo Lens",
        options: [
          ["101", "Wide"],
          ["102", "Linear"],
          ["100", "Max SuperView"],
          ["41", "Ultra Wide 12 MP"],
          ["31", "Wide 27 MP"],
          ["32", "Linear 27 MP"],
        ],
      },
      {
        id: "125",
        label: "Photo Output",
        options: [
          ["0", "Standard"],
          ["1", "Raw"],
          ["2", "HDR"],
          ["3", "SuperPhoto"],
        ],
      },
      {
        id: "187",
        label: "Lapse Mode",
        options: [
          ["0", "TimeWarp"],
          ["1", "Star Trails"],
          ["2", "Light Painting"],
          ["3", "Vehicle Lights"],
          ["8", "Time Lapse Video"],
          ["9", "Night Lapse Video"],
        ],
      },
      {
        id: "123",
        label: "Lapse Lens",
        options: [
          ["101", "Wide"],
          ["102", "Linear"],
          ["100", "Max SuperView"],
          ["19", "Narrow"],
          ["31", "Wide 27 MP"],
          ["32", "Linear 27 MP"],
        ],
      },
    ],
  },
  {
    title: "System",
    description: "Camera feedback and wireless preferences.",
    settings: [
      {
        id: "83",
        label: "GPS",
        options: [
          ["0", "Off"],
          ["1", "On"],
        ],
      },
      {
        id: "91",
        label: "LED",
        options: [
          ["3", "All On"],
          ["4", "All Off"],
          ["5", "Front Off Only"],
          ["100", "Back Only"],
        ],
      },
      {
        id: "178",
        label: "Wireless Band",
        options: [
          ["0", "2.4GHz"],
          ["1", "5GHz"],
        ],
      },
      {
        id: "216",
        label: "Beep Volume",
        options: [
          ["70", "Low"],
          ["85", "Medium"],
          ["100", "High"],
        ],
      },
    ],
  },
];

class OpenGoProConsole extends HTMLElement {
  connectedCallback() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    this._locale = normalizeLocale(this._adapter?.locale || document.documentElement.lang || navigator.language);
    this._cameras = [];
    this._selected = null;
    this._media = [];
    this._presetStatus = null;
    this._scanDevices = [];
    this._provisionAccessPoints = [];
    this._provisionEvents = [];
    this._currentAccessPointSsid = "";
    this._provisionForm = {};
    this._busy = false;
    this._showProvisionModal = false;
    this._showSettingsModal = false;
    this._message = this._t("log.idle");
    this._presenceRequests = new Map();
    this._pollTimer = null;
    this._previewPlayer = null;
    this._refresh();
    this._startPolling();
  }

  disconnectedCallback() {
    this._stopPolling();
    this._presenceRequests?.clear();
    this._teardownPreviewPlayer();
  }

  set adapter(adapter) {
    this._adapter = adapter;
    this._locale = normalizeLocale(adapter?.locale || document.documentElement.lang || navigator.language);
    if (this.shadowRoot) this._refresh();
  }

  _t(key, params = {}) {
    const dictionary = I18N[this._locale] || I18N.en;
    const fallback = I18N.en[key] || key;
    return String(dictionary[key] || fallback).replace(/\{(\w+)\}/g, (_, name) => params[name] ?? "");
  }

  async _run(label, action, options = {}) {
    if (!this._adapter) return;
    const reloadCameras = options.reloadCameras ?? true;
    this._busy = true;
    this._message = `${label}...`;
    this._render();
    try {
      const result = await action();
      this._message = typeof result === "string" ? result : JSON.stringify(result, null, 2);
      if (reloadCameras) await this._loadCameras();
    } catch (error) {
      this._message = JSON.stringify(this._errorDetail(error), null, 2);
    } finally {
      this._busy = false;
      this._render();
    }
  }

  async _refresh() {
    await this._run(this._t("run.refresh"), async () => {
      await this._loadCameras();
      return this._t("run.refreshed");
    });
  }

  async _loadCameras() {
    const existing = new Map(this._cameras.map((camera) => [camera.id, camera]));
    this._cameras = (await this._adapter.listCameras()).map((camera) => ({
      ...existing.get(camera.id),
      ...camera,
    }));
    if (!this._selected && this._cameras.length) this._selected = this._cameras[0].id;
    if (this._selected && !this._cameras.some((camera) => camera.id === this._selected)) {
      this._selected = this._cameras[0]?.id || null;
    }
    this._probePresence();
    this._probePreviewStatus();
  }

  async _command(command, extra = {}) {
    if (!this._selected) return;
    await this._run(command, async () => {
      const result = await this._adapter.command(this._selected, command, extra);
      const state = result?.state || result?.camera_state;
      if (state) this._mergeCameraState(this._selected, state);
      if (command === "sleep") {
        this._mergeCamera(this._selected, {
          power: "standby",
          phase: "ble_standby",
          http_ready: false,
          preview_active: false,
          preview_url: null,
          preview_transport: null,
          recording: false,
        });
        this._showSettingsModal = false;
        this._presetStatus = null;
      }
      if (result?.preview) {
        this._mergeCamera(this._selected, {
          preview_active: Boolean(result.preview.running || state?.preview_active),
          preview_url: result.preview.stream_url || null,
          preview_transport: result.preview.transport || state?.preview_transport || null,
          preview_error: result.preview.error || null,
        });
      } else if (["wake", "set_setting", "set_mode", "set_preset"].includes(command)) {
        await this._loadSelectedState();
        if (command === "set_preset" || command === "set_mode") await this._loadPresets();
      }
      return result;
    }, { reloadCameras: false });
  }

  async _loadSelectedState() {
    if (!this._selected || !this._adapter.loadState) return;
    const result = await this._adapter.loadState(this._selected);
    const state = result?.state || result;
    this._mergeCameraState(this._selected, state);
  }

  async _loadPresets() {
    if (!this._selected || !this._adapter?.loadPresets) return;
    this._presetStatus = await this._adapter.loadPresets(this._selected);
  }

  _startPolling() {
    this._stopPolling();
    this._pollTimer = window.setInterval(() => this._pollState(), 4000);
  }

  _stopPolling() {
    if (!this._pollTimer) return;
    window.clearInterval(this._pollTimer);
    this._pollTimer = null;
  }

  async _pollState() {
    if (!this._adapter || this._busy) return;
    const before = JSON.stringify(this._cameras);
    try {
      await this._loadCameras();
      if (JSON.stringify(this._cameras) !== before) this._render();
    } catch (error) {
      if (this._selected) {
        this._mergeCamera(this._selected, {
          status_error: error?.error || error?.message || String(error),
          status_detail: error?.status_detail || error?.trace || null,
        });
        this._render();
      }
    }
  }

  _mergeCameraState(cameraId, state) {
    if (!state || typeof state !== "object") return;
    this._cameras = this._cameras.map((camera) =>
      camera.id === cameraId
        ? {
            ...camera,
            ...state,
            status_error: null,
            status_detail: null,
          }
        : camera
    );
  }

  _mergeCamera(cameraId, patch) {
    if (!patch || typeof patch !== "object") return;
    this._cameras = this._cameras.map((camera) =>
      camera.id === cameraId ? { ...camera, ...patch } : camera
    );
  }

  _probePresence() {
    if (!this._adapter?.loadPresence) return;
    for (const camera of this._cameras) {
      const cameraId = camera.id;
      if (this._presenceRequests.has(cameraId)) continue;
      this._mergeCamera(cameraId, { power: camera.power || "checking" });
      const request = this._adapter
        .loadPresence(cameraId)
        .then((presence) => {
          if (!this._cameras.some((camera) => camera.id === cameraId)) return;
          this._mergeCamera(cameraId, presence);
          this._render();
        })
        .catch((error) => {
          if (!this._cameras.some((camera) => camera.id === cameraId)) return;
          this._mergeCamera(cameraId, {
            power: "unknown",
            presence_error: error?.error || error?.message || String(error),
          });
          this._render();
        })
        .finally(() => {
          if (this._presenceRequests.get(cameraId) === request) {
            this._presenceRequests.delete(cameraId);
          }
        });
      this._presenceRequests.set(cameraId, request);
    }
  }

  _probePreviewStatus() {
    if (!this._adapter?.loadPreviewStatus) return;
    for (const camera of this._cameras) {
      const cameraId = camera.id;
      this._adapter
        .loadPreviewStatus(cameraId)
        .then((preview) => {
          const patch = {
            preview_active: Boolean(preview.running),
            preview_url: preview.stream_url || null,
            preview_transport: preview.transport || null,
            preview_error: preview.error || null,
          };
          const current = this._cameras.find((camera) => camera.id === cameraId);
          const changed = Object.entries(patch).some(([key, value]) => current?.[key] !== value);
          if (!changed) return;
          this._mergeCamera(cameraId, patch);
          this._render();
        })
        .catch(() => {});
    }
  }

  async _loadMedia() {
    if (!this._selected) return;
    await this._run(this._t("run.load_media"), async () => {
      this._media = await this._adapter.loadMedia(this._selected);
      return { media_count: this._media.length };
    }, { reloadCameras: false });
  }

  async _scan() {
    if (!this._adapter.scan) return;
    await this._run(this._t("run.scan_ble"), async () => {
      const result = await this._adapter.scan();
      this._scanDevices = result?.devices || [];
      return result;
    }, { reloadCameras: false });
  }

  async _provision() {
    if (!this._adapter.provisionCohn) return;
    this._captureProvisionForm();
    if (!this._provisionForm.ble_address) {
      this._message = JSON.stringify({ error: this._t("error.need_ble") }, null, 2);
      this._render();
      return;
    }
    if (!this._provisionForm.ssid || !this._provisionForm.password) {
      this._message = JSON.stringify({ error: this._t("error.need_wifi") }, null, 2);
      this._render();
      return;
    }
    const payload = this._provisionPayload();
    this._provisionEvents = [];
    this._provisionAccessPoints = [];
    if (this._adapter.provisionCohnStream) {
      this._busy = true;
      this._message = this._t("run.configure_cohn_busy");
      this._appendProvisionEvent({ stage: "start" });
      try {
        const result = await this._adapter.provisionCohnStream(payload, (event) =>
          this._handleProvisionEvent(event)
        );
        this._message = JSON.stringify(result, null, 2);
        await this._loadCameras();
      } catch (error) {
        this._message = JSON.stringify(this._errorDetail(error), null, 2);
      } finally {
        this._busy = false;
        this._render();
      }
      return;
    }
    await this._run(this._t("run.configure_cohn"), () => this._adapter.provisionCohn(payload));
  }

  async _scanAccessPoints() {
    if (!this._adapter.scanAccessPoints) return;
    this._captureProvisionForm();
    const selectedScanDevice = this._selectedScanDevice();
    if (!this._provisionForm.ble_address && selectedScanDevice?.address) {
      this._provisionForm.ble_address = selectedScanDevice.address;
      this._provisionForm.name = selectedScanDevice.name || this._provisionForm.name || "GoPro";
    }
    if (!this._provisionForm.ble_address) {
      this._message = JSON.stringify({ error: this._t("error.need_ble_scan") }, null, 2);
      this._render();
      return;
    }
    await this._run(this._t("run.scan_wifi"), async () => {
      const result = await this._adapter.scanAccessPoints({
        ble_address: this._provisionForm.ble_address,
        timeout: 60,
      });
      this._currentAccessPointSsid = result.current_ssid || this._currentAccessPointSsid || "";
      this._setProvisionAccessPoints(result.access_points || []);
      return result;
    }, { reloadCameras: false });
  }

  _provisionPayload() {
    return {
      ble_address: this._provisionForm.ble_address,
      name: this._provisionForm.name || "GoPro",
      ssid: this._provisionForm.ssid,
      password: this._provisionForm.password,
      force_new_credentials: true,
      timeout: 360,
      verify_ssl: false,
    };
  }

  _handleProvisionEvent(event) {
    if (event?.credentials?.ssid) this._currentAccessPointSsid = event.credentials.ssid;
    if (event?.worker?.credentials?.ssid) this._currentAccessPointSsid = event.worker.credentials.ssid;
    if (event?.result?.credentials?.ssid) this._currentAccessPointSsid = event.result.credentials.ssid;
    if (event?.access_points) this._setProvisionAccessPoints(event.access_points);
    if (event?.result?.connect_trace) {
      const scan = event.result.connect_trace.find((item) => item.step === "scan_done");
      if (scan?.entries) this._setProvisionAccessPoints(scan.entries);
    }
    this._appendProvisionEvent(event);
    if (event?.type === "done" || event?.stage === "done") {
      this._message = JSON.stringify(event, null, 2);
    }
    if (event?.type === "error" || event?.stage === "failed") {
      this._message = JSON.stringify(event, null, 2);
    }
    this._render();
  }

  _appendProvisionEvent(event) {
    this._provisionEvents = [
      ...this._provisionEvents,
      {
        ...event,
        time: new Date().toLocaleTimeString(),
      },
    ].slice(-40);
  }

  _setProvisionAccessPoints(points) {
    this._provisionAccessPoints = (points || []).map((point) => ({
      ...point,
      current: Boolean(
        point.current || (this._currentAccessPointSsid && point.ssid === this._currentAccessPointSsid)
      ),
    }));
  }

  _openProvisionModal() {
    this._showProvisionModal = true;
    this._render();
  }

  _openProvisionForCamera(camera) {
    if (!camera) return;
    this._provisionForm = {
      ...this._provisionForm,
      ble_address: camera.ble_address || camera.address || "",
      name: camera.name || this._provisionForm.name || "GoPro",
      ssid: this._provisionForm.ssid || camera.cohn_ssid || "",
      password: this._provisionForm.password || "",
    };
    this._currentAccessPointSsid = camera.cohn_ssid || camera.ssid || "";
    this._showProvisionModal = true;
    this._render();
  }

  _closeProvisionModal() {
    this._captureProvisionForm();
    this._showProvisionModal = false;
    this._render();
  }

  async _openSettingsModal() {
    if (!this._canControl(this._camera())) return;
    if (this._selected) {
      try {
        await this._loadSelectedState();
        await this._loadPresets();
      } catch (error) {
        this._message = JSON.stringify(this._errorDetail(error), null, 2);
      }
    }
    this._showSettingsModal = true;
    this._render();
  }

  _closeSettingsModal() {
    this._showSettingsModal = false;
    this._render();
  }

  _captureProvisionForm() {
    const root = this.shadowRoot;
    if (!root) return;
    this._provisionForm = {
      ble_address: root.querySelector("#ble")?.value.trim() || this._provisionForm.ble_address || "",
      name: root.querySelector("#camera-name")?.value.trim() || this._provisionForm.name || "GoPro",
      ssid: root.querySelector("#ssid")?.value || this._provisionForm.ssid || "",
      password: root.querySelector("#wifi-password")?.value || this._provisionForm.password || "",
    };
  }

  _fillProvisionFromSelectedCamera() {
    const camera = this._camera();
    if (!camera) return;
    this._provisionForm.ble_address =
      this._provisionForm.ble_address || camera.ble_address || camera.address || "";
    this._provisionForm.name = this._provisionForm.name || camera.name || "GoPro";
  }

  _selectScanDevice(device) {
    this._captureProvisionForm();
    this._provisionForm.ble_address = device.address || "";
    this._provisionForm.name = device.name || this._provisionForm.name || "GoPro";
    const existing = this._cameras.find((camera) => camera.ble_address === device.address);
    this._currentAccessPointSsid = existing?.cohn_ssid || existing?.ssid || "";
    this._render();
  }

  _selectedScanDevice() {
    return this._scanDevices.find((item) => item.address === this._provisionForm.ble_address) || null;
  }

  _camera() {
    return this._cameras.find((camera) => camera.id === this._selected) || null;
  }

  _render() {
    this._teardownPreviewPlayer();
    const camera = this._camera();
    const recording = Boolean(camera?.recording);
    const capture = this._captureUi(camera);
    const hasProvision = Boolean(this._adapter?.provisionCohn);
    const canWake = this._canWake(camera);
    const canControl = this._canControl(camera);
    this.shadowRoot.innerHTML = `
      <style>${CONSOLE_STYLES}</style>

      <main class="shell">
        <header class="topbar">
          <div>
            <div class="eyebrow">${this._adapter?.label || "OpenGoPro"}</div>
            <h1>${this._t("title")}</h1>
            <div class="sub">${camera ? this._cameraSubtitle(camera) : this._t("hint.no_camera")}</div>
          </div>
          <div class="toolbar">
            <select ${this._cameras.length ? "" : "disabled"} id="camera-select">
              ${this._cameras.map((item) => `<option value="${this._escape(item.id)}" ${item.id === this._selected ? "selected" : ""}>${this._escape(item.name || "GoPro")}</option>`).join("")}
            </select>
            <button class="ghost" data-action="refresh">${this._t("action.refresh")}</button>
          </div>
        </header>

        <section class="layout">
          <aside class="stack side-stack">
            <div class="panel">
              <div class="panel-title">
                <h2>${this._t("panel.cameras")}</h2>
                ${hasProvision ? `<button class="primary" data-action="open-provision">${this._t("action.add_camera")}</button>` : ""}
              </div>
              <div class="camera-list">
                ${this._cameras.length ? this._cameras.map((item) => this._cameraCard(item)).join("") : `<div class="empty">${this._t("empty.cameras")}</div>`}
              </div>
            </div>
            <div class="panel log-panel">
              <div class="panel-title"><h2>${this._t("panel.log")}</h2></div>
            <div class="log">${this._escape(this._logText(camera))}</div>
            </div>
          </aside>

          <section class="stack">
            <div class="panel preview-panel">
              <div class="panel-title preview-head">
                <h2>Live Preview</h2>
                <div class="preview-head-actions">
                  <div class="mode-tabs" aria-label="Mode">
                    ${(camera?.modes || ["video", "photo", "timelapse"]).map((mode) => `<button class="mode-tab ${mode === camera?.current_mode ? "active" : ""}" data-mode-tab="${this._escape(mode)}" ${canControl ? "" : "disabled"}>${this._escape(this._modeLabel(mode))}</button>`).join("")}
                  </div>
                  <button class="head-settings" data-action="open-settings" ${canControl ? "" : "disabled"}>${this._t("action.settings")}</button>
                </div>
              </div>
              <div class="preview">
                ${this._previewMarkup(camera)}
              </div>
              <div class="preview-status">
                ${this._previewMetric(this._t("metric.connection"), camera?.phase || this._t("unknown"))}
                ${this._previewMetric(this._t("metric.battery"), camera?.battery != null ? `${camera.battery}%` : this._t("unknown"))}
                ${this._previewMetric(this._t("metric.mode"), camera?.current_mode || this._t("unknown"))}
                ${this._previewMetric(this._t("metric.remaining"), camera?.remaining_storage != null ? `${camera.remaining_storage} MB` : this._t("unknown"))}
                ${this._previewMetric(this._t("metric.sd"), camera?.sd_card_status || this._t("unknown"))}
                ${this._previewMetric(this._t("metric.recording"), recording ? this._t("status.recording") : this._t("status.idle"))}
              </div>
              <div class="capture-toolbar">
                <div class="tool-cluster">
                  <span>${this._t("panel.power")}</span>
                  <button class="tool-button" data-command="wake" ${canWake ? "" : "disabled"} title="${this._t("action.wake")}">${this._t("action.wake")}</button>
                  <button class="tool-button" data-command="sleep" ${canControl ? "" : "disabled"} title="${this._t("action.sleep")}">${this._t("action.sleep")}</button>
                </div>
                <button class="record-button ${recording ? "recording" : ""} ${this._escape(capture.className)}" data-command="${this._escape(capture.command)}" ${canControl ? "" : "disabled"}>
                  <span class="record-dot"></span>
                  <strong>${this._escape(capture.label)}</strong>
                </button>
                <div class="tool-cluster">
                  <span>${this._t("panel.preview")}</span>
                  <button class="tool-button accent" data-command="start_preview" ${canControl ? "" : "disabled"}>${camera?.preview_active ? this._t("action.restart") : this._t("action.start")}</button>
                  <button class="tool-button" data-command="stop_preview" ${canControl ? "" : "disabled"}>${this._t("action.stop")}</button>
                </div>
              </div>
            </div>

            <div class="panel">
              <div class="panel-title"><h2>${this._t("panel.media")}</h2><button class="ghost" data-action="media" ${canControl ? "" : "disabled"}>${this._t("panel.media")}</button></div>
              ${this._media.length ? `<div class="media-grid">${this._media.map((item) => this._mediaItem(item)).join("")}</div>` : `<div class="empty">${this._t("empty.media")}</div>`}
            </div>
          </section>
        </section>
        ${
          hasProvision
            ? `<div class="modal-backdrop ${this._showProvisionModal ? "open" : ""}" data-action="close-provision-backdrop">
                <div class="modal" role="dialog" aria-modal="true" aria-label="${this._t("modal.provision_title")}">
                  <div class="modal-head">
                    <div class="modal-title">
                      <strong>${this._t("modal.provision_title")}</strong>
                      <span>${this._t("modal.provision_description")}</span>
                    </div>
                    <button class="ghost icon-button" data-action="close-provision" aria-label="${this._t("action.close")}">×</button>
                  </div>
                  <div class="provision">
                    <div class="scan-results">
                      ${this._scanDevices.length ? this._scanDevices.map((device) => this._scanDevice(device)).join("") : `<div class="empty">${this._t("empty.provision")}</div>`}
                    </div>
                    <label>${this._t("form.ble_address")}<input id="ble" value="${this._escape(this._provisionForm.ble_address || "")}" placeholder=""></label>
                    <label>${this._t("form.camera_name")}<input id="camera-name" value="${this._escape(this._provisionForm.name || "GoPro")}"></label>
                    <label>${this._t("form.wifi_ssid")}
                      <div class="wifi-field">
                        <input id="ssid" list="wifi-ssids" value="${this._escape(this._provisionForm.ssid || "")}" placeholder="${this._t("placeholder.ssid")}">
                        <button class="ghost" data-action="scan-access-points" ${this._busy || !this._adapter?.scanAccessPoints ? "disabled" : ""}>${this._t("action.scan_wifi")}</button>
                      </div>
                      <datalist id="wifi-ssids">
                        ${this._wifiOptions()}
                      </datalist>
                      ${this._provisionAccessPoints.length ? `<span class="wifi-hint">${this._escape(this._wifiSummary())}</span>` : ""}
                    </label>
                    <label>${this._t("form.wifi_password")}<input id="wifi-password" type="password" value="${this._escape(this._provisionForm.password || "")}"></label>
                    <div class="provision-progress">
                      ${this._provisionEvents.length ? this._provisionEvents.map((event) => this._progressLine(event)).join("") : `<div class="empty">${this._t("empty.provision_progress")}</div>`}
                    </div>
                  </div>
                  <div class="modal-actions">
                    <button class="ghost" data-action="scan" ${this._busy ? "disabled" : ""}>${this._t("action.scan_ble")}</button>
                    <div class="row">
                      <button class="ghost" data-action="close-provision" ${this._busy ? "disabled" : ""}>${this._t("action.cancel")}</button>
                      <button class="primary" data-action="provision" ${this._busy ? "disabled" : ""}>${this._t("action.configure_cohn")}</button>
                    </div>
                  </div>
                </div>
              </div>`
            : ""
        }
        <div class="modal-backdrop ${this._showSettingsModal ? "open" : ""}" data-action="close-settings-backdrop">
          <div class="modal settings-modal" role="dialog" aria-modal="true" aria-label="${this._t("modal.settings_title")}">
            <div class="modal-head">
              <div class="modal-title">
                <strong>${this._t("modal.settings_title")}</strong>
                <span>${this._escape(this._t("modal.settings_description", { mode: this._modeLabel(camera?.current_mode || "video") }))}</span>
              </div>
              <button class="ghost icon-button" data-action="close-settings" aria-label="${this._t("action.close")}">×</button>
            </div>
            <div class="settings-workspace">
              ${this._presetMarkup(camera)}
              ${this._settingsMarkup(camera)}
            </div>
          </div>
        </div>
      </main>
    `;

    this._bind();
    this._mountPreviewPlayer();
  }

  _bind() {
    const root = this.shadowRoot;
    root.querySelector("#camera-select")?.addEventListener("change", (event) => {
      this._selected = event.target.value;
      this._media = [];
      this._render();
    });
    root.querySelectorAll("[data-camera-id]").forEach((button) => {
      button.addEventListener("click", () => {
        this._media = [];
        const camera = this._cameras.find((item) => item.id === button.dataset.cameraId);
        this._selected = button.dataset.cameraId;
        if (this._adapter?.provisionCohn) this._openProvisionForCamera(camera);
        else this._render();
      });
    });
    root.querySelectorAll("[data-command]").forEach((button) => {
      button.addEventListener("click", () => {
        const command = button.dataset.command;
        if (command === "shutter_start") this._command("shutter", { active: true });
        else if (command === "shutter_stop") this._command("shutter", { active: false });
        else this._command(command);
      });
    });
    root.querySelector("[data-action='refresh']")?.addEventListener("click", () => this._refresh());
    root.querySelector("[data-action='open-settings']")?.addEventListener("click", () => this._openSettingsModal());
    root.querySelectorAll("[data-action='close-settings']").forEach((button) => button.addEventListener("click", () => this._closeSettingsModal()));
    root.querySelector("[data-action='close-settings-backdrop']")?.addEventListener("click", (event) => {
      if (event.target === event.currentTarget) this._closeSettingsModal();
    });
    root.querySelector("[data-action='open-provision']")?.addEventListener("click", () => this._openProvisionModal());
    root.querySelectorAll("[data-action='close-provision']").forEach((button) => button.addEventListener("click", () => this._closeProvisionModal()));
    root.querySelector("[data-action='close-provision-backdrop']")?.addEventListener("click", (event) => {
      if (event.target === event.currentTarget) this._closeProvisionModal();
    });
    root.querySelectorAll("[data-mode-tab]").forEach((button) => {
      button.addEventListener("click", () => this._command("set_mode", { mode: button.dataset.modeTab }));
    });
    root.querySelector("[data-action='scan']")?.addEventListener("click", () => this._scan());
    root.querySelector("[data-action='scan-access-points']")?.addEventListener("click", () => this._scanAccessPoints());
    root.querySelector("[data-action='provision']")?.addEventListener("click", () => this._provision());
    root.querySelectorAll("[data-scan-address]").forEach((button) => {
      button.addEventListener("click", () => {
        const device = this._scanDevices.find((item) => item.address === button.dataset.scanAddress);
        if (device) this._selectScanDevice(device);
      });
    });
    root.querySelectorAll("[data-action='media']").forEach((button) => button.addEventListener("click", () => this._loadMedia()));
    root.querySelectorAll("[data-setting-id]").forEach((button) => {
      button.addEventListener("click", () => {
        const setting = button.dataset.settingId;
        const option = root.querySelector(`#setting-${CSS.escape(setting)}`)?.value;
        if (setting && option) this._command("set_setting", { setting, option });
      });
    });
    root.querySelectorAll("[data-preset-id]").forEach((button) => {
      button.addEventListener("click", () => {
        const preset = button.dataset.presetId;
        if (preset) this._command("set_preset", { preset });
      });
    });
  }

  _cameraSubtitle(camera) {
    const address = camera.ble_address || camera.address || `${this._t("unknown")} BLE`;
    const endpoint = camera.endpoint || [camera.http_scheme, camera.http_host].filter(Boolean).join("://");
    return `${address}${endpoint ? ` · ${endpoint}` : ""}`;
  }

  _cameraCard(camera) {
    return `
      <button class="camera-card ${camera.id === this._selected ? "active" : ""}" data-camera-id="${this._escape(camera.id)}">
        <span><strong>${this._escape(camera.name || "GoPro")}</strong><br><small>${this._escape(this._cameraSubtitle(camera))}</small></span>
        <i class="state-dot ${this._escape(this._powerClass(camera))}" title="${this._escape(this._powerLabel(camera))}"></i>
      </button>
    `;
  }

  _scanDevice(device) {
    const active = device.address && device.address === this._provisionForm.ble_address;
    return `
      <button class="scan-device ${active ? "active" : ""}" data-scan-address="${this._escape(device.address || "")}">
        <span><strong>${this._escape(device.name || "GoPro")}</strong><small>${this._escape(device.address || "unknown")}</small></span>
        <small>${device.rssi != null ? `${this._escape(device.rssi)} dBm` : ""}</small>
      </button>
    `;
  }

  _wifiOptions() {
    const seen = new Set();
    return this._provisionAccessPoints
      .filter((point) => point.ssid && !seen.has(point.ssid) && seen.add(point.ssid))
      .map((point) => {
        const frequency = point.signal_frequency_mhz || point.frequency;
        const bars = point.signal_strength_bars ?? point.bars;
        const label = [
          bars != null ? this._t("wifi.bars", { count: bars }) : "",
          frequency ? `${frequency} MHz` : "",
          point.current ? this._t("wifi.current") : "",
          point.configured ? this._t("wifi.configured") : "",
        ].filter(Boolean).join(" · ");
        return `<option value="${this._escape(point.ssid)}"${label ? ` label="${this._escape(label)}"` : ""}></option>`;
      })
      .join("");
  }

  _wifiSummary() {
    const count = new Set(this._provisionAccessPoints.map((point) => point.ssid).filter(Boolean)).size;
    return count ? this._t("wifi.summary", { count }) : "";
  }

  _progressLine(event) {
    const stage = event.stage || event.type || "progress";
    return `
      <div class="progress-line">
        <span>${this._escape(event.time || "")}</span>
        <strong>${this._escape(this._stageLabel(stage, event))}</strong>
      </div>
    `;
  }

  _stageLabel(stage, event = {}) {
    const labels = {
      start: this._t("stage.start"),
      resolve_ble: this._t("stage.resolve_ble"),
      ble_connect: this._t("stage.ble_connect"),
      set_datetime: this._t("stage.set_datetime"),
      scan_wifi: this._t("stage.scan_wifi"),
      scan_wifi_done: this._t("stage.scan_wifi_done", { count: (event.access_points || []).length }),
      connect_wifi: this._t("stage.connect_wifi"),
      connect_wifi_done: this._t("stage.connect_wifi_done"),
      clear_certificate: this._t("stage.clear_certificate"),
      create_certificate: this._t("stage.create_certificate"),
      get_certificate: this._t("stage.get_certificate"),
      wait_cohn_status: this._t("stage.wait_cohn_status"),
      cohn_status_done: this._t("stage.cohn_status_done", { address: event.credentials?.ip_address || "" }),
      done: this._t("stage.done"),
      failed: this._t("stage.failed"),
      error: this._t("stage.error"),
    };
    return labels[stage] || stage;
  }

  _powerClass(camera) {
    const power = camera.power || (camera.phase === "http_ready" ? "on" : "");
    if (power === "on") return "on";
    if (power === "standby") return "standby";
    if (power === "off") return "off";
    if (power === "checking") return "checking";
    return "unknown";
  }

  _powerLabel(camera) {
    const power = camera.power || (camera.phase === "http_ready" ? "on" : "unknown");
    const labels = {
      on: this._t("power.on"),
      standby: this._t("power.standby"),
      off: this._t("power.off"),
      checking: this._t("power.checking"),
      unknown: this._t("power.unknown"),
    };
    return labels[power] || labels.unknown;
  }

  _canControl(camera) {
    return Boolean(camera && (camera.http_ready || camera.phase === "http_ready" || camera.power === "on"));
  }

  _canWake(camera) {
    return Boolean(camera && !this._busy && !this._canControl(camera));
  }

  _previewMarkup(camera) {
    if (!camera) {
      return `<div class="reticle"><strong>${this._t("preview.offline_title")}</strong><span>${this._t("preview.offline_body")}</span></div>`;
    }
    const url = this._previewUrl(camera);
    if (url) {
      const overlay = this._previewOverlay(camera);
      if (this._previewTransport(camera, url) === "mpegts") {
        return `<video class="preview-video" data-preview-url="${this._escape(url)}" muted autoplay playsinline controls></video>${overlay}`;
      }
      return `<img class="preview-stream" src="${this._escape(url)}" alt="GoPro Live Preview">${overlay}`;
    }
    if (!this._adapter?.previewUrl) {
      return `<div class="reticle"><strong>${this._t("preview.reserved_title")}</strong><span>${this._t("preview.reserved_body")}</span></div>`;
    }
    return `<div class="reticle"><strong>${this._t("preview.standby_title")}</strong><span>${this._escape(camera.preview_error || this._t("preview.standby_body"))}</span></div>`;
  }

  _previewOverlay(camera) {
    const capture = this._captureUi(camera);
    const mode = this._modeLabel(camera?.current_mode || "video");
    const preset = camera?.preset ? `Preset ${camera.preset}` : `Preset ${this._t("unknown")}`;
    const recording = camera?.recording ? capture.activeLabel : this._t("capture.ready");
    const settings = camera?.settings || {};
    const detail = this._modeDetails(camera?.current_mode, settings);
    return `
      <div class="preview-overlay">
        <div><span>${this._escape(mode)}</span><strong>${this._escape(recording)}</strong></div>
        <div><span>${this._escape(preset)}</span><strong>${this._escape(detail)}</strong></div>
      </div>
    `;
  }

  _captureUi(camera) {
    const mode = camera?.current_mode || "video";
    const active = Boolean(camera?.recording);
    if (mode === "photo") {
      return {
        command: active ? "shutter_stop" : "shutter_start",
        label: active ? this._t("capture.stop_capture") : this._t("capture.take_photo"),
        activeLabel: this._t("capture.capturing"),
        className: "photo",
      };
    }
    if (mode === "timelapse") {
      return {
        command: active ? "shutter_stop" : "shutter_start",
        label: active ? this._t("capture.stop_lapse") : this._t("capture.start_lapse"),
        activeLabel: this._t("capture.lapse_running"),
        className: "lapse",
      };
    }
    return {
      command: active ? "shutter_stop" : "shutter_start",
      label: active ? this._t("capture.stop_recording") : this._t("capture.start_recording"),
      activeLabel: this._t("capture.recording"),
      className: "video",
    };
  }

  _modeDetails(mode, settings) {
    if (mode === "photo") {
      return [
        this._settingDisplay("122", this._t("setting.lens"), settings),
        this._settingDisplay("125", this._t("setting.output"), settings),
      ].filter(Boolean).join(" · ") || this._t("setting.photo");
    }
    if (mode === "timelapse") {
      return [
        this._settingDisplay("187", this._t("setting.mode"), settings),
        this._settingDisplay("123", this._t("setting.lens"), settings),
      ].filter(Boolean).join(" · ") || this._t("setting.lapse");
    }
    return [
      this._settingDisplay("2", this._t("setting.res"), settings),
      this._settingDisplay("3", "FPS", settings),
      this._settingDisplay("121", this._t("setting.lens"), settings),
    ].filter(Boolean).join(" · ") || this._t("setting.video");
  }

  _settingDisplay(settingId, label, settings) {
    const setting = SETTING_GROUPS.flatMap((group) => group.settings).find((item) => item.id === settingId);
    const value = settings?.[settingId] ?? settings?.[Number(settingId)];
    if (value == null) return "";
    const text = this._settingLabel(setting || { options: [] }, String(value));
    return `${label} ${text}`;
  }

  _previewUrl(camera) {
    if (camera.preview_url) return camera.preview_url;
    if (camera.preview_active && this._adapter?.previewUrl) return this._adapter.previewUrl(camera.id);
    return "";
  }

  _previewTransport(camera, url = "") {
    return camera?.preview_transport || (url.endsWith(".ts") ? "mpegts" : "mjpeg");
  }

  _mountPreviewPlayer() {
    const video = this.shadowRoot?.querySelector(".preview-video");
    if (!video) return;
    const url = this._absoluteUrl(video.dataset.previewUrl || "");
    const mpegts = window.mpegts;
    if (!url || !mpegts?.getFeatureList?.().mseLivePlayback) {
      this._message = this._t("error.mpegts_unsupported");
      return;
    }
    try {
      const player = mpegts.createPlayer(
        { type: "mpegts", isLive: true, url },
        {
          enableWorker: true,
          enableStashBuffer: false,
          liveBufferLatencyChasing: true,
          liveBufferLatencyMaxLatency: 1.5,
          liveBufferLatencyMinRemain: 0.5,
        }
      );
      player.on?.(mpegts.Events.ERROR, (type, detail, info) => {
        this._message = JSON.stringify({ type, detail, info }, null, 2);
        this._render();
      });
      player.attachMediaElement(video);
      player.load();
      player.play()?.catch?.((error) => {
        this._message = JSON.stringify(this._errorDetail(error), null, 2);
      });
      this._previewPlayer = player;
    } catch (error) {
      this._message = JSON.stringify(this._errorDetail(error), null, 2);
    }
  }

  _absoluteUrl(url) {
    if (!url) return "";
    try {
      return new URL(url, window.location.href).toString();
    } catch {
      return url;
    }
  }

  _teardownPreviewPlayer() {
    const player = this._previewPlayer;
    if (!player) return;
    this._previewPlayer = null;
    try {
      player.pause?.();
      player.unload?.();
      player.detachMediaElement?.();
      player.destroy?.();
    } catch {
      // Ignore teardown errors from a media element that was already removed.
    }
  }

  _logText(camera) {
    if (!camera?.status_error) return this._message;
    const detail = camera.status_detail ? JSON.stringify(camera.status_detail, null, 2) : "";
    return `${this._t("error.state_failed")}: ${camera.status_error}${detail ? `\n\n${detail}` : ""}\n\n${this._message}`;
  }

  _errorDetail(error) {
    if (error && (error.error || error.trace || error.recovery_error)) return error;
    return {
      error: error?.message || String(error),
      name: error?.name || "Error",
      stack: error?.stack || null,
    };
  }

  _metric(label, value) {
    return `<div class="metric"><span>${this._escape(label)}</span><strong>${this._escape(String(value ?? "unknown"))}</strong></div>`;
  }

  _previewMetric(label, value) {
    return `<div class="preview-metric"><span>${this._escape(label)}</span><strong>${this._escape(String(value ?? "unknown"))}</strong></div>`;
  }

  _presetMarkup(camera) {
    if (!camera) return "";
    const group = this._currentPresetGroup(camera);
    if (!group) {
      return `<div class="preset-empty">${this._t("empty.preset_status")}</div>`;
    }
    const presets = this._presetItems(group);
    return `
      <aside class="preset-pane">
        <div class="pane-title">
          <span>${this._t("panel.presets")}</span>
          <strong>${this._escape(this._modeLabel(camera.current_mode || "video"))}</strong>
        </div>
        <div class="preset-list">
          ${presets.map((preset) => this._presetButton(camera, preset)).join("") || `<span class="preset-empty">${this._t("empty.no_presets")}</span>`}
        </div>
      </aside>
    `;
  }

  _presetGroups() {
    const payload = this._presetStatus || {};
    const groups = payload.presetGroupArray || payload.preset_groups || payload.groups || payload.presets || [];
    return Array.isArray(groups) ? groups : [];
  }

  _presetItems(group) {
    const presets = group.presetArray || group.presets || group.preset || group.items || [];
    return Array.isArray(presets) ? presets : [];
  }

  _currentPresetGroup(camera) {
    const mode = camera?.current_mode || "video";
    return this._presetGroups().find((group) => this._presetGroupMode(group) === mode) || null;
  }

  _presetButton(camera, preset) {
    const id = this._presetId(preset);
    const active = this._presetIsActive(camera, preset);
    const settings = this._presetSettingsSummary(preset);
    const disabled = !id || !this._canControl(camera);
    return `
      <button class="preset-button ${active ? "active" : ""}" data-preset-id="${this._escape(id)}" ${disabled ? "disabled" : ""}>
        <span class="preset-name">${this._escape(this._presetTitle(preset))}</span>
        <span class="preset-meta">${this._escape(settings || `ID ${id || this._t("unknown")}`)}</span>
      </button>
    `;
  }

  _presetIsActive(camera, preset) {
    const id = this._presetId(preset);
    return Boolean(
      preset.current ||
      preset.active ||
      preset.is_current ||
      (id && String(camera?.preset || "") === String(id))
    );
  }

  _presetId(preset) {
    const id = preset.id ?? preset.preset_id ?? preset.preset;
    return id == null ? "" : String(id);
  }

  _presetTitle(item) {
    const raw = item.customName || item.title || item.name || item.display_name || item.label;
    if (raw) return this._humanPresetTitle(raw);
    if (item.titleId != null) return this._humanPresetTitle(String(item.titleId));
    return `Preset ${this._presetId(item)}`;
  }

  _humanPresetTitle(value) {
    return String(value)
      .replace(/^Title\s+/i, "")
      .replace(/^PRESET_TITLE_/i, "")
      .replace(/^PRESET_GROUP_ID_/i, "")
      .replaceAll("_", " ")
      .toLowerCase()
      .replace(/\b\w/g, (char) => char.toUpperCase());
  }

  _presetGroupMode(group) {
    const id = group.id ?? group.group_id ?? group.preset_group;
    const title = String(this._presetTitle(group)).toLowerCase();
    if (id === 1000 || id === "1000" || title.includes("video")) return "video";
    if (id === 1001 || id === "1001" || title.includes("photo")) return "photo";
    if (id === 1002 || id === "1002" || title.includes("time")) return "timelapse";
    return "";
  }

  _presetSettingsSummary(preset) {
    const settings = preset.settingArray || preset.settings || preset.setting_values || [];
    if (!Array.isArray(settings)) return "";
    return settings
      .slice(0, 3)
      .map((item) => {
        const setting = item.setting_id ?? item.setting ?? item.id;
        const option = item.option_id ?? item.option ?? item.value;
        if (setting == null || option == null) return "";
        return `${setting}:${option}`;
      })
      .filter(Boolean)
      .join(" · ");
  }

  _settingsMarkup(camera) {
    if (!camera) return `<div class="empty">${this._t("empty.camera_settings")}</div>`;
    const ids = this._activePresetSettingIds(camera);
    const groups = SETTING_GROUPS.map((group) => ({
      ...group,
      settings: ids.size ? group.settings.filter((setting) => ids.has(setting.id)) : group.settings,
    })).filter((group) => group.settings.length);
    const empty = ids.size && !groups.length;
    return `
      <section class="settings-pane">
        <div class="pane-title settings-pane-title">
          <span>${this._t("panel.current_preset")}</span>
          <strong>${this._escape(this._presetTitle(this._activePreset(camera) || {}))}</strong>
        </div>
        ${empty ? `<div class="preset-empty">${this._t("empty.settings_unmatched")}</div>` : ""}
        <div class="settings-grid">
          ${groups.map((group) => `
            <section class="settings-group">
              <div class="settings-group-head">
                <strong>${this._escape(group.title)}</strong>
                <span>${this._escape(group.description)}</span>
              </div>
              <div class="setting-list">
                ${group.settings.map((setting) => this._settingControl(camera, setting)).join("")}
              </div>
            </section>
          `).join("")}
        </div>
      </section>
    `;
  }

  _settingControl(camera, setting) {
    const current = this._settingValue(camera, setting.id);
    const hasCurrent = current !== "";
    const knownCurrent = setting.options.some(([value]) => value === current);
    const canControl = this._canControl(camera);
    const options = [
      ...(hasCurrent && !knownCurrent ? [[current, this._t("setting.current", { value: current })]] : []),
      ...setting.options,
    ];
    return `
      <div class="setting-control">
        <label for="setting-${this._escape(setting.id)}">
          <span>${this._escape(setting.label)}</span>
          <small>${hasCurrent ? this._escape(this._settingLabel(setting, current)) : `ID ${this._escape(setting.id)}`}</small>
        </label>
        <div class="setting-input">
          <select id="setting-${this._escape(setting.id)}" ${canControl ? "" : "disabled"}>
            ${options.map(([value, label]) => `<option value="${this._escape(value)}" ${value === current ? "selected" : ""}>${this._escape(label)}</option>`).join("")}
          </select>
          <button class="mini-button" data-setting-id="${this._escape(setting.id)}" ${canControl ? "" : "disabled"}>${this._t("action.apply")}</button>
        </div>
      </div>
    `;
  }

  _settingValue(camera, settingId) {
    const presetValue = this._activePresetSettingValue(camera, settingId);
    const value = presetValue ?? camera?.settings?.[settingId] ?? camera?.settings?.[Number(settingId)];
    return value == null ? "" : String(value);
  }

  _activePreset(camera) {
    for (const group of this._presetGroups()) {
      for (const preset of this._presetItems(group)) {
        if (this._presetIsActive(camera, preset)) return preset;
      }
    }
    return null;
  }

  _activePresetSettingIds(camera) {
    const preset = this._activePreset(camera);
    const settings = preset?.settingArray || preset?.settings || preset?.setting_values || [];
    if (!Array.isArray(settings)) return new Set();
    return new Set(
      settings
        .map((item) => item.id ?? item.setting_id ?? item.setting)
        .filter((id) => id != null)
        .map(String)
    );
  }

  _activePresetSettingValue(camera, settingId) {
    const preset = this._activePreset(camera);
    const settings = preset?.settingArray || preset?.settings || preset?.setting_values || [];
    if (!Array.isArray(settings)) return null;
    const match = settings.find((item) => String(item.id ?? item.setting_id ?? item.setting) === String(settingId));
    return match?.value ?? match?.option_id ?? match?.option ?? null;
  }

  _settingLabel(setting, value) {
    const option = setting.options.find(([candidate]) => candidate === value);
    return option?.[1] || value;
  }

  _modeLabel(mode) {
    const labels = {
      video: this._t("mode.video"),
      photo: this._t("mode.photo"),
      timelapse: this._t("mode.timelapse"),
    };
    return labels[mode] || mode;
  }

  _mediaItem(item) {
    const type = item.media_type?.startsWith("image/") ? "IMG" : "VID";
    const href = item.url || item.path || "#";
    const thumbnail = item.thumbnail || "";
    const size = item.size ? this._formatBytes(item.size) : "";
    const thumb = thumbnail
      ? `<img src="${this._escape(thumbnail)}" alt="${this._escape(item.name || "media")}" loading="lazy" onerror="this.remove()">`
      : `<span class="badge">${type}</span>`;
    return `
      <a class="media-item" href="${this._escape(href)}" target="_blank" rel="noreferrer">
        <div class="thumb">${thumb}</div>
        <div class="media-body">
          <div class="badge">${type}</div>
          <strong>${this._escape(item.name || item.path || "media")}</strong>
          <span>${this._escape([item.directory, size].filter(Boolean).join(" · ") || item.media_type || "")}</span>
        </div>
      </a>
    `;
  }

  _formatBytes(value) {
    const bytes = Number(value);
    if (!Number.isFinite(bytes)) return "";
    const units = ["B", "KB", "MB", "GB"];
    let size = bytes;
    let index = 0;
    while (size >= 1024 && index < units.length - 1) {
      size /= 1024;
      index += 1;
    }
    return `${size.toFixed(index === 0 ? 0 : 1)} ${units[index]}`;
  }

  _escape(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }
}

customElements.define("opengopro-console", OpenGoProConsole);
