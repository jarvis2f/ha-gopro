# AGENTS.md

## 项目概览

本仓库是一个 Home Assistant 自定义集成，集成域名为 `opengopro`。
它面向兼容 OpenGoPro 的 GoPro 相机，通过 BLE 完成发现、唤醒和连接流程，
并通过相机 HTTP API 完成控制、状态读取和媒体访问。

主要代码位于 `custom_components/opengopro`。

## 仓库结构

- `custom_components/opengopro/__init__.py`：Home Assistant 集成初始化、服务注册、WebSocket API 注册、前端静态资源注册、媒体代理注册。
- `custom_components/opengopro/client.py`：OpenGoPro BLE/HTTP 传输层和相机状态归一化。
- `custom_components/opengopro/coordinator.py`：生命周期、状态轮询、媒体缓存和 Keep Alive 循环。
- `custom_components/opengopro/{button,switch,select,sensor,binary_sensor}.py`：Home Assistant 实体平台。
- `custom_components/opengopro/media_source.py`：Home Assistant Media Browser 数据源。
- `custom_components/opengopro/media_proxy.py`：通过 Home Assistant 认证代理相机媒体文件。
- `custom_components/opengopro/preview.py`：Home Assistant 侧 UDP MPEG-TS Live Preview relay。
- `custom_components/opengopro/preview_proxy.py`：通过 Home Assistant 认证暴露预览状态和 `.ts` 流。
- `custom_components/opengopro/frontend/panel.js`：侧边栏面板 Web Component。
- `custom_components/opengopro/frontend/vendor/mpegts.min.js`：HA 面板播放 MPEG-TS 预览所需的本地前端库。
- `tests/`：轻量级客户端测试。
- `requirements-dev.txt`：开发和验证依赖，版本与当前验证过的 Home Assistant 版本对齐。
- `scripts/package_integration.py`：打包 `custom_components/opengopro`。
- `scripts/ha_smoke.py`：用 `.env` 中的 Home Assistant token 做远程 smoke check。
- `standalone/`：不依赖 Home Assistant 实例的 HTTP API、BLE worker、UDP MPEG-TS 预览 relay、每日 wake schedule 和网页控制台，复用 OpenGoPro 客户端能力。
- `STANDALONE.md`：独立服务和未来 Docker 部署说明。

## 开发环境

如果本地存在虚拟环境，优先使用它：

```bash
venv/bin/python -m pip install -r requirements-dev.txt
```

当前验证环境为 Python 3.14，Home Assistant 版本为 `2026.5.2`。

## 验证命令

交付修改前运行：

```bash
venv/bin/python -m compileall custom_components standalone scripts tests
venv/bin/python -m pytest -q
venv/bin/python scripts/ha_smoke.py
```

独立服务最小验证：

```bash
venv/bin/python standalone/server.py --help
```

最小 Home Assistant 配置检查：

```bash
tmpdir=$(mktemp -d /private/tmp/ha-gopro-check.XXXXXX)
mkdir -p "$tmpdir/custom_components"
ln -s "$PWD/custom_components/opengopro" "$tmpdir/custom_components/opengopro"
printf 'opengopro:\n' > "$tmpdir/configuration.yaml"
venv/bin/python -m homeassistant --config "$tmpdir" --script check_config
```

本地配置检查时不要默认使用 `default_config:`，除非确实需要验证大量 Home Assistant 内置集成依赖；否则它会安装许多与本项目无关的包，干扰判断。

## 实现约束

- 涉及到 BLE 连接、HTTP 接口的改动，必须直接查询 GoPro 官方 ![OpenGoPro](https://gopro.github.io/OpenGoPro/docs/ble/networking) 文档，不要自己猜测或参考第三方库的实现细节。
- 后续每个改动都必须同时考虑 Home Assistant 集成和 standalone 独立服务。共享能力优先放在 `custom_components/opengopro/client.py` 这类纯协议层；HA 层不得 import `standalone/*`，standalone 层不得依赖 HA runtime。
- 共享前端 UI 放在 `custom_components/opengopro/frontend/opengopro-console.js`。HA 的 `panel.js` 和 standalone 的 `standalone/static/index.html` 只能作为 adapter，不要复制两套 UI。
- 硬件相关的 BLE GATT 命令编码必须集中在 `client.py`，不要散落到实体或前端代码中。
- 不要在实体或前端中直接使用 OpenGoPro 原始状态 ID；先通过 `CameraSnapshot` 归一化。
- 侧边栏面板应通过 Home Assistant WebSocket 命令和服务交互，不要直接从浏览器访问相机。
- 媒体文件必须通过 `media_proxy.py` 走 Home Assistant 认证代理，不要让浏览器直接访问相机的未认证地址。
- Home Assistant 侧已经实现 Live Preview：通过 `custom_components/opengopro/preview.py` 接收 GoPro UDP MPEG-TS datagram，并通过认证 HTTP view 输出 `.ts` 给浏览器。
- standalone 侧也通过 `standalone/preview.py` 做 UDP MPEG-TS relay。两侧可以共享协议理解和前端组件，但 HA 层不得 import `standalone/*` runtime。
- 定时唤醒在 HA 侧优先使用 Home Assistant Automation 组合 `opengopro.guard_wake` 和 `opengopro.wake`；standalone 的 wake schedule 只服务独立模式。
- 相机可见 Wi-Fi AP 扫描目前按官方 BLE protobuf 路径实现，不要猜测不存在的 HTTP endpoint。
- Home Assistant API 变化较快，修改后要用当前安装的 HA 包验证导入、签名和最小 `check_config`。

## 当前已知缺口

- `OpenGoProClient.async_enable_wifi` 已按官方 Set AP Control TLV 命令写入，但尚未用真机验证 response notify、pairing 复用和 AP 启动时序。
- HTTP 状态归一化已按官方常见状态 ID 修正，仍需要用真实相机 payload 校准机型差异。
- Home Assistant 和 standalone 的 MPEG-TS preview relay 已实现，但仍需用真实相机验证 AP/COHN/容器网络下的 UDP 收包路径。
- 当前测试已覆盖客户端、媒体源和 WebSocket payload 的关键路径，但还没有完整 Home Assistant runtime 测试夹具。
- 本仓库尚未完成真实 GoPro 硬件联调。
