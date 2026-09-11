"use strict";
(() => {
  const L = window.LiveQuestions;
  const el = id => document.getElementById(id);
  const quizId = location.pathname.split("/").filter(Boolean)[1];
  let active = false, busy = false, polling = false, epoch = 0, expires = 0;
  function node(tag, text, className) {
    const result = document.createElement(tag);
    if (text !== undefined) result.textContent = text;
    if (className) result.className = className;
    return result;
  }
  function lock(message = "") {
    active = false;
    expires = 0;
    el("quiz-content").hidden = true;
    el("quiz-list").replaceChildren();
    el("quiz-questions").replaceChildren();
    el("join-panel").hidden = false;
    L.status(el("quiz-status"), message);
  }
  function renderQuiz(data) {
    el("quiz-title").textContent = data.title;
    el("quiz-description").textContent = data.description;
    document.title = data.title + " · In-class quizzes";
    data.questions.forEach((question, index) => {
      const card = node("section", undefined, "card quiz-question");
      card.append(node("h2", "Question " + (index + 1)), node("p", question.prompt));
      if (question.code) { const pre = node("pre"); pre.append(node("code", question.code)); card.append(pre); }
      if (question.after) card.append(node("p", question.after));
      if (question.options && question.options.length) {
        const options = node("ol"); options.type = "A";
        question.options.forEach(option => options.append(node("li", option)));
        card.append(options);
      }
      el("quiz-questions").append(card);
    });
  }
  async function load() {
    const ticket = ++epoch;
    try {
      const data = await L.api(quizId ? "/quiz-library/" + encodeURIComponent(quizId) : "/quiz-library");
      if (ticket !== epoch) return;
      el("quiz-list").replaceChildren();
      el("quiz-questions").replaceChildren();
      el("quiz-back").hidden = !quizId;
      if (quizId) renderQuiz(data.quiz);
      else {
        el("quiz-title").textContent = "Quiz library · 课堂测验库";
        el("quiz-description").textContent = "Choose a current or past quiz. · 选择本次或以往测验。";
        for (const quiz of data.quizzes) {
          const link = node("a", undefined, "card quiz-link");
          link.href = "/quiz/" + encodeURIComponent(quiz.id) + "/";
          link.append(node("h2", quiz.title), node("p", quiz.description), node("span", quiz.count + " questions · " + quiz.count + " 道题 →"));
          el("quiz-list").append(link);
        }
      }
      expires = data.expires_at;
      active = true;
      el("student-expiry").hidden = false;
      el("student-expiry").textContent = "Access until " + L.time(expires) + " · 开放至 " + L.time(expires);
      el("join-panel").hidden = true;
      el("quiz-content").hidden = false;
      L.status(el("quiz-status"));
    } catch (error) {
      if (ticket === epoch) lock([401,410].includes(error.status) ? "Enter your teacher’s quiz code. / 请输入老师提供的测验口令。" : error.status === 404 ? "Quiz not found. Return to /quiz/ to choose another. / 未找到测验，请返回 /quiz/。" : error.message);
    }
  }
  el("join-form").addEventListener("submit", async event => {
    event.preventDefault();
    if (busy) return;
    busy = true;
    ++epoch;
    el("join-button").disabled = true;
    try {
      await L.api("/quiz-join", {code: el("quiz-code").value});
      el("quiz-code").value = "";
      await load();
    } catch (error) {
      L.status(el("quiz-status"), error.status === 400 ? "Passcode is incorrect or expired. / 口令错误或已过期。" : error.message, "error");
    } finally { busy = false; el("join-button").disabled = false; }
  });
  window.setInterval(async () => {
    if (active && expires * 1000 <= Date.now()) { ++epoch; lock("Quiz access expired. / 测验访问已过期。"); return; }
    if (!active || busy || polling || document.hidden) return;
    polling = true;
    const ticket = epoch;
    try { await L.api("/quiz-student"); }
    catch (error) {
      if (ticket === epoch) { ++epoch; lock([401,410].includes(error.status) ? "Quiz access has ended. / 测验访问已结束。" : error.message); }
    } finally { polling = false; }
  }, 5000);
  window.addEventListener("pageshow", event => { if (event.persisted) { lock(); load(); } });
  document.addEventListener("visibilitychange", () => { if (!document.hidden && !busy) { lock(); load(); } });
  load();
})();
