// Verify fatal media errors stop the broken player and retry only a bounded number of times.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

let Console;
let nextTimer = 1;
const timers = new Map();
const context = {
  HTMLElement: class {},
  customElements: { define: (_, cls) => { Console = cls; } },
  window: {
    setTimeout(callback) { const id = nextTimer++; timers.set(id, callback); return id; },
    clearTimeout(id) { timers.delete(id); },
  },
};
const source = fs.readFileSync("src/static/opengopro-console.js", "utf8")
  .replace(/^import .*;\n/, "");
vm.runInNewContext(source, context);
const consoleView = new Console();
consoleView._locale = "zh-Hans";
consoleView.isConnected = true;
consoleView._camera = () => ({ preview_url: "/preview.ts" });
consoleView._render = () => {};
consoleView._previewRetryTimer = null;
consoleView._previewStableTimer = null;
consoleView._previewRetryCount = 0;
consoleView._previewBlocked = false;

for (let attempt = 1; attempt <= 4; attempt++) {
  let destroyed = 0;
  const player = { pause() {}, unload() {}, detachMediaElement() {}, destroy() { destroyed++; } };
  consoleView._previewPlayer = player;
  consoleView._recoverPreviewPlayer(player, {}, { message: "decode failed" });
  consoleView._recoverPreviewPlayer(player, {}, { message: "duplicate error" });
  assert.equal(destroyed, 1);
  assert.equal(consoleView._previewRetryCount, attempt);
  if (attempt <= 3) {
    assert.ok(consoleView._previewRetryTimer);
    const id = consoleView._previewRetryTimer;
    const callback = timers.get(id);
    timers.delete(id);
    callback();
  } else {
    assert.equal(consoleView._previewBlocked, true);
    assert.match(consoleView._message, /decode failed/);
  }
}
consoleView._resetPreviewRecovery();
assert.equal(consoleView._previewBlocked, false);
assert.equal(consoleView._previewRetryCount, 0);

// Rotation updates the existing preview in place and survives a page reload.
const saved = new Map();
context.window.localStorage = {
  getItem: (key) => saved.get(key) ?? null,
  setItem: (key, value) => saved.set(key, value),
};
const styles = {};
let quarterTurn = false;
const preview = {
  style: { setProperty: (name, value) => { styles[name] = value; } },
  classList: { toggle: (_, enabled) => { quarterTurn = enabled; } },
};
const rotateButton = {};
consoleView._selected = "camera";
consoleView.shadowRoot = { querySelector: (selector) => selector === ".preview" ? preview : rotateButton };
consoleView._previewRotations = new Map();
for (const angle of [90, 180, 270, 0]) {
  consoleView._rotatePreview();
  assert.equal(styles["--preview-rotation"], `${angle}deg`);
  assert.equal(quarterTurn, angle % 180 !== 0);
  assert.match(rotateButton.textContent, new RegExp(`${angle}°`));
}
consoleView._rotatePreview();
const reloaded = new Console();
assert.equal(reloaded._previewRotation("camera"), 90);
assert.equal(reloaded._previewRotation("other"), 0);
