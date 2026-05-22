# OpenGoPro 独立服务

这个模式不依赖 Home Assistant 实例，直接提供一个轻量 HTTP API 和网页控制台。它复用 `custom_components/opengopro/client.py` 中的 OpenGoPro BLE/HTTP 客户端，适合先在 MacBook、Linux 主机或未来 Docker 环境中独立运行。

网页控制台复用 `custom_components/opengopro/frontend/opengopro-console.js` 这个共享 Web Component，样式在 `custom_components/opengopro/frontend/opengopro-console-styles.js`。Home Assistant 侧边栏面板和 standalone 页面使用同一套 UI，只通过 adapter 区分 HA WebSocket 和 standalone HTTP API。

控制台支持英文和简体中文。standalone 页面按 `?lang=`、`localStorage.opengopro_locale`、浏览器语言的顺序选择语言，例如 `http://localhost:8765/?lang=zh-Hans` 或 `http://localhost:8765/?lang=en`。Home Assistant 面板使用当前 HA 前端语言。

BLE 操作通过 `standalone/ble_worker.py` 以短生命周期子进程执行，具体协议流程在 `standalone/ble_runtime.py`，子进程启动、超时、错误和进度转发由 `standalone/ble_process.py` 管理。

Live Preview 由 `standalone/preview.py` 管理：它负责 UDP 端口绑定、浏览器订阅和 MPEG-TS HTTP relay，`standalone/server.py` 只保留 HTTP 路由编排。

standalone 还提供每日 wake schedule。它适合没有 Home Assistant Automation 的独立部署：在目标唤醒时间前执行一次 guard wake 刷新 BLE 可唤醒窗口，然后在目标时间真正唤醒相机并开启 Wi-Fi。Home Assistant 部署建议使用 `opengopro.guard_wake` 和 `opengopro.wake` 两条 Automation，而不是依赖 standalone 调度器。

## 本地运行

```bash
venv/bin/python standalone/server.py --host 0.0.0.0 --port 8765 --data data/cameras.json
```

打开：

```text
http://localhost:8765
```

主要 API：

- `GET /api/health`
- `GET /api/cameras`
- `POST /api/cameras`
- `POST /api/scan`
- `POST /api/cohn/provision`
- `GET /api/cameras/{camera_id}/state`
- `GET /api/cameras/{camera_id}/media`
- `GET /api/cameras/{camera_id}/preview/status`
- `GET /api/cameras/{camera_id}/preview.ts`
- `POST /api/cameras/{camera_id}/wake-schedule`
- `POST /api/cameras/{camera_id}/command`

配置每日唤醒保护：

```bash
curl -X POST http://localhost:8765/api/cameras/<camera_id>/wake-schedule \
  -H 'Content-Type: application/json' \
  -d '{"target_time":"18:00","guard_lead_hours":6}'
```

关闭调度：

```bash
curl -X POST http://localhost:8765/api/cameras/<camera_id>/wake-schedule \
  -H 'Content-Type: application/json' \
  -d '{"enabled":false}'
```

## Live Preview

standalone 模式可以在浏览器里显示 GoPro Live Preview。GoPro 原生预览是 UDP MPEG-TS，HERO12 及更早机型为 H.264，HERO13 及之后为 HEVC。独立服务不再依赖 `ffmpeg`，而是直接做 UDP 到 HTTP 的 MPEG-TS relay：

1. 独立服务优先绑定官方默认 UDP `8554` 端口；如果端口不可用，再尝试为支持自定义端口的机型选择临时 UDP 端口。
2. 默认端口路径调用相机 `/gopro/camera/stream/start`；自定义端口路径调用 `/gopro/camera/stream/start?port=<端口>`。
3. 独立服务接收相机发来的 UDP MPEG-TS datagram。
4. 页面通过 `/api/cameras/{camera_id}/preview.ts` 和本地 `mpegts.js` 播放。

HERO9、HERO10、HERO11 和 HERO11 Mini 不支持自定义预览端口，因此默认端口 `8554` 是最兼容路径。启动后独立服务会等待首个 UDP 包；如果超时，预览状态会显示端口或网络路径相关错误，而不是让播放器一直空转。

浏览器需要支持 Media Source Extensions。当前前端会加载 `standalone/static/vendor/mpegts.min.js`，无需运行时访问 CDN。

Home Assistant 集成侧也有独立实现的 MPEG-TS relay，位于 `custom_components/opengopro/preview.py` 和 `preview_proxy.py`。两侧共享思路和前端组件，但互不 import runtime。

## HERO12 COHN 配置

页面里的“配置 COHN”会通过 BLE 完成：

1. 扫描并连接 GoPro BLE。
2. 扫描相机可见的 Wi-Fi。
3. 把家庭 Wi-Fi SSID 和密码写入相机。
4. 创建并读取 COHN 证书。
5. 读取相机局域网 IP、HTTPS 用户名和密码。
6. 把相机保存到 `data/cameras.json`。

完成后，状态读取和控制走：

```text
https://<GoPro局域网IP>:443
```

## Docker 构建

```bash
docker build -f Dockerfile.standalone -t opengopro-standalone .
```

Linux 主机上如果要在容器内使用蓝牙，通常需要 host network、D-Bus 和蓝牙设备权限：

```bash
docker run --rm -it \
  --name opengopro \
  --network host \
  --privileged \
  -v /run/dbus:/run/dbus \
  -v "$PWD/data:/data" \
  opengopro-standalone
```

macOS Docker Desktop 通常不能直接把 Mac 蓝牙暴露给 Linux 容器。Mac 开发阶段建议直接运行本地 Python 服务；Docker 蓝牙联调优先放在 Linux、树莓派或 HA OS/Supervised 宿主机上验证。

## 后续与 Home Assistant 的关系

未来可以把 Home Assistant 集成改成两种后端模式：

- `native`：HA 自己通过本机蓝牙或 ESPHome Bluetooth Proxy 连接 GoPro。
- `bridge`：HA 调用这个独立服务的 HTTP API，由独立服务负责 BLE、COHN provisioning 和 GoPro HTTPS 控制。

这样没有蓝牙的 HA 实例也可以通过局域网访问 standalone 服务来控制 GoPro。
