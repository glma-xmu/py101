document.addEventListener("DOMContentLoaded", () => {
  const firstHeaderControl = document.querySelector(".md-header__option");

  if (!firstHeaderControl || document.querySelector(".main-site-link")) {
    return;
  }

  const link = document.createElement("a");
  link.className = "main-site-link";
  link.href = "https://www.maguoliang.com/";
  link.textContent = "Main site";
  link.title = "Visit maguoliang.com";

  firstHeaderControl.before(link);
});