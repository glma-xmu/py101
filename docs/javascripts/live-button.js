/*
 * Course-help links shared by all course-site copies.
 * Absolute URLs keep students on the same classroom and assistant services,
 * including when this course is served below /teaching/py101/ or /py101/.
 * Bump this script's ?v= in mkdocs.yml after changing it.
 * An empty URL hides that entrance if its service is withdrawn.
 */
(function () {
  "use strict";
  var LIVE_URL = "https://maguoliang.cn/live/";
  var ASSISTANT_URL = "https://intelligent-space.zhihuishu.com/knowledgeAssistant/index?mapUid=1897936323847786496&scMapUid=2097636092191674368";

  function createLink(className, url, label, title) {
    if (!url || document.querySelector("." + className)) return;
    try {
      if (new URL(url).protocol !== "https:") return;
    } catch (_) {
      return;
    }
    var link = document.createElement("a");
    link.className = className;
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = label;
    link.title = title;
    link.setAttribute("aria-label", link.textContent + " — " + link.title);
    return link;
  }

  function init() {
    var chinese = (document.documentElement.lang || "en").startsWith("zh");
    var live = createLink("live-fab", LIVE_URL,
      chinese ? "实时提问" : "Live questions",
      chinese ? "加入教师开启的课堂" : "Join a classroom opened by your teacher");
    if (live) document.body.appendChild(live);

    var languageMenu = document.querySelector(".md-header__option .md-select");
    if (!languageMenu) return;
    var languageControl = languageMenu.closest(".md-header__option");
    var assistant = createLink("course-assistant-link", ASSISTANT_URL,
      chinese ? "AI 助教" : "AI assistant",
      chinese ? "打开智慧树课程助教（新标签页）" : "Open the course assistant on Zhihuishu (new tab)");
    if (!assistant) return;
    assistant.classList.add("md-header__button", "md-icon");
    assistant.textContent = "";
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("focusable", "false");
    var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", "M20 2H4a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2M7 11a1 1 0 1 1 0-2 1 1 0 0 1 0 2m5 0a1 1 0 1 1 0-2 1 1 0 0 1 0 2m5 0a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z");
    svg.appendChild(path);
    assistant.appendChild(svg);
    languageControl.after(assistant);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
