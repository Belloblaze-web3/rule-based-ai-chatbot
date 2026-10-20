# RuleBot

**A transparent, deterministic chatbot built with Python and browser-native JavaScript.**

RuleBot began as DecodeLabs AI Industrial Training Kit **Project 1: Rule-Based AI Chatbot**. It has grown into a Python command-line application and a responsive, static web app, with a lightweight local NLP layer for more flexible intent matching.

[**Try RuleBot live**](https://rulebot-chat.onrender.com) · [**View the GitHub repository**](https://github.com/Belloblaze-web3/rule-based-ai-chatbot)

> RuleBot does not use a trained language model or call an LLM API. Its behavior is driven by explicit, inspectable rules; messages in the web app are processed in the browser.

## Highlights

- **Eight intent groups:** greetings, help, identity, time, date, jokes, thanks, and farewell.
- **Local NLP helpers:** text normalization, selected contraction expansion, synonym and chat-shorthand mapping, typo-tolerant phrase matching, and intent ranking.
- **Two interfaces:** a continuous Python CLI and an accessible, responsive browser chat.
- **Predictable behavior:** explicit intent rules, helpful fallback responses, and clean conversation exits.
- **No runtime dependencies for the web app:** static HTML, CSS, and JavaScript; no server-side chat API or database.

## Try the web app

Open the [live RuleBot site](https://rulebot-chat.onrender.com), or run the static app locally with Python:

```bash
python -m http.server 8000 --directory web
```

Then visit <http://localhost:8000>. Try prompts such as `What can you do?`, `wht can u do?`, `What's today's date?`, or `tell a joke`.

## Run the Python chatbot

**Requirements:** Python 3.10 or newer. The CLI uses only the Python standard library.

From the repository root:

```bash
python -m rule_based_ai_chatbot
```

To install the package and its console command in editable mode:

```bash
python -m pip install -e .
rule-chatbot
```

The CLI continues until an exit command such as `bye`, `goodbye`, `exit`, `quit`, `stop`, or `see you`, or until the input stream ends.

## How the local NLP works

Both implementations follow the same explainable intent-matching approach:

1. **Normalize:** lowercase text, clean punctuation and whitespace, and expand selected contractions.
2. **Canonicalize:** map explicitly listed shorthand and synonyms to common forms.
3. **Match:** compare short token windows against the phrase lexicon, using Levenshtein edit distance for limited typo tolerance.
4. **Choose:** select the strongest matching intent; use a helpful fallback when no rule fits.
5. **Respond:** return a fixed response or compute the current local date/time.

For example, `thx` is mapped to `thanks`; a typo such as `helo` can still match a greeting; and a specific request such as “hey, tell a joke” is ranked above the greeting. Short tokens remain protected from broad fuzzy matching to reduce accidental matches.

This is **bounded lexical NLP**, not open-domain semantic understanding. It does not learn from conversations or answer arbitrary questions. To teach RuleBot new behavior, extend its phrase lexicon and responses, then add regression tests for the new examples.

## Test the project

Run the Python unit tests:

```bash
python -m unittest discover -s tests -v
```

Run the browser intent-engine tests (**Node.js 18 or newer**):

```bash
npm --prefix web test
```

The test suites cover normalization, intent matching, synonyms and typos, date/time responses, fallback handling, exit commands, and the CLI conversation loop.

## Deploy the static site

The browser app is deployed as a Render static site. Its configuration is:

| Setting | Value |
| --- | --- |
| Branch | `main` |
| Build command | `npm --prefix web test` |
| Publish directory | `web` |
| Environment variables | None required |

The site can be served by any static host. The Python CLI is not part of the browser deployment; the chat itself needs no backend service.

## Privacy and limitations

The static app processes chat messages in the user's browser tab and does not send them to an LLM, API, or RuleBot server. It has no user accounts or server-side conversation history. The public demo is intended for showcasing the project, not for handling sensitive information.

## Project structure

```text
rule_based_ai_chatbot/
├── pyproject.toml
├── README.md
├── rule_based_ai_chatbot/
│   ├── __init__.py
│   ├── __main__.py
│   ├── chatbot.py       # Python intent lexicon, local NLP, and response rules
│   └── cli.py           # Continuous terminal chat loop
├── tests/
│   └── test_chatbot.py  # Python unit and CLI loop tests
└── web/
    ├── index.html       # Browser app markup
    ├── styles.css       # Responsive interface styles
    ├── app.js           # Browser chat interactions
    ├── bot.js           # Browser-side NLP and intent engine
    ├── bot.test.js      # Node.js intent-engine tests
    └── package.json     # Dependency-free test command
```

## Presentation

The seven-slide project walkthrough is available as a [PDF](presentation/RuleBot-DecodeLabs-Project-1.pdf). Editable HTML slide sources are in [`presentation/source/`](presentation/source/), with the 16:9 cover image in [`presentation/assets/`](presentation/assets/).

## Project context

RuleBot was created for **Project 1: Rule-Based AI Chatbot** in the DecodeLabs Artificial Intelligence Industrial Training Kit. The project emphasizes foundational AI engineering: clear requirements, input preprocessing, intent classification, deterministic control flow, testing, and deployment.
