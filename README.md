# STA1000 - Data Analytics and Metrics

MSc in Digital Marketing, DCU Business School. 10 credits, NFQ level 9.

Approved descriptor: `module_descriptor_2026/STA1000_2026.pdf`. Read
`docs/module_outline.md` first: the outline this repo is built from diverges from
that descriptor on assessment and on indicative content, and those need a
decision before the module runs.

24 lectures of Quarto revealjs slides, `lecture_01.qmd` to `lecture_24.qmd`,
built to the same conventions as `BAA1030/slides/lecture_8.qmd`.

## Structure

```
STA1000/
├── README.md
├── docs/module_outline.md     module map, blocks, LO mapping
├── lectures/
│   ├── _quarto.yml            single source of truth for all deck formatting
│   ├── theme/metropolis.scss  copied from BAA1030
│   ├── _extensions/           metropolis-theme, produnis/timer, quarto-ext/fontawesome
│   └── lecture_01.qmd ... lecture_24.qmd
├── data/                      datasets used in exercises
└── assignments/               portfolio brief, rubric, submissions
```

## Rendering

```bash
cd lectures
quarto render                  # all decks
quarto render lecture_03.qmd   # one deck
quarto preview lecture_03.qmd  # live reload while editing
```

`_quarto.yml` holds the format block, the theme, the author and the Jupyter
kernel. Individual `.qmd` files carry only `title` and `subtitle`, so changing
the theme or the reveal options is a one-file edit.

Decks with executed Python chunks need `jupyter` plus the packages used in that
deck. Most code chunks are currently `#| eval: false` (displayed, not run), so a
plain render works without a Python environment.

## State of the material

Fully written:

- `lecture_01` Data-driven decisions in marketing, portfolio brief
- `lecture_03` Measurement plan and GA4 implementation
- `lecture_05` Tableau I, provenance, grain, dimensions and measures
- `lecture_06` Describing marketing data
- `lecture_07` Tableau II, calculated fields, Simpson's paradox, cohorts
- `lecture_08` Comparison and segmentation
- `lecture_09` Visualisation for stakeholders
- `lecture_10` From chat to agent
- `lecture_11` Python I, notebooks and pandas
- `lecture_12` Python II, grouping and joining
- `lecture_13` Python III, cohorts, retention, RFM and k-means
- `lecture_14` Python IV, text and social data
- `lecture_16` Core marketing metrics
- `lecture_18` Attribution
- `lecture_19` Experimentation
- `lecture_20` Modelling for decisions

Still scaffolds, with `TODO:` markers where the content goes: `lecture_02`,
`lecture_04`, `lecture_15`, `lecture_17`, `lecture_21`, `lecture_22`,
`lecture_23`, `lecture_24`.

Speaker notes are in HTML comments where the pedagogical intent needed
recording.

## Deck conventions

Established by `lecture_01` and applied to every written deck since:

- `## Previously ...` opener, `## Learning Outcomes`, numbered `#` sections,
  a closing numbered AI section, `## Going Further`, `## Next Lecture`
- `. . .` for incremental reveals; `{background="#43464B"}` for exercises,
  demos and discussions
- `::: {.callout-note appearance="minimal"}` for the question put to the room.
  Borrowed from Wilbur's MGT100; it is what turns a content slide into a
  discussion prompt
- `**Prepare**:` line under `## Next Lecture`, naming what students bring
- `{.smaller}` on dense slides
- **Column widths are 45% (two) or 30% (three).** 48/48, 50/50 and 32/32/32
  wrap and stack vertically under this theme. Do not use them
- Verified: all sixteen written decks render, no slide overflows 700px, no
  column block wraps. `lecture_03`, `lecture_10`, `lecture_11` and `lecture_18`
  each still have one slide slightly over height, from before this check
  existed

## Provenance of the 2026 content pass

Lectures 5-9, 12-14, 16, 19 and 20 were rewritten from scaffolds using
material and structure from public Quarto course repositories:

| Source | Fed into |
|---|---|
| [kennethcwilbur/mgt100](https://github.com/kennethcwilbur/mgt100) (UCSD Rady, Customer Analytics) | 6 (visualise before you summarise, revenue concentration), 8 (heterogeneity, the three tests, circularity, CDP), 13 (C matrix, promotion vs retention, k-means), 16 (revenue decomposition, CLV, CAC, fudge factors, firing customers), 19 (selection vs treatment effects, exogenous variation), 20 (retrodiction, cross-validation, regularisation, elasticity, misuse risks) |
| [simoneSantoni/data-viz-smm635](https://github.com/simoneSantoni/data-viz-smm635) (Bayes, Data Visualisation) | 6 (Anscombe), 9 (Tufte, data-ink, chart junk, before/after critique), and the "Prepare" line, from its Prepare/Participate/Practice/Perform/Ponder week structure |
| [avvorstenbosch/Masterclass-LLMs-for-Data-Science](https://github.com/avvorstenbosch/Masterclass-LLMs-for-Data-Science) | 14 (NLP lifecycle inverted, semantic vs pragmatic, aspect-based sentiment, LLM benchmark picture) |
| [tools4ds/DS701-Course-Notes](https://github.com/tools4ds/DS701-Course-Notes) (BU, Tools for Data Science) | 12 (split-apply-combine), 13 (clustering practice), 19-20 (regression to the mean, Galton) |
| [tsrobinson/me324](https://github.com/tsrobinson/me324) (LSE, AI and Deep Learning) | Structural reference only; its `_quarto-slides.yml`-style dual-config and decktape PDF script were considered and not adopted |

Nothing was copied verbatim. Figures referenced in those repos are not
reproduced here; where a source repo made a point with an image, this repo
makes it with numbers or with a table.

Deliberately not adopted, and available if wanted later:

- **DS701's dual config**: a second `_quarto-slides.yml` so the same sources
  render either as decks or as a student handbook website
- **me324's decktape script**: `tools/make-slide-pdfs.sh` producing a PDF
  beside every deck, published to Pages from `docs/`
- **SMM635's `weeks/week-NN/` layout**: separate lecture, case and summary
  files per week

## Relationship to BAA1030

The BAA1030 `lectures/` decks are thin xaringan wrappers around a shared content
repo at `~/Drive/Projects/lectures/` (`data_analytics/`, `tableau/`, `python/`).
That repo was not available when this was built, so nothing was copied from it.
Lectures 5-9 and 11-14 have since been written from other sources (see
Provenance above), so the BAA1030 material below would now be additive rather
than foundational. Material worth pulling across when it is to hand:

| STA1000 lecture | BAA1030 source |
|---|---|
| 6 Describing marketing data | `data_analytics/visualisation_principle.Rmd` |
| 5, 7 Tableau I and II | `tableau/introduction.Rmd`, `lectures/lecture_5.Rmd` (inline) |
| 9 Visualisation for stakeholders | `data_analytics/visualisation_principle.Rmd` |
| 10 Python I | `python/introduction.Rmd` |
| 11 Python II | `python/wrangling.Rmd` |
| 14 Cleaning | `data_analytics/cleaning_transformations.Rmd` |

Two deliberate divergences from BAA1030:

- **pandas, not polars.** The outline specifies pandas, and it is what marketing
  teams and AI assistants assume. Lecture 11 names polars and says the concepts
  transfer. Reversing this is a find-and-replace plus a syntax pass across
  lectures 11 to 15.
- **No lets-plot.** Visualisation is taught in Tableau (block 2) and the Python
  block stays on data manipulation. Add a plotting lecture by porting
  `BAA1030/slides/lecture_8.qmd` if the balance needs shifting.

## Outstanding

- Resolve the assessment conflict with the approved descriptor (see
  `docs/module_outline.md`); lecture 1 and lecture 24 currently brief a portfolio
  that the descriptor does not contain
- Source or simulate the datasets listed in `docs/module_outline.md`

## AI through the module

AI is threaded through every lecture rather than confined to one:

- **Lecture 10, "From Chat to Agent"**, at the head of the Python block. Fully
  written. Covers the three modes, the four verification checks, what an agent
  must not be given access to, cost, and disclosure.
- **A running spine**, one step per block: chat as a tutor (1-4), chat with your
  data attached (5-9), agentic coding (10-15), an analyst you interrogate
  (16-20), a producer (21-24). Introduced in lecture 1, named in lecture 10, and
  restated at the head of each block's AI section.
- **A closing numbered AI section in every lecture**, following the BAA1030
  pattern of a "Vibe Coding with X" section ending lectures 7, 8 and 9. Each has
  its own exercise.
- Claude is the default named in worked examples, with ChatGPT and Copilot given
  as alternatives.

Three points are made repeatedly: verification is checking output, not reading
code; delegate the typing and keep the deciding; disclose use in three sentences
and own every number.
