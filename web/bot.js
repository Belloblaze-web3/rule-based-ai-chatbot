// Browser-side equivalent of the Python RuleBasedChatbot. Keep these rules
// deterministic and aligned with rule_based_ai_chatbot/chatbot.py.
export const KNOWLEDGE_BASE = Object.freeze({
  greeting: {
    phrases: ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
    response: "Hello! How can I help you today?",
  },
  help: {
    phrases: ["help", "what can you do", "what do you do", "commands"],
    response: "I can chat, tell you the date or time, share a joke, and explain what I can do. Try: 'time', 'date', or 'tell me a joke'.",
  },
  identity: {
    phrases: ["your name", "who are you", "what are you"],
    response: "I'm RuleBot, a small rule-based chatbot built with explicit Python logic.",
  },
  time: {
    phrases: ["time", "what time is it", "current time"],
    response: null,
  },
  date: {
    phrases: ["date", "what day is it", "today's date", "todays date"],
    response: null,
  },
  joke: {
    phrases: ["joke", "make me laugh", "tell me something funny"],
    response: "Why did the computer go to the doctor? It had a virus!",
  },
  thanks: {
    phrases: ["thanks", "thank you", "appreciate it"],
    response: "You're welcome!",
  },
  farewell: {
    phrases: [],
    response: "Goodbye! Thanks for chatting. Start a new chat any time to begin again.",
  },
});

export const EXIT_COMMANDS = new Set(["bye", "goodbye", "exit", "quit", "stop", "see you"]);
export const FALLBACK_RESPONSE = "I'm not sure how to respond to that yet. Type 'help' to see what I understand.";

export function normalizeText(text) {
  return String(text ?? "")
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s']/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function containsPhrase(normalizedText, phrase) {
  return ` ${normalizedText} `.includes(` ${phrase} `);
}

export function respond(userText, now = new Date()) {
  const normalized = normalizeText(userText);
  if (!normalized) return { text: FALLBACK_RESPONSE, intent: "fallback", shouldExit: false };

  let intent;
  if (EXIT_COMMANDS.has(normalized)) {
    return { text: KNOWLEDGE_BASE.farewell.response, intent: "farewell", shouldExit: true };
  } else if (KNOWLEDGE_BASE.greeting.phrases.some((phrase) => containsPhrase(normalized, phrase))) {
    intent = "greeting";
  } else if (KNOWLEDGE_BASE.help.phrases.some((phrase) => containsPhrase(normalized, phrase))) {
    intent = "help";
  } else if (KNOWLEDGE_BASE.identity.phrases.some((phrase) => containsPhrase(normalized, phrase))) {
    intent = "identity";
  } else if (KNOWLEDGE_BASE.time.phrases.some((phrase) => containsPhrase(normalized, phrase))) {
    intent = "time";
  } else if (KNOWLEDGE_BASE.date.phrases.some((phrase) => containsPhrase(normalized, phrase))) {
    intent = "date";
  } else if (KNOWLEDGE_BASE.joke.phrases.some((phrase) => containsPhrase(normalized, phrase))) {
    intent = "joke";
  } else if (KNOWLEDGE_BASE.thanks.phrases.some((phrase) => containsPhrase(normalized, phrase))) {
    intent = "thanks";
  } else {
    return { text: FALLBACK_RESPONSE, intent: "fallback", shouldExit: false };
  }

  if (intent === "time") {
    return { text: `The current time is ${now.toLocaleTimeString()}.`, intent, shouldExit: false };
  } else if (intent === "date") {
    const formattedDate = new Intl.DateTimeFormat(undefined, {
      weekday: "long", month: "long", day: "numeric", year: "numeric",
    }).format(now);
    return { text: `Today's date is ${formattedDate}.`, intent, shouldExit: false };
  }
  return { text: KNOWLEDGE_BASE[intent].response, intent, shouldExit: false };
}
