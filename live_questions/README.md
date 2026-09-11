# Live classroom questions

This is a live-question service beside the existing static MkDocs course site. The old Wenjuanxing entrance has been retired after the classroom acceptance check. Students submit at `https://maguoliang.cn/live/`; the teacher signs in at `https://maguoliang.cn/teacher/`. A small FastAPI service checks permissions and sends questions to the teacher using server-sent events (SSE). There is no database.

## Scope and operating limits

Teachers start quiz access from `/teacher/` using their existing login. The
unlisted student page `/quiz/` accepts one temporary code for the full library,
including every quiz JSON file currently in `quizzes/`.
See [quiz editing and deployment](quizzes/README.md) for the content format and
the additional Nginx routes. It does not require starting a live-question room.

- One teacher and one classroom, intended initially for a 50–200-student pilot. This is a planning scope, not a load guarantee for an unmeasured server.
- Classrooms expire after two hours. The service keeps at most 100 recent questions in memory and expires each after ten minutes; background cleanup runs every five seconds. Restarting the service loses questions, login sessions, and the active classroom.
- A successful submission means the service accepted the question, not that the teacher has read it. The teacher's connection indicator helps identify interruptions.
- Question text is displayed as text, never HTML or executable code. Access checks, message limits, and rate limits are enforced by the service. They do not guarantee that anonymously submitted wording is appropriate.
- Keep the teacher's question view private. If you project that browser window, incoming questions become visible to the room. A separate moderated projector display is outside this pilot.
- The application does not write question bodies to files, a database, browser storage, or access logs. Questions necessarily exist in network and browser memory. This is not a guarantee of forensic erasure: operating-system swap, crash capture, proxy/WAF body logging, or third-party monitoring require separate administrator settings. Do not attach request-body logging or session-replay analytics to these routes.

Run exactly **one worker and one service instance**. The room and event stream share in-process memory; extra workers or replicas would split that state. The existing static deployment does not start or update this service.

## Try locally on Windows

From the repository root, create a separate environment:

```powershell
py -m venv .venv-live
.\.venv-live\Scripts\Activate.ps1
python -m pip install -r live_questions/requirements.txt
```

Set an interactive test password. There is no minimum length or password-specific maximum; the password must not be empty. Use a strong password on the public server. The generic 4 KiB request-body limit still applies. The helper prompts without echoing the password and prints a password-hash environment line; the command below assigns only the hash to the current shell:

```powershell
$livePasswordLine = python -m live_questions.password
$env:LIVE_PASSWORD_HASH = $livePasswordLine -replace '^LIVE_PASSWORD_HASH=', ''
$env:LIVE_ORIGIN = 'http://127.0.0.1:8765'
$env:LIVE_DEV = '1'
python -m uvicorn live_questions.app:create_app --factory --host 127.0.0.1 --port 8765 --workers 1 --no-access-log
```

Open `http://127.0.0.1:8765/teacher/`, log in, and start a classroom. Open `http://127.0.0.1:8765/live/` in another browser or private window, enter the classroom code, and submit a question. Development mode disables the cookie's HTTPS-only flag; never use `LIVE_DEV=1` for the public installation.

### If local teacher sign-in is rejected

An address/configuration error (`403`, previously shown as “This action is not permitted”) is not an incorrect-password result (`401`). `LIVE_ORIGIN` must match the browser's scheme, hostname, and port exactly: `localhost` and `127.0.0.1` are different origins. For this local test, stop Uvicorn with **Ctrl+C**, then run these commands in the same PowerShell window:

```powershell
$env:LIVE_ORIGIN = 'http://127.0.0.1:8765'
$env:LIVE_DEV = '1'
python -m uvicorn live_questions.app:create_app --factory --host 127.0.0.1 --port 8765 --workers 1 --no-access-log
```

Reopen `http://127.0.0.1:8765/teacher/`. Use the original password you typed, not the generated hash. If you want to change the password, run the two password-generation/assignment commands above before restarting. Environment settings are read when the service starts; changing them in another terminal does not update an already running service. A new PowerShell window also needs the virtual environment and password hash set again.

Run the backend regression tests in this environment from the repository root:

```powershell
python -m pip install -r live_questions/requirements-dev.txt
python -m pytest live_questions/tests -q
```

## Install on the existing Aliyun Ubuntu server

These are manual operator steps; adding the files to Git does not deploy the service. Complete and verify HTTPS for `maguoliang.cn` before enabling public teacher login. Use your existing sudo account and working SSH authentication.

### 1. Upload the source

From Windows PowerShell in the repository root, replace the username and IP placeholders:

```powershell
ssh YOUR_SUDO_USER@YOUR_SERVER_IP "mkdir -p ~/py101-live-upload"
scp -r .\live_questions YOUR_SUDO_USER@YOUR_SERVER_IP:py101-live-upload/
```

This uploads only the service directory into the administrator's home. It does not require a GitHub private key on the server. For a nonstandard SSH port, supply `-p PORT` to `ssh` and `-P PORT` to `scp`.

### 2. Install a dedicated service account and environment

On Ubuntu:

```bash
sudo apt update
sudo apt install -y python3-venv rsync
sudo adduser --system --group --no-create-home --home /nonexistent py101-live
sudo install -d -m 755 /opt/py101-live/live_questions
sudo rsync -a --chmod=D755,F644 --exclude='__pycache__/' --exclude='*.pyc' ~/py101-live-upload/live_questions/ /opt/py101-live/live_questions/
sudo python3 -m venv /opt/py101-live/.venv
sudo /opt/py101-live/.venv/bin/python -m pip install -r /opt/py101-live/live_questions/requirements.txt
sudo chown -R root:root /opt/py101-live
sudo chmod -R u=rwX,go=rX /opt/py101-live
```

Account creation is an initial-install step; skip it if `py101-live` already exists. Keep `/opt/py101-live` outside `/opt/py101/site`: the static site's existing `rsync --delete` must never touch this service. The service account may read the source, but cannot change it.

### 3. Configure the teacher password and public origin

Generate the hash interactively:

```bash
cd /opt/py101-live
sudo .venv/bin/python -m live_questions.password
```

Copy the resulting `LIVE_PASSWORD_HASH=...` line. The actual password is entered at the hidden prompt, not as a shell argument. Create the root-only configuration:

```bash
sudo install -m 600 -o root -g root /opt/py101-live/live_questions/deploy/py101-live.env.example /etc/py101-live.env
sudo nano /etc/py101-live.env
```

Replace the placeholder hash line with the generated line, retaining:

```text
LIVE_ORIGIN=https://maguoliang.cn
LIVE_DEV=0
```

Use the exact origin without a trailing slash. The origin is part of request-access checks. Do not put a password or this real environment file in Git or the static site. On an existing installation, edit the existing environment file instead of copying the template over it.

### 4. Start the service

```bash
sudo install -m 644 /opt/py101-live/live_questions/deploy/py101-live.service /etc/systemd/system/py101-live.service
sudo systemctl daemon-reload
sudo systemctl enable --now py101-live
sudo systemctl status py101-live --no-pager
curl --fail http://127.0.0.1:8765/live/api/health
```

The service listens only on the server's loopback address. Do not open port 8765 in Aliyun or Ubuntu firewall rules. Nginx is the public entry point on HTTPS port 443. Automatic restart restores a failed process, but loses the classroom's temporary state.

The unit caps service memory at 192 MiB and tasks at 64. Check available memory and classroom usage before a pilot, especially on a 512 MiB instance; the cap does not reserve memory for nginx and Ubuntu. Repeated memory-limit kills require diagnosing capacity rather than adding workers.

### 5. Add the nginx routes

Copy the location snippet:

```bash
sudo install -m 644 /opt/py101-live/live_questions/deploy/nginx-locations.conf /etc/nginx/snippets/py101-live.conf
sudo nginx -T
```

Identify your existing **HTTPS** `server` block for `maguoliang.cn` and edit its configuration file. Add this line **inside that server block**:

```nginx
include /etc/nginx/snippets/py101-live.conf;
```

Keep its current TLS certificates, static document root, and other routes. If `/live/` or `/teacher/` locations already exist, reconcile them rather than creating duplicate locations. The snippet proxies these paths to the service, disables SSE buffering, and disables access logging for live routes. It replaces client-supplied forwarding headers; Uvicorn trusts forwarded headers only from the local nginx proxy.

All course-site copies, including GitHub Pages and your personal site, should link to the canonical `https://maguoliang.cn/live/` address. Open the teacher interface at that same canonical origin. The service does not enable cross-origin access or share authentication with `www`. The existing `www` course site may remain; if you redirect its live routes to the canonical origin, configure that in its own nginx server block.

Validate and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
curl --fail https://maguoliang.cn/live/api/health
```

### 6. Classroom acceptance check

In a teacher browser at `https://maguoliang.cn/teacher/`:

1. Log in and start a classroom. Verify the live connection indicator.
2. In a separate student browser, enter the code and send a question. It should reach the teacher without refreshing.
3. Submit `<script>alert(1)</script>` and confirm it appears literally, with no popup or interpreted HTML.
4. Check that a student cannot view questions or use teacher controls. A guessed teacher page URL must still require authentication.
5. Exercise pause/resume and end-class controls. A closed or expired class must reject new submissions.
6. Briefly disconnect/reconnect the teacher browser and confirm its connection state and recent-question behavior. End the test class afterward.
7. Confirm existing course pages still work, and their live-question button opens the canonical student page.

Do a small real-device trial before inviting the whole class. Local tests cannot establish campus connectivity, latency, or your Aliyun instance's capacity.

### 7. Enable the course-site entry point

The course now loads only `docs/javascripts/live-button.js` for questions. Its enabled `LIVE_URL` opens the Aliyun student page in a new tab. A single "Live questions" / "实时提问" button appears in the lower-left corner on every course page. The old `ask-button.js` is no longer loaded and contains no link.

After a successful public health check and classroom trial, the enabled constant in `docs/javascripts/live-button.js` is:

```javascript
var LIVE_URL = "https://maguoliang.cn/live/";
```

The MkDocs script URL is `javascripts/live-button.js?v=4`, and the stylesheet is `stylesheets/extra.css?v=7`. Increment the respective version again after future edits. This avoids reusing the old disabled script or old styling from browser caches. Commit and push static-site changes through the existing deployment workflow. The teacher can bookmark `https://maguoliang.cn/teacher/`.

The same script adds an "AI assistant" / "AI 助教" chat icon in the header, immediately after the language switcher. It opens the course's supplied Zhihuishu assistant URL in a new tab. This is an external link only: the course does not embed the chatbot or send its questions through the live-question backend.

All course copies use the same absolute student URL. The nested personal-site path, such as `/teaching/py101/py101_md/ch1_2_collections/`, is unchanged; students on that copy also open the Aliyun classroom when they click the button. The separate teacher page remains unchanged in purpose; an in-lesson teacher panel is not implemented.

If one copy looks old, check the published HTML's script version and the served script's `LIVE_URL`. On GitHub Actions, inspect the "Mirror to the Aliyun server" and "Rebuild the personal site" steps individually: both are best-effort, so a green overall run alone does not establish that those copies updated. Try a hard refresh after confirming the new assets are served.

To withdraw the student entry point later, set `LIVE_URL` back to an empty string, bump the script version, and republish. The old form will not reappear automatically.

Changes to `live_questions/static/`, including removal of the old form links from the student and teacher footers, require updating the backend files on Aliyun too; the static-site workflow does not copy those files.

## Updates and troubleshooting

The existing GitHub Actions workflow continues deploying static MkDocs output only. For a service update, repeat the upload, then on Ubuntu:

```bash
sudo rsync -a --chmod=D755,F644 --exclude='__pycache__/' --exclude='*.pyc' ~/py101-live-upload/live_questions/ /opt/py101-live/live_questions/
sudo /opt/py101-live/.venv/bin/python -m pip install -r /opt/py101-live/live_questions/requirements.txt
sudo chown -R root:root /opt/py101-live
sudo chmod -R u=rwX,go=rX /opt/py101-live
sudo systemctl restart py101-live
curl --fail http://127.0.0.1:8765/live/api/health
curl --fail https://maguoliang.cn/live/api/health
```

Schedule updates outside class because restart clears the active class and questions. If the unit or nginx snippet changed, install those files again and run `systemctl daemon-reload` or `nginx -t` and reload nginx as appropriate. These copy steps do not remove obsolete files; review any release that removes or renames service modules.

Useful diagnostics:

```bash
sudo systemctl status py101-live --no-pager
sudo journalctl -u py101-live --since '15 minutes ago' --no-pager
sudo systemctl show py101-live -p MemoryCurrent -p MemoryPeak -p NRestarts
sudo nginx -t
sudo ss -ltnp
```

If local health succeeds but public health fails, inspect nginx/TLS routing. If login works but delivery stalls, check buffering and proxy timeouts and verify there is one worker. If login is rejected, confirm the browser uses `https://maguoliang.cn`, the configured origin matches exactly, and the teacher hash was copied correctly.

To pause the pilot, `sudo systemctl stop py101-live` stops live questions; the static course remains available, but students cannot submit live questions. Hide the course entry point if the outage will be prolonged. Changing the password hash takes effect after restart, which also invalidates existing teacher sessions.
