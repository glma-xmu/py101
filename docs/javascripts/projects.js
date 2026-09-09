/* Asset-relative URLs work on root, subpath and bilingual mirrors. */
(function () {
  "use strict";
  var script = document.currentScript;
  if (!script) return;
  var base = new URL("../", script.src);
  var zh = (document.documentElement.lang || "en").startsWith("zh");
  function t(en, cn) { return zh ? cn : en; }
  function element(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }
  function init() {
    var header = document.querySelector(".md-header__inner");
    if (header && !header.querySelector(".projects-link")) {
      var link = element("a", "md-header__button md-icon projects-link");
      link.href = new URL((zh ? "zh/" : "") + "projects/", base).href;
      link.title = t("Browse student projects", "浏览学生项目");
      link.setAttribute("aria-label", link.title);
      if (location.pathname === new URL(link.href).pathname) link.setAttribute("aria-current", "page");
      link.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 3h8v8H3V3m10 0h8v5h-8V3m0 7h8v11h-8V10M3 13h8v8H3v-8Z"/></svg>';
      var anchor = header.querySelector(".slides-link, .main-site-link");
      if (header.querySelector(".slides-link")) anchor = header.querySelector(".slides-link");
      if (anchor) anchor.after(link); else header.appendChild(link);
    }
    var library = document.querySelector("[data-projects]");
    if (!library) return;
    var grid = library.querySelector(".projects-grid");
    var status = library.querySelector(".projects-status");
    var dialog = element("dialog", "project-reader");
    dialog.setAttribute("aria-labelledby", "project-reader-title");
    var top = element("div", "project-reader__header");
    var title = element("h2"); title.id = "project-reader-title";
    var close = element("button", "", t("Close ×", "关闭 ×")); close.type = "button";
    top.append(title, close);
    var stage = element("div", "project-reader__stage");
    var slide = element("img", "project-reader__image"); slide.draggable = false;
    var error = element("p", "project-reader__error", t("This slide could not load. Please reopen the project to retry.", "此页加载失败，请重新打开项目重试。")); error.hidden = true;
    slide.addEventListener("error", function () { error.hidden = false; });
    slide.addEventListener("load", function () { error.hidden = true; });
    stage.append(slide, error);
    var controls = element("div", "project-reader__controls");
    var prev = element("button", "", t("← Previous", "← 上一页"));
    var next = element("button", "", t("Next →", "下一页 →"));
    prev.type = next.type = "button";
    var count = element("span", "project-reader__count"); count.setAttribute("aria-live", "polite");
    controls.append(prev, count, next); dialog.append(top, stage, controls); document.body.appendChild(dialog);
    var current, page = 0, opener;
    function show(index) {
      page = Math.max(0, Math.min(current.count - 1, index));
      error.hidden = true;
      slide.alt = current.title + " — " + t("Slide ", "第 ") + (page + 1) + (zh ? " 页" : "");
      slide.src = new URL("projects/previews/" + current.id + "/" + (page + 1) + ".webp", base).href;
      count.textContent = (page + 1) + " / " + current.count;
      prev.disabled = page === 0; next.disabled = page === current.count - 1;
    }
    close.addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("close", function () { slide.removeAttribute("src"); if (opener) opener.focus(); });
    prev.addEventListener("click", function () { show(page - 1); });
    next.addEventListener("click", function () { show(page + 1); });
    dialog.addEventListener("keydown", function (event) {
      if (event.key === "ArrowRight" || event.key === "ArrowLeft" || event.key === "Home" || event.key === "End") {
        event.preventDefault();
        show(event.key === "Home" ? 0 : event.key === "End" ? current.count - 1 : page + (event.key === "ArrowRight" ? 1 : -1));
      }
    });
    fetch(new URL("projects/manifest.json", base)).then(function (response) {
      if (!response.ok) throw new Error("Gallery unavailable"); return response.json();
    }).then(function (projects) {
      function render(cohort) {
        grid.replaceChildren();
        var filtered = projects.filter(function (p) { return cohort === "all" || p.cohort === cohort; });
        status.textContent = filtered.length + t(" projects", " 个项目");
        filtered.forEach(function (project) {
          var card = element("button", "project-card"); card.type = "button";
          var cover = element("img"); cover.src = new URL("projects/previews/" + project.id + "/cover.webp", base).href;
          cover.alt = ""; cover.loading = "lazy"; cover.draggable = false;
          var body = element("span", "project-card__body");
          body.append(element("span", "project-card__meta", project.cohort + " · " + project.count + t(" slides", " 页")), element("span", "project-card__title", project.title), element("span", "project-card__action", t("Preview project →", "浏览项目 →")));
          card.append(cover, body);
          card.addEventListener("click", function () { current = project; opener = card; title.textContent = project.title; show(0); dialog.showModal(); close.focus(); });
          grid.appendChild(card);
        });
      }
      library.querySelectorAll("[data-cohort]").forEach(function (button) {
        button.addEventListener("click", function () {
          library.querySelectorAll("[data-cohort]").forEach(function (b) { b.setAttribute("aria-pressed", String(b === button)); });
          render(button.dataset.cohort);
        });
      });
      render("all");
    }).catch(function () { status.textContent = t("Projects could not load. Please refresh to try again.", "项目加载失败，请刷新重试。"); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, {once: true}); else init();
})();
