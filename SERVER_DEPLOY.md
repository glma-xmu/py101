# Deploying the site on the Aliyun 轻量 (Ubuntu) server

The site is static (a plain `site/` folder built by MkDocs), so hosting is just
"build it and let nginx serve it." GitHub Pages stays as your source of truth and
backup; this server is the fast, in-China mirror.

Assumptions: Ubuntu 24.04, a fixed public IP, domain `maguoliang.cn`, repo
`https://github.com/glma-xmu/py101`.

---

## Part A — server prep (can be done any time, before 备案)

SSH in as root (or a sudo user), then:

```bash
# 1) a little swap (the box has only 0.5 GiB RAM — this makes builds safe)
fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# 2) packages
apt update && apt install -y nginx git python3-venv

# 3) get the site and build it
git clone https://github.com/glma-xmu/py101.git /opt/py101
cd /opt/py101
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdocs build            # -> /opt/py101/site
```

nginx site config — `/etc/nginx/sites-available/py101`:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name maguoliang.cn www.maguoliang.cn;

    root /opt/py101/site;
    index index.html;

    # gzip the text assets (speeds up page loads a lot)
    gzip on;
    gzip_types text/plain text/css application/javascript application/json image/svg+xml;

    # Also answer under /py101/ — see "Why the /py101/ alias" below.
    location = /py101 { return 301 /py101/; }
    location /py101/ { rewrite ^/py101/(.*)$ /$1 last; }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Why the `/py101/` alias

The site is built once, with `site_url: https://glma-xmu.github.io/py101/`. Almost
every link MkDocs emits is *relative*, which is why one build can serve correctly
both from GitHub Pages (under `/py101/`) and from this server (at the domain root).

The exception is the **language switcher on the homepage**, which the i18n plugin
writes as absolute paths derived from `site_url` — `/py101/` and `/py101/zh/`.
Served at the domain root those 404, so a student clicking **中文** on the front
page lands on an error. (Inner pages are unaffected: their switcher links are
relative and work fine.)

The two `location` blocks above fix that by making the same tree answer under
`/py101/` as well. The `rewrite … last` strips the prefix and re-runs location
matching, so the file is served from `root` — this avoids the `alias` + `try_files`
interaction, which is easy to get subtly wrong. Query strings are preserved
automatically, so cache-busted assets like `extra.css?v=2` still resolve.

Verify after reloading nginx — all three must return `200`:

```bash
curl -I http://127.0.0.1/            # the normal root
curl -I http://127.0.0.1/py101/      # English, via the alias
curl -I http://127.0.0.1/py101/zh/   # 中文, via the alias
```

> **Note:** this makes the alias resolve; it does **not** change the
> `<link rel="canonical">` tags, which still point at `glma-xmu.github.io`. If you
> later want `maguoliang.cn` to be the address search engines index, build the
> mirror with its own `site_url` (a two-line `mkdocs.mirror.yml` using `INHERIT:`)
> rather than extending this nginx config.

Enable it:

```bash
ln -s /etc/nginx/sites-available/py101 /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
```

Firewall (open SSH + web):

```bash
ufw allow OpenSSH && ufw allow 'Nginx Full' && ufw --force enable
```

> **`.wasm` note:** Pyodide loads a `.wasm` file. Ubuntu 24.04's nginx already
> maps `application/wasm` in `/etc/nginx/mime.types`, so streaming compile works.
> If a browser console ever complains about the wasm MIME type, add
> `application/wasm wasm;` to `/etc/nginx/mime.types` and reload.

At this point the site is served on the server's **public IP** — but on a mainland
box, port 80 for the **domain** stays blocked until 备案 is approved, so test with
the IP or from the server itself (`curl -I http://127.0.0.1`).

---

## Part B — go live on the domain (after 备案 is approved)

1. **DNS:** in Aliyun DNS for `maguoliang.cn`, add an **A record** `@` → your
   server's public IP, and another for `www`. Wait a few minutes for it to resolve.

2. **HTTPS** (free, auto-renewing):

   ```bash
   apt install -y certbot python3-certbot-nginx
   certbot --nginx -d maguoliang.cn -d www.maguoliang.cn
   ```

   certbot edits the nginx config, installs the certificate, and sets up renewal.
   Your site is now live at `https://maguoliang.cn`.

---

## Updating the site

Whenever you push changes to GitHub, refresh the mirror:

```bash
cd /opt/py101 && git pull && . .venv/bin/activate && mkdocs build
```

Optionally automate it with cron (e.g. every 10 min):

```bash
*/10 * * * * cd /opt/py101 && git pull -q && /opt/py101/.venv/bin/mkdocs build -q
```

---

## Notes

- **This mirror hosts only the public course site** — no student data — so a
  mainland server raises no data-residency issue.
- Keep the box patched: `apt update && apt upgrade -y` now and then.
- If you later add the forum, you'd install Node + a database here (and likely add
  RAM); ping me and I'll provide that recipe.
