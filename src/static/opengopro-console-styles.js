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
          container-type: size;
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
        .preview-stream, .preview-video {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%) rotate(var(--preview-rotation, 0deg));
        }
        .preview-quarter-turn .preview-stream, .preview-quarter-turn .preview-video {
          width: 100cqh;
          height: 100cqw;
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

        /* Console design: quiet surfaces, one green accent, and a dedicated viewfinder. */
        :host {
          --bg: #f0f3f1;
          --surface: #ffffff;
          --surface-2: #f5f7f6;
          --ink: #17221e;
          --muted: #63726b;
          --line: #dce4df;
          --accent: #087b59;
          --accent-2: #b8e3cb;
          --danger: #ae403b;
          --shadow: none;
          min-height: 100dvh;
          background: var(--bg);
          font-family: "Avenir Next", "Segoe UI", system-ui, sans-serif;
          font-size: 14px;
        }
        .shell { max-width: 1500px; padding: 26px clamp(18px, 3vw, 40px) 48px; }
        .topbar {
          align-items: center;
          gap: 24px;
          margin-bottom: 26px;
          padding-bottom: 22px;
          border-bottom: 1px solid #d4ded8;
        }
        .eyebrow { font-size: 10px; letter-spacing: .16em; color: var(--accent); }
        h1 { margin-top: 5px; font-size: clamp(25px, 3vw, 36px); line-height: 1.1; letter-spacing: -.035em; }
        .sub { margin-top: 7px; font-size: 13px; line-height: 1.45; }
        .toolbar { justify-content: flex-end; }
        #camera-select:disabled { display: none; }
        select, input, button { min-height: 40px; border-radius: 7px; }
        button { font-weight: 700; }
        button:hover:not(:disabled) { transform: none; border-color: #91a89c; }
        button:active:not(:disabled) { transform: scale(.98); }
        button:focus-visible, input:focus-visible, select:focus-visible, a:focus-visible {
          outline: 3px solid #48a47c;
          outline-offset: 2px;
        }
        button:disabled, select:disabled, input:disabled { opacity: .55; }
        .primary { background: var(--accent); border-color: var(--accent); color: #fff; }
        .primary:hover:not(:disabled) { background: #06694c; border-color: #06694c; }
        .ghost { background: var(--surface); }
        .layout { grid-template-columns: minmax(250px, 292px) minmax(0, 1fr); gap: 20px; }
        .stack { gap: 16px; }
        .side-stack { height: auto; min-height: 0; grid-template-rows: auto minmax(260px, 1fr); }
        .panel { padding: 18px; border-radius: 10px; background: var(--surface); box-shadow: none; }
        .panel-title { margin-bottom: 15px; }
        h2 { color: var(--ink); font-size: 14px; font-weight: 750; letter-spacing: 0; text-transform: none; }
        .camera-list { max-height: 240px; }
        .camera-card { background: var(--surface-2); border-color: transparent; min-height: 70px; }
        .camera-card.active { background: #edf7f1; border-color: #9ecab0; box-shadow: inset 3px 0 0 var(--accent); }
        .empty { border: 1px dashed #d4ded8; background: #f8faf9; padding: 16px; line-height: 1.5; }
        .log { background: #f7f9f8; border: 0; border-radius: 7px; padding: 14px; line-height: 1.6; }
        .preview-panel { background: #151d19; border-color: #151d19; padding: 16px; }
        .preview-panel .panel-title { margin: 0 0 14px; }
        .preview-panel h2 { color: #f5f8f6; font-size: 15px; }
        .mode-tabs { background: #222d27; border-color: #38463d; }
        .mode-tab { color: #c4d0c8; font-weight: 700; }
        .mode-tab.active { color: #173326; background: #cce9d7; border-color: #cce9d7; }
        .head-settings, .tool-button { background: #29352e; border-color: #405047; color: #f4f8f5; }
        .preview { height: auto; aspect-ratio: 16 / 9; min-height: 260px; max-height: 620px; background: #0b100d; border: 1px solid #35443b; }
        .preview::before { display: none; }
        .reticle { padding: 24px; }
        .reticle strong { font-size: 18px; }
        .reticle span { color: #aebcb2; font-size: 13px; }
        .preview-status { gap: 0; margin: 16px 0 0; padding: 0 0 16px; border-bottom: 1px solid #39473e; }
        .preview-metric { border: 0; border-left: 1px solid #39473e; border-radius: 0; background: transparent; padding: 0 12px; }
        .preview-metric:first-child { border-left: 0; padding-left: 0; }
        .preview-metric span { color: #a6b5ab; font-size: 11px; font-weight: 600; text-transform: none; }
        .preview-metric strong { margin-top: 7px; color: #f3f7f4; font-size: 13px; font-weight: 700; }
        .capture-toolbar { margin: 16px 0 0; gap: 12px; }
        .tool-cluster { padding: 0; border: 0; background: transparent; gap: 7px; }
        .tool-cluster > span { color: #a6b5ab; font-size: 11px; font-weight: 600; letter-spacing: 0; text-transform: none; }
        .tool-button.accent { background: #d2eadd; border-color: #d2eadd; color: #173326; }
        .record-button, .record-button.photo, .record-button.lapse {
          min-height: 66px; background: #e3eee7; border-color: #e3eee7; color: #172d20; box-shadow: none;
        }
        .record-button.recording { background: #ae403b; border-color: #ae403b; color: #fff; }
        .record-dot { width: 12px; height: 12px; background: #ae403b; opacity: 1; }
        .recording .record-dot { background: #fff; }
        .media-item { background: var(--surface-2); }
        .badge { background: #263b2f; color: #e4f3e9; }
        .modal { border-radius: 10px; padding: 24px; }
        .modal-backdrop { background: rgba(14, 25, 19, .58); }
        .modal-title strong { color: var(--ink); }
        .settings-modal { padding: 24px; }
        .preset-pane, .settings-pane { background: var(--surface-2); }
        .settings-pane { background: var(--surface); }
        .preset-button.active { background: #edf7f1; }
        .progress-line strong { color: var(--ink); }
        .schedule-modal { width: min(760px, 100%); }
        .schedule-list-head, .schedule-item-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
        .schedule-list-head { margin-bottom: 14px; color: var(--muted); font-size: 12px; }
        .schedule-list { display: grid; gap: 10px; margin-top: 14px; }
        .schedule-item { display: grid; gap: 8px; padding: 14px; border: 1px solid var(--line); border-radius: 8px; background: var(--surface-2); }
        .schedule-item > span, .schedule-item small, .schedule-item-head span { color: var(--muted); font-size: 12px; overflow-wrap: anywhere; }
        .schedule-actions button { min-height: 34px; padding: 6px 10px; font-size: 12px; }
        .schedule-form { display: grid; gap: 16px; }
        .schedule-fields { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
        .schedule-fields input, .schedule-fields select { width: 100%; }
        .schedule-hint { color: var(--muted); font-size: 12px; line-height: 1.5; margin: 0; }
        .schedule-cron { grid-column: 1 / -1; display: grid; gap: 6px; }
        .schedule-cron small { color: var(--muted); font-size: 12px; line-height: 1.5; }
        .schedule-parameters { display: grid; gap: 10px; padding-top: 14px; border-top: 1px solid var(--line); }
        .schedule-parameters > strong { font-size: 13px; }
        .weekdays { border: 0; padding: 0; margin: 0; display: flex; align-items: center; flex-wrap: wrap; gap: 8px; }
        .weekdays legend { color: var(--muted); font-size: 12px; font-weight: 700; margin-bottom: 6px; }
        .weekdays label { display: flex; align-items: center; gap: 4px; }
        .weekdays input { width: auto; min-height: 0; }
        .schedule-error { color: #8b2825; background: #fff1f0; border: 1px solid #ecc3c0; border-radius: 7px; padding: 10px; margin-bottom: 14px; overflow-wrap: anywhere; }
        @media (max-width: 720px) {
          .topbar { grid-template-columns: minmax(0, 1fr) auto; }
          .layout { display: grid; grid-template-columns: 1fr; }
          .side-stack, .main-stack { display: contents; }
          .cameras-panel { order: 1; }
          .preview-panel { order: 2; }
          .main-stack > .panel:not(.preview-panel) { order: 3; }
          .log-panel { order: 4; }
          .log { min-height: 110px; }
          .preview-head { grid-template-columns: auto minmax(0, 1fr); }
          .preview-head-actions { justify-content: flex-end; }
          .preview-status { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px 0; }
          .preview-metric:nth-child(4) { border-left: 0; padding-left: 0; }
          .capture-toolbar { grid-template-columns: minmax(0, 1fr) minmax(160px, 1.2fr) minmax(0, 1fr); }
          .record-button { grid-column: auto; }
        }
        /* Keep the main controls in view on desktop; long lists scroll within their panels. */
        @media (min-width: 721px) and (min-height: 650px) {
          .shell {
            height: 100dvh;
            display: grid;
            grid-template-rows: auto minmax(0, 1fr);
            padding-top: 18px;
            padding-bottom: 18px;
          }
          .topbar {
            grid-template-columns: minmax(0, 1fr) auto;
            margin-bottom: 16px;
            padding-bottom: 14px;
          }
          h1 { font-size: clamp(24px, 2.5vw, 32px); }
          .layout {
            grid-template-columns: minmax(210px, 260px) minmax(0, 1fr);
            min-height: 0;
            gap: 16px;
          }
          .side-stack {
            display: grid;
            grid-template-rows: auto minmax(0, 1fr);
            min-height: 0;
          }
          .main-stack { display: grid; grid-template-rows: minmax(0, 1fr); min-height: 0; }
          .panel { padding: 14px; }
          .panel-title { margin-bottom: 10px; }
          .camera-list { max-height: min(25dvh, 200px); }
          .log { min-height: 0; }
          .preview-panel {
            display: grid;
            grid-template-rows: auto minmax(0, 1fr) auto auto;
            min-height: 0;
          }
          .preview-panel .panel-title { margin-bottom: 10px; }
          .preview-head { grid-template-columns: auto minmax(0, 1fr); }
          .preview-head-actions { justify-content: flex-end; }
          .preview { height: 100%; min-height: 0; max-height: none; aspect-ratio: auto; }
          .preview-status {
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 0;
            margin-top: 10px;
            padding-bottom: 10px;
          }
          .preview-metric:nth-child(4) { border-left: 1px solid #39473e; padding-left: 12px; }
          .capture-toolbar {
            grid-template-columns: minmax(0, 1fr) minmax(140px, 1.1fr) minmax(0, 1fr);
            margin-top: 10px;
          }
          .record-button { grid-column: auto; min-height: 58px; }
        }
        @media (max-width: 560px) {
          .shell { padding: 20px 14px 32px; }
          .topbar { grid-template-columns: 1fr; gap: 15px; margin-bottom: 16px; padding-bottom: 16px; }
          .toolbar { justify-content: flex-start; }
          .layout { gap: 12px; }
          .panel { padding: 15px; }
          .preview-panel { padding: 12px; }
          .preview-head { grid-template-columns: 1fr; }
          .preview-head-actions { display: flex; justify-content: space-between; }
          .mode-tabs { width: auto; display: inline-flex; }
          .preview { min-height: 190px; }
          .preview-status { grid-template-columns: repeat(3, minmax(0, 1fr)); }
          .preview-metric { padding-right: 7px; padding-left: 7px; }
          .capture-toolbar { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .record-button { grid-column: 1 / -1; grid-row: 1; min-height: 58px; }
          .preview-overlay { display: flex; }
          .preview-overlay > div { max-width: 50%; }
          .modal-actions { flex-wrap: wrap; }
          .schedule-fields { grid-template-columns: 1fr; }
        }
        /* Shared select surface. The original select retains its value and change events. */
        .select-control { position: relative; display: inline-flex; width: 100%; min-width: 0; }
        .toolbar > .select-control { width: auto; min-width: 150px; max-width: 220px; }
        .select-native {
          position: absolute !important; width: 1px !important; height: 1px !important;
          min-height: 0 !important; padding: 0 !important; margin: -1px !important;
          overflow: hidden !important; clip-path: inset(50%); border: 0 !important;
        }
        .select-trigger {
          width: 100%; min-width: 0; min-height: 40px; padding: 8px 11px 8px 12px;
          display: flex; justify-content: space-between; gap: 12px; text-align: left;
          color: var(--ink); background: #fff; border: 1px solid #cedbd3; border-radius: 7px;
          font-size: 13px; font-weight: 650;
        }
        .select-trigger:hover:not(:disabled), .select-trigger[aria-expanded="true"] { border-color: #74a58a; background: #f8fbf9; }
        .select-trigger:focus-visible { outline: 3px solid #48a47c; outline-offset: 2px; }
        .select-value { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .select-arrow { flex: 0 0 auto; width: 7px; height: 7px; margin: -3px 3px 0 0; border-right: 1.5px solid #64796c; border-bottom: 1.5px solid #64796c; transform: rotate(45deg); }
        .select-trigger[aria-expanded="true"] .select-arrow { transform: rotate(225deg); margin-top: 3px; }
        .select-menu {
          position: fixed; z-index: 50; overflow: auto; padding: 5px; border-radius: 9px;
          border: 1px solid #d3dfd8; background: #fff; box-shadow: 0 14px 35px rgba(24, 49, 35, .18);
          color: var(--ink); overscroll-behavior: contain;
        }
        .select-option { min-height: 36px; display: flex; align-items: center; padding: 8px 11px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer; overflow-wrap: anywhere; }
        .select-option.highlighted, .select-option:hover { background: #edf6f0; color: #075e42; }
        .select-option[aria-selected="true"] { font-weight: 800; }
        .select-option[aria-selected="true"]::after { content: "✓"; margin-left: auto; padding-left: 12px; color: var(--accent); }
        .select-option[aria-disabled="true"] { opacity: .45; cursor: default; }
        .datalist-option { display: grid; gap: 3px; }
        .datalist-option small { color: var(--muted); font-size: 11px; font-weight: 500; }
        .media-modal { width: min(1050px, 100%); max-height: calc(100dvh - 36px); }
        .media-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin: 4px 0 16px; color: var(--muted); font-size: 13px; font-weight: 700; }
        .media-card { position: relative; min-width: 0; }
        .media-select { position: absolute; z-index: 1; top: 8px; right: 8px; padding: 6px; border-radius: 6px; background: var(--surface-2); }
        .media-select input { width: 18px; height: 18px; display: block; }
        .media-toolbar .row { flex-wrap: wrap; }
        .media-modal .media-grid { max-height: none; overflow: visible; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); }
        .media-modal .media-item { width: 100%; min-height: 200px; grid-template-rows: 128px auto; justify-content: stretch; gap: 0; padding: 0; text-align: left; font-weight: inherit; }
        .media-modal .thumb { min-height: 128px; }
        .media-modal .media-body { padding: 10px; }
        .media-empty { min-height: 140px; display: grid; place-items: center; text-align: center; }
        .media-player { margin: 0 0 18px; padding: 14px; border-radius: 8px; background: #151d19; color: #f3f7f4; }
        .media-player-head { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; }
        .media-player-head > strong { min-width: 0; overflow-wrap: anywhere; }
        .media-player-head .ghost, .media-download { min-height: 36px; padding: 7px 10px; border: 1px solid #405047; border-radius: 7px; background: #29352e; color: #f4f8f5; font-size: 12px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; }
        .media-video { width: 100%; max-height: min(48dvh, 540px); display: block; aspect-ratio: 16 / 9; object-fit: contain; border-radius: 6px; background: #080c09; }
        .media-play-error { margin: 12px 0 0; }
        .media-play-error[hidden] { display: none; }
        .settings-modal { width: min(1040px, calc(100vw - 36px)); height: min(780px, calc(100dvh - 48px)); max-height: calc(100dvh - 48px); display: grid; grid-template-rows: auto minmax(0, 1fr); overflow: hidden; padding: 24px; }
        .settings-modal.has-error { grid-template-rows: auto auto minmax(0, 1fr); }
        .settings-error { margin: 14px 0 0; }
        .settings-modal .modal-head { padding-bottom: 18px; margin: 0; border-bottom: 1px solid var(--line); }
        .settings-workspace { min-height: 0; grid-template-columns: 240px minmax(0, 1fr); gap: 20px; align-items: stretch; padding-top: 18px; }
        .preset-pane, .settings-pane { min-height: 0; border: 0; border-radius: 8px; }
        .preset-pane { position: static; overflow: auto; background: #f3f7f4; padding: 15px; }
        .preset-list { max-height: none; gap: 8px; }
        .preset-button { min-height: 68px; background: #fff; border: 1px solid #e0e9e3; padding: 11px; }
        .preset-button.active { background: #fff; border-color: #8ebda0; box-shadow: inset 3px 0 0 var(--accent); }
        .preset-name { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
        .preset-active { color: #087b59; font-size: 10px; white-space: nowrap; }
        .preset-meta { font-size: 11px; line-height: 1.45; }
        .settings-pane { overflow: auto; padding: 0 4px 12px; background: transparent; }
        .settings-pane-title { padding: 0 0 12px; margin-bottom: 14px; }
        .settings-grid { gap: 12px; }
        .settings-group { border: 1px solid #e0e9e3; border-radius: 8px; background: #fff; }
        .settings-group-head { background: #f7faf8; padding: 12px 14px; }
        .setting-list { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .setting-control { padding: 12px 14px 14px; gap: 9px; border-top: 1px solid #edf2ee; }
        .setting-control:nth-child(even) { border-left: 1px solid #edf2ee; }
        .setting-control label { grid-template-columns: 1fr; gap: 4px; }
        .setting-control label small { text-align: left; }
        .setting-input { grid-template-columns: minmax(0, 1fr) auto; }
        .setting-input .select-trigger, .mini-button { min-height: 38px; }
        .mini-button { padding: 6px 13px; background: #eaf5ee; border-color: #c5dfcd; color: #075b40; }
        @media (max-width: 720px) {
          .settings-modal { height: min(780px, calc(100dvh - 36px)); padding: 18px; }
          .settings-workspace { display: block; overflow: auto; }
          .preset-pane { margin-bottom: 16px; }
          .preset-list { max-height: 180px; }
          .settings-pane { overflow: visible; }
          .preview-head-actions { flex-wrap: wrap; }
        }
        @media (max-width: 560px) {
          .toolbar > .select-control { min-width: 120px; }
          .setting-list { grid-template-columns: 1fr; }
          .setting-control:nth-child(even) { border-left: 0; }
          .media-modal .media-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .media-player-head { align-items: flex-start; flex-direction: column; }
        }
        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after { transition-duration: .01ms !important; animation-duration: .01ms !important; animation-iteration-count: 1 !important; }
        }
`;
