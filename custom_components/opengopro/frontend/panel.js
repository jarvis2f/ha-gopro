import "./opengopro-console.js";

class OpenGoProPanel extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    this._ensureConsole();
  }

  set panel(panel) {
    this._panel = panel;
  }

  _ensureConsole() {
    if (!this._hass || this._console) return;
    this._ensureMpegts();
    this._console = document.createElement("opengopro-console");
    this._console.adapter = {
      label: "Home Assistant",
      locale: this._hass.language || document.documentElement.lang || navigator.language,
      listCameras: async () => {
        const cameras = await this._hass.callWS({ type: "opengopro/cameras" });
        return cameras.map((camera) => ({
          ...camera,
          id: camera.entry_id,
          endpoint: camera.http_host ? `${camera.http_scheme || "http"}://${camera.http_host}:${camera.http_port || 8080}` : "",
        }));
      },
      command: async (id, command, extra = {}) => {
        const haCommand = command === "set_mode"
          ? "set_mode"
          : command === "set_setting"
            ? "set_setting"
            : command === "set_preset"
              ? "set_preset"
            : command;
        return this._hass.callWS({
          type: "opengopro/command",
          entry_id: id,
          command: haCommand,
          ...extra,
        });
      },
      loadState: async (id) => {
        const cameras = await this._hass.callWS({ type: "opengopro/cameras" });
        return cameras.find((camera) => camera.entry_id === id) || {};
      },
      loadPresence: async (id) => this._hass.callWS({ type: "opengopro/presence", entry_id: id }),
      loadPreviewStatus: async (id) => fetch(`/api/opengopro/preview/${id}/status`, {
        credentials: "same-origin",
      }).then((response) => response.json()),
      previewUrl: (id) => `/api/opengopro/preview/${id}.ts`,
      scanAccessPoints: async (payload) => this._hass.callWS({
        type: "opengopro/scan_access_points",
        entry_id: payload.entry_id || payload.id || this._console?._selected,
        timeout: payload.timeout || 30,
      }),
      loadPresets: async (id) => this._hass.callWS({ type: "opengopro/presets", entry_id: id }),
      loadMedia: async (id) => this._hass.callWS({ type: "opengopro/media", entry_id: id }),
    };
    this.replaceChildren(this._console);
  }

  _ensureMpegts() {
    if (window.mpegts || document.querySelector("script[data-opengopro-mpegts]")) return;
    const script = document.createElement("script");
    script.src = "/api/opengopro/frontend/vendor/mpegts.min.js";
    script.dataset.opengoproMpegts = "true";
    document.head.appendChild(script);
  }
}

customElements.define("opengopro-panel", OpenGoProPanel);
