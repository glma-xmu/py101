document.addEventListener("DOMContentLoaded", () => {
  const firstHeaderControl = document.querySelector(".md-header__option");

  if (!firstHeaderControl || document.querySelector(".main-site-link")) {
    return;
  }

  const link = document.createElement("a");
  link.className = "md-header__button md-icon main-site-link";
  link.href = "https://www.maguoliang.com/";
  link.title = "Visit main site";
  link.setAttribute("aria-label", "Visit main site");

  link.innerHTML = `
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"></path>
    </svg>
  `;

  firstHeaderControl.before(link);
});