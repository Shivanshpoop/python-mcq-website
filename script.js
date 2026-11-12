const quiz = document.querySelector("#quiz");
const count = document.querySelector("#count");
const category = document.querySelector("#category");
const fill = document.querySelector("#progress-fill");
const submit = document.querySelector("#submit");
const result = document.querySelector("#result");
let questions = [];
let answers = {};

async function start() {
  try {
    const response = await fetch("/api/questions");
    if (!response.ok) throw new Error("Could not load questions");
    ({questions} = await response.json());
    render();
  } catch (error) {
    quiz.textContent = "Unable to load the quiz. Please restart the Python server.";
    count.textContent = "Error";
  }
}
function render() {
  count.textContent = `${questions.length} questions`;
  category.textContent = "MIXED QUIZ";
  fill.style.width = "0%";
  quiz.innerHTML = questions.map((q, i) => `
    <article class="question-block">
      <h2 class="question">${i + 1}. ${escapeHtml(q.question)}</h2>
      ${q.options.map((option, j) => `
        <label class="option">
          <input type="radio" name="q-${q.id}" value="${j}" ${answers[q.id] === j ? "checked" : ""}>
          <span>${escapeHtml(option)}</span>
        </label>`).join("")}
    </article>`).join("");
  quiz.querySelectorAll("input").forEach(input => input.addEventListener("change", event => {
    const [_, id] = event.target.name.split("-");
    answers[id] = Number(event.target.value);
    fill.style.width = `${Object.keys(answers).length / questions.length * 100}%`;
    submit.disabled = Object.keys(answers).length !== questions.length;
  }));
  submit.disabled = true;
  result.innerHTML = "";
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
}
submit.addEventListener("click", async () => {
  submit.disabled = true;
  try {
    const response = await fetch("/api/submit", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({answers})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Submission failed");
    result.innerHTML = `<p class="score">${data.score} / ${data.total} · ${data.percentage}%</p><p class="muted">Your quiz has been evaluated. Review the explanations below.</p>` +
      data.details.map((item, i) => `<div class="review"><strong>Question ${i + 1}: ${item.correct ? "Correct ✓" : "Review this one"}</strong><br><span class="muted">${escapeHtml(item.explanation)}</span></div>`).join("");
    result.scrollIntoView({behavior:"smooth",block:"nearest"});
  } catch (error) {
    result.textContent = error.message;
    submit.disabled = false;
  }
});
start();
