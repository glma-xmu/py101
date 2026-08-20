/*
 * Make the homepage language switcher work wherever the site is served from.
 *
 * Almost every link MkDocs emits is relative, so one build serves correctly from
 * any base path. The exception is the language switcher on the two HOMEPAGES
 * (`/` and `/zh/`), which the i18n plugin writes as ABSOLUTE paths derived from
 * `site_url` in mkdocs.yml — e.g. `/teaching/py101/` and `/teaching/py101/zh/`.
 * Inner pages are unaffected; their switcher links are already relative.
 *
 * That is fine on the canonical host and broken everywhere else: the same build
 * also goes to GitHub Pages (under /py101/) and to the Aliyun mirror (at the
 * domain root), where those absolute paths 404 — so a student clicking 中文 on
 * the front page lands on an error.
 *
 * This rewrites them at load time to point at wherever the page actually is.
 * The runtime base comes from this script's own URL, the same trick runnable.js
 * uses for its vendored assets. When the deployed base already matches
 * `site_url`, every rewrite is a no-op.
 *
 * This replaces the nginx `/py101/` alias that SERVER_DEPLOY.md used to need.
 */
(function () {
  "use strict";

  var self = document.currentScript;
  if (!self || !self.src) { return; }

  // ".../javascripts/lang-switch-fix.js?v=1" -> ".../"  (absolute path, no origin)
  var base = new URL(self.src, location.href).pathname
    .replace(/javascripts\/lang-switch-fix\.js.*$/, "");

  function run() {
    // The English alternate is always the site root as `site_url` declared it.
    var en = document.querySelector('link[rel="alternate"][hreflang="en"], ' +
                                    'a.md-select__link[hreflang="en"]');
    if (!en) { return; }

    var configured = en.getAttribute("href");
    if (!configured || configured.charAt(0) !== "/") { return; }  // already relative
    if (configured === base) { return; }                          // already correct

    var links = document.querySelectorAll(
      'link[rel="alternate"][hreflang], a.md-select__link[hreflang]'
    );
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute("href");
      if (href && href.indexOf(configured) === 0) {
        links[i].setAttribute("href", base + href.slice(configured.length));
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
