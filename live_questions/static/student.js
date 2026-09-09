"use strict";

(() => {
  const L = window.LiveQuestions;
  const el = id => document.getElementById(id);
  const status = el("student-status");
  const question = el("question");
  const send = el("send-button");
  let room = null;
  let busy = false;
  let pending = null;
  let maxChars = 500;
  let polling = false;
  let epoch = 0;

  // The room code is a convenience, not a teacher credential. Do not retain it
  // in history, storage, analytics, or subsequent outgoing links.
  if (location.hash) {
    try { el("room-code").value = decodeURIComponent(location.hash.slice(1)).slice(0, 16); } catch { /* Ignore malformed links. */ }
    history.replaceState(null, "", location.pathname + location.search);
  }

  function updateCount() {
    const count = Array.from(question.value).length;
    el("question-count").textContent = count + " / " + maxChars;
    question.setCustomValidity(count > maxChars ? "Please shorten the question. / 请缩短问题。" : "");
  }

  function showRoom(nextRoom) {
    room = nextRoom;
    el("join-panel").hidden = Boolean(room);
    el("question-panel").hidden = !room;
    if (!room) return;
    el("room-expiry").textContent = "Class ends by " + L.time(room.expires_at) + " · 课堂最晚于此时结束";
    el("class-state").textContent = room.paused ? "Paused · 已暂停" : "Connected · 已连接";
    el("class-state").className = "pill " + (room.paused ? "warning" : "connected");
    send.disabled = busy || room.paused;
  }

  function clearSession() {
    epoch += 1;
    busy = false;
    el("join-button").disabled = false;
    el("change-class").disabled = false;
    send.disabled = true;
    room = null;
    pending = null;
    question.value = "";
    question.readOnly = false;
    L.clearAuth();
    showRoom(null);
    updateCount();
    send.textContent = "Send question · 发送问题";
  }

  el("question").addEventListener("input", updateCount);
  el("join-form").addEventListener("submit", async event => {
    event.preventDefault();
    if (busy) return;
    const code = el("room-code").value.trim().toUpperCase();
    if (!code) return;
    const joinEpoch = epoch;
    busy = true;
    el("join-button").disabled = true;
    L.status(status, "Joining class… / 正在加入课堂…");
    try {
      const data = await L.api("/join", { code });
      if (joinEpoch !== epoch) return;
      pending = null;
      question.readOnly = false;
      showRoom(data.room);
      L.status(status, data.room.paused ? "The teacher has paused questions. / 老师已暂停接收问题。" : "");
      question.focus();
    } catch (error) {
      if (joinEpoch === epoch) L.status(status, error.message, "error");
    } finally {
      if (joinEpoch === epoch) {
        busy = false;
        el("join-button").disabled = false;
        if (room) send.disabled = room.paused;
      }
    }
  });

  el("question-form").addEventListener("submit", async event => {
    event.preventDefault();
    if (busy || !room || room.paused) return;
    const text = question.value.trim();
    if (!text || Array.from(text).length > maxChars) {
      L.status(status, "Enter a question within the character limit. / 请在字数限制内输入问题。", "error");
      return;
    }
    if (!pending) pending = { text, request_id: L.requestId() };
    const request = pending;
    const thisEpoch = epoch;
    busy = true;
    question.readOnly = true;
    send.disabled = true;
    el("change-class").disabled = true;
    send.textContent = "Sending… / 发送中…";
    L.status(status);
    try {
      const data = await L.api("/questions", request);
      if (thisEpoch !== epoch) return;
      if (data.accepted !== true) throw new Error("The service did not confirm receipt. Please retry. / 服务尚未确认收到，请重试。");
      pending = null;
      question.value = "";
      question.readOnly = false;
      updateCount();
      L.status(status, "Received by the service. Your teacher may not have read it yet. / 服务已收到；老师可能尚未阅读。", "success");
      send.textContent = "Send question · 发送问题";
      question.focus();
    } catch (error) {
      if (thisEpoch !== epoch) return;
      if ([401, 410].includes(error.status)) {
        clearSession();
        el("room-code").focus();
        L.status(status, error.message, "error");
      } else if ([400, 413, 422].includes(error.status)) {
        // A definite rejection can be edited into a new request. Network
        // failures retain the exact request UUID and text until acknowledged.
        pending = null;
        question.readOnly = false;
        send.textContent = "Send question · 发送问题";
        L.status(status, error.message, "error");
      } else {
        send.textContent = "Retry this question · 重试此问题";
        L.status(status, error.message + "\nYour question is kept here for retry; reusing the same request avoids duplicates. / 问题暂留在当前页面，重试将复用同一请求以避免重复。", "error");
      }
    } finally {
      if (thisEpoch === epoch) {
        busy = false;
        el("change-class").disabled = false;
        send.disabled = !room || room.paused;
      }
    }
  });

  el("change-class").addEventListener("click", () => {
    if (busy) return;
    if (pending && !window.confirm("Delivery has not been confirmed. Changing classes discards the pending retry. Continue? / 发送状态尚未确认；更换课堂将放弃当前重试。继续？")) return;
    clearSession();
    L.status(status);
    el("room-code").focus();
  });

  window.addEventListener("pagehide", () => {
    clearSession();
    el("room-code").value = "";
    L.status(status);
  });
  window.addEventListener("pageshow", async event => {
    if (!event.persisted) return;
    const thisEpoch = epoch;
    try {
      const next = await L.api("/student");
      if (thisEpoch === epoch) showRoom(next.room);
    } catch (error) {
      if (thisEpoch === epoch && ![401, 410].includes(error.status)) L.status(status, error.message, "error");
    }
  });

  async function refreshRoom() {
    if (!room || polling || busy || document.hidden) return;
    polling = true;
    const thisEpoch = epoch;
    try {
      const data = await L.api("/student");
      if (thisEpoch === epoch) showRoom(data.room);
    } catch (error) {
      if (thisEpoch !== epoch) return;
      if ([401, 410].includes(error.status)) {
        clearSession();
        L.status(status, error.message, "error");
      } else {
        el("class-state").textContent = "Reconnecting · 重新连接中";
        el("class-state").className = "pill warning";
      }
    } finally {
      polling = false;
    }
  }

  async function init() {
    const initEpoch = epoch;
    el("join-button").disabled = true;
    const results = await Promise.allSettled([L.api("/config"), L.api("/student")]);
    if (initEpoch !== epoch) return;
    if (results[0].status === "fulfilled") {
      const config = results[0].value;
      if (Number.isInteger(config.max_message_chars) && config.max_message_chars > 0) {
        maxChars = config.max_message_chars;
        // JS and Python count Unicode code points; native maxlength counts
        // UTF-16 units. Let our own validation preserve the agreed limit.
        question.removeAttribute("maxlength");
      }
      el("privacy-detail").textContent = "Questions stay in memory for up to " + config.message_ttl_minutes + " minutes (newest " + config.buffer_size + " only), and disappear when the class ends or the service restarts. Do not include personal or sensitive information.\n问题仅在内存中保留最多 " + config.message_ttl_minutes + " 分钟（最多保留最新 " + config.buffer_size + " 条），课堂结束或服务重启后消失。请勿包含个人或敏感信息。";
    }
    if (results[1].status === "fulfilled") {
      showRoom(results[1].value.room);
    } else if (![401, 410].includes(results[1].reason.status)) {
      L.status(status, "Live questions are temporarily unavailable. Try joining shortly, or use Wenjuanxing below. / 实时提问暂不可用，请稍后尝试，或使用下方问卷星。", "error");
    }
    el("join-button").disabled = false;
    updateCount();
  }

  window.setInterval(refreshRoom, 15000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) refreshRoom(); });
  init();
})();
