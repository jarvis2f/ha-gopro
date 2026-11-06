// A delayed event stream must not leave the initial state unknown, and an
// older snapshot must never overwrite a newer event or a different camera.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

let Console;
let nextTimer = 1;
const timers = new Map();
const context = {
  HTMLElement: class {},
  customElements: { define: (_, cls) => { Console = cls; } },
  document: { hidden: false },
  window: {
    setTimeout(callback) { const id = nextTimer++; timers.set(id, callback); return id; },
    clearTimeout(id) { timers.delete(id); },
  },
};
vm.runInNewContext(fs.readFileSync("src/static/opengopro-console.js", "utf8")
  .replace(/^import .*;\n/, ""), context);

async function main() {
  const view = new Console();
  Object.assign(view, {
    _cameras: [{ id: "camera" }, { id: "other" }], _selected: "camera",
    _statusGeneration: 0, _render() {}, _canRenderBackground: () => true,
  });
  let emit;
  let resolveSnapshot;
  view._adapter = {
    subscribeState(id, onState) { emit = onState; return { close() {} }; },
    loadStatusSnapshot() { return new Promise((resolve) => { resolveSnapshot = resolve; }); },
  };
  view._syncStateStream();
  const firstTimer = timers.get(view._statusSnapshotTimer);
  firstTimer();
  resolveSnapshot({ http_ready: true, state: { battery: 47 } });
  await new Promise(setImmediate);
  assert.equal(view._cameras[0].battery, 47);
  assert.equal(view._cameras[0].http_ready, true);

  const pending = view._loadStatusSnapshot("camera");
  emit({ http_ready: true, state: { battery: 46 } });
  resolveSnapshot({ state: { battery: 47 } });
  await pending;
  assert.equal(view._cameras[0].battery, 46);

  const otherPending = view._loadStatusSnapshot("camera");
  view._selected = "other";
  view._syncStateStream();
  resolveSnapshot({ state: { battery: 45 } });
  await otherPending;
  assert.equal(view._cameras[0].battery, 46);
  view._closeStateStream();

  // A list request that started before a status event must not erase it.
  view._selected = "camera";
  view._syncStateStream = () => {};
  view._probePresence = () => {};
  view._probePreviewStatus = () => {};
  let resolveList;
  view._adapter.listCameras = () => new Promise((resolve) => { resolveList = resolve; });
  const loading = view._loadCameras();
  view._applyStatusUpdate("camera", { http_ready: true, state: { battery: 42 } });
  resolveList([{ id: "camera" }, { id: "other" }]);
  await loading;
  assert.equal(view._cameras[0].battery, 42);
}
main().catch((error) => { console.error(error); process.exitCode = 1; });
