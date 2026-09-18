# Auto-deploy to the Aliyun mirror (GitHub Actions → server over SSH)

Every push to `main` builds the textbook and **rsyncs it to your server over SSH**.
GitHub connects to Aliyun; the server does not need to reach GitHub or run
`git pull`. GitHub Pages still deploys as before; the textbook mirror step is
best-effort and never blocks it. Quiz JSON has a separate, failure-visible
workflow after the one-time setup in section 5 below.

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

(`deploy` is unprivileged. Do not give this account sudo access. Besides its own
home, the intended deployment write locations are the static site folder and,
after section 5, the quiz-content directory; not backend code or configuration.)

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

## 5. Automatic quiz-content deployment (existing backend only)

If `/quiz/` already works and the `SERVER_*` secrets already exist, do not repeat
the key/account setup above. On **Aliyun**, run this once. `deploy` must match
your GitHub `SERVER_USER` secret; substitute the existing account if different:

```bash
sudo chown deploy /opt/py101-live/live_questions/quizzes
sudo chmod 755 /opt/py101-live/live_questions/quizzes
sudo -u deploy test -w /opt/py101-live/live_questions/quizzes && echo 'Quiz deployment ready'
```

This changes only the directory owner, not the owner of `/opt/py101-live`, Python
source, the service, or `/etc/py101-live.env`. The existing JSON files installed
with mode `644` can remain root-owned: deployment replaces changed files using
temporary files and rename. If you previously changed their permissions, restore
readable mode `644` on the affected JSON files. The service remains read-only.
Directory ownership permits the deployment account to manage any files in that
directory; the workflow restricts what it uploads to validated quiz JSON.

Then commit and push your local changes to `main`. GitHub Actions runs
**Deploy quizzes to Aliyun** whenever quiz contents or that workflow change.
It checks every quiz with the backend reader, then pushes only top-level JSON
files to `/opt/py101-live/live_questions/quizzes/`. It never restarts the backend,
changes Nginx, or uploads quizzes to the public static site. Refresh `/quiz/`
after the run succeeds; existing login sessions and quiz codes remain valid.
This first run uploads all committed quizzes, including ones previously missed.

The workflow reuses `SERVER_HOST`, `SERVER_USER`, `SERVER_SSH_KEY`, and optional
`SERVER_PORT` (default `22`). Optionally supply `SERVER_KNOWN_HOSTS` with a trusted
OpenSSH known-hosts entry for this host/port to pin the server's host key; without
it, the workflow obtains that key with `ssh-keyscan` at connection time, as the
existing textbook mirror does. No server-to-GitHub connection is needed.

Check **Actions → Deploy quizzes to Aliyun**, not just the textbook build. Missing
secrets, invalid quizzes, connection errors, or missing directory permissions
fail this separate workflow visibly. After fixing setup, use **Run workflow**
on `main`. Manual runs on other branches do not deploy; reruns validate and
publish the latest `main`, not the old run's contents. There is no automatic
retry schedule: a later quiz push or manual run retries the upload.

Old server quizzes are deliberately **not deleted**. Removing or renaming a JSON
file in Git does not withdraw its previous server copy; removal from Aliyun is a
separate explicit administrator action. Updates are atomic per file, not across
the whole library. A failed transfer may require rerunning the workflow.
All committed quizzes are available during an open quiz session; keep drafts
elsewhere. A public GitHub repository also makes committed JSON publicly readable.

Backend code updates still follow `live_questions/README.md` and may require a
restart outside class. Those instructions preserve this directory's owner.

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
