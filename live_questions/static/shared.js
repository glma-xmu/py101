"use strict";

window.LiveQuestions = (() => {
  let csrf = "";
  let authEpoch = 0;
  const messages = {
    400: "Please check your entry and try again. / 请检查输入后重试。",
    401: "Your session has ended. Please sign in or join again. / 会话已结束，请重新登录或加入课堂。",
    403: "This action is not permitted. Please sign in or join again. / 暂无操作权限，请重新登录或加入课堂。",
    404: "Classroom not found. Check the code with your teacher. / 未找到课堂，请向老师确认课堂码。",
    409: "The classroom is not ready for this action. It may be paused. / 课堂暂不支持此操作，可能已暂停提问。",
    410: "This classroom has ended or expired. / 本课堂已结束或过期。",
    413: "This request is too large. Please shorten your entry. / 请求内容过长，请缩短后重试。",
    422: "Please check the classroom code or question format. / 请检查课堂码或问题格式。",
    429: "Too many requests. Please wait a moment before retrying. / 请求过于频繁，请稍后重试。",
    503: "The service or teacher connection is temporarily unavailable. Please retry shortly. / 服务或教师连接暂不可用，请稍后重试。"
  };

  async function api(path, body) {
    const requestEpoch = authEpoch;
    const headers = { Accept: "application/json" };
    const options = { method: body === undefined ? "GET" : "POST", headers, credentials: "same-origin", cache: "no-store" };
    if (body !== undefined) {
      headers["Content-Type"] = "application/json";
      headers["X-Live-Request"] = "1";
      if (csrf) headers["X-CSRF-Token"] = csrf;
      options.body = JSON.stringify(body);
    }
    const controller = new AbortController();
    options.signal = controller.signal;
    const timer = window.setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch("/live/api" + path, options);
      let data;
      try { data = await response.json(); } catch { data = null; }
      if (!response.ok) {
        let message = messages[response.status] || "The request could not be completed. Please retry. / 请求未完成，请重试。";
        if (response.status === 403 && data && data.code === "origin_mismatch") {
          message = "The page address does not match the server's LIVE_ORIGIN setting. Update LIVE_ORIGIN to "
            + window.location.origin + " and restart the service, or open the configured address. "
            + "/ 页面地址与服务器的 LIVE_ORIGIN 配置不一致。请修改配置并重启服务，或使用已配置的地址。";
          if (typeof data.expected_origin === "string") message += " LIVE_ORIGIN: " + data.expected_origin;
        }
        const error = new Error(message);
        error.status = response.status;
        error.retryAfter = response.headers.get("Retry-After");
        throw error;
      }
      if (typeof data !== "object" || data === null) throw new Error("Unexpected server response.");
      if (requestEpoch === authEpoch && typeof data.csrf === "string") csrf = data.csrf;
      return data;
    } catch (error) {
      if (error.status) throw error;
      const networkError = new Error("The connection was interrupted. Please try again. / 连接中断，请重试。");
      networkError.status = 0;
      throw networkError;
    } finally {
      window.clearTimeout(timer);
    }
  }

  function status(element, text = "", kind = "") {
    element.textContent = text;
    element.className = "status" + (kind ? " " + kind : "");
  }

  function time(unix) {
    const date = new Date(Number(unix) * 1000);
    return Number.isNaN(date.getTime()) ? "" : date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function requestId() {
    if (typeof crypto.randomUUID === "function") return crypto.randomUUID();
    const bytes = crypto.getRandomValues(new Uint8Array(16));
    bytes[6] = (bytes[6] & 15) | 64;
    bytes[8] = (bytes[8] & 63) | 128;
    const hex = Array.from(bytes, value => value.toString(16).padStart(2, "0"));
    return [hex.slice(0, 4).join(""), hex.slice(4, 6).join(""), hex.slice(6, 8).join(""), hex.slice(8, 10).join(""), hex.slice(10).join("")].join("-");
  }

  return { api, status, time, requestId, clearAuth: () => { csrf = ""; authEpoch += 1; }, setCsrf: value => { if (typeof value === "string") csrf = value; } };
})();
