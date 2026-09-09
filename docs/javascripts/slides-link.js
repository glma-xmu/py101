/*
 * Header shortcut to the course's slide library.
 * Resolve from this asset so the same build works at /, /py101/ and
 * /teaching/py101/. Keep this entry independent of the textbook sidebar.
 */
(function () {
  "use strict";

  var script = document.currentScript;
  if (!script || !script.src) return;
  var base = new URL("../", script.src);

  function init() {
    if (document.querySelector(".slides-link")) return;
    var header = document.querySelector(".md-header__inner");
    if (!header) return;
    var chinese = (document.documentElement.lang || "en").toLowerCase().startsWith("zh");
    var text = chinese ? "课件" : "Slides";
    var title = chinese ? "浏览课堂课件" : "Browse lecture slides";
    var destination = new URL((chinese ? "zh/" : "") + "slides/", base);

    var link = document.createElement("a");
    link.className = "md-header__button md-icon slides-link";
    link.href = destination.href;
    link.title = title;
    link.setAttribute("aria-label", text + " — " + title);
    if (location.pathname === destination.pathname) {
      link.setAttribute("aria-current", "page");
    }

    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("focusable", "false");
    var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", "M4 3h16a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1h-7v2.3l4.5 2.3-.9 1.8L12 20l-4.6 2.4-.9-1.8L11 18.3V16H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Zm1 2v9h14V5H5Zm2 2h10v2H7V7Zm0 4h6v1H7v-1Z");
    svg.appendChild(path);
    var label = document.createElement("span");
    label.className = "slides-link__label";
    label.textContent = text;
    link.append(svg, label);

    var home = header.querySelector(".main-site-link");
    var controls = header.querySelector(".md-header__option");
    var heading = header.querySelector(".md-header__title");
    if (home) home.after(link);
    else if (controls) controls.before(link);
    else if (heading) heading.after(link);
    else header.appendChild(link);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
