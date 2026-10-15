"""Deterministic, rule-based chatbot for Project 1.

This module intentionally uses explicit rules rather than a learned or generative
model so that every response is predictable, inspectable, and easy to test.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Callable


# A simple, inspectable knowledge base. Each intent has example phrases and a
# response; the rules below determine which intent is selected.
KNOWLEDGE_BASE: dict[str, dict[str, tuple[str, ...] | str]] = {
    "greeting": {
        "phrases": ("hello", "hi", "hey", "good morning", "good afternoon", "good evening"),
        "response": "Hello! How can I help you today?",
    },
    "help": {
        "phrases": ("help", "what can you do", "what do you do", "commands"),
        "response": "I can chat, tell you the date or time, share a joke, and explain what I can do. Try: 'time', 'date', or 'tell me a joke'.",
    },
    "identity": {
        "phrases": ("your name", "who are you", "what are you"),
        "response": "I'm RuleBot, a small rule-based chatbot built with explicit Python logic.",
    },
    "time": {
        "phrases": ("time", "what time is it", "current time"),
        "response": "",
    },
    "date": {
        "phrases": ("date", "what day is it", "today's date", "todays date"),
        "response": "",
    },
    "joke": {
        "phrases": ("joke", "make me laugh", "tell me something funny"),
        "response": "Why did the computer go to the doctor? It had a virus!",
    },
    "thanks": {
        "phrases": ("thanks", "thank you", "appreciate it"),
        "response": "You're welcome!",
    },
    "farewell": {
        "phrases": (),
        "response": "Goodbye! Thanks for chatting. Enter 'hello' any time to start another conversation.",
    },
}

# Exit phrases are matched as complete commands to avoid accidentally ending
# the chat when a user mentions a word such as "stop" in a longer sentence.
EXIT_COMMANDS = {"bye", "goodbye", "exit", "quit", "stop", "see you"}
FALLBACK_RESPONSE = "I'm not sure how to respond to that yet. Type 'help' to see what I understand."


@dataclass(frozen=True)
class ChatbotReply:
    """A response and its control-flow meaning for the chat loop."""

    text: str
    intent: str
    should_exit: bool = False


def normalize_text(text: str) -> str:
    """Lowercase input, normalize punctuation to spaces, and collapse whitespace."""
    lowered = text.lower().strip()
    without_punctuation = re.sub(r"[^\w\s']", " ", lowered)
    return " ".join(without_punctuation.split())


def _contains_phrase(normalized_text: str, phrase: str) -> bool:
    """Match a phrase on token boundaries, not as an accidental substring."""
    return f" {phrase} " in f" {normalized_text} "


class RuleBasedChatbot:
    """Respond to predefined user inputs using transparent if/elif rules."""

    def __init__(self, now_provider: Callable[[], datetime] | None = None) -> None:
        self._now_provider = now_provider or datetime.now

    def respond(self, user_text: str) -> ChatbotReply:
        """Return one deterministic response for a single user message."""
        normalized = normalize_text(user_text)

        if not normalized:
            return ChatbotReply(FALLBACK_RESPONSE, "fallback")

        # Exit commands take priority and must be entered as a complete command.
        if normalized in EXIT_COMMANDS:
            response = str(KNOWLEDGE_BASE["farewell"]["response"])
            return ChatbotReply(response, "farewell", should_exit=True)
        elif any(_contains_phrase(normalized, phrase) for phrase in KNOWLEDGE_BASE["greeting"]["phrases"]):
            intent = "greeting"
        elif any(_contains_phrase(normalized, phrase) for phrase in KNOWLEDGE_BASE["help"]["phrases"]):
            intent = "help"
        elif any(_contains_phrase(normalized, phrase) for phrase in KNOWLEDGE_BASE["identity"]["phrases"]):
            intent = "identity"
        elif any(_contains_phrase(normalized, phrase) for phrase in KNOWLEDGE_BASE["time"]["phrases"]):
            intent = "time"
        elif any(_contains_phrase(normalized, phrase) for phrase in KNOWLEDGE_BASE["date"]["phrases"]):
            intent = "date"
        elif any(_contains_phrase(normalized, phrase) for phrase in KNOWLEDGE_BASE["joke"]["phrases"]):
            intent = "joke"
        elif any(_contains_phrase(normalized, phrase) for phrase in KNOWLEDGE_BASE["thanks"]["phrases"]):
            intent = "thanks"
        else:
            return ChatbotReply(FALLBACK_RESPONSE, "fallback")

        if intent == "time":
            response = f"The current time is {self._now_provider().strftime('%H:%M:%S')}."
        elif intent == "date":
            response = f"Today's date is {self._now_provider().strftime('%A, %B %d, %Y').replace(' 0', ' ')}."
        else:
            response = str(KNOWLEDGE_BASE[intent]["response"])

        return ChatbotReply(response, intent)
