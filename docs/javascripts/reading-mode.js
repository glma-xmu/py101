/*
 * Reading mode: a single toggle that folds/unfolds every collapsible block on
 * the page, so a student can hide Examples, exercises, notes, etc. and read the
 * prose straight through — then unfold to dig in.
 */
(function () {
  "use strict";
  function init() {
    var article = document.querySelector(".md-content article") || document.querySelector("article");
    if (!article || !article.querySelector("details")) { return; }
    var zh = (document.documentElement.lang || "en").slice(0, 2) === "zh";
    var L = zh ? { fold: "折叠所有区块", unfold: "展开所有区块" }
               : { fold: "Fold all blocks", unfold: "Unfold all blocks" };

    var bar = document.createElement("div");
    bar.className = "reading-toggle";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "md-button reading-toggle-btn";
    btn.textContent = L.fold;
    var folded = false;
    btn.addEventListener("click", function () {
      folded = !folded;
      article.querySelectorAll("details").forEach(function (d) { d.open = !folded; });
      btn.textContent = folded ? L.unfold : L.fold;
    });
    bar.appendChild(btn);

    var h1 = article.querySelector("h1");
    if (h1 && h1.nextSibling) { article.insertBefore(bar, h1.nextSibling); }
    else { article.insertBefore(bar, article.firstChild); }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
