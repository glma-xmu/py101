/*
 * Live classroom entrance shared by all course-site copies.
 * The absolute URL keeps students on the same Aliyun classroom service,
 * including when this course is served below /teaching/py101/ or /py101/.
 * Bump this script's ?v= in mkdocs.yml after changing it.
 * An empty URL hides the entrance if the service is withdrawn.
 */
(function () {
  "use strict";
  var LIVE_URL = "https://maguoliang.cn/live/";

  if (!LIVE_URL) return;
  try {
    if (new URL(LIVE_URL).protocol !== "https:") return;
  } catch (_) {
    return;
  }

  function init() {
    if (document.querySelector(".live-fab")) return;
    var chinese = (document.documentElement.lang || "en").startsWith("zh");
    var link = document.createElement("a");
    link.className = "live-fab";
    link.href = LIVE_URL;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = chinese ? "实时提问" : "Live questions";
    link.title = chinese ? "加入教师开启的课堂" : "Join a classroom opened by your teacher";
    link.setAttribute("aria-label", link.textContent + " — " + link.title);
    document.body.appendChild(link);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
