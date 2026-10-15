"""Command-line interface for RuleBot."""

from __future__ import annotations

from collections.abc import Callable

from .chatbot import RuleBasedChatbot


def run_chat(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    chatbot: RuleBasedChatbot | None = None,
) -> None:
    """Run the conversation until an exit command or end-of-input."""
    bot = chatbot or RuleBasedChatbot()
    output_fn("RuleBot: Hello! I'm RuleBot. Type 'help' for options, or 'quit' to exit.")

    while True:
        try:
            user_text = input_fn("You: ")
        except EOFError:
            output_fn("RuleBot: Input stream closed. Goodbye!")
            return
        except KeyboardInterrupt:
            output_fn("\nRuleBot: Chat interrupted. Goodbye!")
            return

        reply = bot.respond(user_text)
        output_fn(f"RuleBot: {reply.text}")
        if reply.should_exit:
            break


def main() -> None:
    """Start an interactive terminal session."""
    run_chat()
