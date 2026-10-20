## Design Concept
This deck serves as a technical walkthrough and pedagogical presentation for professional learners, showcasing a software engineering project. It anchors itself in the aesthetic of a modern developer IDE or CLI environment—borrowing the dark canvas and monospace constraints of tools like VS Code or Terminal—while applying the rigorous grid and typographic scale of Swiss International Style to ensure it functions as a readable presentation, not a website. The color story is cool, deliberate, and high-contrast: a dark charcoal background establishes the engineering environment, while crisp white typography ensures projection legibility. A vibrant teal serves as the sole accent for logic flows and highlights, deliberately avoiding the worn-out "hacker neon green" cliché in favor of a mature, production-ready aesthetic. The typographic voice is utilitarian and precise, pairing a clean geometric sans-serif for narrative clarity with a monospace typeface for technical labels and system states.

## Visual Language
- **Imagery**: Supporting role only. Purely decorative imagery is strictly prohibited. The user-provided RuleBot screenshot appears exclusively on the product experience slide, housed in a portrait frame that fits within the canvas height without cropping any UI contents.
- **Containers**: Whitespace-first grid layout. Code snippets, NLP rules, and case comparisons are enclosed in subtle dark-gray rounded cards to differentiate them from the main charcoal canvas.
- **Icons**: Minimalist, solid icons used exclusively within system pipeline diagrams to denote data states; never used as generic bullet points.
- **Dataviz**: Tables are used for NLP scoring comparisons (e.g., Levenshtein typo examples) with teal text highlighting successful matches and gray text for discarded inputs. Charts are unnecessary for this scope.
- **Motif**: A monospace text string `[ input → intent → response ]` acts as a recurring pipeline indicator, placed consistently in the top right corner of every slide. The active stage of the pipeline can be highlighted in teal depending on the slide's focus.

## Layout Directives
- **Global**: 60px margins on all sides; motif at top right; slide numbers at bottom right; all text left-aligned to mirror code formatting.
- **Cover**: Massive sans-serif title, monospace subtitle, featuring a teal terminal cursor block at the end of the title.
- **Table of Contents**: Rendered as a horizontal system pipeline flowchart rather than a bulleted list.
- **Section Dividers**: Echo a CLI prompt (e.g., `> execute section_name`) centered on the canvas.
- **Closing**: Echoes the cover layout with a system exit command (`return 0;`).
- **Slide Map**:

| id | pattern | image | density |
| :--- | :--- | :--- | :--- |
| cover | Centered title with monospace subtitle | none | low |
| project_brief | Two-column: problem statement left, scope bulleted right | none | medium |
| system_flow | Full-page horizontal process diagram | none | medium-high |
| experience | Two-column: portrait screenshot left, descriptive text right | hero | medium |
| local_nlp | Concept explanation above a comparison data table | none | high |
| engineering | Grid of four rounded cards detailing intent rules | none | medium-high |
| deployment | Text-left, system architecture diagram right | none | medium |

## Design Tokens

| token | hex | usage |
| :--- | :--- | :--- |
| bg-canvas | #18181B | Global page background (dark charcoal) |
| bg-card | #27272A | Background for code, tables, and concept cards |
| text-main | #F4F4F5 | Primary headings and body text (crisp white) |
| text-muted | #A1A1AA | Captions, secondary labels, and inactive motif states |
| accent-teal | #0D9488 | System flow arrows, highlights, and active motif states |
| border-line | #3F3F46 | Subtle borders for tables and UI frames |

| role | family | size (px) | applies_to |
| :--- | :--- | :--- | :--- |
| display | Inter | 56 | Cover and divider titles |
| heading | Inter | 36 | Slide titles |
| body | Inter | 20 | Main paragraph text and primary bullets |
| monospace | JetBrains Mono | 18 | Motif, code snippets, NLP labels, and table data |
| caption | Inter | 14 | Source notes and slide numbers |

## Guardrails
- **Forbidden**: Do not use neon gradients or glowing drop shadows; do not crop the UI screenshot to fit a landscape box; do not invent conversational placeholder text or fake metrics; do not use pure white (#FFFFFF) for backgrounds.
- **Size floors**: body ≥18px, monospace labels ≥18px, caption ≥14px. Minimum text size inside diagrams is 16px.
