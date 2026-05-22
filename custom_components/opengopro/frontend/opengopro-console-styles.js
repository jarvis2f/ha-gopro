export const CONSOLE_STYLES = `        :host {
          --bg: var(--primary-background-color, #eef2ed);
          --surface: var(--card-background-color, #fbfcf8);
          --surface-2: color-mix(in srgb, var(--surface), #132019 7%);
          --ink: var(--primary-text-color, #142019);
          --muted: var(--secondary-text-color, #637066);
          --line: color-mix(in srgb, var(--divider-color, #d8dfd9), transparent 12%);
          --accent: #00a676;
          --accent-2: #d9f35f;
          --danger: #c64f42;
          --shadow: 0 18px 48px rgba(13, 23, 17, 0.12);
          display: block;
          min-height: 100vh;
          color: var(--ink);
          background:
            linear-gradient(135deg, color-mix(in srgb, var(--accent), transparent 92%), transparent 38%),
            linear-gradient(180deg, color-mix(in srgb, var(--surface), transparent 15%), transparent 260px),
            var(--bg);
          font-family: "Avenir Next", "Segoe UI", ui-sans-serif, system-ui, sans-serif;
        }
        * { box-sizing: border-box; }
        .shell {
          max-width: 1380px;
          margin: 0 auto;
          padding: clamp(18px, 3vw, 34px);
        }
        .topbar {
          display: grid;
          grid-template-columns: minmax(0, 1fr) auto;
          gap: 16px;
          align-items: end;
          margin-bottom: 18px;
        }
        .eyebrow {
          color: var(--accent);
          font-size: 12px;
          font-weight: 800;
          letter-spacing: 0.14em;
          text-transform: uppercase;
        }
        h1 {
          margin: 4px 0 0;
          font-size: clamp(30px, 5vw, 62px);
          line-height: 0.92;
          letter-spacing: 0;
        }
        .sub {
          margin-top: 10px;
          color: var(--muted);
          max-width: 760px;
        }
        .toolbar, .row {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
          align-items: center;
        }
        select, input, button {
          min-width: 0;
          min-height: 40px;
          border-radius: 8px;
          border: 1px solid var(--line);
          background: var(--surface);
          color: var(--ink);
          padding: 8px 11px;
          font: inherit;
          letter-spacing: 0;
        }
        button {
          cursor: pointer;
          font-weight: 800;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          transition: transform 120ms ease, border-color 120ms ease, background 120ms ease;
        }
        button:hover { transform: translateY(-1px); }
        button:disabled, select:disabled, input:disabled {
          opacity: 0.55;
          cursor: default;
          transform: none;
        }
        .primary {
          background: var(--accent);
          border-color: var(--accent);
          color: #001a12;
        }
        .danger {
          background: var(--danger);
          border-color: var(--danger);
          color: white;
        }
        .ghost {
          background: color-mix(in srgb, var(--surface), transparent 30%);
        }
        .layout {
          display: grid;
          grid-template-columns: minmax(250px, 320px) minmax(0, 1fr);
          gap: 16px;
          min-width: 0;
        }
        .stack {
          display: grid;
          gap: 16px;
          min-width: 0;
          align-content: start;
        }
        .side-stack {
          grid-template-rows: auto minmax(240px, 1fr);
          height: calc(100vh - 174px);
          min-height: 520px;
        }
        .panel {
          border: 1px solid var(--line);
          border-radius: 8px;
          background: color-mix(in srgb, var(--surface), transparent 2%);
          box-shadow: var(--shadow);
          padding: 16px;
          min-width: 0;
        }
        .panel-title {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
          margin-bottom: 13px;
        }
        h2 {
          margin: 0;
          color: var(--muted);
          font-size: 12px;
          font-weight: 900;
          letter-spacing: 0.12em;
          text-transform: uppercase;
        }
        .camera-list {
          display: grid;
          gap: 8px;
          max-height: 124px;
          overflow: auto;
        }
        .camera-card {
          width: 100%;
          justify-content: flex-start;
          text-align: left;
          background: var(--surface-2);
          color: var(--ink);
          border-color: var(--line);
          min-height: 66px;
          padding-block: 9px;
        }
        .camera-card.active {
          border-color: var(--accent);
          box-shadow: inset 4px 0 0 var(--accent);
        }
        .camera-card small {
          color: var(--muted);
          font-weight: 600;
          overflow-wrap: anywhere;
        }
        .camera-card strong {
          overflow-wrap: anywhere;
        }
        .camera-card > span {
          min-width: 0;
          flex: 1;
        }
        .state-dot {
          width: 10px;
          height: 10px;
          border-radius: 999px;
          background: #9aa39d;
          box-shadow: 0 0 0 3px rgba(154, 163, 157, 0.14);
          flex: 0 0 auto;
        }
        .state-dot.on {
          background: var(--accent);
          box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent), transparent 76%);
        }
        .state-dot.off {
          background: var(--danger);
          box-shadow: 0 0 0 3px color-mix(in srgb, var(--danger), transparent 76%);
        }
        .state-dot.standby {
          background: #58a6ff;
          box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.2);
        }
        .state-dot.checking {
          background: var(--accent-2);
          box-shadow: 0 0 0 3px rgba(217, 243, 95, 0.24);
        }
        .status-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 10px;
        }
        .metric {
          min-height: 88px;
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 12px;
          background: var(--surface-2);
          position: relative;
          overflow: hidden;
        }
        .metric::after {
          content: "";
          position: absolute;
          right: 10px;
          top: 10px;
          width: 8px;
          height: 8px;
          border-radius: 999px;
          background: var(--accent-2);
          opacity: 0.7;
        }
        .metric span {
          color: var(--muted);
          font-size: 12px;
          font-weight: 700;
        }
        .metric strong {
          display: block;
          margin-top: 13px;
          font-size: clamp(18px, 2.2vw, 28px);
          line-height: 1;
          overflow-wrap: anywhere;
        }
        .preview-panel {
          padding: 12px;
          background: #050806;
          border-color: color-mix(in srgb, var(--accent), transparent 55%);
        }
        .preview-panel .panel-title {
          margin: 2px 4px 10px;
        }
        .preview-panel h2 {
          color: rgba(238,247,239,0.72);
        }
        .preview-head {
          display: grid;
          grid-template-columns: auto minmax(0, 1fr);
          align-items: center;
        }
        .preview-head-actions {
          display: flex;
          justify-content: flex-end;
          align-items: center;
          gap: 8px;
          min-width: 0;
        }
        .mode-tabs {
          display: inline-flex;
          align-items: center;
          gap: 4px;
          min-width: 0;
          padding: 4px;
          border: 1px solid rgba(238,247,239,0.14);
          border-radius: 8px;
          background: rgba(238,247,239,0.06);
        }
        .mode-tab {
          min-height: 30px;
          padding: 5px 10px;
          color: rgba(238,247,239,0.72);
          background: transparent;
          border-color: transparent;
          font-size: 12px;
          white-space: nowrap;
        }
        .mode-tab.active {
          color: #001a12;
          background: var(--accent-2);
          border-color: var(--accent-2);
        }
        .head-settings {
          min-height: 38px;
          color: #eef7ef;
          background: rgba(238,247,239,0.08);
          border-color: rgba(238,247,239,0.16);
          white-space: nowrap;
        }
        .preview-status {
          display: grid;
          grid-template-columns: repeat(6, minmax(0, 1fr));
          gap: 8px;
          margin: 10px 4px 0;
        }
        .preview-metric {
          min-width: 0;
          border: 1px solid rgba(238,247,239,0.14);
          border-radius: 8px;
          padding: 9px 10px;
          background: rgba(238,247,239,0.06);
          color: #eef7ef;
        }
        .preview-metric span {
          display: block;
          color: rgba(238,247,239,0.58);
          font-size: 10px;
          font-weight: 900;
          text-transform: uppercase;
        }
        .preview-metric strong {
          display: block;
          margin-top: 4px;
          font-size: 13px;
          line-height: 1.2;
          overflow-wrap: anywhere;
        }
        .capture-toolbar {
          display: grid;
          grid-template-columns: minmax(180px, 0.95fr) minmax(220px, 1.1fr) minmax(180px, 0.95fr);
          gap: 10px;
          align-items: stretch;
          margin: 12px 4px 2px;
        }
        .tool-cluster {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 6px;
          min-width: 0;
          border: 1px solid rgba(238,247,239,0.12);
          border-radius: 8px;
          padding: 8px;
          background: rgba(238,247,239,0.05);
        }
        .tool-cluster > span {
          grid-column: 1 / -1;
          color: rgba(238,247,239,0.54);
          font-size: 10px;
          font-weight: 900;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }
        .tool-button {
          min-height: 34px;
          padding: 7px 8px;
          color: #eef7ef;
          background: rgba(238,247,239,0.08);
          border-color: rgba(238,247,239,0.16);
          font-size: 12px;
        }
        .tool-button.accent {
          color: #001a12;
          background: var(--accent);
          border-color: var(--accent);
        }
        .record-button {
          min-height: 100%;
          color: #07100b;
          background: var(--accent-2);
          border: 1px solid color-mix(in srgb, var(--accent-2), #000 14%);
          border-radius: 8px;
          padding: 12px 16px;
          box-shadow: inset 0 -2px 0 rgba(0,0,0,0.12);
        }
        .record-button.recording {
          color: white;
          background: var(--danger);
          border-color: color-mix(in srgb, var(--danger), #000 12%);
        }
        .record-button.photo {
          background: #f6f0df;
          border-color: rgba(246,240,223,0.72);
        }
        .record-button.lapse {
          background: #9fd8ff;
          border-color: rgba(159,216,255,0.72);
        }
        .record-dot {
          width: 10px;
          height: 10px;
          border-radius: 999px;
          background: currentColor;
          opacity: 0.8;
        }
        .settings-grid {
          display: grid;
          grid-template-columns: 1fr;
          gap: 10px;
          align-items: start;
        }
        .settings-modal {
          width: min(1120px, calc(100vw - 36px));
          max-height: calc(100vh - 72px);
          padding: 22px;
          overflow: auto;
        }
        .settings-workspace {
          display: grid;
          grid-template-columns: 280px minmax(0, 1fr);
          gap: 16px;
          align-items: start;
        }
        .preset-pane,
        .settings-pane {
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 12px;
          background: color-mix(in srgb, var(--surface-2), transparent 10%);
          min-width: 0;
        }
        .settings-pane {
          background: var(--surface);
          overflow: hidden;
        }
        .preset-pane {
          position: sticky;
          top: 0;
        }
        .pane-title {
          display: flex;
          justify-content: space-between;
          align-items: baseline;
          gap: 10px;
          margin-bottom: 12px;
          padding: 0 2px 10px;
          border-bottom: 1px solid var(--line);
        }
        .pane-title span,
        .preset-empty {
          color: var(--muted);
          font-size: 12px;
          font-weight: 700;
        }
        .pane-title strong {
          font-size: 15px;
          text-align: right;
          min-width: 0;
          overflow-wrap: anywhere;
        }
        .preset-list {
          display: grid;
          gap: 5px;
          max-height: min(52vh, 520px);
          overflow: auto;
          padding-right: 1px;
        }
        .preset-button {
          width: 100%;
          display: grid;
          justify-content: stretch;
          gap: 3px;
          text-align: left;
          background: transparent;
          border-color: var(--line);
          padding: 8px 10px;
          min-height: 58px;
          box-shadow: none;
        }
        .preset-button.active {
          border-color: var(--accent);
          background: color-mix(in srgb, var(--accent), transparent 88%);
          box-shadow: inset 3px 0 0 var(--accent);
        }
        .preset-name,
        .preset-meta {
          overflow-wrap: anywhere;
        }
        .preset-name {
          color: var(--ink);
          font-size: 13px;
          font-weight: 850;
        }
        .preset-meta {
          color: var(--muted);
          font-size: 11px;
          font-weight: 700;
        }
        .settings-group {
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 0;
          background: transparent;
          min-width: 0;
          overflow: hidden;
        }
        .settings-group-head {
          display: grid;
          gap: 4px;
          padding: 10px 12px 8px;
          background: color-mix(in srgb, var(--surface-2), transparent 35%);
        }
        .settings-group-head strong {
          font-size: 14px;
        }
        .settings-group-head span {
          color: var(--muted);
          font-size: 12px;
          line-height: 1.35;
        }
        .setting-list {
          display: grid;
        }
        .setting-control {
          display: grid;
          grid-template-columns: 1fr;
          gap: 8px;
          align-items: stretch;
          min-width: 0;
          padding: 12px;
          border-top: 1px solid var(--line);
        }
        .setting-control label {
          display: grid;
          grid-template-columns: minmax(0, 1fr) auto;
          gap: 6px 12px;
          align-items: baseline;
        }
        .setting-control label span {
          color: var(--ink);
          font-size: 13px;
          line-height: 1.2;
        }
        .setting-control label small {
          color: var(--muted);
          font-weight: 700;
          overflow-wrap: anywhere;
          text-align: right;
          max-width: 240px;
        }
        .setting-input {
          display: grid;
          grid-template-columns: minmax(0, 1fr) 82px;
          gap: 8px;
          min-width: 0;
        }
        .setting-input select {
          min-height: 36px;
          padding-block: 6px;
          width: 100%;
        }
        .mini-button {
          min-height: 36px;
          padding: 6px 8px;
          font-size: 12px;
          background: color-mix(in srgb, var(--accent), transparent 86%);
          border-color: color-mix(in srgb, var(--accent), transparent 45%);
          color: var(--ink);
        }
        .preview {
          width: 100%;
          height: clamp(260px, 52vh, 620px);
          border-radius: 8px;
          overflow: hidden;
          position: relative;
          display: grid;
          place-items: center;
          background:
            linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px),
            linear-gradient(0deg, rgba(255,255,255,0.07) 1px, transparent 1px),
            radial-gradient(circle at 72% 18%, rgba(217,243,95,0.25), transparent 26%),
            #0e1511;
          background-size: 28px 28px, 28px 28px, auto, auto;
          color: #eef7ef;
        }
        .preview::before {
          content: "";
          position: absolute;
          inset: 18px;
          border: 1px solid rgba(238,247,239,0.2);
          border-radius: 6px;
          pointer-events: none;
          z-index: 1;
        }
        .preview-stream {
          width: 100%;
          height: 100%;
          object-fit: contain;
          background: #050806;
          display: block;
          z-index: 0;
        }
        .preview-video {
          width: 100%;
          height: 100%;
          object-fit: contain;
          background: #050806;
          display: block;
          z-index: 0;
        }
        .preview-overlay {
          position: absolute;
          left: 18px;
          right: 18px;
          bottom: 18px;
          z-index: 2;
          display: flex;
          justify-content: space-between;
          gap: 10px;
          pointer-events: none;
        }
        .preview-overlay > div {
          min-width: 0;
          max-width: 50%;
          border: 1px solid rgba(238,247,239,0.18);
          border-radius: 8px;
          padding: 9px 11px;
          background: rgba(5,8,6,0.66);
          backdrop-filter: blur(10px);
        }
        .preview-overlay span {
          display: block;
          color: rgba(238,247,239,0.62);
          font-size: 10px;
          font-weight: 900;
          text-transform: uppercase;
        }
        .preview-overlay strong {
          display: block;
          margin-top: 4px;
          color: #eef7ef;
          font-size: 13px;
          line-height: 1.2;
          overflow-wrap: anywhere;
        }
        .reticle {
          z-index: 1;
          text-align: center;
          display: grid;
          gap: 8px;
        }
        .reticle strong { font-size: 20px; }
        .reticle span { color: rgba(238,247,239,0.7); }
        .media-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
          gap: 12px;
        }
        .media-item {
          min-height: 220px;
          border-radius: 8px;
          border: 1px solid var(--line);
          background: var(--surface-2);
          display: grid;
          grid-template-rows: 130px auto;
          overflow: hidden;
          color: var(--ink);
          text-decoration: none;
          transition: transform 120ms ease, border-color 120ms ease;
        }
        .media-item:hover {
          transform: translateY(-2px);
          border-color: var(--accent);
        }
        .thumb {
          min-height: 130px;
          background:
            linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px),
            linear-gradient(0deg, rgba(255,255,255,0.08) 1px, transparent 1px),
            #101713;
          background-size: 22px 22px;
          display: grid;
          place-items: center;
          overflow: hidden;
        }
        .thumb img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          display: block;
        }
        .media-body {
          display: grid;
          gap: 6px;
          padding: 10px;
          align-content: end;
        }
        .badge {
          width: max-content;
          min-width: 42px;
          border-radius: 6px;
          padding: 5px 7px;
          background: #101713;
          color: var(--accent-2);
          font-weight: 900;
          font-size: 11px;
        }
        .media-item strong {
          font-size: 13px;
          overflow-wrap: anywhere;
        }
        .media-item span { color: var(--muted); font-size: 12px; }
        .empty, .log {
          border: 1px dashed var(--line);
          border-radius: 8px;
          color: var(--muted);
          padding: 16px;
          background: color-mix(in srgb, var(--surface), transparent 24%);
          min-width: 0;
          max-width: 100%;
          overflow-wrap: anywhere;
        }
        .log {
          white-space: pre-wrap;
          height: 100%;
          min-height: 180px;
          max-height: none;
          overflow: auto;
          font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
          font-size: 12px;
          line-height: 1.45;
        }
        .log-panel {
          display: grid;
          grid-template-rows: auto minmax(0, 1fr);
          min-height: 0;
        }
        .provision {
          display: grid;
          gap: 9px;
        }
        .scan-results {
          display: grid;
          gap: 7px;
          max-height: 86px;
          overflow: auto;
        }
        .scan-device {
          width: 100%;
          justify-content: space-between;
          text-align: left;
          background: var(--surface-2);
        }
        .scan-device strong, .scan-device small {
          display: block;
        }
        .scan-device small {
          color: var(--muted);
          font-weight: 600;
          overflow-wrap: anywhere;
        }
        .wifi-field {
          display: grid;
          grid-template-columns: minmax(0, 1fr) auto;
          gap: 8px;
        }
        .wifi-hint {
          color: var(--muted);
          font-size: 11px;
          font-weight: 650;
        }
        .provision-progress {
          border: 1px solid var(--line);
          border-radius: 8px;
          background: color-mix(in srgb, var(--surface-2), transparent 18%);
          padding: 10px;
          max-height: 180px;
          overflow: auto;
          display: grid;
          gap: 7px;
        }
        .progress-line {
          display: grid;
          grid-template-columns: 72px 1fr;
          gap: 8px;
          font-size: 12px;
          color: var(--muted);
        }
        .progress-line strong {
          color: var(--text);
          font-size: 12px;
        }
        .modal-backdrop {
          position: fixed;
          inset: 0;
          z-index: 20;
          display: none;
          place-items: center;
          padding: 18px;
          background: rgba(8, 13, 10, 0.54);
          backdrop-filter: blur(12px);
        }
        .modal-backdrop.open {
          display: grid;
        }
        .modal {
          width: min(560px, 100%);
          max-height: calc(100vh - 36px);
          overflow: auto;
          border: 1px solid color-mix(in srgb, var(--line), white 18%);
          border-radius: 8px;
          background: var(--surface);
          box-shadow: 0 28px 84px rgba(0, 0, 0, 0.32);
          padding: 18px;
        }
        .modal-head {
          display: flex;
          justify-content: space-between;
          align-items: start;
          gap: 12px;
          margin-bottom: 16px;
        }
        .modal-title {
          display: grid;
          gap: 5px;
        }
        .modal-title strong {
          font-size: 20px;
          line-height: 1.1;
        }
        .modal-title span {
          color: var(--muted);
          font-size: 13px;
        }
        .icon-button {
          width: 38px;
          min-height: 38px;
          padding: 0;
          font-size: 20px;
          line-height: 1;
        }
        .modal-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 10px;
          margin-top: 16px;
        }
        label {
          display: grid;
          gap: 5px;
          color: var(--muted);
          font-size: 12px;
          font-weight: 700;
        }
        @media (max-width: 980px) {
          .topbar, .layout { grid-template-columns: 1fr; }
          .side-stack { height: auto; min-height: 0; }
          .status-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .preview-status, .capture-toolbar { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .settings-workspace { grid-template-columns: 1fr; }
          .preset-pane { position: static; }
          .preset-list { max-height: 220px; }
          .preview-head { grid-template-columns: 1fr; gap: 10px; }
          .preview-head-actions { justify-content: space-between; }
          .record-button { grid-column: 1 / -1; min-height: 64px; }
        }
        @media (max-width: 560px) {
          .shell { padding: 16px; }
          .status-grid, .preview-status, .capture-toolbar, .settings-grid, .setting-control, .setting-input { grid-template-columns: 1fr; }
          .preview-head-actions { display: grid; grid-template-columns: 1fr; }
          .mode-tabs { width: 100%; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); }
          .preview-overlay { display: grid; }
          .preview-overlay > div { max-width: none; }
          .record-button { min-height: 58px; }
        }
`;
