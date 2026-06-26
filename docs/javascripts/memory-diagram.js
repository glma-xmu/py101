/*
 * Declarative memory diagrams, in two styles.
 *
 * LEGACY (object-centric, Chapter 1): a framed "Heap" box holds
 * OBJECTS shown as value · address · type; names in a single namespace arrow
 * into the object they refer to. Used by the live "Show memory" button too.
 *
 *   memory: Heap
 *   namespace: Global Namespace
 *   objects:
 *     o1: int 1 @ 0x100
 *   names:
 *     a -> o1
 *
 * CALL style (Chapter 2, function calls): three header-aligned boxes —
 *   1. Global Namespace : the module's names (its local namespace IS the global
 *                          namespace — the bottom frame of the call stack).
 *   2. Heap     : the objects, shown as a bare VALUE, in the middle.
 *   3. Call Stack        : dashed FRAMES, one per running call (local namespaces).
 * Names on both sides arrow INTO the shared objects, so names sharing an object
 * converge. A binding marked `name -> obj @return` is drawn in green, to show a
 * value handed back across the frame boundary by `return`.
 *
 *   memory: Heap
 *   stack: Call Stack
 *   objects:
 *     fn: a function
 *     i4: 4
 *     i16: 16
 *   globals: Global Namespace
 *     square -> fn
 *     number -> i4
 *     answer -> i16 @return
 *   frame: square(n)
 *     n -> i4
 *     result -> i16
 *
 * Also: window.renderMemoryDiagram(hostEl, spec) renders from a data object
 * (used by runnable.js for the LIVE legacy diagram).
 */
(function () {
  "use strict";

  function bind(line) {
    var ret = false, ln = line;
    if (/@return\s*$/.test(ln)) { ret = true; ln = ln.replace(/@return\s*$/, "").trim(); }
    var b;
    if (/->|→/.test(ln)) { var p = ln.split(/->|→/); b = { name: p[0].trim(), key: p[1].trim() }; }
    else { var eq = ln.indexOf("="); b = eq >= 0 ? { name: ln.slice(0, eq).trim(), value: ln.slice(eq + 1).trim() } : { name: ln.trim() }; }
    b.ret = ret; return b;
  }

  function parse(text) {
    var spec = {
      memTitle: "Heap", nsTitle: "namespace", stackTitle: "Call Stack",
      globalsTitle: "Global Namespace",
      objects: [], names: [], globals: [], frames: [], call: false
    };
    var section = null, curFrame = null;
    text.split("\n").forEach(function (raw) {
      var line = raw.trim();
      if (!line || line.charAt(0) === "#") { return; }
      var low = line.toLowerCase();
      function val() { return line.slice(line.indexOf(":") + 1).trim(); }

      if (low.indexOf("memory:") === 0) { spec.memTitle = val(); return; }
      if (low.indexOf("namespace:") === 0) { spec.nsTitle = val(); return; }
      if (low.indexOf("stack:") === 0) { spec.stackTitle = val(); spec.call = true; return; }
      if (low.indexOf("globals:") === 0) { var g = val(); if (g) { spec.globalsTitle = g; } spec.call = true; section = "globals"; return; }
      if (low.indexOf("frame:") === 0) {
        curFrame = { title: val(), rows: [] };
        spec.frames.push(curFrame); spec.call = true; section = "frame"; return;
      }
      if (low === "names:") { section = "names"; return; }
      if (low === "objects:") { section = "objects"; return; }

      if (section === "objects") {
        var i = line.indexOf(":");
        if (i < 0) { return; }
        var key = line.slice(0, i).trim();
        var rest = line.slice(i + 1).trim();
        var addr = null;
        var at = rest.lastIndexOf("@");
        if (at >= 0) { addr = rest.slice(at + 1).trim(); rest = rest.slice(0, at).trim(); }
        var rawv = rest;
        var sp = rest.indexOf(" ");
        var type = sp > 0 ? rest.slice(0, sp) : rest;
        var value = sp > 0 ? rest.slice(sp + 1).trim() : "";
        spec.objects.push({ key: key, type: type, value: value, addr: addr, raw: rawv });
      } else if (section === "names") {
        if (/->|→/.test(line)) { spec.names.push(bind(line)); }
      } else if (section === "globals") {
        spec.globals.push(bind(line));
      } else if (section === "frame" && curFrame) {
        curFrame.rows.push(bind(line));
      }
    });
    spec.objects.forEach(function (o, idx) {
      if (!o.addr) { o.addr = "0x" + (0x5563e0 + idx * 48).toString(16); }
    });
    return spec;
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) { e.className = cls; }
    if (text != null) { e.textContent = text; }
    return e;
  }
  function esc(k) { return (window.CSS && CSS.escape) ? CSS.escape(k) : k; }

  function makeSvg() {
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "mem-arrows"); return svg;
  }
  function marker(svg, id, cls) {
    var m = document.createElementNS(svg.namespaceURI, "marker");
    m.setAttribute("id", id); m.setAttribute("markerWidth", "8"); m.setAttribute("markerHeight", "8");
    m.setAttribute("refX", "6"); m.setAttribute("refY", "3"); m.setAttribute("orient", "auto");
    var tip = document.createElementNS(svg.namespaceURI, "path");
    tip.setAttribute("d", "M0,0 L6,3 L0,6 Z"); tip.setAttribute("class", cls);
    m.appendChild(tip); return m;
  }
  function path(svg, d, cls, markerId) {
    var p = document.createElementNS(svg.namespaceURI, "path");
    p.setAttribute("d", d); p.setAttribute("class", cls);
    if (markerId) { p.setAttribute("marker-end", "url(#" + markerId + ")"); }
    svg.appendChild(p);
  }
  function arrowDotToObject(svg, host, cr, row, green) {
    var target = host.querySelector('.mem-object[data-key="' + esc(row.getAttribute("data-key")) + '"]');
    var dotEl = row.querySelector(".mem-dot");
    if (!target || !dotEl) { return; }
    var dot = dotEl.getBoundingClientRect(), tg = target.getBoundingClientRect();
    var x1 = dot.left + dot.width / 2 - cr.left, y1 = dot.top + dot.height / 2 - cr.top;
    var rightward = x1 < (tg.left + tg.width / 2 - cr.left);
    var x2 = rightward ? (tg.left - cr.left + 3) : (tg.right - cr.left - 3);
    var y2 = tg.top + tg.height / 2 - cr.top;
    var mx = (x1 + x2) / 2;
    path(svg, "M" + x1 + "," + y1 + " C" + mx + "," + y1 + " " + mx + "," + y2 + " " + x2 + "," + y2,
      green ? "mem-arrow mem-arrow-return" : "mem-arrow", green ? "mem-arrowhead-ret" : "mem-arrowhead");
  }

  // ===== LEGACY object-centric diagram (Chapter 1) =========================
  function buildLegacy(host, spec) {
    var canvas = el("div", "mem-canvas");
    var nsCol = el("div", "mem-names");
    nsCol.appendChild(el("div", "mem-names-title", spec.nsTitle || "namespace"));
    spec.names.forEach(function (n) {
      var row = el("div", "mem-name"); row.setAttribute("data-key", n.key);
      row.appendChild(el("span", "mem-name-key", n.name));
      row.appendChild(el("span", "mem-dot"));
      nsCol.appendChild(row);
    });
    var mem = el("div", "mem-memory");
    mem.appendChild(el("div", "mem-memory-title", spec.memTitle));
    spec.objects.forEach(function (o) {
      var row = el("div", "mem-object"); row.setAttribute("data-key", o.key);
      row.appendChild(el("span", "mem-obj-val", o.value));
      row.appendChild(el("span", "mem-obj-addr", o.addr));
      row.appendChild(el("span", "mem-obj-type", o.type));
      mem.appendChild(row);
    });
    var svg = makeSvg();
    canvas.appendChild(nsCol); canvas.appendChild(mem); canvas.appendChild(svg);
    host.appendChild(canvas);
    function draw() {
      while (svg.firstChild) { svg.removeChild(svg.firstChild); }
      var cr = canvas.getBoundingClientRect();
      svg.setAttribute("width", cr.width); svg.setAttribute("height", cr.height);
      svg.setAttribute("viewBox", "0 0 " + cr.width + " " + cr.height);
      var defs = document.createElementNS(svg.namespaceURI, "defs");
      defs.appendChild(marker(svg, "mem-arrowhead", "mem-arrowtip")); svg.appendChild(defs);
      host.querySelectorAll(".mem-name").forEach(function (row) { arrowDotToObject(svg, host, cr, row, false); });
    }
    schedule(draw);
  }

  // ===== CALL diagram (Chapter 2 function calls) ===========================
  function refRow(b, dotFirst) {
    // a name that refers to an object: dot + name, ordered for the facing side
    var row = el("div", "mem-frow"); row.setAttribute("data-fname", b.name);
    var nameEl = el("span", "mem-fname", b.name);
    var dotEl = el("span", "mem-dot");
    if (b.key) {
      row.classList.add("mem-ref"); row.setAttribute("data-key", b.key);
      if (b.ret) { row.classList.add("mem-ref-return"); }
      if (dotFirst) { row.appendChild(dotEl); row.appendChild(nameEl); }
      else { row.appendChild(nameEl); row.appendChild(dotEl); }
    } else if (b.value != null) {
      row.appendChild(nameEl);
      row.appendChild(el("span", "mem-farrow", "→"));
      row.appendChild(el("span", "mem-fval", b.value));
    } else {
      row.classList.add("mem-frow-pending");
      row.appendChild(nameEl);
      row.appendChild(el("span", "mem-frow-pendmark", "—"));
    }
    return row;
  }

  function buildCall(host, spec) {
    var canvas = el("div", "mem-canvas mem-call");
    var lang = (document.documentElement.lang || "en").slice(0, 2);
    var localLabel = lang === "zh" ? "局部命名空间" : "local namespace";

    // 1. Global namespace box (names point right, into the heap)
    var gBox = el("div", "mem-box mem-global-box");
    gBox.appendChild(el("div", "mem-box-title", spec.globalsTitle));
    var gRows = el("div", "mem-box-rows");
    spec.globals.forEach(function (b) { gRows.appendChild(refRow(b, false)); });
    gBox.appendChild(gRows);

    // 2. Heap (middle), value-only objects
    var mem = el("div", "mem-memory mem-memory-call");
    mem.appendChild(el("div", "mem-memory-title", spec.memTitle));
    spec.objects.forEach(function (o) {
      var row = el("div", "mem-object mem-object-simple"); row.setAttribute("data-key", o.key);
      row.appendChild(el("span", "mem-obj-val", o.raw != null ? o.raw : o.value));
      mem.appendChild(row);
    });

    // 3. Call stack box of dashed frames (local namespaces; names point left)
    var stack = el("div", "mem-box mem-stackbox");
    stack.appendChild(el("div", "mem-box-title", spec.stackTitle));
    var framesWrap = el("div", "mem-frames");
    spec.frames.forEach(function (f) {
      var fr = el("div", "mem-frame");
      fr.appendChild(el("div", "mem-frame-title", f.title));
      fr.appendChild(el("div", "mem-frame-kind", localLabel));
      f.rows.forEach(function (b) { fr.appendChild(refRow(b, true)); });
      framesWrap.appendChild(fr);
    });
    stack.appendChild(framesWrap);

    var svg = makeSvg();
    canvas.appendChild(gBox); canvas.appendChild(mem); canvas.appendChild(stack); canvas.appendChild(svg);
    host.appendChild(canvas);

    function draw() {
      while (svg.firstChild) { svg.removeChild(svg.firstChild); }
      var cr = canvas.getBoundingClientRect();
      svg.setAttribute("width", cr.width); svg.setAttribute("height", cr.height);
      svg.setAttribute("viewBox", "0 0 " + cr.width + " " + cr.height);
      var defs = document.createElementNS(svg.namespaceURI, "defs");
      defs.appendChild(marker(svg, "mem-arrowhead", "mem-arrowtip"));
      defs.appendChild(marker(svg, "mem-arrowhead-ret", "mem-arrowtip-ret"));
      svg.appendChild(defs);
      host.querySelectorAll(".mem-ref").forEach(function (row) {
        arrowDotToObject(svg, host, cr, row, row.classList.contains("mem-ref-return"));
      });
    }
    schedule(draw);
  }

  function schedule(draw) {
    requestAnimationFrame(draw);
    var t;
    window.addEventListener("resize", function () { clearTimeout(t); t = setTimeout(draw, 120); });
  }

  function buildDiagram(host, spec) {
    host.innerHTML = "";
    host.classList.add("mem-rendered");
    if (spec.call) { buildCall(host, spec); } else { buildLegacy(host, spec); }
  }

  window.renderMemoryDiagram = buildDiagram;

  function init() {
    document.querySelectorAll(".memory-diagram").forEach(function (host) {
      buildDiagram(host, parse(host.textContent));
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
