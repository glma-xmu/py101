/*
 * Interactive teaching terminals for Appendix A2.
 *
 * A `terminal` fenced block becomes a live shell. The commands run in Python,
 * on Pyodide's real in-memory filesystem (see shell_backend.py) — so paths,
 * wildcards, redirection and pipes behave the way they actually do, while the
 * command set stays small enough to teach in one sitting.
 *
 * Every terminal on a page shares ONE filesystem and one working directory:
 * a `cd` in §2 is still in effect in §5, which is the point. "Reset files"
 * rebuilds the practice tree.
 *
 * Pyodide is shared with runnable.js (window.py101Pyodide) so a page with both
 * runnable cells and terminals loads Python only once.
 */
(function () {
  "use strict";

  var _self = document.currentScript;
  var ASSET_BASE = (_self && _self.src) ? _self.src.replace(/javascripts\/shell\.js.*$/, "") : "";
  var PYODIDE_BASE = ASSET_BASE + "vendor/pyodide/";

  var terminals = [];
  var shellPromise = null;

  function loadPyodide_() {
    if (window.py101Pyodide) { return window.py101Pyodide(function () {}); }
    // Standalone fallback: a page with terminals but no runnable cells.
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = PYODIDE_BASE + "pyodide.js";
      s.onload = resolve;
      s.onerror = function () { reject(new Error("Failed to load Pyodide")); };
      document.head.appendChild(s);
    }).then(function () {
      return loadPyodide({ indexURL: PYODIDE_BASE });
    });
  }

  function getShell(onStatus) {
    if (!shellPromise) {
      shellPromise = loadPyodide_(onStatus)
        .then(function (py) {
          if (onStatus) { onStatus("Starting the shell..."); }
          // ?v= is a cache buster: this URL is fetched at runtime, so without it
          // a returning student can keep an old backend. Bump on every edit to
          // shell_backend.py.
          return fetch(ASSET_BASE + "javascripts/shell_backend.py?v=1")
            .then(function (r) {
              if (!r.ok) { throw new Error("Could not load shell_backend.py"); }
              return r.text();
            })
            .then(function (src) {
              py.runPython(src);
              return {
                run: py.globals.get("shell_run"),
                reset: py.globals.get("shell_reset"),
                prompt: py.globals.get("shell_prompt")
              };
            });
        });
    }
    return shellPromise;
  }

  function mkBtn(cls, text) {
    var b = document.createElement("button");
    b.type = "button"; b.className = cls; b.textContent = text;
    return b;
  }

  function refreshPrompts(text) {
    terminals.forEach(function (t) { t.promptEl.textContent = text; });
  }

  function build(host) {
    var lang = (document.documentElement.lang || "en").slice(0, 2);
    var zh = lang === "zh";
    var suggestions = host.textContent.split("\n")
      .map(function (s) { return s.trim(); })
      .filter(function (s) { return s && s.indexOf("#") !== 0; });

    host.textContent = "";
    host.classList.add("term-ready");

    var bar = document.createElement("div"); bar.className = "term-bar";
    var title = document.createElement("span"); title.className = "term-title";
    title.textContent = zh ? "终端（练习用）" : "Terminal (practice)";
    var resetBtn = mkBtn("term-reset md-button", zh ? "重置文件" : "Reset files");
    var status = document.createElement("span"); status.className = "term-status";
    bar.appendChild(title); bar.appendChild(resetBtn); bar.appendChild(status);

    var log = document.createElement("pre"); log.className = "term-log";

    var row = document.createElement("div"); row.className = "term-inputrow";
    var promptEl = document.createElement("span");
    promptEl.className = "term-prompt";
    promptEl.textContent = "student@py101:~$";
    var input = document.createElement("input");
    input.className = "term-input";
    input.setAttribute("spellcheck", "false");
    input.setAttribute("autocomplete", "off");
    input.setAttribute("autocapitalize", "off");
    input.setAttribute("aria-label", zh ? "终端输入" : "Terminal input");
    row.appendChild(promptEl); row.appendChild(input);

    host.appendChild(bar); host.appendChild(log); host.appendChild(row);

    if (suggestions.length) {
      var chips = document.createElement("div"); chips.className = "term-chips";
      var chipLabel = document.createElement("span");
      chipLabel.className = "term-chiplabel";
      chipLabel.textContent = zh ? "试一试：" : "Try:";
      chips.appendChild(chipLabel);
      suggestions.forEach(function (cmd) {
        var c = mkBtn("term-chip", cmd);
        c.addEventListener("click", function () { input.value = cmd; submit(); });
        chips.appendChild(c);
      });
      host.appendChild(chips);
    }

    var self = { promptEl: promptEl };
    terminals.push(self);

    var history = [], hpos = 0, busy = false;

    function write(text, cls) {
      var span = document.createElement("span");
      if (cls) { span.className = cls; }
      span.textContent = text + "\n";
      log.appendChild(span);
      log.scrollTop = log.scrollHeight;
    }

    function submit() {
      if (busy) { return; }
      var line = input.value;
      input.value = "";
      write(promptEl.textContent + " " + line, "term-echo");
      if (line.trim()) { history.push(line); }
      hpos = history.length;
      busy = true;
      getShell(function (m) { status.textContent = m; })
        .then(function (sh) {
          status.textContent = "";
          var res = JSON.parse(sh.run(line));
          if (res.clear) {
            log.textContent = "";
          } else if (res.out) {
            write(res.out, res.error ? "term-err" : null);
          }
          refreshPrompts(res.prompt);
        })
        .catch(function (err) {
          write(String((err && err.message) || err), "term-err");
        })
        .then(function () {
          busy = false; status.textContent = "";
          input.focus();
        });
    }

    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); submit(); }
      else if (e.key === "ArrowUp") {
        e.preventDefault();
        if (hpos > 0) { hpos--; input.value = history[hpos]; }
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        if (hpos < history.length - 1) { hpos++; input.value = history[hpos]; }
        else { hpos = history.length; input.value = ""; }
      }
    });

    // Load Python on first focus, so the wait happens before the first Enter.
    var warmed = false;
    input.addEventListener("focus", function () {
      if (warmed) { return; }
      warmed = true;
      status.textContent = zh ? "正在加载 shell...（仅首次）" : "Loading the shell... (first time only)";
      getShell(function (m) { status.textContent = m; })
        .then(function (sh) { refreshPrompts(sh.prompt()); status.textContent = ""; })
        .catch(function (err) { status.textContent = String((err && err.message) || err); });
    });

    log.addEventListener("click", function () { input.focus(); });

    resetBtn.addEventListener("click", function () {
      getShell(function (m) { status.textContent = m; })
        .then(function (sh) {
          var p = sh.reset();
          refreshPrompts(p);
          log.textContent = "";
          write(zh ? "练习文件已恢复原状。" : "Practice files put back as they were.", "term-note");
          input.focus();
        })
        .catch(function (err) { write(String((err && err.message) || err), "term-err"); });
    });

    write(zh
      ? "输入命令后按回车。输入 help 查看可用命令。"
      : "Type a command and press Enter. Type help to see what this shell knows.",
      "term-note");
  }

  function init() {
    var hosts = document.querySelectorAll(".terminal-widget:not(.term-ready)");
    for (var i = 0; i < hosts.length; i++) { build(hosts[i]); }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
