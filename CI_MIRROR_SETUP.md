# Auto-deploy to the Aliyun mirror (GitHub Actions → server over SSH)

Every `git push` builds the site and **rsyncs it to your server over SSH**. The
server never contacts GitHub (which the GFW blocks from the mainland), so this
sidesteps that problem completely. GitHub Pages still deploys as before; the mirror
step is best-effort and never blocks it.

Do this once. Three parts: make a key, trust it on the server, add three secrets.

---

## 1. Make a deploy key (on your laptop, in Git Bash)

```bash
ssh-keygen -t ed25519 -C "py101-ci-deploy" -f py101_deploy -N ""
```

This creates two files: `py101_deploy` (private) and `py101_deploy.pub` (public).
Keep the private one secret.

---

## 2. On the server: a locked-down deploy user that trusts the key

SSH into the server as root, then:

```bash
apt-get install -y rsync                       # CI uses rsync
adduser --disabled-password --gecos "" deploy  # unprivileged deploy user
install -d -m 700 -o deploy -g deploy /home/deploy/.ssh

# paste the CONTENTS of py101_deploy.pub inside the quotes below:
echo 'ssh-ed25519 AAAA...your-public-key... py101-ci-deploy' \
  | tee /home/deploy/.ssh/authorized_keys
chown deploy:deploy /home/deploy/.ssh/authorized_keys
chmod 600 /home/deploy/.ssh/authorized_keys

# let 'deploy' own the folder nginx serves
chown -R deploy:deploy /opt/py101/site
```

(`deploy` is unprivileged and can only write the site folder — so even if the key
leaked, it couldn't touch the rest of the server.)

---

## 3. Add the secrets on GitHub

Repo → **Settings → Secrets and variables → Actions → New repository secret**. Add:

| Name | Value |
|------|-------|
| `SERVER_HOST` | your server's public IP |
| `SERVER_USER` | `deploy` |
| `SERVER_SSH_KEY` | the **entire** contents of the **private** key file `py101_deploy`, including the `-----BEGIN…` and `-----END…` lines |
| `SERVER_PORT` | `22` — only add this if you changed the SSH port |

---

## 4. Push, and watch it work

```bash
git add .
git commit -m "Add CI auto-deploy to the Aliyun mirror"
git push
```

Open the repo's **Actions** tab → the run → the **build** job. The
**"Mirror to the Aliyun server"** step should connect and rsync the site. From now
on, **one push updates both GitHub Pages and your server** — you never pull on the
server again.

---

## Notes

- The mirror step is `continue-on-error`, so if the server is ever down or
  unreachable, GitHub Pages still publishes normally.
- `rsync --delete` keeps the server's `site/` an exact match of the build (stale
  files are removed).
- Because CI now owns updating `/opt/py101/site`, you don't build on the server
  anymore. The git clone there can stay (harmless) or be removed.
- Test a change end-to-end: edit any page, push, and after ~2 min it should appear
  on both `github.io` and (once 备案 clears + DNS points at the box) your domain.
