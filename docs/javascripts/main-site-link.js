document.addEventListener("DOMContentLoaded", () => {
  const firstHeaderControl = document.querySelector(".md-header__option");

  if (!firstHeaderControl || document.querySelector(".main-site-link")) {
    return;
  }

  const destination = "https://www.maguoliang.com/";
  const reachabilityURL = "https://www.maguoliang.com/favicon.ico";
  const timeoutMilliseconds = 5000;

  // Create the header icon.
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

  // Create the message shown only after a failed connection check.
  const dialog = document.createElement("dialog");
  dialog.className = "main-site-dialog";

  dialog.innerHTML = `
    <div class="main-site-dialog__content">
      <h2>主站似乎暂时无法访问</h2>

      <p>
        页面若未能抵达，请稍后重试或换个网络；无需反复刷新到怀疑人生。
      </p>

      <p>
        Network conditions vary. The website, like a cat, may not come when called.
      </p>

      <div class="main-site-dialog__actions">
        <button type="button" class="md-button main-site-cancel">
          关闭 / Close
        </button>

        <a
          class="md-button md-button--primary"
          href="${destination}"
        >
          仍然尝试 / Try anyway
        </a>
      </div>
    </div>
  `;

  document.body.appendChild(dialog);

  // Quietly check whether the main site can be reached.
  async function canReachMainSite() {
    const controller = new AbortController();

    const timeout = window.setTimeout(() => {
      controller.abort();
    }, timeoutMilliseconds);

    try {
      await fetch(`${reachabilityURL}?check=${Date.now()}`, {
        mode: "no-cors",
        cache: "no-store",
        signal: controller.signal
      });

      return true;
    } catch {
      return false;
    } finally {
      window.clearTimeout(timeout);
    }
  }

  link.addEventListener("click", async (event) => {
    event.preventDefault();

    // Prevent repeated clicks while checking.
    if (link.classList.contains("main-site-link--checking")) {
      return;
    }

    link.classList.add("main-site-link--checking");
    link.setAttribute("aria-busy", "true");

    const reachable = await canReachMainSite();

    link.classList.remove("main-site-link--checking");
    link.removeAttribute("aria-busy");

    if (reachable) {
      // Reachable: navigate without showing any message.
      window.location.assign(destination);
    } else {
      // Unreachable or timed out: show the explanation.
      dialog.showModal();
    }
  });

  dialog
    .querySelector(".main-site-cancel")
    .addEventListener("click", () => {
      dialog.close();
    });

  // Close when the user clicks the dark backdrop.
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      dialog.close();
    }
  });
});