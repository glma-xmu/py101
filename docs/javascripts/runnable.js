/*
 * Runnable code cells, powered by Pyodide (CPython in the browser via WebAssembly)
 * with a CodeMirror editor for a Jupyter/Colab-like feel.
 *
 * Each "Example" admonition becomes an editable, runnable cell:
 *   - syntax-highlighted editor with line numbers (CodeMirror 5)
 *   - Run (Ctrl/Cmd+Enter) and Reset
 *   - captured stdout/stderr and inline matplotlib figures
 *   - "Show memory": draws a LIVE object-centric memory diagram from the actual
 *     run (real types, addresses; names that share an object converge as arrows)
 *
 * Pyodide loads lazily on first Run; everything runs in the browser, no server.
 * CodeMirror + KaTeX are vendored locally (docs/vendor); only Pyodide still
 * defaults to a CDN — set PYODIDE_BASE below to your own server if needed.
 */
(function () {
  "use strict";

  // Local vendored assets (no foreign CDNs). ASSET_BASE is derived from this
  // script's own URL so it resolves under any GitHub Pages subpath.
  var _self = document.currentScript;
  var ASSET_BASE = (_self && _self.src) ? _self.src.replace(/javascripts\/runnable\.js.*$/, "") : "";
  var CM = ASSET_BASE + "vendor/codemirror/";
  // Pyodide runtime + packages. Repoint to your own server to avoid CDNs.
  // Vendored locally too; repoint to a CDN or your server only if you need
  // on-demand packages (numpy/pandas/matplotlib) that are not vendored here.
  var PYODIDE_BASE = ASSET_BASE + "vendor/pyodide/";

  var cache = {};
  function loadScript(url) {
    if (!cache[url]) {
      cache[url] = new Promise(function (resolve, reject) {
        var s = document.createElement("script");
        s.src = url; s.onload = resolve;
        s.onerror = function () { reject(new Error("Failed to load " + url)); };
        document.head.appendChild(s);
      });
    }
    return cache[url];
  }
  function loadCss(url) {
    if (!cache[url]) {
      var l = document.createElement("link");
      l.rel = "stylesheet"; l.href = url; document.head.appendChild(l); cache[url] = true;
    }
  }

  var cmPromise = null;
  function loadCodeMirror() {
    if (!cmPromise) {
      loadCss(CM + "codemirror.css");
      cmPromise = loadScript(CM + "codemirror.js").then(function () {
        return loadScript(CM + "python.js");
      });
    }
    return cmPromise;
  }

  var pyodidePromise = null;
  function getPyodide(onStatus) {
    if (!pyodidePromise) {
      pyodidePromise = loadScript(PYODIDE_BASE + "pyodide.js").then(function () {
        if (onStatus) { onStatus("Loading Python... (first run only)"); }
        return loadPyodide({ indexURL: PYODIDE_BASE });
      });
    }
    return pyodidePromise;
  }

  var FIGURE_CAPTURE = [
    "import sys, json as _json",
    "_imgs = []",
    "if 'matplotlib' in sys.modules:",
    "    import io as _io, base64 as _b64",
    "    import matplotlib.pyplot as _plt",
    "    for _n in _plt.get_fignums():",
    "        _buf = _io.BytesIO()",
    "        _plt.figure(_n).savefig(_buf, format='png', bbox_inches='tight')",
    "        _imgs.append(_b64.b64encode(_buf.getvalue()).decode())",
    "    _plt.close('all')",
    "_json.dumps(_imgs)"
  ].join("\n");

  // Re-exec the cell in a FRESH namespace (silently) and report user variables,
  // so the memory diagram reflects just this cell, regardless of run order.
  var MEM_HELPER = [
    "def _mem_snapshot(_src):",
    "    import json as _j, types as _t, io as _io2, contextlib as _ctx",
    "    _ns = {}",
    "    try:",
    "        with _ctx.redirect_stdout(_io2.StringIO()):",
    "            exec(compile(_src, '<cell>', 'exec'), _ns)",
    "    except Exception:",
    "        pass",
    "    _out = []",
    "    for _k, _v in _ns.items():",
    "        if _k.startswith('__'):",
    "            continue",
    "        if isinstance(_v, _t.ModuleType):",
    "            continue",
    "        try:",
    "            _r = repr(_v)",
    "        except Exception:",
    "            _r = '<unrepr>'",
    "        if len(_r) > 42:",
    "            _r = _r[:39] + '...'",
    "        _out.append({'name': _k, 'id': id(_v), 'type': type(_v).__name__, 'value': _r})",
    "    return _j.dumps(_out)"
  ].join("\n");

  function runCode(py, source, stdoutEl, figuresEl) {
    stdoutEl.textContent = ""; stdoutEl.classList.remove("error"); figuresEl.innerHTML = "";
    py.setStdout({ batched: function (s) { stdoutEl.textContent += s + "\n"; } });
    py.setStderr({ batched: function (s) { stdoutEl.textContent += s + "\n"; } });
    return py.loadPackagesFromImports(source)
      .then(function () { return py.runPythonAsync(source); })
      .then(function (result) {
        if (result !== undefined && result !== null) { stdoutEl.textContent += String(result) + "\n"; }
        try {
          JSON.parse(py.runPython(FIGURE_CAPTURE)).forEach(function (b64) {
            var img = new Image(); img.className = "runnable-figure";
            img.src = "data:image/png;base64," + b64; figuresEl.appendChild(img);
          });
        } catch (e) { /* no figures */ }
      })
      .catch(function (err) {
        stdoutEl.classList.add("error");
        stdoutEl.textContent += String((err && err.message) || err);
      });
  }

  // Snapshot the cell's variables and convert to a memory-diagram spec.
  function memorySnapshot(py, src) {
    return py.loadPackagesFromImports(src).then(function () {
      py.runPython(MEM_HELPER);
      py.globals.set("_mem_src", src);
      return JSON.parse(py.runPython("_mem_snapshot(_mem_src)"));
    });
  }
  function toSpec(entries, lang) {
    var objects = [], seen = {}, names = [];
    entries.forEach(function (e) {
      var key = String(e.id);
      if (!seen[key]) {
        seen[key] = true;
        objects.push({ key: key, type: e.type, value: e.value, addr: "0x" + Number(e.id).toString(16) });
      }
      names.push({ name: e.name, key: key });
    });
    return {
      memTitle: lang === "zh" ? "堆内存" : "Heap",
      nsTitle: lang === "zh" ? "命名空间" : "namespace",
      objects: objects, names: names
    };
  }

  function enhance(admonition) {
    var codeEl = admonition.querySelector("div.highlight pre > code, pre > code");
    if (!codeEl) { return; }
    var source = codeEl.textContent.replace(/\n+$/, "");
    var highlight = admonition.querySelector("div.highlight") || codeEl;
    var lang = (document.documentElement.lang || "en").slice(0, 2);

    var wrap = document.createElement("div"); wrap.className = "runnable";
    var ta = document.createElement("textarea"); ta.value = source;

    var bar = document.createElement("div"); bar.className = "runnable-bar";
    var runBtn = mkBtn("runnable-run md-button", "▶ " + (lang === "zh" ? "运行" : "Run"));
    var resetBtn = mkBtn("runnable-reset md-button", lang === "zh" ? "重置" : "Reset");
    var memBtn = mkBtn("runnable-mem md-button", lang === "zh" ? "显示内存" : "Show memory");
    var status = document.createElement("span"); status.className = "runnable-status";
    bar.appendChild(runBtn); bar.appendChild(resetBtn); bar.appendChild(memBtn); bar.appendChild(status);

    var output = document.createElement("div"); output.className = "runnable-output";
    var stdoutEl = document.createElement("pre"); stdoutEl.className = "runnable-stdout";
    var figuresEl = document.createElement("div"); figuresEl.className = "runnable-figures";
    output.appendChild(stdoutEl); output.appendChild(figuresEl);

    var memEl = document.createElement("div"); memEl.className = "runnable-memory"; memEl.style.display = "none";

    wrap.appendChild(ta); wrap.appendChild(bar); wrap.appendChild(output); wrap.appendChild(memEl);
    highlight.style.display = "none";
    highlight.parentNode.insertBefore(wrap, highlight.nextSibling);

    var cm = CodeMirror.fromTextArea(ta, {
      mode: "python", lineNumbers: true, indentUnit: 4, viewportMargin: Infinity,
      extraKeys: { "Ctrl-Enter": run, "Cmd-Enter": run }
    });

    var memVisible = false;
    function refreshMemory(py) {
      return memorySnapshot(py, cm.getValue()).then(function (entries) {
        if (!entries.length) {
          memEl.innerHTML = '<div class="runnable-memnote">' +
            (lang === "zh" ? "暂无变量。" : "No variables defined yet.") + "</div>";
        } else {
          window.renderMemoryDiagram(memEl, toSpec(entries, lang));
        }
      });
    }

    function run() {
      runBtn.disabled = true; status.textContent = "";
      getPyodide(function (m) { status.textContent = m; })
        .then(function (py) {
          status.textContent = lang === "zh" ? "运行中..." : "Running...";
          return runCode(py, cm.getValue(), stdoutEl, figuresEl).then(function () {
            if (memVisible) { return refreshMemory(py); }
          });
        })
        .catch(function (err) {
          stdoutEl.classList.add("error"); stdoutEl.textContent = String((err && err.message) || err);
        })
        .then(function () { status.textContent = ""; runBtn.disabled = false; });
    }

    runBtn.addEventListener("click", run);
    resetBtn.addEventListener("click", function () {
      cm.setValue(source);
      stdoutEl.textContent = ""; stdoutEl.classList.remove("error"); figuresEl.innerHTML = "";
    });
    memBtn.addEventListener("click", function () {
      memVisible = !memVisible;
      memEl.style.display = memVisible ? "" : "none";
      memBtn.textContent = memVisible
        ? (lang === "zh" ? "隐藏内存" : "Hide memory")
        : (lang === "zh" ? "显示内存" : "Show memory");
      if (memVisible) {
        memBtn.disabled = true; status.textContent = lang === "zh" ? "读取内存..." : "Reading memory...";
        getPyodide(function (m) { status.textContent = m; })
          .then(function (py) { return refreshMemory(py); })
          .catch(function () {})
          .then(function () { status.textContent = ""; memBtn.disabled = false; });
      }
    });
  }

  function mkBtn(cls, text) {
    var b = document.createElement("button"); b.type = "button"; b.className = cls; b.textContent = text; return b;
  }

  function init() {
    var examples = document.querySelectorAll(".admonition.example, details.example");
    if (!examples.length) { return; }
    loadCodeMirror().then(function () {
      for (var i = 0; i < examples.length; i++) { enhance(examples[i]); }
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
