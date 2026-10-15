# RuleBot — Rule-Based AI Chatbot

A transparent, deterministic chatbot built for **Project 1: Rule-Based AI Chatbot** in the DecodeLabs Artificial Intelligence Industrial Training Kit. The project now includes both the original Python command-line version and a responsive browser interface. It uses explicit rules—not a trained model or generative API.

## Rubric coverage

| Project criterion | Implementation |
| --- | --- |
| Handle greetings | Recognizes hello/hi/hey and time-of-day greetings, case-insensitively. |
| Handle exit commands | `bye`, `goodbye`, `exit`, `quit`, `stop`, and `see you` produce a farewell and end the conversation. |
| Use if/else logic | The Python and browser intent routers use ordered `if`/`elif`/`else` decisions. |
| Run continuously | The Python CLI loops until an exit command, EOF, or Ctrl+C. The web interface accepts repeated messages until the user ends or restarts the conversation. |
| Sanitize input | Lowercases, normalizes punctuation, trims, and collapses whitespace before matching. |
| Knowledge base with 5+ intents | Dictionary-driven knowledge base includes greeting, help, identity, time, date, joke, thanks, and farewell. |
| Fallback for unknown input | Unmatched and empty inputs receive a helpful default response. |
| Clean exit | The CLI exits on an exit command; the browser UI closes the active conversation and offers a new-chat action. |

## Python CLI

Requirements: Python 3.10 or newer. No third-party dependencies.

```bash
python -m rule_based_ai_chatbot
```

To install the console command:

```bash
python -m pip install -e .
rule-chatbot
```

## Browser app

The static browser interface is in `web/`. It needs no server-side code, API key, or JavaScript dependencies. To run it locally:

```bash
python -m http.server 8000 --directory web
```

Then open `http://localhost:8000`. Chats are held only in the current browser tab and are not sent to a backend.

## Tests

Python tests:

```bash
python -m unittest discover -s tests -v
```

Browser-rule tests (Node.js 18+):

```bash
npm --prefix web test
```

## Render static-site settings

The web interface can be hosted on Render as a free static site, using the private GitHub repo's `main` branch:

- Build command: `npm --prefix web test`
- Publish directory: `web`
- No environment variables or backend service are required

Static hosting avoids a backend cold start. The public website contains no user account or server-side chat storage; the GitHub source repository remains private.

## Project structure

```text
rule_based_ai_chatbot/
├── pyproject.toml
├── README.md
├── rule_based_ai_chatbot/
│   ├── __init__.py
│   ├── __main__.py
│   ├── chatbot.py       # Python knowledge base, rules, and normalization
│   └── cli.py           # Continuous terminal conversation loop
├── tests/
│   └── test_chatbot.py  # Python unit and loop tests
└── web/
    ├── index.html       # Accessible browser interface
    ├── styles.css       # Responsive visual design
    ├── app.js           # Conversation UI and controls
    ├── bot.js           # Browser-side deterministic intent rules
    ├── bot.test.js      # Node.js tests for browser rules
    └── package.json     # Dependency-free test command
```

## Engineering notes

- **Explainability:** rules are ordered and the matched intent is visible in each browser response.
- **Reliability:** Python date/time responses use an injectable clock; the JS rule engine accepts a test date too.
- **Efficiency:** phrase checks are simple and auditable for this small fixed rule set. For a much larger rule base, use an indexed matcher.
- **Scope:** RuleBot only understands predefined phrases. It does not learn or reason beyond the implemented rules.
