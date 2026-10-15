import { respond } from "./bot.js";

const conversation = document.querySelector("#conversation");
const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const sendButton = document.querySelector("#send-button");
const newChatButton = document.querySelector("#new-chat");
const welcomeMessage = "Hello! I'm RuleBot. Type help to see what I understand, or choose a prompt on the left.";
let ended = false;

function currentTimeLabel() {
  return new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit" })
    .format(new Date()).toUpperCase();
}

function addMessage(kind, text, intent = "") {
  const row = document.createElement("div");
  row.className = `message-row ${kind === "bot" ? "bot-row" : "user-row"}`;

  if (kind === "bot") {
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = "R";
    row.append(avatar);
  }

  const content = document.createElement("div");
  content.className = "message-content";
  const author = document.createElement("span");
  author.className = "message-author";
  author.textContent = kind === "bot" ? "RULEBOT" : "YOU";
  if (kind === "bot" && intent) {
    const tag = document.createElement("span");
    tag.className = "intent-tag";
    tag.textContent = intent.toUpperCase();
    author.append(" ", tag);
  }

  const bubble = document.createElement("div");
  bubble.className = `bubble ${kind === "bot" ? "bot-bubble" : "user-bubble"}`;
  bubble.textContent = text;
  const time = document.createElement("time");
  time.className = "message-time";
  time.textContent = currentTimeLabel();
  content.append(author, bubble, time);
  row.append(content);
  conversation.append(row);
  conversation.scrollTop = conversation.scrollHeight;
}

function sendMessage(rawText) {
  if (ended) return;
  const text = String(rawText ?? "").trim();
  if (!text) return;
  addMessage("user", text);
  input.value = "";

  const reply = respond(text);
  addMessage("bot", reply.text, reply.intent);
  if (reply.shouldExit) {
    ended = true;
    input.disabled = true;
    sendButton.disabled = true;
    input.placeholder = "Conversation ended — start a new chat to continue";
    newChatButton.classList.add("attention");
    newChatButton.focus();
  } else {
    input.focus();
  }
}

function startNewChat() {
  ended = false;
  input.disabled = false;
  sendButton.disabled = false;
  input.placeholder = "Type a message…";
  newChatButton.classList.remove("attention");
  conversation.replaceChildren();
  const divider = document.createElement("div");
  divider.className = "day-divider";
  const dividerText = document.createElement("span");
  dividerText.textContent = "NEW CONVERSATION";
  divider.append(dividerText);
  conversation.append(divider);
  addMessage("bot", welcomeMessage, "WELCOME");
  input.focus();
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

newChatButton.addEventListener("click", startNewChat);

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.dataset.prompt));
});
