document.addEventListener("DOMContentLoaded", () => {
  const firstHeaderControl = document.querySelector(".md-header__option");

  if (!firstHeaderControl || document.querySelector(".main-site-link")) {
    return;
  }

  const destination = "https://www.maguoliang.com/";

  // Header icon
  const link = document.createElement("a");
  link.className = "md-header__button md-icon main-site-link";
  link.href = destination;
  link.title = "Visit main site";
  link.setAttribute("aria-label", "Visit main site");

  link.innerHTML = `
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"></path>
    </svg>
  `;

  firstHeaderControl.before(link);

  // Confirmation dialog
  const dialog = document.createElement("dialog");
  dialog.className = "main-site-dialog";

  dialog.innerHTML = `
    <div class="main-site-dialog__content">
      <h2>前往主站 / Visit main site</h2>

      <p>
        页面若未能抵达，请稍后重试或换个网络；无需反复刷新到怀疑人生。
      </p>

      <p>
        Network conditions vary. The website, like a cat, may not come when called.
      </p>

      <div class="main-site-dialog__actions">
        <button type="button" class="md-button main-site-cancel">
          取消 / Cancel
        </button>

        <a class="md-button md-button--primary" href="${destination}">
          继续访问 / Continue
        </a>
      </div>
    </div>
  `;

  document.body.appendChild(dialog);

  link.addEventListener("click", (event) => {
    event.preventDefault();
    dialog.showModal();
  });

  dialog
    .querySelector(".main-site-cancel")
    .addEventListener("click", () => dialog.close());

  // Clicking the dark backdrop closes the dialog.
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      dialog.close();
    }
  });
});