/* Dependency-free theme regression checks: node scripts/check_theme_controls.cjs */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const root = path.resolve(__dirname, "..");
const key = "py101-display-theme";

function loadTheme(file, { saved = null, dark = true, blocked = false, legacy = false } = {}) {
  const events = {};
  const loaded = [];
  const changes = {};
  const attributes = {};
  const select = { value: "", addEventListener: (name, callback) => { changes[name] = callback; } };
  const media = { matches: dark };
  let systemChanged;
  media[legacy ? "addListener" : "addEventListener"] = (...args) => { systemChanged = args.at(-1); };
  const stored = new Map(saved === null ? [] : [[key, saved]]);
  const storage = {
    getItem: name => stored.get(name) ?? null,
    setItem: (name, value) => stored.set(name, value),
    removeItem: name => stored.delete(name),
  };
  const window = {
    matchMedia: query => { assert.equal(query, "(prefers-color-scheme: dark)"); return media; },
    addEventListener: (name, callback) => { events[name] = callback; },
    get localStorage() {
      if (blocked) throw new Error("Storage disabled");
      return storage;
    },
  };
  const document = {
    documentElement: { setAttribute: (name, value) => { attributes[name] = value; } },
    querySelector: selector => { assert.equal(selector, "[data-theme-select]"); return select; },
    addEventListener: (name, callback) => { assert.equal(name, "DOMContentLoaded"); loaded.push(callback); },
  };
  vm.runInNewContext(fs.readFileSync(path.join(root, file), "utf8"), { window, document }, { filename: file });
  // Only the first DCL listener owns theme UI. The other initializes the app/player.
  assert.equal(loaded.length, 2);
  const initialTheme = attributes["data-theme"];
  loaded[0]();
  return {
    initialTheme, attributes, select, stored,
    choose(value) { select.value = value; changes.change(); },
    system(value) { media.matches = value; systemChanged(); },
    storage(value, storageKey = key) { events.storage({ key: storageKey, newValue: value }); },
  };
}

for (const file of ["docs/slides/assets/course-slides.js", "live_questions/static/teacher.js"]) {
  const page = loadTheme(file);
  assert.equal(page.initialTheme, "dark", "Auto theme must apply before DOMContentLoaded");
  assert.equal(page.select.value, "auto");
  page.choose("light");
  assert.equal(page.attributes["data-theme"], "light");
  assert.equal(page.stored.get(key), "light");
  page.system(true);
  assert.equal(page.attributes["data-theme"], "light", "Explicit Light overrides system Dark");
  assert.equal(loadTheme(file, { saved: page.stored.get(key) }).initialTheme, "light");
  page.choose("dark");
  page.system(false);
  assert.equal(page.attributes["data-theme"], "dark", "Explicit Dark overrides system Light");
  page.choose("auto");
  assert.equal(page.stored.has(key), false);
  assert.equal(page.attributes["data-theme"], "light");
  page.system(true);
  assert.equal(page.attributes["data-theme"], "dark");
  page.storage("light");
  assert.equal(page.select.value, "light");
  assert.equal(page.attributes["data-theme"], "light");
  page.storage("dark", "unrelated");
  assert.equal(page.attributes["data-theme"], "light");
  page.storage(null, null);
  assert.equal(page.select.value, "auto", "Clearing storage restores Auto");
  assert.equal(page.attributes["data-theme"], "dark");
  assert.equal(loadTheme(file, { saved: "invalid", dark: false }).initialTheme, "light");
  const restricted = loadTheme(file, { blocked: true, legacy: true });
  restricted.choose("light");
  assert.equal(restricted.attributes["data-theme"], "light");
  restricted.choose("auto");
  restricted.system(false);
  assert.equal(restricted.attributes["data-theme"], "light");
  console.log("Theme checks passed:", file);
}
