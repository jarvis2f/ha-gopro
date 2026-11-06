# gopro-ctl

通过 BLE 和 OpenGoPro HTTP API 控制兼容的 GoPro 相机的 Docker 服务，提供网页控制台、媒体浏览、实时预览和定时唤醒。

## 功能

- 扫描 GoPro BLE 设备，唤醒、休眠和连接相机。
- 控制拍摄与相机设置，读取状态，浏览和下载媒体。
- 为支持 COHN 的相机配置 Wi-Fi，扫描相机可见的接入点。
- 接收相机 UDP MPEG-TS 预览，通过网页播放。
- 配置每日唤醒和提前刷新 BLE 唤醒窗口；网页支持英文和简体中文。
- 创建一次性、每日、指定星期或自定义 Cron 的照片、视频和延时拍摄计划；也可按经纬度计算的日落时间触发。

## Home Assistant 蓝牙桥接

当蓝牙适配器或 ESPHome 蓝牙代理已由 Home Assistant 管理时，可以让 gopro-ctl 通过 HA 执行 BLE 操作。HA 继续负责选择可连接的适配器和管理连接槽；相机的 HTTP 控制、媒体和预览仍由 gopro-ctl 直接通过局域网访问。扫描、唤醒、休眠、Wi-Fi 扫描和 COHN 配置，以及拍摄计划的定期唤醒均使用同一个桥接后端。

1. 在项目目录执行 `python3 tools/build_ha_bridge.py`，生成 `dist/gopro_ble_bridge.zip`。将压缩包内的 `custom_components/gopro_ble_bridge` 目录复制到 Home Assistant 配置目录的 `custom_components/` 下。
2. 在 HA 的 `configuration.yaml` 中加入一行 `gopro_ble_bridge:`，检查配置并重启 HA。该集成依赖 HA 的 Bluetooth 集成，ESPHome 代理必须支持主动连接。更新 gopro-ctl 后重新构建并复制压缩包中的目录，再重启 HA，以保持两端 BLE 实现一致。
3. 在 gopro-ctl 所在机器创建仅本机可读的 `.env` 文件，设置 `GOPRO_HA_URL=https://你的HA地址:8123` 和 `GOPRO_HA_TOKEN=你的HA长期访问令牌`。令牌须属于 HA 管理员；勿提交或分享令牌。HA URL 应使用可信 HTTPS，尤其是跨不可信网络时。
4. 在 Linux 部署机器运行 `docker compose -f compose.ha.yaml up -d --build`。此配置不需要将蓝牙或 D-Bus 直通给 gopro-ctl；HA 和相机仍需网络可达。使用其他部署方式时，设置 `GOPRO_BLE_BACKEND=home_assistant`、`GOPRO_HA_URL` 和 `GOPRO_HA_TOKEN`；默认 `local` 保留原来的本地蓝牙模式。
5. 在网页重新扫描相机并使用 HA 返回的蓝牙 MAC 地址。macOS 的 BLE UUID 不是 Linux/HA 的 MAC 地址；原有相机记录不会自动改地址。重建记录或在数据文件中更新原记录的 `ble_address` 前请备份数据，避免丢失 COHN 凭据和计划引用。

GoPro 要求每个新 BLE 客户端配对。必要时把相机切换到 GoPro Quik 配对模式，使用 HA 管理员令牌向 `/api/gopro_ble_bridge/execute` 发送 JSON `{"command":"pair","ble_address":"相机MAC地址"}`；相机如有提示需确认。例如，在已设置 `GOPRO_HA_URL` 和 `GOPRO_HA_TOKEN` 环境变量的终端中（将示例地址换为扫描到的地址）：

```sh
curl --fail-with-body -X POST "$GOPRO_HA_URL/api/gopro_ble_bridge/execute" \
  -H "Authorization: Bearer $GOPRO_HA_TOKEN" -H 'Content-Type: application/json' \
  --data '{"command":"pair","ble_address":"EC:EB:B3:69:DE:25"}'
```

配对由所选适配器/代理处理，代理固件对加密、配对和保存绑定的支持以及 GoPro 的兼容性需要真机验证。扫描成功不代表配对或唤醒一定成功，跨适配器切换也可能需要重新配对。

通过桥接配置 COHN 时页面显示开始与最终结果，中间阶段目前不实时推送。定期唤醒保护需要 HA 提供新收到的相机广播，不能判断时会安全跳过；它不能恢复已超过唤醒窗口的相机。HA 未运行、连接槽耗尽或相机不可见时不会自动切换到本地蓝牙。

## Docker 部署

需要 Linux 主机、Docker 和 Docker Compose，以及可用的蓝牙适配器和运行中的系统 D-Bus。主机须能够访问相机的 Wi-Fi 网络或 COHN 局域网。macOS Docker Desktop 通常无法将主机蓝牙提供给 Linux 容器。

```bash
docker compose up -d --build
```

打开 `http://<主机地址>:8765`。配置和相机凭据保存在 `./data/cameras.json`；备份和迁移时请妥善保护该目录。调度时间使用容器时区，可通过环境变量设置，例如 `TZ=Asia/Shanghai docker compose up -d`。

Compose 使用 host 网络接收预览 UDP 流、挂载系统 D-Bus，并以 privileged 模式运行以访问蓝牙设备。镜像可单独构建运行：

```bash
docker build -t gopro-ctl .
docker run -d --name gopro-ctl --restart unless-stopped \
  --network host --privileged \
  -e TZ=Asia/Shanghai \
  -v /run/dbus:/run/dbus -v "$PWD/data:/data" gopro-ctl
```

服务本身没有用户认证，请仅在可信网络中使用，或在反向代理中配置认证并限制网络访问。

## 使用

在网页中扫描相机并添加，或对支持的机型执行 COHN 配网。COHN 成功后，服务使用相机返回的局域网 HTTPS 连接信息。页面语言按 `?lang=`、浏览器中保存的语言、浏览器语言的顺序选择，例如 `http://localhost:8765/?lang=zh-Hans`。

预览默认使用 UDP 8554；端口占用时会尝试其他端口，但部分机型只支持默认端口。浏览器需要支持 Media Source Extensions，HEVC 预览还取决于浏览器和系统的解码支持。BLE 配对、COHN 和预览网络路径仍需使用实际相机验证。

媒体弹窗中的视频可以在浏览器内播放，代理会转发 HTTP Range 请求以便分段加载和拖动进度。实际效果取决于相机是否支持文件分段读取、视频的 MP4 索引位置、网络速度以及浏览器对视频编码（如 HEVC）的支持；播放失败时可下载原文件。

在“计划任务”中创建拍摄计划前，请先唤醒相机并连接，以读取可用预设。每项计划可保存预设、自定义参数和视频或延时拍摄时长。日落计划使用手动填写的经纬度离线计算，可设置提前或延后的分钟数；所有时间均使用服务的 `TZ` 时区。计划和最近执行记录保存在数据目录中的 `capture-schedules.json`，需与 `cameras.json` 一同备份；同一数据目录只运行一个服务实例。

选择“高级 Cron”可填写标准五字段表达式 `分 时 日 月 星期`，支持 `*`、列表、范围、步长以及英文月份和星期名称。例如 `0 18 * * *` 为每天 18:00，`0 8,18 * * 1-5` 为工作日 08:00 和 18:00，`*/15 * * * *` 为每 15 分钟。星期日可用 0 或 7；日和星期都受限时，任一匹配即执行。Cron 本身指定时间，与日落触发分开选择。夏令时不存在的本地时间跳过，重复的本地时间只执行第一次。高频任务若与拍摄或其他相机操作重叠可能被跳过；长期停机后，较早的错过记录会合并，最近 90 分钟的错过任务逐次记录，均不补拍。

服务会在目标时间前约两分钟准备相机，拍摄后尝试停止并休眠；错过的任务不会补拍。相机已在拍摄、参数写入失败、无法确认拍摄状态等情况会记录为跳过、失败或结果不确定，请在计划任务的执行记录中检查。成功表示相机接受了快门并恢复空闲，未单独验证媒体文件是否写入 SD 卡。服务重启后会尝试停止中断的定时视频或延时拍摄；若恢复失败，需要手动检查相机。计划依赖服务持续运行、准确的系统时间、相机电源及 BLE/网络连接；精确快门时间、长期供电状态和拍摄结果需用实际相机验证。

只要相机有启用的拍摄计划，服务便为该相机维护一项共享的定期唤醒任务：首次尽快检查，确认相机原本处于休眠后才通过 BLE 唤醒；确认相机空闲、未录制和未预览后再请求休眠，并检查休眠广播。确认成功后约 6 小时再执行；失败或相机已开机时约 15 分钟后重试，临近拍摄或相机被操作时延后。计划列表显示最近状态及下次检查时间；所有计划停用后停止该相机的任务。计时和状态保存在 `capture-schedules.json`，服务停止期间无法执行。若相机已超出 BLE 唤醒窗口、广播没有可识别的电源状态，或其他设备占用连接，需要人工检查；是否能持续刷新唤醒窗口仍需真机长期验证。

每日唤醒可在网页配置，也可调用 API：

```bash
curl -X POST http://localhost:8765/api/cameras/<camera_id>/wake-schedule \
  -H 'Content-Type: application/json' \
  -d '{"target_time":"18:00","guard_lead_hours":6}'
```

关闭调度时发送 `{"enabled":false}`。拍摄计划接口包括 `/api/schedules` 和 `/api/schedules/{schedule_id}`，历史记录为 `/api/schedules/{schedule_id}/history`。其他主要接口包括 `/api/health`、`/api/cameras`、`/api/scan`、`/api/cohn/provision`，以及 `/api/cameras/{camera_id}/state`、`media`、`preview/status`、`preview.ts` 和 `command`。

## 开发与验证

`src/client.py`、`src/protocol.py`、`src/models.py` 和 `src/state.py` 实现相机协议与状态归一化；`src/server.py` 提供 HTTP API；`src/ble_runtime.py` 和 `src/ble_worker.py` 处理 BLE 操作；`src/preview.py` 和 `src/static/` 提供预览与控制台。

```bash
venv/bin/python -m pip install -r requirements-dev.txt
venv/bin/python -m compileall src tests
venv/bin/python -m pytest -q
venv/bin/python src/server.py --help
```
