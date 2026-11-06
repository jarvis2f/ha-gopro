# AGENTS.md

## 项目概览

gopro-ctl 是通过 Docker 部署的 GoPro 控制服务，使用 BLE 发现、唤醒和连接相机，并通过 OpenGoPro HTTP API 控制相机、读取状态和访问媒体。

## 结构

- `src/client.py`、`src/protocol.py`、`src/models.py`、`src/state.py`：BLE/HTTP 协议及状态归一化。
- `src/server.py`：HTTP API 和服务生命周期。
- `src/ble_runtime.py`、`src/ble_process.py`、`src/ble_worker.py`：BLE 操作和 worker。
- `src/preview.py`：UDP MPEG-TS 预览 relay。
- `src/store.py`：相机配置持久化。
- `src/static/`：网页控制台和本地播放器。
- `Dockerfile`、`compose.yaml`：容器构建和部署。
- `tests/`：协议与服务测试。

## 验证

使用本地虚拟环境执行 `venv/bin/python -m compileall src tests`、`venv/bin/python -m pytest -q` 和 `venv/bin/python src/server.py --help`。Docker、Linux、蓝牙或网络相关验证在 pve-dev 测试服务器进行，不要在本地使用 Docker。

## 构建与发布

- 在 `pve-dev` 上使用仓库的 `Dockerfile` 构建 Linux 镜像；不要在本地运行 Docker。构建上下文只需 `Dockerfile`、`requirements.txt` 和 `src/`，不要包含 `data/` 或凭据。
- 为每次发布使用可识别的镜像标签，通过 `docker save` 导出并传输到 `pve-debian12-prod`，校验 SHA-256 后使用 `docker load` 导入。可通过 MCP 上传和下载中转；不要编写脚本手动调用 MCP 或发送 JSON-RPC。
- 生产部署目录为 `/docker/gopro-ctl`，使用该目录的 `compose.yaml` 管理容器。更新镜像前先备份现有 Compose 文件，保留其中的网络、环境文件、日志及其他生产配置，然后执行 `docker compose up -d --no-build`。保留旧镜像和配置以便回退。
- 服务使用 host 网络，监听内网地址 `192.168.2.123:9898`；数据持久化在 `/docker/gopro-ctl/data`，容器内挂载为 `/data`。保留现有的 `cameras.json`、`capture-schedules.json` 和 `gopro-ctl.env`，不要覆盖、公开或提交其中的凭据。
- 发布后检查容器状态和日志，从另一台内网主机访问 `http://192.168.2.123:9898/api/health`，并确认已有相机和定时任务仍可读取。涉及相机的实际 BLE、媒体删除和预览功能仍须按需使用真机验证。清理本次传输产生的临时镜像包。

## 实现约束

- 涉及 BLE 连接或 HTTP 接口的改动必须直接查询 [GoPro 官方 OpenGoPro 文档](https://gopro.github.io/OpenGoPro/docs/ble/networking)。
- BLE GATT 命令编码集中在客户端协议层，状态先通过 `CameraSnapshot` 归一化。
- 相机可见 Wi-Fi AP 扫描使用官方 BLE protobuf 路径。
- 不在仓库提交相机凭据。BLE 配对、COHN 和预览 UDP 网络路径仍需真机验证。
