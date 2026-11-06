import { CONSOLE_STYLES } from "./opengopro-console-styles.js?v=17";

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
    "empty.media": "Refresh to show camera media.",
    "media.empty": "No media found on the camera.",
    "media.loading": "Loading camera media…",
    "media.error": "Could not load media",
    "media.offline": "Connect the camera to browse its media.",
    "media.description": "Browse photos and videos stored on this camera.",
    "media.refresh": "Refresh media",
    "media.select_all": "Select all",
    "media.delete": "Delete selected",
    "media.confirm_delete": "Delete {count} selected file(s) from the camera? This cannot be undone.",
    "media.delete_failed": "Some files could not be deleted",
    "media.unknown_time": "Capture time unavailable",
    "media.close_player": "Close player",
    "media.download": "Download original",
    "media.play_error": "This video could not be played. Check the camera connection or download the original; your browser may not support its video format.",
    "preset.active": "Active",
    "empty.no_presets": "No presets",
    "empty.preset_status": "Camera Preset Status has not been loaded. Confirm the current preset before writing parameters.",
    "empty.provision": "Scan BLE and choose a camera, or enter the BLE address manually.",
    "empty.provision_progress": "Provisioning progress appears here in real time.",
    "empty.settings_unmatched": "The current preset did not match built-in setting controls. Use the setting:value entries on the preset card; this mapping can be expanded later.",
    "error.mpegts_unsupported": "This browser does not support mpegts.js/MSE live playback",
    "error.preview_retry": "Preview playback failed; reconnecting ({count}/3).",
    "error.preview_failed": "Preview playback failed. Check the browser's video codec support and network, then restart the preview.",
    "error.need_ble": "Scan and select a GoPro first, or enter the BLE address manually",
    "error.need_ble_scan": "Select a GoPro from the BLE scan list first, or enter the BLE address manually",
    "error.need_wifi": "Home Wi-Fi SSID and password are required",
    "error.state_failed": "State read failed",
    "form.ble_address": "BLE address",
    "form.camera_name": "Name",
    "form.wifi_password": "Home Wi-Fi password",
    "form.wifi_ssid": "Wi-Fi SSID",
    "hint.no_camera": "No camera selected. Scan BLE first and configure HERO12 COHN.",
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
    "preview.rotate": "Rotate {angle}°",
    "preview.rotate_hint": "Rotate preview clockwise by 90 degrees",
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
    "stage.scan_wifi_error": "Wi-Fi scan failed: {message}",
    "stage.scan_wifi_timeout": "Wi-Fi scan timed out while waiting for the camera",
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
    "empty.media": "刷新后显示相机媒体。",
    "media.empty": "相机中暂无媒体文件。",
    "media.loading": "正在读取相机媒体…",
    "media.error": "媒体读取失败",
    "media.offline": "连接相机后可浏览媒体文件。",
    "media.description": "浏览保存在此相机中的照片和视频。",
    "media.refresh": "刷新媒体",
    "media.select_all": "全选",
    "media.delete": "删除所选",
    "media.confirm_delete": "确定从相机删除选中的 {count} 个文件吗？此操作无法撤销。",
    "media.delete_failed": "部分文件删除失败",
    "media.unknown_time": "拍摄时间未知",
    "media.close_player": "关闭播放器",
    "media.download": "下载原文件",
    "media.play_error": "无法播放此视频。请检查相机连接或下载原文件；当前浏览器可能不支持此视频格式。",
    "preset.active": "当前使用",
    "empty.no_presets": "暂无 preset",
    "empty.preset_status": "未读取到相机 Preset Status。参数写入前建议先确认当前相机 preset。",
    "empty.provision": "点击扫描 BLE 后选择相机，或手动填写 BLE 地址。",
    "empty.provision_progress": "配置过程会实时显示在这里。",
    "empty.settings_unmatched": "当前 preset 没有匹配到内置设置控件。请查看 preset 卡片里的 setting:value，后续可继续扩充映射。",
    "error.mpegts_unsupported": "当前浏览器不支持 mpegts.js/MSE Live Playback",
    "error.preview_retry": "预览播放出错，正在重新连接（{count}/3）。",
    "error.preview_failed": "预览播放失败，请检查浏览器视频编码支持和网络，然后重新启动预览。",
    "error.need_ble": "请先扫描并选择 GoPro，或手动填写 BLE 地址",
    "error.need_ble_scan": "请先从 BLE 扫描列表选择 GoPro，或手动填写 BLE 地址",
    "error.need_wifi": "家庭 Wi-Fi SSID 和密码是必填字段",
    "error.state_failed": "状态读取失败",
    "form.ble_address": "BLE 地址",
    "form.camera_name": "名称",
    "form.wifi_password": "家庭 Wi-Fi 密码",
    "form.wifi_ssid": "Wi-Fi SSID",
    "hint.no_camera": "还没有选择相机。可以先扫描 BLE 并配置 HERO12 COHN。",
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
    "modal.settings_description": "{mode}预设与当前参数。",
    "modal.settings_title": "相机设置",
    "panel.cameras": "相机列表",
    "panel.log": "日志",
    "panel.media": "媒体",
    "panel.presets": "预设",
    "panel.current_preset": "当前预设",
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
    "preview.rotate": "旋转 {angle}°",
    "preview.rotate_hint": "顺时针旋转预览 90 度",
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
    "stage.scan_wifi_error": "Wi-Fi 扫描失败：{message}",
    "stage.scan_wifi_timeout": "Wi-Fi 扫描超时：相机未返回扫描结果",
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
    this._mediaSelected = new Set();
    this._mediaPlaying = null;
    this._mediaPlaybackError = false;
    this._showMediaModal = false;
    this._mediaLoading = false;
    this._mediaLoaded = false;
    this._mediaError = "";
    this._mediaRequest = 0;
    this._presetStatus = null;
    this._scanDevices = [];
    this._provisionAccessPoints = [];
    this._provisionEvents = [];
    this._currentAccessPointSsid = "";
    this._provisionForm = {};
    this._busy = false;
    this._showProvisionModal = false;
    this._showSettingsModal = false;
    this._settingsError = "";
    this._showSchedulesModal = false;
    this._schedules = [];
    this._scheduleTimezone = "";
    this._scheduleDraft = null;
    this._scheduleHistory = null;
    this._scheduleError = "";
    this._message = this._t("log.idle");
    this._presenceRequests = new Map();
    this._pollTimer = null;
    this._stateSource = null;
    this._stateSourceCamera = null;
    this._stateStreamConnected = false;
    this._stateStreamHasData = false;
    this._statusGeneration = 0;
    this._statusSnapshotTimer = null;
    this._snapshotPending = null;
    this._visibilityHandler = () => {
      if (document.hidden) {
        this._stopPolling();
        this._closeStateStream();
      } else {
        this._startPolling();
        this._syncStateStream();
        this._pollState();
      }
    };
    document.addEventListener("visibilitychange", this._visibilityHandler);
    this._selectOutsideHandler = (event) => {
      if (!event.composedPath().includes(this)) this._closeSelect();
    };
    this._selectResizeHandler = () => this._closeSelect();
    this._selectScrollHandler = (event) => {
      if (this._selectMenu && !this._selectMenu.contains(event.target)) this._closeSelect();
    };
    this._selectRootHandler = (event) => {
      if (this._selectMenu && !event.composedPath().includes(this._selectMenu) && !event.composedPath().includes(this._selectTrigger)) this._closeSelect();
    };
    document.addEventListener("pointerdown", this._selectOutsideHandler);
    window.addEventListener("resize", this._selectResizeHandler);
    this.shadowRoot.addEventListener("scroll", this._selectScrollHandler, true);
    this.shadowRoot.addEventListener("pointerdown", this._selectRootHandler);
    this._previewPlayer = null;
    this._previewRetryTimer = null;
    this._previewStableTimer = null;
    this._previewRetryCount = 0;
    this._previewBlocked = false;
    this._previewRotations = new Map();
    this._refresh();
    this._startPolling();
  }

  disconnectedCallback() {
    this._stopPolling();
    this._closeStateStream();
    document.removeEventListener("visibilitychange", this._visibilityHandler);
    document.removeEventListener("pointerdown", this._selectOutsideHandler);
    window.removeEventListener("resize", this._selectResizeHandler);
    this.shadowRoot?.removeEventListener("scroll", this._selectScrollHandler, true);
    this.shadowRoot?.removeEventListener("pointerdown", this._selectRootHandler);
    this._presenceRequests?.clear();
    this._resetPreviewRecovery();
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
    if (this._showSettingsModal) this._settingsError = "";
    this._message = `${label}...`;
    this._render();
    try {
      const result = await action();
      this._message = typeof result === "string" ? result : JSON.stringify(result, null, 2);
      if (reloadCameras) await this._loadCameras();
    } catch (error) {
      this._message = JSON.stringify(this._errorDetail(error), null, 2);
      if (this._showSettingsModal) this._settingsError = error?.error?.message || error?.error || error?.message || String(error);
    } finally {
      this._busy = false;
      this._render();
    }
  }

  async _refresh() {
    await this._run(this._t("run.refresh"), async () => {
      await this._loadCameras();
      return this._t("run.refreshed");
    }, { reloadCameras: false });
  }

  async _loadCameras() {
    const previousSelection = this._selected;
    const cameras = await this._adapter.listCameras();
    // Status events can arrive while listCameras is in flight. Merge against
    // the current state, not a copy taken before the request started.
    const existing = new Map(this._cameras.map((camera) => [camera.id, camera]));
    this._cameras = cameras.map((camera) => ({
      ...existing.get(camera.id),
      ...camera,
    }));
    if (!this._selected && this._cameras.length) this._selected = this._cameras[0].id;
    if (this._selected && !this._cameras.some((camera) => camera.id === this._selected)) {
      this._selected = this._cameras[0]?.id || null;
    }
    if (previousSelection !== this._selected) {
      this._resetPreviewRecovery();
      this._media = [];
      this._mediaSelected = new Set();
      this._mediaPlaying = null;
      this._mediaLoaded = false;
      this._mediaError = "";
      this._mediaLoading = false;
      this._mediaRequest++;
    }
    this._syncStateStream();
    this._probePresence();
    this._probePreviewStatus();
  }

  async _command(command, extra = {}) {
    if (!this._selected) return;
    if (["start_preview", "stop_preview", "sleep"].includes(command)) this._resetPreviewRecovery();
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
    const cameraId = this._selected;
    const result = await this._adapter.loadState(cameraId);
    const state = result?.state || result;
    this._mergeCameraState(cameraId, state);
  }

  async _loadPresets() {
    if (!this._selected || !this._adapter?.loadPresets) return;
    this._presetStatus = await this._adapter.loadPresets(this._selected);
  }

  _startPolling() {
    this._stopPolling();
    if (document.hidden) return;
    this._pollTimer = window.setInterval(() => this._pollState(), 30000);
  }

  _stopPolling() {
    if (!this._pollTimer) return;
    window.clearInterval(this._pollTimer);
    this._pollTimer = null;
  }

  async _pollState() {
    if (!this._adapter || this._busy || this._scheduleDraft || document.hidden || this._polling) return;
    this._polling = true;
    const before = JSON.stringify(this._cameras);
    try {
      await this._loadCameras();
      if ((!this._stateStreamConnected || !this._stateStreamHasData) && this._selected) {
        await this._loadStatusSnapshot(this._selected);
      }
      if (JSON.stringify(this._cameras) !== before && this._canRenderBackground()) this._render();
    } catch (error) {
      if (this._selected) {
        this._mergeCamera(this._selected, {
          status_error: error?.error || error?.message || String(error),
          status_detail: error?.status_detail || error?.trace || null,
        });
        if (this._canRenderBackground()) this._render();
      }
    } finally {
      this._polling = false;
    }
  }

  _closeStateStream() {
    if (this._statusSnapshotTimer) window.clearTimeout(this._statusSnapshotTimer);
    this._statusSnapshotTimer = null;
    this._statusGeneration++;
    this._stateSource?.close();
    this._stateSource = null;
    this._stateSourceCamera = null;
    this._stateStreamConnected = false;
    this._stateStreamHasData = false;
  }

  _canRenderBackground() {
    return !this._busy && !this._scheduleDraft && !this._showProvisionModal
      && !this._showSettingsModal && !this._showSchedulesModal && !this._showMediaModal;
  }

  _syncStateStream() {
    const cameraId = this._selected;
    if (document.hidden || !cameraId || !this._adapter?.subscribeState) {
      this._closeStateStream();
      return;
    }
    if (this._stateSource && this._stateSourceCamera === cameraId) return;
    this._closeStateStream();
    this._stateSourceCamera = cameraId;
    this._stateSource = this._adapter.subscribeState(cameraId, (update) => {
      if (this._stateSourceCamera !== cameraId || !this._cameras.some((camera) => camera.id === cameraId)) return;
      this._stateStreamHasData = true;
      this._statusGeneration++;
      if (this._statusSnapshotTimer) window.clearTimeout(this._statusSnapshotTimer);
      this._statusSnapshotTimer = null;
      this._applyStatusUpdate(cameraId, update);
    }, (connected) => {
      if (this._stateSourceCamera === cameraId) this._stateStreamConnected = connected;
    });
    if (this._adapter.loadStatusSnapshot) {
      this._statusSnapshotTimer = window.setTimeout(() => {
        this._statusSnapshotTimer = null;
        if (!this._stateStreamHasData) void this._loadStatusSnapshot(cameraId).catch(() => {});
      }, 1000);
    }
  }

  async _loadStatusSnapshot(cameraId) {
    if (!this._adapter?.loadStatusSnapshot || this._snapshotPending === cameraId) return;
    this._snapshotPending = cameraId;
    const generation = this._statusGeneration;
    try {
      const update = await this._adapter.loadStatusSnapshot(cameraId);
      if (this._selected === cameraId && this._statusGeneration === generation) {
        this._applyStatusUpdate(cameraId, update);
      }
    } finally {
      if (this._snapshotPending === cameraId) this._snapshotPending = null;
    }
  }

  _applyStatusUpdate(cameraId, update) {
    if (!update || typeof update !== "object") return;
    const before = JSON.stringify(this._cameras);
    if (update.state) this._mergeCameraState(cameraId, update.state);
    const { state, ...presence } = update;
    this._mergeCamera(cameraId, presence);
    if (JSON.stringify(this._cameras) !== before && this._canRenderBackground()) this._render();
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
      if (cameraId === this._stateSourceCamera && this._stateStreamConnected) continue;
      if (this._presenceRequests.has(cameraId)) continue;
      this._mergeCamera(cameraId, { power: camera.power || "checking" });
      const request = this._adapter
        .loadPresence(cameraId)
        .then((presence) => {
          if (!this._cameras.some((camera) => camera.id === cameraId)) return;
          if (cameraId === this._stateSourceCamera && this._stateStreamConnected) return;
          this._mergeCamera(cameraId, presence);
          if (this._canRenderBackground()) this._render();
        })
        .catch((error) => {
          if (!this._cameras.some((camera) => camera.id === cameraId)) return;
          if (cameraId === this._stateSourceCamera && this._stateStreamConnected) return;
          this._mergeCamera(cameraId, {
            power: "unknown",
            presence_error: error?.error || error?.message || String(error),
          });
          if (this._canRenderBackground()) this._render();
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
          if (this._canRenderBackground()) this._render();
        })
        .catch(() => {});
    }
  }

  async _loadMedia() {
    if (!this._selected || this._mediaLoading) return;
    const cameraId = this._selected;
    const requestId = ++this._mediaRequest;
    this._mediaLoading = true;
    this._mediaError = "";
    this._render();
    try {
      const items = await this._adapter.loadMedia(cameraId);
      if (requestId === this._mediaRequest && this._selected === cameraId) {
        this._media = items || [];
        this._mediaSelected = new Set();
        this._mediaLoaded = true;
      }
    } catch (error) {
      if (requestId === this._mediaRequest && this._selected === cameraId) this._mediaError = error?.error?.message || error?.error || error?.message || String(error);
    } finally {
      if (requestId === this._mediaRequest) {
        this._mediaLoading = false;
        this._render();
      }
    }
  }


  async _deleteMedia() {
    if (!this._selected || this._mediaLoading || !this._adapter.deleteMedia || !this._mediaSelected.size) return;
    const cameraId = this._selected;
    const paths = [...this._mediaSelected];
    if (!window.confirm(this._t("media.confirm_delete").replace("{count}", paths.length))) return;
    const requestId = ++this._mediaRequest;
    this._mediaLoading = true;
    this._mediaError = "";
    this._render();
    try {
      const result = await this._adapter.deleteMedia(cameraId, paths);
      if (requestId !== this._mediaRequest || this._selected !== cameraId) return;
      const deleted = new Set(result.deleted || []);
      this._media = this._media.filter((item) => !deleted.has(item.path));
      this._mediaSelected = new Set(paths.filter((path) => !deleted.has(path)));
      if (deleted.has(this._mediaPlaying?.path)) this._mediaPlaying = null;
      if (result.failed?.length) this._mediaError = `${this._t("media.delete_failed")}: ${result.failed.map((item) => `${item.path}: ${item.error}`).join("; ")}`;
    } catch (error) {
      if (requestId === this._mediaRequest && this._selected === cameraId) this._mediaError = error?.error?.message || error?.error || error?.message || String(error);
    } finally {
      if (requestId === this._mediaRequest) { this._mediaLoading = false; this._render(); }
    }
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
      this._appendProvisionEvent({ stage: "scan_wifi_error", message: this._t("error.need_ble_scan") });
      this._render();
      return;
    }
    this._busy = true;
    this._provisionAccessPoints = [];
    this._appendProvisionEvent({ stage: "scan_wifi" });
    this._render();
    try {
      const result = await this._adapter.scanAccessPoints({
        ble_address: this._provisionForm.ble_address,
        timeout: 60,
      });
      this._currentAccessPointSsid = result.current_ssid || this._currentAccessPointSsid || "";
      this._setProvisionAccessPoints(result.access_points || []);
      this._appendProvisionEvent({ stage: "scan_wifi_done", access_points: result.access_points || [] });
      this._message = JSON.stringify(result, null, 2);
    } catch (error) {
      const detail = this._errorDetail(error);
      const message = detail.error?.message || detail.error || error?.message || String(error);
      this._appendProvisionEvent({ stage: "scan_wifi_error", message: String(message) });
      this._message = JSON.stringify(detail, null, 2);
    } finally {
      this._busy = false;
      this._render();
    }
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
    this._settingsError = "";
    if (this._selected) {
      try {
        await this._loadSelectedState();
        await this._loadPresets();
      } catch (error) {
        this._message = JSON.stringify(this._errorDetail(error), null, 2);
        this._settingsError = error?.error?.message || error?.error || error?.message || String(error);
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
    this._closeSelect();
    const scrollPositions = new Map();
    for (const selector of [".settings-pane", ".settings-workspace", ".preset-pane", ".media-modal"]) {
      const element = this.shadowRoot?.querySelector(selector);
      if (element?.closest(".modal-backdrop.open")) scrollPositions.set(selector, element.scrollTop);
    }
    const scheduleModal = this.shadowRoot?.querySelector(".schedule-modal");
    if (scheduleModal?.querySelector("#schedule-form")) scrollPositions.set(".schedule-modal", scheduleModal.scrollTop);
    const camera = this._camera();
    const oldMediaVideo = this.shadowRoot?.querySelector(".media-video");
    const preserveMediaVideo = Boolean(oldMediaVideo && this._showMediaModal && this._mediaPlaying
      && oldMediaVideo.dataset.mediaUrl === this._mediaPlaying.url);
    const mediaWasPlaying = preserveMediaVideo && !oldMediaVideo.paused;
    if (preserveMediaVideo) oldMediaVideo.remove();
    else if (oldMediaVideo) {
      oldMediaVideo.pause();
      oldMediaVideo.removeAttribute("src");
      oldMediaVideo.load();
    }
    const oldVideo = this.shadowRoot?.querySelector(".preview-video");
    const nextPreviewUrl = camera ? this._previewUrl(camera) : "";
    const preserveVideo = Boolean(oldVideo && this._previewPlayer && nextPreviewUrl
      && this._previewTransport(camera, nextPreviewUrl) === "mpegts"
      && this._absoluteUrl(oldVideo.dataset.previewUrl || "") === this._absoluteUrl(nextPreviewUrl));
    const wasPlaying = preserveVideo && !oldVideo.paused;
    if (preserveVideo) oldVideo.remove();
    else this._teardownPreviewPlayer();
    const recording = Boolean(camera?.recording);
    const capture = this._captureUi(camera);
    const hasProvision = Boolean(this._adapter?.provisionCohn);
    const canWake = this._canWake(camera);
    const canControl = this._canControl(camera) && !this._busy;
    const previewRotation = this._previewRotation(camera?.id);
    this.shadowRoot.innerHTML = `
      <style>${CONSOLE_STYLES}</style>

      <main class="shell">
        <header class="topbar">
          <div>
            <div class="eyebrow">${this._adapter?.label || "gopro-ctl"}</div>
            <h1>${this._t("title")}</h1>
            <div class="sub">${camera ? this._cameraSubtitle(camera) : this._t("hint.no_camera")}</div>
          </div>
          <div class="toolbar">
            ${this._adapter?.listSchedules ? `<button class="ghost" data-action="open-schedules">${this._st("title")}</button>` : ""}
            <select aria-label="${this._t("panel.cameras")}" ${this._cameras.length ? "" : "disabled"} id="camera-select">
              ${this._cameras.map((item) => `<option value="${this._escape(item.id)}" ${item.id === this._selected ? "selected" : ""}>${this._escape(item.name || "GoPro")}</option>`).join("")}
            </select>
            <button class="ghost" data-action="refresh">${this._t("action.refresh")}</button>
          </div>
        </header>

        <section class="layout">
          <aside class="stack side-stack">
            <div class="panel cameras-panel">
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

          <section class="stack main-stack">
            <div class="panel preview-panel">
              <div class="panel-title preview-head">
                <h2>${this._t("panel.preview")}</h2>
                <div class="preview-head-actions">
                  <div class="mode-tabs" aria-label="Mode">
                    ${(camera?.modes || ["video", "photo", "timelapse"]).map((mode) => `<button class="mode-tab ${mode === camera?.current_mode ? "active" : ""}" data-mode-tab="${this._escape(mode)}" ${canControl ? "" : "disabled"}>${this._escape(this._modeLabel(mode))}</button>`).join("")}
                  </div>
                  <button class="head-settings" data-action="open-media" ${camera ? "" : "disabled"}>${this._t("panel.media")}</button>
                  <button class="head-settings preview-rotate" data-action="rotate-preview" title="${this._t("preview.rotate_hint")}" aria-label="${this._t("preview.rotate_hint")}" ${camera ? "" : "disabled"}>↻ ${this._t("preview.rotate", { angle: previewRotation })}</button>
                  <button class="head-settings" data-action="open-settings" ${canControl ? "" : "disabled"}>${this._t("action.settings")}</button>
                </div>
              </div>
              <div class="preview ${previewRotation % 180 ? "preview-quarter-turn" : ""}" style="--preview-rotation: ${previewRotation}deg">
                ${this._previewMarkup(camera)}
              </div>
              <div class="preview-status">
                ${this._previewMetric(this._t("metric.connection"), camera?.phase || this._t("unknown"))}
                ${this._previewMetric(this._t("metric.battery"), camera?.battery != null ? `${camera.battery}%` : this._t("unknown"))}
                ${this._previewMetric(this._t("metric.mode"), camera?.current_mode || this._t("unknown"))}
                ${this._previewMetric(this._t("metric.remaining"), camera?.remaining_storage != null ? `${camera.remaining_storage} MB` : this._t("unknown"))}
                ${this._previewMetric(this._t("metric.sd"), camera?.sd_card_status || this._t("unknown"))}
                ${this._previewMetric(this._t("metric.recording"), camera?.recording == null ? this._t("unknown") : recording ? this._t("status.recording") : this._t("status.idle"))}
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

          </section>
        </section>
        ${this._showMediaModal ? `<div class="modal-backdrop open" data-action="close-media-backdrop">
          <div class="modal media-modal" role="dialog" aria-modal="true" aria-label="${this._t("panel.media")}">
            <div class="modal-head">
              <div class="modal-title"><strong>${this._t("panel.media")}</strong><span>${this._t("media.description")}</span></div>
              <button class="ghost icon-button" data-action="close-media" aria-label="${this._t("action.close")}">×</button>
            </div>
            <div class="media-toolbar"><span>${camera ? this._escape(camera.name || "GoPro") : ""}</span><div class="row"><label><input type="checkbox" data-action="media-select-all" ${this._media.length && this._mediaSelected.size === this._media.length ? "checked" : ""} ${!canControl || this._mediaLoading || !this._media.length ? "disabled" : ""}> ${this._t("media.select_all")}</label><button class="ghost" data-action="media-delete" ${!canControl || this._mediaLoading || !this._mediaSelected.size || !this._adapter.deleteMedia ? "disabled" : ""}>${this._t("media.delete")} (${this._mediaSelected.size})</button><button class="ghost" data-action="media" ${!canControl || this._mediaLoading ? "disabled" : ""}>${this._t("media.refresh")}</button></div></div>
            ${this._mediaPlaying ? this._mediaPlayerMarkup(this._mediaPlaying) : ""}
            ${this._mediaError ? `<div class="schedule-error" role="alert">${this._t("media.error")}: ${this._escape(this._mediaError)}</div>` : ""}
            ${this._mediaLoading ? `<div class="empty media-empty" role="status">${this._t("media.loading")}</div>` : this._media.length ? `<div class="media-grid">${this._media.map((item, index) => this._mediaItem(item, index)).join("")}</div>` : `<div class="empty media-empty">${this._t(!canControl && !this._mediaLoaded ? "media.offline" : this._mediaLoaded ? "media.empty" : "empty.media")}</div>`}
          </div>
        </div>` : ""}
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
        ${this._scheduleModal()}
        <div class="modal-backdrop ${this._showSettingsModal ? "open" : ""}" data-action="close-settings-backdrop">
          <div class="modal settings-modal ${this._settingsError ? "has-error" : ""}" role="dialog" aria-modal="true" aria-label="${this._t("modal.settings_title")}">
            <div class="modal-head">
              <div class="modal-title">
                <strong>${this._t("modal.settings_title")}</strong>
                <span>${this._escape(this._t("modal.settings_description", { mode: this._modeLabel(camera?.current_mode || "video") }))}</span>
              </div>
              <button class="ghost icon-button" data-action="close-settings" aria-label="${this._t("action.close")}">×</button>
            </div>
            ${this._settingsError ? `<div class="schedule-error settings-error" role="alert">${this._escape(this._settingsError)}</div>` : ""}
            <div class="settings-workspace">
              ${this._presetMarkup(camera)}
              ${this._settingsMarkup(camera)}
            </div>
          </div>
        </div>
      </main>
    `;

    this._bind();
    this._enhanceSelects();
    this._enhanceDatalists();
    if (preserveMediaVideo) {
      this.shadowRoot.querySelector(".media-video")?.replaceWith(oldMediaVideo);
      if (mediaWasPlaying) oldMediaVideo.play()?.catch(() => {});
    }
    for (const [selector, position] of scrollPositions) {
      const element = this.shadowRoot.querySelector(selector);
      if (element && (selector !== ".schedule-modal" || element.querySelector("#schedule-form"))) element.scrollTop = position;
    }
    const newVideo = this.shadowRoot.querySelector(".preview-video");
    if (preserveVideo && newVideo) {
      newVideo.replaceWith(oldVideo);
      if (wasPlaying) oldVideo.play()?.catch?.(() => {});
    } else {
      if (preserveVideo) this._teardownPreviewPlayer();
      this._mountPreviewPlayer();
    }
  }

  _bind() {
    const root = this.shadowRoot;
    root.querySelector("#camera-select")?.addEventListener("change", (event) => {
      this._resetPreviewRecovery();
      this._selected = event.target.value;
      this._syncStateStream();
      this._media = [];
      this._mediaSelected = new Set();
      this._mediaPlaying = null;
      this._mediaLoaded = false;
      this._mediaError = "";
      this._mediaLoading = false;
      this._mediaRequest++;
      this._render();
    });
    root.querySelectorAll("[data-camera-id]").forEach((button) => {
      button.addEventListener("click", () => {
        if (this._selected !== button.dataset.cameraId) this._resetPreviewRecovery();
        this._media = [];
        this._mediaSelected = new Set();
        this._mediaPlaying = null;
        this._mediaLoaded = false;
        this._mediaError = "";
        this._mediaLoading = false;
        this._mediaRequest++;
        const camera = this._cameras.find((item) => item.id === button.dataset.cameraId);
        this._selected = button.dataset.cameraId;
        this._syncStateStream();
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
    root.querySelector("[data-action='rotate-preview']")?.addEventListener("click", () => this._rotatePreview());
    this._bindSchedules(root);
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
    root.querySelector("[data-action='open-media']")?.addEventListener("click", () => {
      this._showMediaModal = true;
      this._mediaError = "";
      this._render();
      if (this._canControl(this._camera()) && !this._mediaLoaded) this._loadMedia();
    });
    root.querySelector("[data-action='close-media']")?.addEventListener("click", () => { this._showMediaModal = false; this._mediaPlaying = null; this._render(); });
    root.querySelector("[data-action='close-media-backdrop']")?.addEventListener("click", (event) => {
      if (event.target === event.currentTarget) { this._showMediaModal = false; this._mediaPlaying = null; this._render(); }
    });
    root.querySelector("[data-action='media-delete']")?.addEventListener("click", () => this._deleteMedia());
    root.querySelector("[data-action='media-select-all']")?.addEventListener("change", (event) => {
      this._mediaSelected = new Set(event.target.checked ? this._media.map((item) => item.path) : []);
      this._render();
    });
    root.querySelectorAll("[data-media-select]").forEach((input) => input.addEventListener("change", () => {
      const item = this._media[Number(input.dataset.mediaSelect)];
      if (!item) return;
      if (input.checked) this._mediaSelected.add(item.path); else this._mediaSelected.delete(item.path);
      this._render();
    }));
    root.querySelectorAll("[data-media-play]").forEach((button) => button.addEventListener("click", () => {
      const item = this._media[Number(button.dataset.mediaPlay)];
      if (!item?.url) return;
      this._mediaPlaying = item;
      this._mediaPlaybackError = false;
      this._render();
      const player = this.shadowRoot.querySelector(".media-video");
      player?.play()?.catch(() => {});
      player?.scrollIntoView({ block: "nearest" });
    }));
    root.querySelector("[data-action='close-media-player']")?.addEventListener("click", () => {
      this._mediaPlaying = null;
      this._mediaPlaybackError = false;
      this._render();
    });
    const mediaVideo = root.querySelector(".media-video");
    mediaVideo?.addEventListener("error", () => {
      if (!mediaVideo.isConnected || !this._showMediaModal || mediaVideo.dataset.mediaUrl !== this._mediaPlaying?.url) return;
      this._mediaPlaybackError = true;
      const message = root.querySelector(".media-play-error");
      if (message) message.hidden = false;
    });
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

  _st(key) {
    const zh = {
      cron: "高级 Cron", cronExpression: "Cron 表达式", cronHint: "格式：分 时 日 月 星期，例如 0 18 * * *（每天 18:00）。支持 *、列表、范围和步长；星期日为 0 或 7。日与星期同时指定时，任一匹配即可。高频任务可能因相机忙碌而跳过。",
      title: "计划任务", new: "新建计划", edit: "编辑", remove: "删除", enable: "启用", disable: "停用", history: "执行记录", back: "返回", save: "保存计划", cancel: "取消", name: "计划名称", camera: "相机", mode: "拍摄类型", repeat: "重复方式", once: "一次", daily: "每天", weekly: "指定星期", date: "日期", trigger: "触发方式", fixed: "固定时间", sunset: "日落", time: "拍摄时间", latitude: "纬度", longitude: "经度", offset: "日落偏移（分钟）", duration: "拍摄时长（秒）", preset: "相机预设", parameters: "自定义参数", usePreset: "使用预设值", none: "还没有计划任务。", noHistory: "暂无执行记录。", noPreset: "当前模式没有可用预设", choosePreset: "请选择预设", online: "创建或编辑计划前，请先唤醒相机并连接。", timezone: "服务时区", next: "下次", last: "最近", disabled: "已停用", unavailable: "当天无日落或时间不存在", error: "操作失败", deleteConfirm: "删除此计划及其执行记录？", hint: "设置的时间是目标快门时间。服务会提前准备，错过的任务不会补拍。", loading: "正在读取相机预设…", days: ["一", "二", "三", "四", "五", "六", "日"], scheduled: "计划", started: "开始", finished: "结束", status: { success: "成功", failed: "失败", missed: "错过", skipped: "已跳过", preparing: "准备中", capturing: "拍摄中", interrupted: "已中断", uncertain: "结果不确定" },
    };
    const en = {
      cron: "Advanced Cron", cronExpression: "Cron expression", cronHint: "Format: minute hour day month weekday, e.g. 0 18 * * * (daily at 18:00). Supports *, lists, ranges and steps. When day and weekday are both restricted, either may match. Frequent runs may be skipped if the camera is busy.",
      title: "Schedules", new: "New schedule", edit: "Edit", remove: "Delete", enable: "Enable", disable: "Disable", history: "History", back: "Back", save: "Save schedule", cancel: "Cancel", name: "Schedule name", camera: "Camera", mode: "Capture type", repeat: "Repeat", once: "Once", daily: "Every day", weekly: "Selected weekdays", date: "Date", trigger: "Trigger", fixed: "Fixed time", sunset: "Sunset", time: "Capture time", latitude: "Latitude", longitude: "Longitude", offset: "Sunset offset (minutes)", duration: "Duration (seconds)", preset: "Camera preset", parameters: "Custom settings", usePreset: "Use preset value", none: "No schedules yet.", noHistory: "No runs yet.", noPreset: "No presets available for this mode", choosePreset: "Select a preset", online: "Wake and connect the camera before creating or editing a schedule.", timezone: "Service timezone", next: "Next", last: "Last", disabled: "Disabled", unavailable: "No sunset or local time does not exist", error: "Operation failed", deleteConfirm: "Delete this schedule and its history?", hint: "The time is the target shutter time. Preparation starts early; missed captures are not replayed.", loading: "Loading camera presets…", days: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], scheduled: "Scheduled", started: "Started", finished: "Finished", status: { success: "Success", failed: "Failed", missed: "Missed", skipped: "Skipped", preparing: "Preparing", capturing: "Capturing", interrupted: "Interrupted", uncertain: "Uncertain" },
    };
    return (this._locale === "zh-Hans" ? zh : en)[key] ?? key;
  }

  _wakeGuardText(guard) {
    const zh = this._locale === "zh-Hans";
    const labels = zh
      ? { pending: "等待执行", success: "已唤醒并确认休眠", failed: "失败", deferred: "拍摄或操作中，已推迟", skipped_awake: "相机已开机，暂不休眠", skipped_active: "相机忙碌，未休眠", skipped_unknown: "无法确认状态，已跳过", sleep_unverified: "无法确认休眠" }
      : { pending: "Pending", success: "Woken and confirmed asleep", failed: "Failed", deferred: "Deferred while camera is busy", skipped_awake: "Camera is already awake", skipped_active: "Camera is active", skipped_unknown: "Camera state unknown", sleep_unverified: "Sleep could not be confirmed" };
    const status = guard ? (labels[guard.status] || guard.status || "") : (zh ? "等待执行" : "Pending");
    const next = guard?.next_at ? ` · ${zh ? "下次检查" : "Next check"}: ${this._scheduleTime(guard.next_at)}` : "";
    const error = guard?.error?.message || (typeof guard?.error === "string" ? guard.error : "");
    return `${zh ? "定期唤醒" : "Wake guard"}: ${status}${next}${error ? ` · ${error}` : ""}`;
  }

  async _loadSchedules() {
    const result = await this._adapter.listSchedules();
    this._schedules = result.schedules || [];
    this._scheduleTimezone = result.timezone || "";
  }

  async _openSchedules() {
    this._showSchedulesModal = true;
    this._scheduleDraft = null;
    this._scheduleHistory = null;
    this._scheduleError = "";
    try { await this._loadSchedules(); } catch (e) { this._scheduleError = e.error || e.message || String(e); }
    this._render();
  }

  async _editSchedule(id = null) {
    const item = id ? this._schedules.find((s) => s.id === id) : null;
    const cameraId = item?.camera_id || this._selected;
    const camera = this._cameras.find((c) => c.id === cameraId);
    if (!this._canControl(camera)) { this._scheduleError = this._st("online"); this._render(); return; }
    this._scheduleDraft = item ? { ...item, settings: { ...item.settings }, weekdays: [...item.weekdays] } : {
      name: "", camera_id: cameraId, mode: "photo", repeat: "daily", weekdays: [], date: "", trigger: "fixed", time: "18:00", cron_expression: "0 18 * * *", latitude: "", longitude: "", offset_minutes: 0, duration_seconds: 60, preset: "", settings: {}, enabled: true,
    };
    this._scheduleError = "";
    this._scheduleLoading = true;
    this._render();
    try {
      this._presetStatus = await this._adapter.loadPresets(cameraId);
    } catch (e) {
      this._scheduleError = e.error || e.message || String(e);
      this._presetStatus = null;
    } finally { this._scheduleLoading = false; this._render(); }
  }

  _schedulePresets(draft) {
    const group = this._presetGroups().find((g) => this._presetGroupMode(g) === draft.mode);
    return group ? this._presetItems(group) : [];
  }

  _scheduleSettings(draft) {
    const preset = this._schedulePresets(draft).find((p) => this._presetId(p) === String(draft.preset));
    const entries = preset?.settingArray || preset?.settings || preset?.setting_values || [];
    const ids = new Set(entries.map((s) => String(s.id ?? s.setting_id ?? s.setting ?? "")));
    return SETTING_GROUPS.flatMap((g) => g.settings).filter((s) => ids.has(s.id));
  }

  _scheduleLabel(value) {
    if (this._locale !== "zh-Hans") return value;
    const labels = { Resolution: "分辨率", FPS: "帧率", Aspect: "画面比例", Lens: "镜头", Horizon: "水平校正", "Max Lens": "Max 镜头", "Lens Mod": "镜头模组", "Bit Rate": "码率", "Bit Depth": "色深", Profile: "色彩配置", "System Video": "视频质量", "Video Duration": "相机视频时长", HindSight: "回溯拍摄", "Anti-Flicker": "防闪烁", "Auto Power Down": "自动关机", "Photo Lens": "照片镜头", "Photo Output": "照片格式", "Lapse Mode": "延时模式", "Lapse Lens": "延时镜头", "Wireless Band": "无线频段", "Beep Volume": "提示音音量", Off: "关闭", On: "开启", Low: "低", Medium: "中", High: "高", Max: "最高", Standard: "标准", None: "无", Wide: "广角", Linear: "线性", Narrow: "窄", Locked: "锁定", Never: "从不", "No Limit": "不限制", "5 Seconds": "5 秒", "15 Seconds": "15 秒", "30 Seconds": "30 秒", "1 Minute": "1 分钟", "5 Minutes": "5 分钟", "1 Hour": "1 小时", "1 Min": "1 分钟", "5 Min": "5 分钟", "15 Min": "15 分钟", "30 Min": "30 分钟", "Auto Detect": "自动检测", "All On": "全部开启", "All Off": "全部关闭", "Front Off Only": "仅关闭前灯", "Back Only": "仅后灯", "Time Lapse Video": "延时视频", "Night Lapse Video": "夜间延时视频", "Star Trails": "星轨", "Light Painting": "光绘", "Vehicle Lights": "车灯轨迹" };
    return labels[value] || value;
  }

  _scheduleErrorText(error) {
    const message = error?.error?.message || error?.error || error?.message || String(error);
    if (this._locale !== "zh-Hans" || typeof message !== "string") return message;
    if (message.startsWith("Cron expression must contain five fields")) return "Cron 表达式须包含五个字段：分、时、日、月、星期。";
    return ({
      "Invalid cron expression": "Cron 表达式无效，请检查字段范围和格式。",
      "Cron supports numbers, names, *, ranges, lists and steps": "Cron 仅支持数字、月份或星期英文名称、*、范围、列表和步长。",
      "Cron expression has no matching date": "Cron 表达式没有可执行的日期。",
      "Preset is unavailable for the selected mode": "所选预设在当前拍摄类型下不可用，请刷新相机状态后重新选择。",
      "Preset identity changed; edit the schedule": "相机预设已发生变化，请编辑计划并重新选择预设。",
      "A requested setting is not available in the selected preset": "所选预设不支持某些拍摄参数，请重新选择参数。",
    })[message] || message;
  }

  _scheduleTime(value) {
    if (!value) return "—";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    try { return new Intl.DateTimeFormat(this._locale, { dateStyle: "medium", timeStyle: "short", timeZone: this._scheduleTimezone || undefined }).format(date); }
    catch { return date.toLocaleString(this._locale); }
  }

  _scheduleModal() {
    if (!this._showSchedulesModal) return "";
    const draft = this._scheduleDraft;
    const esc = (x) => this._escape(String(x ?? ""));
    const select = (id, label, value, options) => `<label>${esc(label)}<select data-sfield="${id}">${options.map(([v, l]) => `<option value="${esc(v)}" ${String(value) === String(v) ? "selected" : ""}>${esc(l)}</option>`).join("")}</select></label>`;
    const input = (id, label, type, value, extra = "") => `<label>${esc(label)}<input data-sfield="${id}" type="${type}" value="${esc(value)}" ${extra}></label>`;
    let content;
    if (draft) {
      const presets = this._schedulePresets(draft);
      const settings = this._scheduleSettings(draft);
      content = `<form id="schedule-form" class="schedule-form">
        <p class="schedule-hint">${esc(this._st("hint"))} ${esc(this._st("timezone"))}: ${esc(this._scheduleTimezone)}</p>
        <div class="schedule-fields">
          ${input("name", this._st("name"), "text", draft.name, 'required maxlength="100"')}
          ${select("camera_id", this._st("camera"), draft.camera_id, this._cameras.map((c) => [c.id, c.name || "GoPro"]))}
          ${select("mode", this._st("mode"), draft.mode, [["photo", this._t("mode.photo")], ["video", this._t("mode.video")], ["timelapse", this._t("mode.timelapse")]])}
          ${select("repeat", this._st("repeat"), draft.repeat, [["once", this._st("once")], ["daily", this._st("daily")], ["weekly", this._st("weekly")], ["cron", this._st("cron")]])}
          ${draft.repeat === "once" ? input("date", this._st("date"), "date", draft.date, "required") : ""}
          ${draft.repeat === "weekly" ? `<fieldset class="weekdays"><legend>${esc(this._st("weekly"))}</legend>${this._st("days").map((day, index) => `<label><input type="checkbox" data-weekday="${index}" ${draft.weekdays.includes(index) ? "checked" : ""}>${esc(day)}</label>`).join("")}</fieldset>` : ""}
          ${draft.repeat === "cron" ? `<div class="schedule-cron">${input("cron_expression", this._st("cronExpression"), "text", draft.cron_expression || "", 'required maxlength="120" placeholder="0 18 * * *" spellcheck="false"')}<small>${esc(this._st("cronHint"))}</small></div>` : `${select("trigger", this._st("trigger"), draft.trigger, [["fixed", this._st("fixed")], ["sunset", this._st("sunset")]])}${draft.trigger === "fixed" ? input("time", this._st("time"), "time", draft.time, "required") : `${input("latitude", this._st("latitude"), "number", draft.latitude, 'required min="-90" max="90" step="any"')}${input("longitude", this._st("longitude"), "number", draft.longitude, 'required min="-180" max="180" step="any"')}${input("offset_minutes", this._st("offset"), "number", draft.offset_minutes, 'required min="-720" max="720" step="1"')}`}`}
          ${draft.mode !== "photo" ? input("duration_seconds", this._st("duration"), "number", draft.duration_seconds, 'required min="1" max="86400" step="1"') : ""}
          ${select("preset", this._st("preset"), draft.preset, [["", this._scheduleLoading ? this._st("loading") : this._st(presets.length ? "choosePreset" : "noPreset")], ...presets.map((p) => [this._presetId(p), this._presetTitle(p)])])}
        </div>
        ${settings.length ? `<div class="schedule-parameters"><strong>${esc(this._st("parameters"))}</strong><div class="schedule-fields">${settings.map((s) => `<label>${esc(this._scheduleLabel(s.label))}<select data-ssetting="${esc(s.id)}"><option value="">${esc(this._st("usePreset"))}</option>${s.options.map(([v, l]) => `<option value="${esc(v)}" ${draft.settings[s.id] === v ? "selected" : ""}>${esc(this._scheduleLabel(l))}</option>`).join("")}</select></label>`).join("")}</div></div>` : ""}
        <div class="modal-actions"><button type="button" class="ghost" data-saction="cancel">${esc(this._st("cancel"))}</button><button type="submit" class="primary" ${this._scheduleLoading ? "disabled" : ""}>${esc(this._st("save"))}</button></div>
      </form>`;
    } else if (this._scheduleHistory) {
      content = `<button class="ghost" data-saction="back">${esc(this._st("back"))}</button><div class="schedule-list">${this._scheduleHistory.length ? this._scheduleHistory.map((r) => `<article class="schedule-item"><strong>${esc(this._st("status")[r.status] || r.status)}</strong><span>${esc(this._st("scheduled"))}: ${esc(this._scheduleTime(r.scheduled_at))}</span><span>${esc(this._st("started"))}: ${esc(this._scheduleTime(r.started_at))}</span><span>${esc(this._st("finished"))}: ${esc(this._scheduleTime(r.finished_at))}</span>${r.error ? `<small>${esc(r.error)}</small>` : ""}</article>`).join("") : `<div class="empty">${esc(this._st("noHistory"))}</div>`}</div>`;
    } else {
      content = `<div class="schedule-list-head"><span>${esc(this._st("timezone"))}: ${esc(this._scheduleTimezone)}</span><button class="primary" data-saction="new">${esc(this._st("new"))}</button></div><div class="schedule-list">${this._schedules.length ? this._schedules.map((s) => `<article class="schedule-item"><div class="schedule-item-head"><strong>${esc(s.name)}</strong><span>${esc(s.enabled ? this._modeLabel(s.mode) : this._st("disabled"))}</span></div><span>${esc(this._cameras.find((c) => c.id === s.camera_id)?.name || s.camera_id)} · ${esc(this._st("next"))}: ${esc(s.next_unavailable_date ? `${s.next_unavailable_date} ${this._st("unavailable")}` : this._scheduleTime(s.next_at))}</span>${s.repeat === "cron" ? `<span>${esc(this._st("cron"))}: <code>${esc(s.cron_expression)}</code></span>` : ""}${s.enabled ? `<span>${esc(this._wakeGuardText(s.wake_guard))}</span>` : ""}${s.last_run ? `<span>${esc(this._st("last"))}: ${esc(this._st("status")[s.last_run.status] || s.last_run.status)}${s.last_run.error ? ` · ${esc(s.last_run.error)}` : ""}</span>` : ""}<div class="row schedule-actions"><button data-saction="edit" data-id="${esc(s.id)}">${esc(this._st("edit"))}</button><button data-saction="toggle" data-id="${esc(s.id)}">${esc(this._st(s.enabled ? "disable" : "enable"))}</button><button data-saction="history" data-id="${esc(s.id)}">${esc(this._st("history"))}</button><button data-saction="delete" data-id="${esc(s.id)}">${esc(this._st("remove"))}</button></div></article>`).join("") : `<div class="empty">${esc(this._st("none"))}</div>`}</div>`;
    }
    return `<div class="modal-backdrop open" data-saction="backdrop"><div class="modal schedule-modal" role="dialog" aria-modal="true" aria-label="${esc(this._st("title"))}"><div class="modal-head"><div class="modal-title"><strong>${esc(draft ? this._st(draft.id ? "edit" : "new") : this._st("title"))}</strong></div><button class="ghost icon-button" data-saction="close" aria-label="${esc(this._t("action.close"))}">×</button></div>${this._scheduleError ? `<div class="schedule-error" role="alert">${esc(this._st("error"))}: ${esc(this._scheduleError)}</div>` : ""}${content}</div></div>`;
  }

  _bindSchedules(root) {
    root.querySelector("[data-action='open-schedules']")?.addEventListener("click", () => this._openSchedules());
    root.querySelectorAll("[data-saction]").forEach((el) => el.addEventListener("click", async (event) => {
      const action = el.dataset.saction;
      if (action === "backdrop" && event.target !== el) return;
      this._scheduleError = "";
      if (action === "close" || action === "backdrop") { this._showSchedulesModal = false; this._scheduleDraft = null; this._render(); return; }
      if (action === "cancel" || action === "back") { this._scheduleDraft = null; this._scheduleHistory = null; this._render(); return; }
      if (action === "new" || action === "edit") { await this._editSchedule(el.dataset.id); return; }
      const item = this._schedules.find((s) => s.id === el.dataset.id);
      try {
        if (action === "history") this._scheduleHistory = (await this._adapter.scheduleHistory(el.dataset.id)).history;
        if (action === "toggle") await this._adapter.enableSchedule(item.id, !item.enabled);
        if (action === "delete" && window.confirm(this._st("deleteConfirm"))) await this._adapter.deleteSchedule(item.id);
        if (action === "toggle" || action === "delete") await this._loadSchedules();
      } catch (e) { this._scheduleError = e.error || e.message || String(e); }
      this._render();
    }));
    root.querySelectorAll("[data-sfield]").forEach((el) => {
      const update = async () => {
        const key = el.dataset.sfield;
        const previous = this._scheduleDraft[key];
        this._scheduleDraft[key] = el.value;
        if (key === "repeat") {
          if (el.value === "cron") {
            this._scheduleDraft.trigger = "cron";
            this._scheduleDraft.cron_expression ||= "0 18 * * *";
          } else if (previous === "cron") {
            this._scheduleDraft.trigger = "fixed";
            this._scheduleDraft.time ||= "18:00";
          }
        }
        if (["camera_id", "mode", "preset"].includes(key)) {
          this._scheduleDraft.settings = {};
          this._scheduleDraft.preset_identity = "";
        }
        if (["mode", "camera_id"].includes(key)) this._scheduleDraft.preset = "";
        if (key === "camera_id") {
          const camera = this._cameras.find((c) => c.id === el.value);
          if (!this._canControl(camera)) { this._presetStatus = null; this._scheduleError = this._st("online"); }
          else {
            this._scheduleLoading = true; this._render();
            try { this._presetStatus = await this._adapter.loadPresets(el.value); this._scheduleError = ""; }
            catch (e) { this._presetStatus = null; this._scheduleError = e.error || e.message || String(e); }
            finally { this._scheduleLoading = false; }
          }
        }
        if (["camera_id", "mode", "preset", "repeat", "trigger"].includes(key)) this._render();
      };
      el.addEventListener(el.tagName === "SELECT" ? "change" : "input", update);
    });
    root.querySelectorAll("[data-weekday]").forEach((el) => el.addEventListener("change", () => {
      const day = Number(el.dataset.weekday);
      this._scheduleDraft.weekdays = el.checked ? [...new Set([...this._scheduleDraft.weekdays, day])] : this._scheduleDraft.weekdays.filter((d) => d !== day);
    }));
    root.querySelectorAll("[data-ssetting]").forEach((el) => el.addEventListener("change", () => {
      if (el.value) this._scheduleDraft.settings[el.dataset.ssetting] = el.value;
      else delete this._scheduleDraft.settings[el.dataset.ssetting];
    }));
    root.querySelector("#schedule-form")?.addEventListener("submit", async (event) => {
      event.preventDefault();
      try {
        await this._adapter.saveSchedule(this._scheduleDraft, this._scheduleDraft.id);
        this._scheduleDraft = null; this._scheduleError = ""; await this._loadSchedules();
      } catch (e) { this._scheduleError = this._scheduleErrorText(e); }
      this._render();
    });
  }

  _closeSelect(returnFocus = false) {
    const trigger = this._selectTrigger;
    this._selectMenu?.remove();
    this._selectMenu = null;
    this._selectTrigger = null;
    if (trigger?.isConnected) {
      trigger.setAttribute("aria-expanded", "false");
      trigger.removeAttribute("aria-activedescendant");
      trigger.onkeydown = null;
      if (returnFocus) trigger.focus();
    }
  }

  _enhanceSelects() {
    const root = this.shadowRoot;
    root.querySelectorAll("select").forEach((select, index) => {
      if (select.id === "camera-select" && select.disabled) return;
      const parentLabel = select.closest("label");
      const linkedLabel = select.id ? root.querySelector(`label[for="${CSS.escape(select.id)}"]`) : null;
      const label = select.getAttribute("aria-label") || linkedLabel?.querySelector("span")?.textContent
        || linkedLabel?.textContent?.trim() || Array.from(parentLabel?.childNodes || [])
          .filter((node) => node.nodeType === Node.TEXT_NODE).map((node) => node.textContent.trim()).filter(Boolean).join(" ")
        || this._t("action.settings");
      const wrapper = document.createElement("span");
      wrapper.className = "select-control";
      const trigger = document.createElement("button");
      trigger.type = "button";
      trigger.className = "select-trigger";
      trigger.setAttribute("role", "combobox");
      trigger.setAttribute("aria-label", label);
      trigger.setAttribute("aria-haspopup", "listbox");
      trigger.setAttribute("aria-expanded", "false");
      trigger.disabled = select.disabled;
      const value = document.createElement("span");
      value.className = "select-value";
      value.textContent = select.selectedOptions[0]?.textContent || "";
      trigger.append(value);
      const arrow = document.createElement("span");
      arrow.className = "select-arrow";
      arrow.setAttribute("aria-hidden", "true");
      trigger.append(arrow);
      select.before(wrapper);
      wrapper.append(select, trigger);
      select.classList.add("select-native");
      select.tabIndex = -1;
      select.setAttribute("aria-hidden", "true");
      for (const associatedLabel of new Set([parentLabel, linkedLabel])) {
        associatedLabel?.addEventListener("click", (event) => {
          if (!event.composedPath().includes(trigger)) {
            event.preventDefault();
            if (!trigger.disabled) trigger.focus();
          }
        });
      }

      const open = () => {
        if (trigger.disabled || this._selectTrigger === trigger) return;
        this._closeSelect();
        const menu = document.createElement("div");
        menu.className = "select-menu";
        menu.id = `select-menu-${index}`;
        menu.setAttribute("role", "listbox");
        menu.setAttribute("aria-label", label);
        const options = Array.from(select.options);
        let active = Math.max(0, options.findIndex((option) => option.selected && !option.disabled));
        let query = "";
        let lastType = 0;
        const rows = options.map((option, optionIndex) => {
          const row = document.createElement("div");
          row.className = "select-option";
          row.id = `${menu.id}-option-${optionIndex}`;
          row.setAttribute("role", "option");
          row.setAttribute("aria-selected", String(option.selected));
          if (option.disabled) row.setAttribute("aria-disabled", "true");
          row.textContent = option.textContent;
          row.addEventListener("pointerdown", (event) => event.preventDefault());
          row.addEventListener("click", () => choose(optionIndex));
          menu.append(row);
          return row;
        });
        const highlight = (next) => {
          if (next < 0 || next >= rows.length || options[next]?.disabled) return;
          active = next;
          rows.forEach((row, rowIndex) => row.classList.toggle("highlighted", rowIndex === active));
          trigger.setAttribute("aria-activedescendant", rows[active].id);
          rows[active].scrollIntoView({ block: "nearest" });
        };
        const choose = (optionIndex) => {
          if (!options[optionIndex] || options[optionIndex].disabled) return;
          const changed = select.selectedIndex !== optionIndex;
          select.selectedIndex = optionIndex;
          value.textContent = options[optionIndex].textContent;
          this._closeSelect(true);
          if (changed) {
            const field = select.dataset.sfield;
            const setting = select.dataset.ssetting;
            const id = select.id;
            select.dispatchEvent(new Event("change", { bubbles: true }));
            if (!trigger.isConnected) {
              const replacement = id ? root.querySelector(`#${CSS.escape(id)}`)
                : field ? root.querySelector(`[data-sfield="${CSS.escape(field)}"]`)
                  : setting ? root.querySelector(`[data-ssetting="${CSS.escape(setting)}"]`) : null;
              replacement?.parentElement?.querySelector(".select-trigger")?.focus();
            }
          }
        };
        const onMenuKeyDown = (event) => {
          if (this._selectTrigger !== trigger) return;
          if (event.key === "Escape") { event.preventDefault(); this._closeSelect(true); return; }
          if (event.key === "Tab") { this._closeSelect(); return; }
          if (event.key === "Enter" || event.key === " ") { event.preventDefault(); choose(active); return; }
          if (["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) {
            event.preventDefault();
            let next = event.key === "Home" ? 0 : event.key === "End" ? options.length - 1 : active + (event.key === "ArrowDown" ? 1 : -1);
            const direction = ["ArrowUp", "End"].includes(event.key) ? -1 : 1;
            while (next >= 0 && next < options.length && options[next].disabled) next += direction;
            highlight(next);
            return;
          }
          if (event.key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
            const now = Date.now();
            query = (now - lastType > 700 ? "" : query) + event.key.toLocaleLowerCase();
            lastType = now;
            const match = options.findIndex((option) => !option.disabled && option.textContent.trim().toLocaleLowerCase().startsWith(query));
            if (match >= 0) highlight(match);
          }
        };
        const dialog = select.closest('[role="dialog"]');
        (dialog || root).append(menu);
        this._selectMenu = menu;
        this._selectTrigger = trigger;
        queueMicrotask(() => {
          if (this._selectTrigger === trigger) trigger.onkeydown = onMenuKeyDown;
        });
        trigger.setAttribute("aria-controls", menu.id);
        trigger.setAttribute("aria-expanded", "true");
        const rect = trigger.getBoundingClientRect();
        const bounds = dialog?.getBoundingClientRect();
        const minTop = Math.max(10, (bounds?.top ?? 0) + 8);
        const maxBottom = Math.min(window.innerHeight - 10, (bounds?.bottom ?? window.innerHeight) - 8);
        const minLeft = Math.max(10, (bounds?.left ?? 0) + 8);
        const maxRight = Math.min(window.innerWidth - 10, (bounds?.right ?? window.innerWidth) - 8);
        const below = maxBottom - rect.bottom;
        const above = rect.top - minTop;
        const upwards = below < 180 && above > below;
        const available = Math.max(60, upwards ? above : below);
        menu.style.maxHeight = `${Math.min(280, available)}px`;
        menu.style.width = `${Math.min(Math.max(rect.width, 180), maxRight - minLeft)}px`;
        menu.style.left = `${Math.max(minLeft, Math.min(rect.left, maxRight - menu.offsetWidth))}px`;
        if (upwards) menu.style.bottom = `${window.innerHeight - rect.top + 5}px`;
        else menu.style.top = `${rect.bottom + 5}px`;
        if (!options[active]?.disabled) highlight(active);
      };
      trigger.addEventListener("click", () => {
        if (this._selectTrigger === trigger) this._closeSelect(true);
        else open();
      });
      trigger.addEventListener("keydown", (event) => {
        if (this._selectTrigger === trigger) return;
        if (["ArrowDown", "ArrowUp", "Enter", " "].includes(event.key)) { event.preventDefault(); open(); }
      });
    });
  }

  _enhanceDatalists() {
    const root = this.shadowRoot;
    root.querySelectorAll("input[list]").forEach((input, index) => {
      const list = root.getElementById(input.getAttribute("list"));
      const options = Array.from(list?.options || []);
      if (!options.length) return;
      input.removeAttribute("list");
      input.setAttribute("role", "combobox");
      input.setAttribute("aria-autocomplete", "list");
      input.setAttribute("aria-haspopup", "listbox");
      input.setAttribute("aria-expanded", "false");
      const label = Array.from(input.closest("label")?.childNodes || [])
        .filter((node) => node.nodeType === Node.TEXT_NODE).map((node) => node.textContent.trim()).filter(Boolean).join(" ");
      if (label) input.setAttribute("aria-label", label);
      let active = -1;
      let displayed = [];
      let selecting = false;
      const highlight = (position) => {
        if (!this._selectMenu || this._selectTrigger !== input || !displayed.length) return;
        active = Math.max(0, Math.min(position, displayed.length - 1));
        Array.from(this._selectMenu.children).forEach((row, rowIndex) => row.classList.toggle("highlighted", rowIndex === active));
        const row = this._selectMenu.children[active];
        input.setAttribute("aria-activedescendant", row.id);
        row.scrollIntoView({ block: "nearest" });
      };
      const choose = (option) => {
        selecting = true;
        input.value = option.value;
        this._closeSelect(true);
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.dispatchEvent(new Event("change", { bubbles: true }));
        selecting = false;
      };
      const open = () => {
        if (selecting) return;
        displayed = options.filter((option) => option.value.toLocaleLowerCase().includes(input.value.toLocaleLowerCase()));
        this._closeSelect();
        active = -1;
        if (!displayed.length) return;
        const menu = document.createElement("div");
        menu.className = "select-menu";
        menu.id = `datalist-menu-${index}`;
        menu.setAttribute("role", "listbox");
        menu.setAttribute("aria-label", label);
        displayed.forEach((option, optionIndex) => {
          const row = document.createElement("div");
          row.className = "select-option datalist-option";
          row.id = `${menu.id}-option-${optionIndex}`;
          row.setAttribute("role", "option");
          row.setAttribute("aria-selected", "false");
          const name = document.createElement("span");
          name.textContent = option.value;
          row.append(name);
          if (option.label && option.label !== option.value) {
            const detail = document.createElement("small");
            detail.textContent = option.label;
            row.append(detail);
          }
          row.addEventListener("pointerdown", (event) => event.preventDefault());
          row.addEventListener("click", () => choose(option));
          menu.append(row);
        });
        const dialog = input.closest('[role="dialog"]');
        (dialog || root).append(menu);
        this._selectMenu = menu;
        this._selectTrigger = input;
        input.setAttribute("aria-controls", menu.id);
        input.setAttribute("aria-expanded", "true");
        const rect = input.getBoundingClientRect();
        const bounds = dialog?.getBoundingClientRect();
        const minTop = Math.max(10, (bounds?.top ?? 0) + 8);
        const maxBottom = Math.min(window.innerHeight - 10, (bounds?.bottom ?? window.innerHeight) - 8);
        const minLeft = Math.max(10, (bounds?.left ?? 0) + 8);
        const maxRight = Math.min(window.innerWidth - 10, (bounds?.right ?? window.innerWidth) - 8);
        const below = maxBottom - rect.bottom;
        const above = rect.top - minTop;
        const upwards = below < 180 && above > below;
        menu.style.maxHeight = `${Math.min(280, Math.max(60, upwards ? above : below))}px`;
        menu.style.width = `${Math.min(Math.max(rect.width, 180), maxRight - minLeft)}px`;
        menu.style.left = `${Math.max(minLeft, Math.min(rect.left, maxRight - menu.offsetWidth))}px`;
        if (upwards) menu.style.bottom = `${window.innerHeight - rect.top + 5}px`;
        else menu.style.top = `${rect.bottom + 5}px`;
      };
      input.addEventListener("focus", open);
      input.addEventListener("input", open);
      input.addEventListener("keydown", (event) => {
        if (event.key === "ArrowDown" || event.key === "ArrowUp") {
          event.preventDefault();
          if (this._selectTrigger !== input) open();
          highlight(active + (event.key === "ArrowDown" ? 1 : -1));
        } else if (event.key === "Enter" && this._selectTrigger === input && active >= 0) {
          event.preventDefault();
          choose(displayed[active]);
        } else if (event.key === "Escape" && this._selectTrigger === input) {
          event.preventDefault();
          this._closeSelect(true);
        } else if (event.key === "Tab" && this._selectTrigger === input) this._closeSelect();
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
      scan_wifi_error: /timed out|超时/i.test(event.message || "")
        ? this._t("stage.scan_wifi_timeout")
        : this._t("stage.scan_wifi_error", { message: event.message || "" }),
      connect_wifi: this._t("stage.connect_wifi"),
      connect_wifi_done: this._t("stage.connect_wifi_done"),
      clear_certificate: this._t("stage.clear_certificate"),
      create_certificate: this._t("stage.create_certificate"),
      get_certificate: this._t("stage.get_certificate"),
      wait_cohn_status: this._t("stage.wait_cohn_status"),
      cohn_status_done: this._t("stage.cohn_status_done", { address: event.credentials?.ip_address || "" }),
      done: this._t("stage.done"),
      failed: [this._t("stage.failed"), event.error?.message || ""].filter(Boolean).join(": "),
      error: [this._t("stage.error"), event.error?.message || ""].filter(Boolean).join(": "),
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

  _previewRotation(cameraId) {
    if (!cameraId) return 0;
    this._previewRotations ||= new Map();
    if (!this._previewRotations.has(cameraId)) {
      let value = 0;
      try { value = Number(window.localStorage.getItem(`gopro-preview-rotation:${cameraId}`)); } catch (_) {}
      this._previewRotations.set(cameraId, [0, 90, 180, 270].includes(value) ? value : 0);
    }
    return this._previewRotations.get(cameraId);
  }

  _rotatePreview() {
    const cameraId = this._selected;
    if (!cameraId) return;
    const angle = (this._previewRotation(cameraId) + 90) % 360;
    this._previewRotations.set(cameraId, angle);
    try { window.localStorage.setItem(`gopro-preview-rotation:${cameraId}`, String(angle)); } catch (_) {}
    const preview = this.shadowRoot?.querySelector(".preview");
    preview?.style.setProperty("--preview-rotation", `${angle}deg`);
    preview?.classList.toggle("preview-quarter-turn", angle % 180 !== 0);
    const button = this.shadowRoot?.querySelector("[data-action='rotate-preview']");
    if (button) button.textContent = `↻ ${this._t("preview.rotate", { angle })}`;
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
    if (!video || this._previewRetryTimer || this._previewBlocked) return;
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
          liveBufferLatencyMaxLatency: 0.9,
          liveBufferLatencyMinRemain: 0.35,
          autoCleanupSourceBuffer: true,
          autoCleanupMaxBackwardDuration: 30,
          autoCleanupMinBackwardDuration: 15,
        }
      );
      const recover = (error) => this._recoverPreviewPlayer(player, video, error);
      video.addEventListener("error", () => recover(video.error), { once: true });
      video.addEventListener("playing", () => {
        if (this._previewStableTimer) window.clearTimeout(this._previewStableTimer);
        this._previewStableTimer = window.setTimeout(() => {
          if (this._previewPlayer === player) this._previewRetryCount = 0;
          this._previewStableTimer = null;
        }, 15000);
      });
      player.on?.(mpegts.Events.ERROR, (type, detail, info) => recover({ type, detail, info }));
      this._previewPlayer = player;
      player.attachMediaElement(video);
      player.load();
      player.play()?.catch?.((error) => {
        this._message = JSON.stringify(this._errorDetail(error), null, 2);
      });
    } catch (error) {
      this._teardownPreviewPlayer();
      this._message = JSON.stringify(this._errorDetail(error), null, 2);
    }
  }

  _resetPreviewRecovery() {
    if (this._previewRetryTimer) window.clearTimeout(this._previewRetryTimer);
    if (this._previewStableTimer) window.clearTimeout(this._previewStableTimer);
    this._previewRetryTimer = null;
    this._previewStableTimer = null;
    this._previewRetryCount = 0;
    this._previewBlocked = false;
  }

  _recoverPreviewPlayer(player, video, error) {
    if (this._previewPlayer !== player || this._previewRetryTimer || this._previewBlocked) return;
    if (this._previewStableTimer) window.clearTimeout(this._previewStableTimer);
    this._previewStableTimer = null;
    this._teardownPreviewPlayer();
    this._previewRetryCount += 1;
    if (this._previewRetryCount > 3) {
      this._previewBlocked = true;
      this._message = `${this._t("error.preview_failed")} ${error?.message || error?.detail || ""}`.trim();
    } else {
      this._message = this._t("error.preview_retry", { count: this._previewRetryCount });
      this._previewRetryTimer = window.setTimeout(() => {
        this._previewRetryTimer = null;
        if (this.isConnected && this._previewUrl(this._camera() || {})) this._render();
      }, 1000);
    }
    this._render();
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
    for (const method of ["pause", "unload", "detachMediaElement", "destroy"]) {
      try { player[method]?.(); } catch { /* Continue releasing remaining resources. */ }
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
    const presets = group ? this._presetItems(group) : [];
    return `
      <aside class="preset-pane">
        <div class="pane-title">
          <span>${this._t("panel.presets")}</span>
          <strong>${this._escape(this._modeLabel(camera.current_mode || "video"))}</strong>
        </div>
        <div class="preset-list">
          ${presets.map((preset) => this._presetButton(camera, preset)).join("") || `<span class="preset-empty">${this._t(group ? "empty.no_presets" : "empty.preset_status")}</span>`}
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
    const disabled = !id || !this._canControl(camera) || this._busy;
    return `
      <button class="preset-button ${active ? "active" : ""}" data-preset-id="${this._escape(id)}" ${disabled ? "disabled" : ""}>
        <span class="preset-name">${this._escape(this._presetTitle(preset))}${active ? `<span class="preset-active">${this._t("preset.active")}</span>` : ""}</span>
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
    const known = { "1000": "video", "1001": "photo", "1002": "timelapse", PRESET_GROUP_ID_VIDEO: "video", PRESET_GROUP_ID_PHOTO: "photo", PRESET_GROUP_ID_TIMELAPSE: "timelapse" };
    if (known[id]) return known[id];
    const title = String(this._presetTitle(group)).toLowerCase();
    if (title.includes("video")) return "video";
    if (title.includes("photo")) return "photo";
    if (title.includes("time")) return "timelapse";
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
        const definition = SETTING_GROUPS.flatMap((group) => group.settings).find((entry) => entry.id === String(setting));
        if (!definition) return "";
        return `${this._scheduleLabel(definition.label)} ${this._scheduleLabel(this._settingLabel(definition, String(option)))}`;
      })
      .filter(Boolean)
      .join(" · ");
  }

  _settingsGroupText(value) {
    if (this._locale !== "zh-Hans") return value;
    return ({
      "Video": "视频", "Resolution, frame cadence and capture shape.": "分辨率、帧率与画面比例。",
      "Stabilization": "防抖与镜头", "Motion smoothing, horizon handling and lens mods.": "防抖、水平校正与镜头模组。",
      "Quality": "画质", "Compression, bit depth and camera processing profile.": "码率、色深与色彩配置。",
      "Capture": "拍摄", "Duration, hindsight and camera behavior.": "拍摄时长、回溯与相机行为。",
      "Photo / Lapse": "照片与延时", "Still capture, lapse modes and intervals.": "照片格式、延时模式与镜头。",
      "System": "系统", "Camera feedback and wireless preferences.": "提示音、指示灯和无线设置。",
    })[value] || value;
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
                <strong>${this._escape(this._settingsGroupText(group.title))}</strong>
                <span>${this._escape(this._settingsGroupText(group.description))}</span>
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
    const canControl = this._canControl(camera) && !this._busy;
    const options = [
      ...(hasCurrent && !knownCurrent ? [[current, this._t("setting.current", { value: current })]] : []),
      ...setting.options,
    ];
    return `
      <div class="setting-control">
        <label for="setting-${this._escape(setting.id)}">
          <span>${this._escape(this._scheduleLabel(setting.label))}</span>
          <small>${hasCurrent ? this._escape(this._t("setting.current", { value: this._scheduleLabel(this._settingLabel(setting, current)) })) : `ID ${this._escape(setting.id)}`}</small>
        </label>
        <div class="setting-input">
          <select id="setting-${this._escape(setting.id)}" ${canControl ? "" : "disabled"}>
            ${options.map(([value, label]) => `<option value="${this._escape(value)}" ${value === current ? "selected" : ""}>${this._escape(this._scheduleLabel(label))}</option>`).join("")}
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

  _mediaPlayerMarkup(item) {
    const name = this._escape(item.name || item.path || "video");
    const url = this._escape(item.url || "");
    return `
      <section class="media-player" aria-label="${name}">
        <div class="media-player-head">
          <strong>${name}</strong>
          <div class="row">
            <a class="media-download" href="${url}" download>${this._t("media.download")}</a>
            <button class="ghost" data-action="close-media-player">${this._t("media.close_player")}</button>
          </div>
        </div>
        <video class="media-video" data-media-url="${url}" src="${url}" controls playsinline preload="metadata" aria-label="${name}"></video>
        <div class="schedule-error media-play-error" role="alert" ${this._mediaPlaybackError ? "" : "hidden"}>${this._t("media.play_error")}</div>
      </section>
    `;
  }

  _mediaItem(item, index) {
    const type = item.media_type?.startsWith("image/") ? "IMG" : "VID";
    const href = item.url || item.path || "#";
    const thumbnail = item.thumbnail || "";
    const size = item.size ? this._formatBytes(item.size) : "";
    const thumb = thumbnail
      ? `<img src="${this._escape(thumbnail)}" alt="${this._escape(item.name || "media")}" loading="lazy" onerror="this.remove()">`
      : `<span class="badge">${type}</span>`;
    const isVideo = item.media_type?.startsWith("video/");
    const open = isVideo
      ? `<button type="button" class="media-item" data-media-play="${index}">`
      : `<a class="media-item" href="${this._escape(href)}" target="_blank" rel="noreferrer">`;
    return `
      <div class="media-card">
      <label class="media-select"><input type="checkbox" data-media-select="${index}" aria-label="${this._escape(item.name || item.path)}" ${this._mediaSelected.has(item.path) ? "checked" : ""} ${this._mediaLoading ? "disabled" : ""}></label>
      ${open}
        <div class="thumb">${thumb}</div>
        <div class="media-body">
          <div class="badge">${type}</div>
          <strong>${this._escape(item.name || item.path || "media")}</strong>
          <span>${this._escape([item.directory, size].filter(Boolean).join(" · ") || item.media_type || "")}</span>
          <span>${this._escape(this._mediaTime(item.created))}</span>
        </div>
      ${isVideo ? "</button>" : "</a>"}
      </div>
    `;
  }

  _mediaTime(value) {
    const seconds = Number(value);
    if (!value || !Number.isFinite(seconds) || seconds <= 0) return this._t("media.unknown_time");
    const date = new Date(seconds * 1000);
    if (!Number.isFinite(date.getTime())) return this._t("media.unknown_time");
    return new Intl.DateTimeFormat(this._locale, { dateStyle: "medium", timeStyle: "medium" }).format(date);
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
