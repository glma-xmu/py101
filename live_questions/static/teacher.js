"use strict";

(() => {
  const L = window.LiveQuestions;
  const el = id => document.getElementById(id);
  const status = el("teacher-status");
  const list = el("question-list");
  const stage = el("barrage-stage");
  const nodes = new Map();
  let state = null;
  let stream = null;
  let busy = false;
  let authCheck = false;
  let epoch = 0;
  let revision = -1;
  let mode = "feed";
  let lane = 0;
  let messageTtlSeconds = 600;
  const barrageTimers = new Map();

  function connection(text, kind = "") {
    el("connection-state").textContent = text;
    el("connection-state").className = "pill " + kind;
  }

  function removeBarrage(node) {
    const timer = barrageTimers.get(node);
    if (timer) window.clearTimeout(timer);
    barrageTimers.delete(node);
    node.remove();
  }

  function clearQuestions() {
    nodes.clear();
    list.replaceChildren();
    Array.from(stage.children).forEach(removeBarrage);
    el("question-total").textContent = "0";
    el("empty-feed").hidden = false;
    el("new-question-notice").textContent = "";
  }

  function resetAuth(message = "") {
    epoch += 1;
    if (stream) stream.close();
    stream = null;
    state = null;
    revision = -1;
    L.clearAuth();
    clearQuestions();
    el("teacher-room-code").textContent = "";
    el("teacher-room-expiry").textContent = "";
    el("teacher-password").value = "";
    el("login-button").disabled = false;
    setBusy(false);
    el("teacher-desk").hidden = true;
    el("logout-button").hidden = true;
    el("login-panel").hidden = false;
    L.status(status, message, message ? "error" : "");
  }

  function setBusy(value) {
    busy = value;
    el("teacher-desk").querySelectorAll("button").forEach(button => { button.disabled = value; });
    el("logout-button").disabled = value;
  }

  function launchBarrage(message) {
    if (mode !== "barrage") return;
    const node = document.createElement("div");
    node.className = "barrage-message barrage-lane-" + (lane++ % 5);
    node.dataset.id = message.id;
    node.textContent = message.text;
    stage.appendChild(node);
    // Keep the animation small and bound its in-memory lifetime, including
    // browsers with reduced motion where animationend never fires.
    while (stage.children.length > 5) removeBarrage(stage.firstElementChild);
    node.addEventListener("animationend", () => removeBarrage(node), { once: true });
    barrageTimers.set(node, window.setTimeout(() => removeBarrage(node), 19000));
  }

  function questionNode(message) {
    const item = document.createElement("li");
    item.className = "question-item";
    const meta = document.createElement("div");
    meta.className = "question-meta";
    const sender = document.createElement("span");
    sender.textContent = "Student session / 学生会话 " + String(message.sender_id).slice(0, 8);
    const time = document.createElement("time");
    time.textContent = L.time(message.created_at);
    time.dateTime = new Date(Number(message.created_at) * 1000).toISOString();
    meta.append(sender, time);
    const text = document.createElement("p");
    text.className = "question-text";
    // Student content must never become HTML, Markdown, or executable code.
    text.textContent = message.text;
    const actions = document.createElement("div");
    actions.className = "question-actions";
    const dismiss = document.createElement("button");
    dismiss.type = "button";
    dismiss.className = "button";
    dismiss.textContent = "Dismiss · 移除";
    dismiss.addEventListener("click", () => mutate("/room/dismiss", { id: message.id }));
    const mute = document.createElement("button");
    mute.type = "button";
    mute.className = "button danger";
    mute.textContent = "Mute session · 静音此会话";
    mute.addEventListener("click", () => {
      if (window.confirm("Remove this session's questions and block further submissions until class ends? / 清除该学生会话的问题，并阻止其继续提问，直到课堂结束？")) {
        mutate("/room/mute", { sender_id: message.sender_id });
      }
    });
    actions.append(dismiss, mute);
    item.append(meta, text, actions);
    return item;
  }

  function applyState(next, forceRender = false) {
    if (!next || typeof next !== "object" || !Array.isArray(next.messages)) return;
    if (Number.isInteger(next.revision) && next.revision < revision) return;
    L.setCsrf(next.csrf);
    state = next;
    el("login-panel").hidden = true;
    el("teacher-desk").hidden = false;
    el("logout-button").hidden = false;
    el("no-room").hidden = Boolean(next.room);
    el("active-room").hidden = !next.room;
    el("feed-panel").hidden = !next.room;
    if (!next.room) {
      clearQuestions();
      el("teacher-room-code").textContent = "";
      el("teacher-room-expiry").textContent = "";
      revision = next.revision;
      return;
    }
    el("teacher-room-code").textContent = next.room.code;
    el("teacher-room-expiry").textContent = "Ends by " + L.time(next.room.expires_at) + " · 课堂最晚于此时结束";
    el("pause-button").textContent = next.room.paused ? "Resume · 恢复提问" : "Pause · 暂停提问";
    el("pause-button").setAttribute("aria-pressed", String(next.room.paused));
    if (next.revision === revision && !forceRender) return;
    revision = next.revision;
    const messages = next.messages;
    const ids = new Set(messages.map(message => message.id));
    for (const [id, node] of nodes) {
      if (!ids.has(id)) {
        node.remove();
        nodes.delete(id);
      }
    }
    Array.from(stage.children).forEach(node => { if (!ids.has(node.dataset.id)) removeBarrage(node); });
    const newMessages = [];
    for (const message of messages) {
      if (!nodes.has(message.id)) {
        nodes.set(message.id, questionNode(message));
        newMessages.push(message);
      }
    }
    // Reuse existing nodes so incoming questions do not reset focus or scroll.
    const ordered = [...messages].reverse();
    ordered.forEach((message, index) => {
      const node = nodes.get(message.id);
      const current = list.children[index];
      if (current !== node) list.insertBefore(node, current || null);
    });
    if (newMessages.length) {
      el("new-question-notice").textContent = newMessages.length + " new question(s) / 条新问题";
      newMessages.slice(-5).forEach(launchBarrage);
    }
    el("question-total").textContent = String(messages.length);
    el("empty-feed").hidden = messages.length > 0;
    if (busy) list.querySelectorAll("button").forEach(button => { button.disabled = true; });
  }

  async function refreshAuth(thisEpoch) {
    if (authCheck || !state) return;
    authCheck = true;
    try {
      const next = await L.api("/teacher");
      if (epoch === thisEpoch) applyState(next);
    } catch (error) {
      if (epoch === thisEpoch && [401, 403].includes(error.status)) resetAuth(error.message);
    } finally {
      authCheck = false;
    }
  }

  function connect() {
    if (stream) stream.close();
    connection("Connecting · 连接中");
    const thisEpoch = epoch;
    const source = new EventSource("/live/api/events");
    stream = source;
    source.addEventListener("open", () => {
      if (epoch === thisEpoch) connection("Live · 实时连接", "connected");
    });
    source.addEventListener("snapshot", event => {
      if (epoch !== thisEpoch) return;
      try {
        applyState(JSON.parse(event.data));
        connection("Live · 实时连接", "connected");
      } catch {
        connection("Connection error · 连接异常", "warning");
      }
    });
    source.addEventListener("session_expired", () => {
      if (epoch === thisEpoch) resetAuth("Your teacher session has ended. Sign in again. / 教师会话已结束，请重新登录。");
    });
    source.addEventListener("error", () => {
      if (epoch !== thisEpoch) return;
      connection("Reconnecting; feed may be stale · 正在重连，列表可能未更新", "warning");
      refreshAuth(thisEpoch);
    });
  }

  async function mutate(path, body = {}) {
    if (busy || !state) return;
    const thisEpoch = epoch;
    setBusy(true);
    L.status(status);
    try {
      const next = await L.api(path, body);
      if (thisEpoch === epoch) applyState(next);
    } catch (error) {
      if (thisEpoch !== epoch) return;
      if ([401, 403].includes(error.status)) resetAuth(error.message);
      else {
        L.status(status, error.message, "error");
        refreshAuth(thisEpoch);
      }
    } finally {
      if (thisEpoch === epoch) setBusy(false);
    }
  }

  el("login-form").addEventListener("submit", async event => {
    event.preventDefault();
    if (busy) return;
    const password = el("teacher-password").value;
    el("teacher-password").value = "";
    if (!password) return;
    busy = true;
    el("login-button").disabled = true;
    const loginEpoch = epoch;
    L.status(status, "Signing in… / 正在登录…");
    try {
      const next = await L.api("/login", { password });
      if (loginEpoch !== epoch) return;
      revision = -1;
      applyState(next);
      connect();
      L.status(status);
    } catch (error) {
      if (loginEpoch !== epoch) return;
      const message = error.status === 401 ? "Sign-in failed. Please check your password. / 登录失败，请检查密码。" : error.message;
      L.status(status, message, "error");
      el("teacher-password").focus();
    } finally {
      if (loginEpoch === epoch) {
        setBusy(false);
        el("login-button").disabled = false;
      }
    }
  });

  el("logout-button").addEventListener("click", async () => {
    if (busy) return;
    const thisEpoch = epoch;
    setBusy(true);
    try {
      await L.api("/logout", {});
      if (thisEpoch === epoch) resetAuth();
    } catch (error) {
      if (thisEpoch !== epoch) return;
      if ([401, 403].includes(error.status)) resetAuth();
      else L.status(status, "Sign-out was not confirmed. Please retry. / 尚未确认退出，请重试。", "error");
    } finally {
      if (thisEpoch === epoch) setBusy(false);
    }
  });
  el("start-button").addEventListener("click", () => mutate("/room/start"));
  el("pause-button").addEventListener("click", () => {
    if (state && state.room) mutate("/room/pause", { paused: !state.room.paused });
  });
  el("clear-button").addEventListener("click", () => {
    if (window.confirm("Clear all current questions? They cannot be recovered. / 清空当前所有问题？清空后无法恢复。")) mutate("/room/clear");
  });
  el("end-button").addEventListener("click", () => {
    if (window.confirm("End class, expire the code, and erase all questions? / 结束课堂、使课堂码失效并清空所有问题？")) mutate("/room/close");
  });
  el("copy-link-button").addEventListener("click", async () => {
    if (!state || !state.room) return;
    const url = location.origin + "/live/#" + encodeURIComponent(state.room.code);
    try {
      await navigator.clipboard.writeText(url);
      L.status(status, "Student link copied. / 已复制学生链接。", "success");
    } catch {
      L.status(status, "Copy this student link / 请复制学生链接：\n" + url);
    }
  });

  function setMode(nextMode) {
    mode = nextMode;
    el("feed-view").hidden = mode !== "feed";
    el("barrage-view").hidden = mode !== "barrage";
    for (const view of ["feed", "barrage"]) {
      const button = el(view + "-view-button");
      button.setAttribute("aria-pressed", String(view === mode));
      button.classList.toggle("selected", view === mode);
    }
    Array.from(stage.children).forEach(removeBarrage);
    if (mode === "barrage" && state) state.messages.slice(-5).forEach(launchBarrage);
  }
  el("feed-view-button").addEventListener("click", () => setMode("feed"));
  el("barrage-view-button").addEventListener("click", () => setMode("barrage"));

  // A back/forward-cache copy must not reveal old private questions before
  // the service verifies the teacher's current session again.
  window.addEventListener("pagehide", () => resetAuth());
  window.addEventListener("pageshow", async event => {
    if (!event.persisted) return;
    const thisEpoch = epoch;
    try {
      const next = await L.api("/teacher");
      if (thisEpoch !== epoch) return;
      applyState(next);
      connect();
    } catch (error) {
      if (thisEpoch === epoch) resetAuth(error.message);
    }
  });

  function pruneExpiredQuestions() {
    if (!state || !state.room) return;
    const now = Date.now() / 1000;
    if (state.room.expires_at <= now) {
      applyState({ ...state, room: null, messages: [] }, true);
      L.status(status, "The classroom has expired. Start a new class when ready. / 课堂已到期，需要时可开始新课堂。");
      return;
    }
    const messages = state.messages.filter(message => message.created_at + messageTtlSeconds > now);
    if (messages.length !== state.messages.length) applyState({ ...state, messages }, true);
  }

  async function init() {
    const initEpoch = epoch;
    el("login-button").disabled = true;
    const results = await Promise.allSettled([L.api("/config"), L.api("/teacher")]);
    if (initEpoch !== epoch) return;
    if (results[0].status === "fulfilled") {
      const c = results[0].value;
      if (Number.isFinite(c.message_ttl_minutes)) messageTtlSeconds = c.message_ttl_minutes * 60;
      el("retention-note").textContent = "Questions expire after " + c.message_ttl_minutes + " minutes. Only the newest " + c.buffer_size + " stay in memory. Class end and service restart erase them.\n问题保留 " + c.message_ttl_minutes + " 分钟，内存中最多保留最新 " + c.buffer_size + " 条；课堂结束或服务重启后清空。";
    }
    if (results[1].status === "fulfilled") {
      applyState(results[1].value);
      connect();
    } else if (results[1].reason.status !== 401) {
      L.status(status, "The live service is temporarily unavailable. Please try signing in again shortly. / 实时服务暂不可用，请稍后重新登录。", "error");
    }
    el("login-button").disabled = false;
  }

  window.setInterval(pruneExpiredQuestions, 1000);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden && state) {
      pruneExpiredQuestions();
      refreshAuth(epoch);
    }
  });
  init();
})();
