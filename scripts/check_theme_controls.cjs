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
  const documentEvents = {};
  const attributes = {};
  const choices = ["light", "dark"].map(value => ({
    value, attributes: {}, click: null,
    getAttribute: name => name === "data-theme-choice" ? value : null,
    setAttribute(name, next) { this.attributes[name] = next; },
    addEventListener(name, callback) { assert.equal(name, "click"); this.click = callback; },
  }));
  const trigger = { focused: false, focus() { this.focused = true; } };
  const menu = {
    open: false,
    contains: node => node === trigger || choices.includes(node),
    querySelector: selector => { assert.equal(selector, "summary"); return trigger; },
    querySelectorAll: selector => { assert.equal(selector, "[data-theme-choice]"); return choices; },
  };
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
    querySelector: selector => selector === "[data-theme-menu]" ? menu : null,
    addEventListener: (name, callback) => {
      if (name === "DOMContentLoaded") loaded.push(callback);
      else documentEvents[name] = callback;
    },
  };
  vm.runInNewContext(fs.readFileSync(path.join(root, file), "utf8"), { window, document }, { filename: file });
  // Only the first DCL listener owns theme UI. The other initializes the app/player.
  assert.equal(loaded.length, 2);
  const initialTheme = attributes["data-theme"];
  loaded[0]();
  return {
    initialTheme, attributes, choices, menu, trigger, stored,
    choose(value) { menu.open = true; choices.find(button => button.value === value).click(); },
    selected() { return choices.find(button => button.attributes["aria-pressed"] === "true").value; },
    system(value) { media.matches = value; systemChanged(); },
    storage(value, storageKey = key) {
      if (storageKey === key || storageKey === null) {
        if (value === null) stored.delete(key); else stored.set(key, value);
      }
      events.storage({ key: storageKey, newValue: value });
    },
    outside() { menu.open = true; documentEvents.click({ target: {} }); },
    escape() {
      menu.open = true;
      documentEvents.keydown({ key: "Escape", preventDefault() {}, stopImmediatePropagation() {} });
    },
  };
}

for (const file of ["docs/slides/assets/course-slides.js", "live_questions/static/teacher.js"]) {
  const page = loadTheme(file);
  assert.equal(page.initialTheme, "dark", "Auto theme must apply before DOMContentLoaded");
  assert.equal(page.selected(), "dark");
  page.choose("light");
  assert.equal(page.attributes["data-theme"], "light");
  assert.equal(page.stored.get(key), "light");
  assert.equal(page.menu.open, false, "Selecting a theme closes its menu");
  assert.equal(page.trigger.focused, true);
  page.system(true);
  assert.equal(page.attributes["data-theme"], "light", "Explicit Light overrides system Dark");
  assert.equal(loadTheme(file, { saved: page.stored.get(key) }).initialTheme, "light");
  page.choose("dark");
  page.system(false);
  assert.equal(page.attributes["data-theme"], "dark", "Explicit Dark overrides system Light");
  page.storage(null);
  assert.equal(page.stored.has(key), false);
  assert.equal(page.attributes["data-theme"], "light");
  page.system(true);
  assert.equal(page.attributes["data-theme"], "dark");
  page.storage("light");
  assert.equal(page.selected(), "light");
  assert.equal(page.attributes["data-theme"], "light");
  page.storage("dark", "unrelated");
  assert.equal(page.attributes["data-theme"], "light");
  page.storage(null, null);
  assert.equal(page.selected(), "dark", "Clearing storage restores the browser preference");
  assert.equal(page.attributes["data-theme"], "dark");
  assert.equal(loadTheme(file, { saved: "invalid", dark: false }).initialTheme, "light");
  const restricted = loadTheme(file, { blocked: true, legacy: true });
  restricted.choose("light");
  assert.equal(restricted.attributes["data-theme"], "light");
  restricted.storage(null);
  restricted.system(false);
  assert.equal(restricted.attributes["data-theme"], "light");
  page.outside();
  assert.equal(page.menu.open, false);
  page.escape();
  assert.equal(page.menu.open, false);
  console.log("Theme checks passed:", file);
}
