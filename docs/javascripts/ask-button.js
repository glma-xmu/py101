/*
 * Floating "Ask a question" button (anonymous, for in-class questions).
 *
 * It simply opens a question form you control (e.g. a 问卷星 / 腾讯问卷 form, or a
 * 腾讯文档) in a new tab. No backend needed — students post anonymously, you watch
 * the answers come in live during class.
 *
 * ----------------------------------------------------------------------------
 * TO TURN IT ON: paste your form's share link between the quotes below.
 * Leave it empty ("") and the button stays hidden.
 * ----------------------------------------------------------------------------
 */
(function () {
  "use strict";

  var ASK_URL = "https://v.wjx.cn/vm/OttnIWh.aspx#";   // <-- paste your 问卷星 / 腾讯问卷 / 腾讯文档 link here

  if (!ASK_URL) { return; }   // hidden until a link is set

  var lang = (document.documentElement.lang || "en").slice(0, 2);
  var label = lang === "zh" ? "提问" : "Ask";
  var tip = lang === "zh" ? "课堂提问（匿名）" : "Ask a question (anonymous)";

  function init() {
    var a = document.createElement("a");
    a.className = "ask-fab";
    a.href = ASK_URL;
    a.target = "_blank";
    a.rel = "noopener";
    a.title = tip;
    a.setAttribute("aria-label", tip);
    a.innerHTML = '<span class="ask-fab-ic">💬</span><span class="ask-fab-tx"></span>';
    a.querySelector(".ask-fab-tx").textContent = label;
    document.body.appendChild(a);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
