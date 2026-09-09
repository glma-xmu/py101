/* Local controls for the course's standalone Reveal slide decks. */
(function () {
  "use strict";

  var reveal = window.Reveal;
  var toolbar = document.querySelector(".slide-toolbar");
  var overviewButton = document.getElementById("slides-overview");
  var fullscreenButton = document.getElementById("slides-fullscreen");
  var readingButton = document.getElementById("slides-reading");
  var textbookLink = document.getElementById("slides-textbook");
  var outline = document.querySelector(".slide-outline");
  var contentsButton = document.getElementById("slides-contents");
  var outlineLinks = Array.prototype.slice.call(document.querySelectorAll("#slides-outline a[data-start]"));
  var slides = Array.prototype.slice.call(document.querySelectorAll(".reveal .slides > section"));
  // The deck content remains English; only navigation follows this explicit locale.
  var chinese = new URLSearchParams(window.location.search).get("lang") === "zh";
  var reading = false;
  var ready = false;
  var currentIndex = 0;
  var lastManagedHash = window.location.hash;
  var scrollFrame = null;
  var toolbarHeight = 0;
  var statusTimer = null;
  var originalAttributes = new Map();
  var manualCopy = null;
  var t = function (english, zh) { return chinese ? zh : english; };

  function hashIndex() {
    var id;
    try { id = decodeURIComponent(window.location.hash.replace(/^#\/?/, "")); }
    catch (_) { return -1; }
    var direct = slides.findIndex(function (slide) { return slide.id === id; });
    if (direct !== -1) return direct;
    // Old slide-number bookmarks remain valid when a topic receives a stable ID.
    var legacy = /^slide-(\d+)$/.exec(id);
    if (!legacy) return -1;
    return slides.findIndex(function (slide, index) {
      return Number(slide.getAttribute("data-slide-number") || index + 1) === Number(legacy[1]);
    });
  }

  function setBookmark(index, push) {
    if (!slides[index] || !slides[index].id) return;
    var hash = "#/" + encodeURIComponent(slides[index].id);
    if (window.location.hash !== hash) {
      window.history[push ? "pushState" : "replaceState"](window.history.state, "", hash);
    }
    lastManagedHash = hash;
  }

  function updateTopic(index) {
    if (!slides[index]) return;
    currentIndex = index;
    var slide = slides[index];
    var title = slide.getAttribute("data-topic-title") || "";
    var related = slide.getAttribute("data-textbook-related") === "true";
    if (textbookLink) {
      var href = slide.getAttribute(chinese ? "data-textbook-zh" : "data-textbook-en");
      textbookLink.setAttribute("href", href || (chinese ? "../../../zh/" : "../../../"));
      textbookLink.textContent = t("Text", "正文");
      textbookLink.title = (related ? t("Related textbook reading", "教材延伸阅读") : t("Read this topic in the textbook", "在教材中阅读本节")) + (title ? ": " + title : "");
      textbookLink.setAttribute("aria-label", textbookLink.textContent + (title ? ": " + title : ""));
    }
    var active = null;
    outlineLinks.forEach(function (link) {
      if (Number(link.getAttribute("data-start")) <= index + 1) active = link;
    });
    outlineLinks.forEach(function (link) {
      if (link === active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  }

  function syncToolbarHeight() {
    if (!toolbar) return;
    var height = Math.ceil(toolbar.getBoundingClientRect().height);
    if (!height || height === toolbarHeight) return;
    toolbarHeight = height;
    document.documentElement.style.setProperty("--slide-toolbar-height", height + "px");
    if (ready && !reading) reveal.layout();
  }

  var backLink = document.querySelector(".slides-back");
  if (backLink) {
    backLink.setAttribute("href", chinese ? "../../../zh/slides/" : "../../");
    backLink.textContent = t("Slides", "课件");
  }
  if (contentsButton) contentsButton.textContent = t("Contents", "目录");
  if (overviewButton) overviewButton.textContent = t("Overview", "概览");
  if (readingButton) readingButton.textContent = t("Reading view", "阅读视图");
  if (outline) {
    var outlineNav = outline.querySelector("nav");
    if (outlineNav) outlineNav.setAttribute("aria-label", t("Slide sections", "幻灯片章节"));
  }
  var initialIndex = hashIndex();
  if (initialIndex !== -1) {
    currentIndex = initialIndex;
    setBookmark(initialIndex, false);
  }
  updateTopic(currentIndex);

  var status = document.createElement("p");
  status.className = "slides-status";
  status.setAttribute("role", "status");
  status.setAttribute("aria-live", "polite");
  document.body.appendChild(status);

  function announce(message) {
    window.clearTimeout(statusTimer);
    status.textContent = message;
    statusTimer = window.setTimeout(function () { status.textContent = ""; }, 4500);
  }

  function eligibleKeyboard(event) {
    if (reading || event.defaultPrevented || event.ctrlKey || event.metaKey || event.altKey) return false;
    var target = event.target;
    if (outline && outline.open) return false;
    if (target && target.closest && target.closest("button, a, input, textarea, select, summary, details, [contenteditable], .slide-toolbar, .slides-copy-fallback")) return false;
    var selection = window.getSelection();
    return !selection || !selection.toString().trim();
  }

  function copySource(code) {
    if (code.hasAttribute("data-copy-source")) return code.getAttribute("data-copy-source");
    var clone = code.cloneNode(true);
    clone.querySelectorAll("[data-copy-ignore], .code-error-marker, .error-marker, .code-annotation, .copy-ignore").forEach(function (marker) {
      marker.remove();
    });
    // Keep normal Python comments, including intentional-error explanations.
    return clone.textContent.replace(/^\n/, "").replace(/\n$/, "");
  }

  function showManualCopy(text, trigger) {
    if (manualCopy) manualCopy.remove();
    var panel = document.createElement("div");
    panel.className = "slides-copy-fallback";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", t("Copy code", "复制代码"));
    var label = document.createElement("label");
    label.htmlFor = "slides-manual-copy";
    label.textContent = t("Select the code and press Ctrl+C or Cmd+C.", "请选择代码，然后按 Ctrl+C 或 Cmd+C。");
    var area = document.createElement("textarea");
    area.id = "slides-manual-copy";
    area.readOnly = true;
    area.value = text;
    var close = document.createElement("button");
    close.type = "button";
    close.textContent = t("Close", "关闭");
    function dismiss() {
      panel.remove();
      manualCopy = null;
      trigger.focus();
    }
    close.addEventListener("click", dismiss);
    panel.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        event.preventDefault();
        event.stopPropagation();
        dismiss();
      }
    });
    panel.append(label, area, close);
    document.body.appendChild(panel);
    manualCopy = panel;
    area.focus();
    area.select();
  }

  async function copyCode(code, button) {
    var text = copySource(code);
    var copied = false;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        await navigator.clipboard.writeText(text);
        copied = true;
      } catch (_) { /* Try the legacy selection-based copy below. */ }
    }
    if (!copied) {
      var area = document.createElement("textarea");
      area.className = "slides-clipboard-buffer";
      area.value = text;
      area.setAttribute("aria-hidden", "true");
      area.tabIndex = -1;
      document.body.appendChild(area);
      area.select();
      try { copied = Boolean(document.execCommand("copy")); } catch (_) { copied = false; }
      area.remove();
      button.focus();
    }
    if (copied) {
      announce(t("Code copied.", "代码已复制。"));
      button.textContent = t("Copied", "已复制");
      window.setTimeout(function () { button.textContent = t("Copy", "复制"); }, 1800);
    } else {
      showManualCopy(text, button);
    }
  }

  document.querySelectorAll(".reveal pre > code").forEach(function (code, index) {
    var pre = code.parentElement;
    if (pre.querySelector(".slide-copy") || pre.classList.contains("no-copy")) return;
    var button = document.createElement("button");
    button.type = "button";
    button.className = "slide-copy";
    button.textContent = t("Copy", "复制");
    button.setAttribute("aria-label", t("Copy code example ", "复制代码示例 ") + (index + 1));
    button.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      copyCode(code, button);
    });
    pre.appendChild(button);
  });

  function nearestReadingSlide() {
    var reference = (toolbar ? toolbar.getBoundingClientRect().height : 48) + 20;
    for (var i = 0; i < slides.length; i++) {
      if (slides[i].getBoundingClientRect().bottom > reference) return i;
    }
    return Math.max(0, slides.length - 1);
  }

  function goToSlide(index, push) {
    if (!slides[index]) return;
    setBookmark(index, push);
    updateTopic(index);
    if (reading) slides[index].scrollIntoView({ block: "start" });
    else if (ready) reveal.slide(index);
  }

  outlineLinks.forEach(function (link) {
    link.addEventListener("click", function (event) {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
      event.preventDefault();
      event.stopPropagation();
      if (outline) outline.open = false;
      goToSlide(Number(link.getAttribute("data-start")) - 1, true);
      if (contentsButton) contentsButton.focus({ preventScroll: true });
    });
  });
  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape" || !outline || !outline.open) return;
    event.preventDefault();
    event.stopPropagation();
    outline.open = false;
    if (contentsButton) contentsButton.focus({ preventScroll: true });
  }, true);

  window.addEventListener("hashchange", function () {
    var index = hashIndex();
    if (index !== -1) goToSlide(index, false);
    else lastManagedHash = window.location.hash;
  });
  window.addEventListener("scroll", function () {
    if (!reading || scrollFrame !== null) return;
    scrollFrame = window.requestAnimationFrame(function () {
      scrollFrame = null;
      if (!reading) return;
      // A pending scroll must not overwrite a just-requested bookmark or Back action.
      if (window.location.hash !== lastManagedHash) return;
      var index = nearestReadingSlide();
      updateTopic(index);
      setBookmark(index, false);
    });
  }, { passive: true });

  function setReading(enabled) {
    if (reading === enabled) return;
    var index = reading ? nearestReadingSlide() : (ready ? reveal.getIndices().h : currentIndex);
    reading = enabled;
    if (ready && reveal.isOverview()) reveal.toggleOverview(false);
    document.documentElement.classList.toggle("slides-reading", reading);
    document.body.classList.toggle("slides-reading", reading);
    if (readingButton) {
      readingButton.setAttribute("aria-pressed", String(reading));
      readingButton.textContent = reading ? t("Slideshow", "幻灯片") : t("Reading view", "阅读视图");
      readingButton.title = reading ? t("Return to the slide presentation", "返回幻灯片演示") : t("Read all slides as a scrolling page", "以滚动页面阅读所有幻灯片");
    }
    if (overviewButton) overviewButton.disabled = reading || !ready;
    updateTopic(index);
    syncToolbarHeight();

    if (reading) {
      if (ready) reveal.configure({ keyboard: false, touch: false, controls: false, progress: false, slideNumber: false, hash: false });
      slides.forEach(function (slide) {
        originalAttributes.set(slide, {
          hidden: slide.getAttribute("hidden"),
          ariaHidden: slide.getAttribute("aria-hidden"),
          inert: slide.getAttribute("inert")
        });
        slide.removeAttribute("hidden");
        slide.removeAttribute("aria-hidden");
        slide.removeAttribute("inert");
      });
      window.requestAnimationFrame(function () {
        if (reading && slides[index]) {
          slides[index].scrollIntoView({ block: "start" });
          setBookmark(index, false);
        }
      });
    } else {
      slides.forEach(function (slide) {
        var previous = originalAttributes.get(slide);
        if (!previous) return;
        [["hidden", previous.hidden], ["aria-hidden", previous.ariaHidden], ["inert", previous.inert]].forEach(function (entry) {
          if (entry[1] === null) slide.removeAttribute(entry[0]);
          else slide.setAttribute(entry[0], entry[1]);
        });
      });
      originalAttributes.clear();
      window.scrollTo(0, 0);
      if (ready) {
        reveal.configure({ keyboard: true, touch: true, controls: true, progress: true, slideNumber: "c/t", hash: true });
        reveal.sync();
        reveal.layout();
        reveal.slide(index);
      }
    }
  }

  if (!readingButton && toolbar) {
    readingButton = document.createElement("button");
    readingButton.id = "slides-reading";
    readingButton.type = "button";
    readingButton.textContent = t("Reading view", "阅读视图");
    toolbar.appendChild(readingButton);
  }
  if (readingButton) {
    readingButton.setAttribute("aria-pressed", "false");
    readingButton.addEventListener("click", function () { setReading(!reading); });
  }
  if (overviewButton) {
    overviewButton.setAttribute("aria-pressed", "false");
    overviewButton.addEventListener("click", function () {
      if (ready && !reading) reveal.toggleOverview();
    });
  }

  function fullscreenSupported() {
    return Boolean(document.fullscreenEnabled && document.documentElement.requestFullscreen);
  }
  function updateFullscreen() {
    if (!fullscreenButton) return;
    fullscreenButton.hidden = !fullscreenSupported();
    fullscreenButton.textContent = document.fullscreenElement ? t("Exit full screen", "退出全屏") : t("Full screen", "全屏");
    fullscreenButton.setAttribute("aria-pressed", String(Boolean(document.fullscreenElement)));
  }
  if (fullscreenButton) {
    updateFullscreen();
    fullscreenButton.addEventListener("click", async function () {
      try {
        if (document.fullscreenElement) await document.exitFullscreen();
        else await document.documentElement.requestFullscreen();
      } catch (_) {
        announce(t("Full screen is unavailable in this window. Try opening the slides in your browser.", "此窗口不支持全屏，请尝试在浏览器中打开课件。"));
      }
      updateFullscreen();
    });
    document.addEventListener("fullscreenchange", updateFullscreen);
  }

  syncToolbarHeight();
  if (window.ResizeObserver && toolbar) {
    new ResizeObserver(syncToolbarHeight).observe(toolbar);
  } else {
    window.addEventListener("resize", syncToolbarHeight);
  }

  if (!reveal || typeof reveal.initialize !== "function") {
    setReading(true);
    announce(t("The presentation controls did not load. All slides are available in reading view.", "演示控件未加载；所有幻灯片仍可在阅读视图中查看。"));
    return;
  }

  reveal.initialize({
    width: 1280,
    height: 720,
    margin: 0.055,
    center: false,
    transition: "none",
    backgroundTransition: "none",
    hash: true,
    slideNumber: "c/t",
    controls: true,
    progress: true,
    keyboard: true,
    keyboardCondition: eligibleKeyboard,
    embedded: false,
    scrollActivationWidth: null,
    help: true,
    touch: true
  }).then(function () {
    ready = true;
    updateTopic(reveal.getIndices().h);
    syncToolbarHeight();
    reveal.on("slidechanged", function () {
      if (!reading) updateTopic(reveal.getIndices().h);
    });
    if (overviewButton) overviewButton.disabled = false;
    reveal.on("overviewshown", function () {
      if (overviewButton) overviewButton.setAttribute("aria-pressed", "true");
    });
    reveal.on("overviewhidden", function () {
      if (overviewButton) overviewButton.setAttribute("aria-pressed", "false");
    });
    // A side panel benefits from readable, unscaled content immediately.
    if (window.matchMedia("(max-width: 760px)").matches || reading) {
      if (reading) reading = false;
      setReading(true);
    }
  }).catch(function () {
    setReading(true);
    announce(t("Presentation mode is unavailable. The slides remain readable below.", "演示模式暂不可用，仍可在下方阅读课件。"));
  });
})();
