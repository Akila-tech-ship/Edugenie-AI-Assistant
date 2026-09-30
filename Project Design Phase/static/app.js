const API_BASE = (() => {
    const currentOrigin = window.location.origin;
    if (!currentOrigin || currentOrigin === "null" || /:(5500|5501|4173|3000)$/.test(currentOrigin)) {
        return "http://127.0.0.1:8000";
    }
    return currentOrigin;
})();

function apiUrl(path) {
    return `${API_BASE}${path.startsWith("/") ? path : `/${path}`}`;
}

const state = {
    task: "qa",
    busy: false,
    score: 0,
    answered: 0,
    total: 0
};

const config = {
    qa: {
        endpoint: "/qa",
        label: "Ask your question",
        placeholder: "Example: Which is the largest ocean?",
        helper: "Tip: Ask a clear question for a focused answer.",
        button: "Ask EduGenie"
    },
    explain: {
        endpoint: "/explain",
        label: "Enter a topic",
        placeholder: "Example: Explain Pythagoras theorem in simple words.",
        helper: "Tip: Enter a concept you want to understand from the basics.",
        button: "Explain with EduGenie"
    },
    summarize: {
        endpoint: "/summarize",
        label: "Paste your study material",
        placeholder: "Paste a paragraph, lesson, article, or notes here...",
        helper: "Tip: Longer educational text works well for revision summaries.",
        button: "Summarize Content"
    },
    quiz: {
        endpoint: "/quiz",
        label: "Enter a quiz topic",
        placeholder: "Example: Photosynthesis, SQL joins, Indian history...",
        helper: "Tip: EduGenie generates 3 questions with 4 options each.",
        button: "Generate Quiz"
    },
    learn: {
        endpoint: "/learn/recommendations",
        label: "Enter a learning topic",
        placeholder: "Example: SQL, Python, Cloud Computing, Networking...",
        helper: "Tip: Start with a subject you want to learn from beginner to advanced.",
        button: "Build Learning Path"
    }
};

const taskButtons = document.querySelectorAll(".task");
const input = document.getElementById("inputText");
const label = document.getElementById("inputLabel");
const helper = document.getElementById("helperText");
const button = document.getElementById("submitBtn");
const buttonText = document.getElementById("buttonText");
const result = document.getElementById("result");
const status = document.getElementById("status");
const charCount = document.getElementById("charCount");

taskButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        if (state.busy) return;
        setTask(btn.dataset.task);
    });
});

document.querySelectorAll(".example-row button").forEach(btn => {
    btn.addEventListener("click", () => {
        input.value = btn.dataset.example;
        updateCharCount();
        setTask(btn.dataset.example === "SQL" ? "learn" : btn.dataset.example === "Pythagoras theorem" ? "explain" : "qa");
        input.focus();
    });
});

input.addEventListener("input", updateCharCount);
button.addEventListener("click", runEduGenie);

function setTask(task) {
    state.task = task;
    const c = config[task];

    taskButtons.forEach(btn => btn.classList.toggle("active", btn.dataset.task === task));
    label.textContent = c.label;
    input.placeholder = c.placeholder;
    helper.textContent = c.helper;
    buttonText.textContent = c.button;
}

function updateCharCount() {
    charCount.textContent = `${input.value.length.toLocaleString()} characters`;
}

async function runEduGenie() {
    if (state.busy) return;

    const text = input.value.trim();
    if (!text) {
        showError("Please enter some content first.");
        return;
    }

    state.busy = true;
    button.disabled = true;
    status.textContent = "THINKING";
    status.className = "response-status busy";
    buttonText.textContent = "EduGenie is thinking...";

    result.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <div>Generating your ${state.task === "quiz" ? "quiz" : "learning response"}...</div>
        </div>
    `;

    try {
        const response = await fetch(apiUrl(config[state.task].endpoint), {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const rawText = await response.text();
        let data = null;

        if (rawText) {
            try {
                data = JSON.parse(rawText);
            } catch (parseError) {
                throw new Error(rawText.slice(0, 500) || "The server returned an invalid response.");
            }
        }

        if (!response.ok) {
            const message = data && (data.detail || data.message)
                ? data.detail || data.message
                : rawText || "The server could not complete the request.";
            throw new Error(message);
        }

        if (state.task === "quiz") {
            renderQuiz(data.result);
        } else {
            renderText(data.result);
        }

        status.textContent = "COMPLETED";
        status.className = "response-status done";
    } catch (error) {
        showError(error.message || "The server could not complete the request.");
    } finally {
        state.busy = false;
        button.disabled = false;
        buttonText.textContent = config[state.task].button;
    }
}

function renderText(text) {
    result.innerHTML = `<div class="response-text">${formatText(text)}</div>`;
}

function renderQuiz(quiz) {
    state.score = 0;
    state.answered = 0;
    state.total = quiz.questions.length;

    let html = `<div class="quiz-score" id="quizScore">Score: 0 / ${state.total}</div>`;

    quiz.questions.forEach((q, index) => {
        html += `
            <div class="quiz-question" data-correct="${escapeAttr(q.correct_answer)}">
                <h3>${index + 1}. ${escapeHtml(q.question)}</h3>
                <div>
                    ${q.options.map(option => `
                        <button class="option" data-answer="${escapeAttr(option)}">
                            ${escapeHtml(option)}
                        </button>
                    `).join("")}
                </div>
                <div class="feedback" hidden></div>
            </div>
        `;
    });

    result.innerHTML = html;

    result.querySelectorAll(".option").forEach(option => {
        option.addEventListener("click", () => answerQuiz(option));
    });
}

function answerQuiz(selected) {
    const card = selected.closest(".quiz-question");
    if (card.dataset.answered === "true") return;

    card.dataset.answered = "true";
    const correct = card.dataset.correct;
    const feedback = card.querySelector(".feedback");
    const options = card.querySelectorAll(".option");

    options.forEach(btn => btn.disabled = true);

    if (selected.dataset.answer === correct) {
        state.score++;
        selected.classList.add("correct");
        feedback.textContent = "✓ Correct answer!";
        feedback.style.color = "#86efac";
    } else {
        selected.classList.add("wrong");
        options.forEach(btn => {
            if (btn.dataset.answer === correct) btn.classList.add("correct");
        });
        feedback.textContent = `✗ Incorrect. Correct answer: ${correct}`;
        feedback.style.color = "#fda4af";
    }

    state.answered++;
    feedback.hidden = false;
    document.getElementById("quizScore").textContent = `Score: ${state.score} / ${state.total}`;

    if (state.answered === state.total) {
        document.getElementById("quizScore").textContent =
            `Quiz completed — Score: ${state.score} / ${state.total}`;
    }
}

function showError(message) {
    status.textContent = "ERROR";
    status.className = "response-status error";
    result.innerHTML = `<div class="error-box"><strong>EduGenie could not complete this request.</strong><br>${escapeHtml(message)}</div>`;
}

function formatText(text) {
    return escapeHtml(text)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/^### (.*)$/gm, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");
}

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = String(value);
    return div.innerHTML;
}

function escapeAttr(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

setTask("qa");
updateCharCount();
