# RuleBot — Rule-Based AI Chatbot

A small, transparent command-line chatbot built for **Project 1: Rule-Based AI Chatbot** in the DecodeLabs Artificial Intelligence Industrial Training Kit. It demonstrates deterministic AI foundations with explicit Python control flow—no model, API, or network access is used.

## Rubric coverage

| Project criterion | Implementation |
| --- | --- |
| Handle greetings | Recognizes hello/hi/hey and time-of-day greetings, case-insensitively. |
| Handle exit commands | `bye`, `goodbye`, `exit`, `quit`, `stop`, and `see you` produce a farewell and stop the loop. |
| Use if/else logic | `RuleBasedChatbot.respond()` uses an ordered `if`/`elif`/`else` decision tree. |
| Run continuously | `run_chat()` loops until an exit command, EOF, or Ctrl+C. |
| Sanitize input | Lowercases, normalizes punctuation, trims, and collapses whitespace before matching. |
| Knowledge base with 5+ intents | Dictionary-driven knowledge base includes greeting, help, identity, time, date, joke, thanks, and farewell. |
| Fallback for unknown input | Unmatched and empty inputs receive a helpful default response. |
| Clean exit | Exit commands generate a farewell and break the loop; EOF and Ctrl+C are handled gracefully. |

## Requirements

- Python 3.10 or newer
- No third-party dependencies

## Run

From this directory:

```bash
python -m rule_based_ai_chatbot
```

Or install it in editable mode to use the console command:

```bash
python -m pip install -e .
rule-chatbot
```

Type `help` for example requests. Type `quit` (or another supported exit command) to leave.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Example session

```text
RuleBot: Hello! I'm RuleBot. Type 'help' for options, or 'quit' to exit.
You:   HI!!
RuleBot: Hello! How can I help you today?
You: tell me a joke
RuleBot: Why did the computer go to the doctor? It had a virus!
You: what time is it?
RuleBot: The current time is 14:05:09.
You: quit
RuleBot: Goodbye! Thanks for chatting. Enter 'hello' any time to start another conversation.
```

## Project structure

```text
rule_based_ai_chatbot/
├── pyproject.toml
├── README.md
├── rule_based_ai_chatbot/
│   ├── __init__.py
│   ├── __main__.py
│   ├── chatbot.py       # Knowledge base, normalization, and deterministic rules
│   └── cli.py           # Continuous terminal conversation loop
└── tests/
    └── test_chatbot.py  # Unit and loop tests; standard-library unittest
```

## Engineering notes

- **Explainability:** rules are ordered and the matched intent is returned with each reply.
- **Reliability:** date/time use an injectable clock, so behavior can be tested deterministically.
- **Efficiency:** intent matching uses a small fixed set of phrase checks; responses are looked up by intent in a dictionary. For a tiny training bot this is easy to audit; for a very large rule base, use a trie or indexed matcher.
- **Scope:** this is deliberately a rule-based chatbot, not a language model. It only understands its predefined phrases and does not claim to learn or reason beyond them.
