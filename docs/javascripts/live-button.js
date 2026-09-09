/*
 * Optional live classroom entrance. Keep the Wenjuanxing Ask button unchanged.
 * After deploying and testing live_questions/, set LIVE_URL below to
 * "https://maguoliang.cn/live/" and bump this script's ?v= in mkdocs.yml.
 * An empty URL keeps the pilot hidden until the service is ready.
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
    document.body.appendChild(link);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
