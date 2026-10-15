// Dependency-free local NLP, mirrored by the Python RuleBasedChatbot.
// This is deterministic lexical matching, not an LLM or remote API.
export const KNOWLEDGE_BASE = Object.freeze({
  greeting: {
    phrases: ["hello", "hi", "hey", "hiya", "howdy", "greetings", "good day", "good morning", "good afternoon", "good evening"],
    response: "Hello! How can I help you today?",
  },
  help: {
    phrases: ["help", "help me", "what can you do", "what do you do", "commands", "what can you help with", "what are you able to do", "show me options"],
    response: "I can chat, tell you the date or time, share a joke, and explain what I can do. Try: 'time', 'date', or 'tell me a joke'.",
  },
  identity: {
    phrases: ["your name", "who are you", "what are you", "what is your name", "who created you"],
    response: "I'm RuleBot, a small rule-based chatbot built with explicit Python logic.",
  },
  time: {
    phrases: ["time", "what time is it", "current time", "what is the time", "tell me the time", "time right now", "time now", "the time"],
    response: null,
  },
  date: {
    phrases: ["date", "today", "what day is it", "today's date", "todays date", "current date", "what is the date", "what is today's date", "what is the date today", "the date"],
    response: null,
  },
  joke: {
    phrases: ["joke", "make me laugh", "tell me something funny", "say something funny", "something funny", "tell a joke", "crack a joke"],
    response: "Why did the computer go to the doctor? It had a virus!",
  },
  thanks: {
    phrases: ["thanks", "thank you", "appreciate it", "much appreciated", "thank u", "thx"],
    response: "You're welcome!",
  },
  farewell: {
    phrases: [],
    response: "Goodbye! Thanks for chatting. Start a new chat any time to begin again.",
  },
});

const TOKEN_SYNONYMS = Object.freeze({
  hiya: "hello", howdy: "hello", greetings: "hello", u: "you",
  pls: "please", plz: "please", thx: "thanks", ty: "thanks",
});
const INTENT_ORDER = ["greeting", "help", "identity", "time", "date", "joke", "thanks"];
export const EXIT_COMMANDS = new Set(["bye", "goodbye", "exit", "quit", "stop", "see you"]);
export const FALLBACK_RESPONSE = "I'm not sure how to respond to that yet. Type 'help' to see what I understand.";

export function normalizeText(text) {
  let lowered = String(text ?? "").toLowerCase().replaceAll("’", "'");
  for (const [pattern, replacement] of [
    [/\bwhat's\b/g, "what is"], [/\bwhats\b/g, "what is"],
    [/\bwho's\b/g, "who is"], [/\bwhos\b/g, "who is"],
    [/\bit's\b/g, "it is"], [/\btoday's\b/g, "todays"],
    [/\bi'm\b/g, "i am"], [/\byou're\b/g, "you are"],
  ]) lowered = lowered.replace(pattern, replacement);
  const words = lowered.replace(/[^a-z0-9\s]/g, " ").trim().split(/\s+/).filter(Boolean);
  return words.map((word) => TOKEN_SYNONYMS[word] ?? word).join(" ");
}

function editDistance(left, right) {
  if (left === right) return 0;
  if (Math.abs(left.length - right.length) > 2) return 3;
  let previous = Array.from({ length: right.length + 1 }, (_, i) => i);
  for (let row = 1; row <= left.length; row += 1) {
    const current = [row];
    for (let column = 1; column <= right.length; column += 1) {
      current[column] = Math.min(
        current[column - 1] + 1,
        previous[column] + 1,
        previous[column - 1] + (left[row - 1] === right[column - 1] ? 0 : 1),
      );
    }
    previous = current;
  }
  return previous.at(-1);
}

function tokenSimilarity(expected, actual) {
  if (expected === actual) return 2;
  if (Math.min(expected.length, actual.length) < 3 || Math.max(expected.length, actual.length) < 4) return 0;
  const limit = Math.max(expected.length, actual.length) >= 8 ? 2 : 1;
  return editDistance(expected, actual) <= limit ? 1 : 0;
}

function phraseScore(normalizedText, phrase) {
  const expected = normalizeText(phrase).split(" ").filter(Boolean);
  const actual = normalizedText.split(" ").filter(Boolean);
  if (!expected.length || expected.length > actual.length) return 0;
  const allowedTypos = expected.length >= 8 ? 2 : 1;
  let bestScore = 0;
  for (let start = 0; start <= actual.length - expected.length; start += 1) {
    const scores = expected.map((wanted, i) => tokenSimilarity(wanted, actual[start + i]));
    if (!scores.includes(0) && scores.filter((score) => score === 1).length <= allowedTypos) {
      bestScore = Math.max(bestScore, scores.reduce((sum, score) => sum + score, 0));
    }
  }
  return bestScore;
}

function bestIntent(normalizedText) {
  let winner = null;
  let winnerScore = 0;
  for (const intent of INTENT_ORDER) {
    const score = Math.max(...KNOWLEDGE_BASE[intent].phrases.map((phrase) => phraseScore(normalizedText, phrase)), 0);
    if (score > winnerScore) {
      winner = intent;
      winnerScore = score;
    }
  }
  return winner;
}

export function respond(userText, now = new Date()) {
  const normalized = normalizeText(userText);
  if (!normalized) return { text: FALLBACK_RESPONSE, intent: "fallback", shouldExit: false };

  if (EXIT_COMMANDS.has(normalized)) {
    return { text: KNOWLEDGE_BASE.farewell.response, intent: "farewell", shouldExit: true };
  }

  const intent = bestIntent(normalized);
  if (intent === null) return { text: FALLBACK_RESPONSE, intent: "fallback", shouldExit: false };
  else if (intent === "time") {
    return { text: `The current time is ${now.toLocaleTimeString()}.`, intent, shouldExit: false };
  } else if (intent === "date") {
    const formattedDate = new Intl.DateTimeFormat(undefined, {
      weekday: "long", month: "long", day: "numeric", year: "numeric",
    }).format(now);
    return { text: `Today's date is ${formattedDate}.`, intent, shouldExit: false };
  }
  return { text: KNOWLEDGE_BASE[intent].response, intent, shouldExit: false };
}
