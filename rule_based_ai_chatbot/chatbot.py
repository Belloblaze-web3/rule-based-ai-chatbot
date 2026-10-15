"""Deterministic, local NLP chatbot for Project 1.

The bot uses token normalization, a small synonym map, edit-distance tolerance,
and scored intent phrases. It intentionally uses no learned or generative model,
API, or network access so every decision remains inspectable and testable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Callable


# Each intent is an explicit, human-readable mini-lexicon.
KNOWLEDGE_BASE: dict[str, dict[str, tuple[str, ...] | str]] = {
    "greeting": {
        "phrases": (
            "hello", "hi", "hey", "hiya", "howdy", "greetings", "good day",
            "good morning", "good afternoon", "good evening",
        ),
        "response": "Hello! How can I help you today?",
    },
    "help": {
        "phrases": (
            "help", "help me", "what can you do", "what do you do", "commands",
            "what can you help with", "what are you able to do", "show me options",
        ),
        "response": "I can chat, tell you the date or time, share a joke, and explain what I can do. Try: 'time', 'date', or 'tell me a joke'.",
    },
    "identity": {
        "phrases": (
            "your name", "who are you", "what are you", "what is your name",
            "who created you",
        ),
        "response": "I'm RuleBot, a small rule-based chatbot built with explicit Python logic.",
    },
    "time": {
        "phrases": (
            "time", "what time is it", "current time", "what is the time",
            "tell me the time", "time right now", "time now", "the time",
        ),
        "response": "",
    },
    "date": {
        "phrases": (
            "date", "today", "what day is it", "today's date", "todays date",
            "current date", "what is the date", "what is today's date",
            "what is the date today", "the date",
        ),
        "response": "",
    },
    "joke": {
        "phrases": (
            "joke", "make me laugh", "tell me something funny", "say something funny",
            "something funny", "tell a joke", "crack a joke",
        ),
        "response": "Why did the computer go to the doctor? It had a virus!",
    },
    "thanks": {
        "phrases": (
            "thanks", "thank you", "appreciate it", "much appreciated", "thank u", "thx",
        ),
        "response": "You're welcome!",
    },
    "farewell": {
        "phrases": (),
        "response": "Goodbye! Thanks for chatting. Enter 'hello' any time to start another conversation.",
    },
}

# Short, transparent normalizations—not a statistical language model.
TOKEN_SYNONYMS = {
    "hiya": "hello",
    "howdy": "hello",
    "greetings": "hello",
    "u": "you",
    "pls": "please",
    "plz": "please",
    "thx": "thanks",
    "ty": "thanks",
}
EXIT_COMMANDS = {"bye", "goodbye", "exit", "quit", "stop", "see you"}
FALLBACK_RESPONSE = "I'm not sure how to respond to that yet. Type 'help' to see what I understand."
INTENT_ORDER = ("greeting", "help", "identity", "time", "date", "joke", "thanks")


@dataclass(frozen=True)
class ChatbotReply:
    """A response and its control-flow meaning for the chat loop."""

    text: str
    intent: str
    should_exit: bool = False


def normalize_text(text: str) -> str:
    """Expand common contractions, normalize punctuation, and canonicalize tokens."""
    lowered = str(text or "").lower().replace("’", "'")
    contractions = (
        (r"\bwhat's\b", "what is"),
        (r"\bwhats\b", "what is"),
        (r"\bwho's\b", "who is"),
        (r"\bwhos\b", "who is"),
        (r"\bit's\b", "it is"),
        (r"\btoday's\b", "todays"),
        (r"\bi'm\b", "i am"),
        (r"\byou're\b", "you are"),
    )
    for pattern, replacement in contractions:
        lowered = re.sub(pattern, replacement, lowered)
    without_punctuation = re.sub(r"[^a-z0-9\s]", " ", lowered)
    tokens = " ".join(without_punctuation.split()).split()
    return " ".join(TOKEN_SYNONYMS.get(token, token) for token in tokens)


def _edit_distance(left: str, right: str) -> int:
    """Return Levenshtein edit distance for two short words."""
    if left == right:
        return 0
    if abs(len(left) - len(right)) > 2:
        return 3
    previous = list(range(len(right) + 1))
    for row, left_char in enumerate(left, start=1):
        current = [row]
        for column, right_char in enumerate(right, start=1):
            current.append(min(
                current[-1] + 1,
                previous[column] + 1,
                previous[column - 1] + (left_char != right_char),
            ))
        previous = current
    return previous[-1]


def _token_similarity(expected: str, actual: str) -> int:
    """Score an exact token as 2, a close spelling as 1, and a miss as 0."""
    if expected == actual:
        return 2
    if min(len(expected), len(actual)) < 3 or max(len(expected), len(actual)) < 4:
        return 0
    distance_limit = 2 if max(len(expected), len(actual)) >= 8 else 1
    return 1 if _edit_distance(expected, actual) <= distance_limit else 0


def _phrase_score(normalized_text: str, phrase: str) -> int:
    """Score a phrase over same-length token windows with limited typo tolerance."""
    expected = normalize_text(phrase).split()
    actual = normalized_text.split()
    if not expected or len(expected) > len(actual):
        return 0

    best_score = 0
    allowed_typos = 2 if len(expected) >= 8 else 1
    for start in range(len(actual) - len(expected) + 1):
        scores = [
            _token_similarity(wanted, found)
            for wanted, found in zip(expected, actual[start:start + len(expected)])
        ]
        if 0 not in scores and scores.count(1) <= allowed_typos:
            best_score = max(best_score, sum(scores))
    return best_score


def _best_intent(normalized_text: str) -> str | None:
    """Choose the strongest matching intent; longer and exact phrases score higher."""
    winning_intent: str | None = None
    winning_score = 0
    for intent in INTENT_ORDER:
        phrases = KNOWLEDGE_BASE[intent]["phrases"]
        score = max((_phrase_score(normalized_text, phrase) for phrase in phrases), default=0)
        if score > winning_score:
            winning_intent, winning_score = intent, score
    return winning_intent


class RuleBasedChatbot:
    """Respond using local, transparent NLP features and explicit decision rules."""

    def __init__(self, now_provider: Callable[[], datetime] | None = None) -> None:
        self._now_provider = now_provider or datetime.now

    def respond(self, user_text: str) -> ChatbotReply:
        """Return a deterministic reply with typo-tolerant phrase intent matching."""
        normalized = normalize_text(user_text)
        if not normalized:
            return ChatbotReply(FALLBACK_RESPONSE, "fallback")

        # Exit phrases are complete commands only, to prevent accidental exits.
        if normalized in EXIT_COMMANDS:
            response = str(KNOWLEDGE_BASE["farewell"]["response"])
            return ChatbotReply(response, "farewell", should_exit=True)

        intent = _best_intent(normalized)
        if intent is None:
            return ChatbotReply(FALLBACK_RESPONSE, "fallback")
        elif intent == "time":
            response = f"The current time is {self._now_provider().strftime('%H:%M:%S')}."
        elif intent == "date":
            response = f"Today's date is {self._now_provider().strftime('%A, %B %d, %Y').replace(' 0', ' ')}."
        else:
            response = str(KNOWLEDGE_BASE[intent]["response"])

        return ChatbotReply(response, intent)
