# OpenGoPro for Home Assistant

用于 Home Assistant 的 GoPro 自定义集成，通过 BLE 唤醒/连接流程和相机 HTTP API 控制兼容 OpenGoPro 的 GoPro 相机。

## v1 功能

- 支持兼容 OpenGoPro 相机的 BLE 发现和 config flow。自动发现同时识别 `GoPro*` / `HERO*` 名称和官方 `0xFEA6` BLE service UUID。
- 支持一键唤醒流程：BLE 连接、启用相机 Wi-Fi、HTTP 就绪检查和 Keep Alive 管理。
- 支持 `guard_wake` 服务，用于 Home Assistant Automation 在目标时间前刷新 8 小时 BLE 唤醒窗口，然后让相机回到睡眠状态。
- 提供录制、快门、唤醒、休眠、重连、模式、预设和状态等实体。
- 接入 Home Assistant Media Browser，用于浏览相机媒体文件，并通过认证代理下载或播放。
- 在 `/opengopro` 提供侧边栏面板，包含连接、拍摄控制、状态、媒体、BLE presence 和 Live Preview 播放。
- Home Assistant 和 standalone 都使用 UDP MPEG-TS relay，并由浏览器端 `mpegts.js` 播放预览流；不依赖运行时 `ffmpeg`。
- Home Assistant 配置流、选项、实体和服务提供英文/简体中文翻译；共享网页控制台也支持英文/简体中文。
- HERO12 及更新机型的 COHN 配网、相机可见 Wi-Fi AP 扫描和 COHN 进度流目前由 standalone 网页控制台提供；HA 端可通过 WebSocket 扫描已配置相机可见的 Wi-Fi AP。

## 安装

1. 将 `custom_components/opengopro` 复制到 Home Assistant 的 `custom_components` 目录。
2. 重启 Home Assistant。
3. 在 **设置 > 设备与服务 > 添加集成 > OpenGoPro** 中添加集成。
4. 使用蓝牙自动发现，或手动输入 BLE 地址。

也可以先在本仓库打包：

```bash
venv/bin/python scripts/package_integration.py
```

然后将 `dist/opengopro-custom-component.zip` 解压到 Home Assistant 配置目录，使最终路径为：

```text
config/custom_components/opengopro/manifest.json
```

重启 Home Assistant 后，可用 `.env` 中的长期访问令牌做 smoke check：

```bash
venv/bin/python scripts/ha_smoke.py
```

## 部署说明

当前版本优先面向 Home Assistant OS/Supervised。Home Assistant Container/Core 也可以运行，但蓝牙、主机网络和权限需要由部署者自行配置。

如果不想绑定 Home Assistant，也可以运行独立服务模式。它提供 HTTP API 和网页控制台，未来可作为 Docker 部署和 HA bridge 后端：

```bash
venv/bin/python standalone/server.py --host 0.0.0.0 --port 8765 --data data/cameras.json
```

详见 [STANDALONE.md](STANDALONE.md)。

## 开发

本项目刻意将客户端层设计为可替换结构：

- `client.py` 包含 BLE/HTTP OpenGoPro 传输逻辑。
- `protocol.py` 集中维护 OpenGoPro UUID、BLE 命令、HTTP 参数、状态 ID 和设置 ID。
- `models.py` 定义异常、连接阶段、凭据、媒体项、Wi-Fi 扫描结果和归一化快照。
- `state.py` 负责把相机 HTTP 状态 payload 归一化为 `CameraSnapshot`。
- `coordinator.py` 负责生命周期、状态轮询和 Keep Alive。
- `preview.py` 管理 Home Assistant 侧 Live Preview UDP 监听、订阅和 MPEG-TS relay。
- `button.py`、`switch.py`、`select.py`、`sensor.py`、`binary_sensor.py` 将 coordinator 映射为 Home Assistant 实体。
- `media_source.py` 将相机媒体列表暴露给 Home Assistant Media Browser。
- `preview_proxy.py` 将本地 MPEG-TS 预览流通过 Home Assistant 认证 HTTP view 暴露给面板。
- `frontend/opengopro-console.js` 是 Home Assistant 和 standalone 共用的控制台 Web Component。
- `frontend/opengopro-console-styles.js` 只保存共享控制台样式。
- `frontend/panel.js` 是 Home Assistant 侧边栏 adapter。
- `frontend/vendor/mpegts.min.js` 是面板播放 MPEG-TS 预览所需的本地 vendored 前端库。
- `strings.json` 和 `translations/*.json` 提供 Home Assistant 后端翻译；共享控制台的运行时文案字典保留在 `frontend/opengopro-console.js`。

standalone 侧入口保持在 `standalone/server.py`，但实现已按职责拆分：

- `standalone/ble_process.py` 管理短生命周期 BLE worker 子进程和进度流。
- `standalone/preview.py` 管理 Live Preview UDP 监听、订阅和 MPEG-TS HTTP relay。
- `standalone/store.py` 管理相机配置持久化。

OpenGoPro 的 BLE GATT 命令常量会随 API 版本和相机固件差异变化。v1 将这些调用隔离在客户端层，便于后续用真实设备 trace 强化命令编码，而不影响 Home Assistant 实体、服务和前端接口。

## Home Assistant 自动化示例

如果相机一天内只需要在固定时间醒来，建议使用两条 Automation：

```yaml
alias: GoPro guard wake
trigger:
  - platform: time
    at: "12:00:00"
action:
  - service: opengopro.guard_wake
    data:
      name: GoPro
      hold: 3
```

```yaml
alias: GoPro target wake
trigger:
  - platform: time
    at: "18:00:00"
action:
  - service: opengopro.wake
    data:
      name: GoPro
```

`guard_wake` 用于在目标时间前刷新 GoPro 睡眠后的 BLE 可唤醒窗口；真正使用相机时仍调用 `opengopro.wake`。

## Live Preview

Home Assistant 面板和 standalone 网页控制台都直接接收 GoPro 原生 UDP MPEG-TS 预览数据，并通过认证 HTTP endpoint 转给浏览器播放：

- Home Assistant：`/api/opengopro/preview/{entry_id}.ts`
- standalone：`/api/cameras/{camera_id}/preview.ts`

HERO9、HERO10、HERO11 和 HERO11 Mini 不支持自定义预览端口，因此默认 UDP `8554` 是最兼容路径。运行 HA 的主机必须能接收相机发来的 UDP preview 数据；如果跨网段、容器网络或防火墙阻断 UDP，面板会显示 relay 状态错误。

### HERO12 及更新机型的 COHN 模式

HERO12 及更新机型支持 OpenGoPro 的 COHN（Camera on the Home Network）能力，可以让相机作为 Wi-Fi Station 加入家庭网络。完成 COHN provisioning 后，Home Assistant 不需要切换到 GoPro 自己的 AP 网络，而是通过局域网 HTTPS 访问相机。

当前集成已支持手动填写 COHN 连接参数：

- `HTTP 协议`：`https`
- `相机 HTTP 主机`：COHN 状态返回的局域网 IP，例如 `192.168.50.103`
- `HTTP 端口`：通常为 `443`
- `HTTP 用户名` / `HTTP 密码`：COHN provisioning 返回的 Basic Auth 凭据
- `校验 HTTPS 证书`：首次联调可以关闭；生产使用应保存并校验 GoPro 返回的 COHN 证书
