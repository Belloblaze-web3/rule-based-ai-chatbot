# RuleBot — Rule-Based AI Chatbot

A transparent, deterministic chatbot built for **Project 1: Rule-Based AI Chatbot** in the DecodeLabs Artificial Intelligence Industrial Training Kit. The project includes the original Python command-line version and a responsive browser app. Both now use lightweight, fully local NLP helpers—not a trained model or generative API.

## Local NLP capabilities

- **Normalization:** lowercase text, punctuation cleanup, whitespace cleanup, and common contraction expansion (`what's` → `what is`).
- **Synonyms and chat shorthand:** handles a small explicit map such as `hiya` → `hello`, `u` → `you`, and `thx` → `thanks`.
- **Typo tolerance:** matches short intent phrases with Levenshtein edit-distance scoring while keeping short words and unrelated text from matching accidentally.
- **Intent ranking:** longer, more specific matching phrases can win when a message contains more than one intent (for example, a greeting plus a joke request).
- **Temporal phrasing:** recognizes natural date/time variants and formats results with the local clock available to the CLI or browser.

This is deliberately bounded local NLP. Messages are not sent to a model or external API; the bot does not understand arbitrary topics beyond its phrase lexicon.

## Rubric coverage

| Project criterion | Implementation |
| --- | --- |
| Handle greetings | Recognizes greetings, time-of-day greetings, common synonyms, and small spelling errors. |
| Handle exit commands | `bye`, `goodbye`, `exit`, `quit`, `stop`, and `see you` produce a farewell and end the conversation. |
| Use if/else logic | The Python and browser intent routers use explicit deterministic decision branches. |
| Run continuously | The Python CLI loops until an exit command, EOF, or Ctrl+C. The web interface accepts repeated messages until the user ends or restarts the conversation. |
| Sanitize input | Expands selected contractions, canonicalizes synonyms, normalizes punctuation and whitespace, then scores token-boundary phrase matches. |
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

The browser interface is hosted on Render as a free static site, using the private GitHub repo's `main` branch:

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
│   ├── chatbot.py       # Python knowledge base, local NLP, and rules
│   └── cli.py           # Continuous terminal conversation loop
├── tests/
│   └── test_chatbot.py  # Python unit and loop tests
└── web/
    ├── index.html       # Accessible browser interface
    ├── styles.css       # Responsive visual design
    ├── app.js           # Conversation UI and controls
    ├── bot.js           # Browser-side local NLP and deterministic rules
    ├── bot.test.js      # Node.js tests for browser behavior
    └── package.json     # Dependency-free test command
```

## Engineering notes

- **Explainability:** rule phrases, token aliases, typo thresholds, and the winning intent are inspectable in source.
- **Reliability:** Python date/time responses use an injectable clock; the JS rule engine accepts a test date too.
- **Efficiency:** edit-distance work is limited to short tokens and a small fixed phrase set.
- **Privacy:** no model, API key, or network service is used to process messages.
- **Scope:** this is local lexical NLP, not open-domain semantic reasoning. Add a trained model or LLM only if broader answers are required and the additional hosting/API trade-offs are acceptable.
