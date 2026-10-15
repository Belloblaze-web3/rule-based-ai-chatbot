import assert from "node:assert/strict";
import test from "node:test";
import { FALLBACK_RESPONSE, KNOWLEDGE_BASE, normalizeText, respond } from "./bot.js";

test("normalizes case, punctuation, contractions, and repeated whitespace", () => {
  assert.equal(normalizeText("  HELLO,   there!!  "), "hello there");
  assert.equal(normalizeText("What’s today’s date?"), "what is todays date");
});

test("provides a dictionary knowledge base with eight intents", () => {
  assert.equal(Object.keys(KNOWLEDGE_BASE).length, 8);
});

test("matches greetings without accidental substring matches", () => {
  assert.equal(respond("  GOOD MORNING!!! ").intent, "greeting");
  assert.equal(respond("This is a test").intent, "fallback");
});

test("matches all predefined response categories", () => {
  assert.equal(respond("help").intent, "help");
  assert.equal(respond("Who are you?").intent, "identity");
  assert.equal(respond("what time is it", new Date("2026-10-15T18:12:08Z")).intent, "time");
  assert.equal(respond("today's date", new Date("2026-10-15T18:12:08Z")).intent, "date");
  assert.equal(respond("tell me a joke").intent, "joke");
  assert.equal(respond("thank you").intent, "thanks");
});

test("tolerates typos, contractions, and common chat synonyms", () => {
  assert.equal(respond("helo!").intent, "greeting");
  assert.equal(respond("wht can u do?").intent, "help");
  assert.equal(respond("thx!").intent, "thanks");
  assert.equal(respond("Todai").intent, "date");
});

test("understands varied date/time questions and selects the strongest intent", () => {
  assert.equal(respond("What's the time right now?").intent, "time");
  assert.equal(respond("What's today's date?").intent, "date");
  assert.equal(respond("hey, can you tell a joke?").intent, "joke");
});

test("exit commands request a clean end; mentions in a sentence do not", () => {
  for (const command of ["bye", "goodbye", "exit", "quit", "stop", "see you"]) {
    assert.equal(respond(`${command.toUpperCase()}!`).shouldExit, true);
  }
  assert.equal(respond("please stop by later").shouldExit, false);
});

test("returns a useful fallback for unknown and empty input", () => {
  assert.equal(respond("Can you fly a spaceship?").text, FALLBACK_RESPONSE);
  assert.equal(respond("   ").text, FALLBACK_RESPONSE);
});
