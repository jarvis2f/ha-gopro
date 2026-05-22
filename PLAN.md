# PLAN.md

## 目标

构建一个兼容 HACS 的 Home Assistant 自定义集成，用于通过 BLE 和 HTTP 控制兼容 OpenGoPro 的 GoPro 相机。

## v1 范围

- 将 OpenGoPro 作为 Home Assistant 自定义集成添加。
- 支持 BLE 自动发现/config flow，以及手动输入 BLE 地址。
- 提供一键唤醒流程：BLE 连接、启用 Wi-Fi 步骤、HTTP 就绪探测、Keep Alive 循环。
- 通过 Home Assistant 实体暴露相机控制和状态。
- 为侧边栏面板提供 Home Assistant 服务和 WebSocket 命令。
- 在 `/opengopro` 添加现代化 Home Assistant 侧边栏面板。
- 通过 Home Assistant Media Browser 和认证媒体代理暴露相机媒体文件。
- Home Assistant 和 standalone 都实现基于 UDP MPEG-TS relay 的 Live Preview 浏览器播放，不依赖运行时 `ffmpeg`。
- 为 Home Assistant Automation 暴露 `guard_wake`，用于定时刷新 GoPro 睡眠后的 BLE 可唤醒窗口。

## 当前状态

已完成：

- 在 `custom_components/opengopro` 下创建集成骨架。
- 添加 HACS 元数据、README、开发依赖和 `.gitignore`。
- 实现 config flow、options flow、服务、WebSocket 命令、诊断和翻译。
- 实现 OpenGoPro 客户端抽象和 coordinator。
- 添加 button、switch、select、sensor、binary_sensor 实体平台。
- 添加 Media Browser 数据源和认证媒体代理。
- 添加侧边栏前端面板。
- Home Assistant 模式已实现 Live Preview：启动 GoPro UDP MPEG-TS 预览流、通过认证 HTTP view relay 给面板播放。
- standalone 模式已实现 Live Preview：启动 GoPro UDP MPEG-TS 预览流、通过 HTTP relay 和 `mpegts.js` 页面内嵌显示。
- 已添加 BLE discovery 的 `0xFEA6` service UUID 识别。
- 已添加 HA `guard_wake` / `set_preset` 服务、BLE presence WebSocket、相机可见 Wi-Fi AP 扫描 WebSocket。
- standalone 已添加每日 wake schedule API；HA 侧定时建议使用 Automation。
- 已添加项目图标 `custom_components/opengopro/icon.svg` 和 `icon.png`。
- 已验证：
  - `venv/bin/python -m compileall custom_components standalone scripts tests`
  - `venv/bin/python -m pytest -q`
  - 基于 `homeassistant==2026.5.2` 的模块导入检查
  - 最小 `homeassistant --script check_config`
- 已连接测试 Home Assistant 实例 `http://192.168.2.118:8123`，API token 可用。
- 已通过 SSH 安装 `custom_components/opengopro` 到测试实例，Home Assistant 已识别 `opengopro` config flow handler；尚未创建相机 config entry。

## 后续任务

1. 安装到真实 Home Assistant OS/Supervised 实例。
2. 通过 Bluetooth discovery 添加一台真实兼容 OpenGoPro 的相机。
3. 采集真实 `/gopro/camera/state` 和 `/gopro/media/list` payload。
4. 根据真实 payload 强化 `client.py` 的状态归一化。
5. 用真机验证 `async_enable_wifi` 的 Set AP Control TLV 写入、response notify、配对复用和 AP 启动时序。
6. 用真机验证 wake、sleep、shutter、mode selection、Keep Alive 和 media browsing。
7. 添加带 mocked config entry 和 coordinator state 的 Home Assistant 集成测试。
8. 用真机验证 HA/standalone MPEG-TS relay 在 AP 模式、COHN 模式、容器/宿主机网络下的 UDP 收包路径。
9. 当本地 HA 开发服务可用后，添加前端 smoke test。
10. 如需让无蓝牙 HA 实例直接使用 MacBook 蓝牙，设计并实现 Mac BLE bridge 模式。

## 验收标准

- Home Assistant 可以加载该集成且无配置错误。
- GoPro 可以通过自动发现或手动配置添加。
- 兼容相机的一键唤醒流程可以到达 `http_ready`。
- 可以从实体和侧边栏面板启动/停止录制。
- 电池、模式、录制状态、存储空间、BLE、Wi-Fi、SD 卡、温度等状态会以实体形式展示。
- Media Browser 可以展示相机文件，并通过 Home Assistant 认证 URL 解析为可播放或可下载的媒体。
- Home Assistant 面板和 standalone 页面都可以启动/停止并显示 Live Preview。
- Home Assistant Automation 可以通过 `opengopro.guard_wake` 和 `opengopro.wake` 组合实现每日定时唤醒。

## 设计约束

- 保持客户端层可替换，并与 Home Assistant 实体代码隔离。
- 前端 UI 保持高信息密度、响应式、偏控制台风格；不要做营销页式布局。
- 不要把 standalone runtime 直接耦合进 Home Assistant 集成；HA 侧的预览 relay 必须保持在 `custom_components/opengopro` 内独立实现。
- 优先使用 Home Assistant 原生模式：config entry、update coordinator、entity platform、service、WebSocket command 和 media source。
