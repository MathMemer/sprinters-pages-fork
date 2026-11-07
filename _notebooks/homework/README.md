# CSA Java homework notebooks

My own homework notebooks for the AP CSA Java lessons at `/topics/?category=java`. A lesson that ends with
**"Prepare your submission IPYNB"** asks each student to build a notebook here, publish it on their own site, and
submit that page's link on the lesson page.

**Never push this work to the teacher's repo** (`Open-Coding-Society/pages`). It goes only to my fork,
`MathMemer/sprinters-pages-fork`, and is published at `https://mathmemer.github.io/sprinters-pages-fork/`.
The `teacher` remote is fetch-only and `homework-csa` has no upstream, so a bare `git push` cannot reach it.
No pull requests upstream.

## Status

| Lesson | Notebook | Permalink | Status |
| --- | --- | --- | --- |
| 1.5 Casting and Range | `2025-09-21-csa-unit_01-1_5-hw.ipynb` | `/csa/unit_01/1_5_hw` | built, audited |
| 1.6 Compound Assignment | `2025-09-21-csa-unit_01-1_6-hw.ipynb` | `/csa/unit_01/1_6_hw` | built, audited |
| 1.10 Calling Class Methods | `2025-09-21-csa-unit_01-1_10-hw.ipynb` | `/csa/unit_01/1_10_hw` | built, audited |
| 1.11 Math Class | `2025-09-21-csa-unit_01-1_11-hw.ipynb` | `/csa/unit_01/1_11_student_hw` | built, audited |
| 1.12 Classes & Objects | `2025-09-21-csa-unit_01-1_12-hw.ipynb` | `/csa/unit_01/1_12_hw` | built, audited |
| 2.1 Algorithms with Selection and Repetition | `2025-09-21-csa-unit_02-2_1-hw.ipynb` | `/csa/unit_02/2_1_hw` | built, audited |
| 2.2 Boolean Expressions | `2025-09-21-csa-unit_02-2_2-hw.ipynb` | `/csa/unit_02/2_2_hw` | built, audited |
| 2.3 if Statements | `2025-09-21-csa-unit_02-2_3-hw.ipynb` | `/csa/unit_02/2_3_hw` | built, audited |
| 2.4 Nested `if` Statements | `2025-09-21-csa-unit_02-2_4-hw.ipynb` | `/csa/unit_02/2_4_hw` | built, audited |
| 2.5 Compound Boolean Expressions | `2025-09-21-csa-unit_02-2_5-hw.ipynb` | `/csa/unit_02/2_5_hw` | built, audited |

Not generated yet: Unit 2 (2.6 to 2.12), Unit 3 (3.1, 3.3, 3.7, 3.8, 3.9), Unit 4 (4.2, 4.3, 4.6, 4.7, 4.8, 4.10,
4.13 to 4.15, 4.17). 4.4 and 4.16 say "you do not need to create a separate notebook" (submit the saved code runners instead). Unit 1 lessons whose text does **not** require a notebook, so they are skipped unless asked:
1.7, 1.8 ("a Jupyter notebook or Java file"), 1.9 (submits in the page), 1.13 to 1.15.

"Audited" means `hwlib.audit` passes (see below) and the notebook converts to a page with no runner includes, every code
cell followed by its saved output. The outputs come from real `javac` / `java` 21 runs on this machine.

## Conventions

The lessons leave some things open. This is what every notebook here does, so they stay consistent.

**File and URL**
- File name: `2025-09-21-csa-unit_UU-N_M-hw.ipynb`. The date prefix is required: Jekyll silently skips an undated post.
- Permalink: the one the lesson's front-matter template gives; otherwise `/csa/unit_UU/N_M_hw`.
- Before using a permalink, check it is unused. The teacher already owns `/csa/unit_01/1_9_hw`, `/csa/unit_01/1_11_hw`,
  `/csa/unit_01/1_10/homework` and `/csa/unit_01/1_12/homework`. On a collision use `/csa/unit_UU/N_M_student_hw`.

**Front matter** (cell 0, a *raw* cell; the converter needs raw, even where the lesson says "markdown cell")
- The lesson's template values: `layout: post`, `title: CSA Unit N.M <Topic> HW`, `categories: [Java, <Topic>]`,
  `lesson_language: Java`, `lesson_topic: <Topic> HW`, `lesson_part: interactive`, `lesson_type: lesson`, `permalink`, `author`.
- Added for the same look as the lesson pages: `description`, `lesson_source: APCSA`, `codemirror: true` (it loads the
  code highlighting the lesson pages use), and `menu: nav/csa_units/csaunit<U>.html`.
- `author` is my GitHub id, not the `yourGithubID` placeholder.
- No `assignment`, `team_teach` or `microblog`. The homework is submitted as a link on the teacher's lesson page, and those
  keys would make this page call the teacher's Spring backend.

**Code cells**
- Plain Java code cells. **No `// CODE_RUNNER:` marker**, so there is no Run button. The cell's **last line is
  `ClassName.main(null);`**, which is how a Java kernel runs a class (the lessons ask for exactly this).
- The real output is saved inside the cell (`outputs`). The converter keeps saved outputs for cells without the marker and
  shows them as static text under the code, so the page needs no Java server. It deletes the outputs of marker cells.
- Why not the web runner: the lessons' homework steps say "code cells", "Java cells" and "Choose a Java kernel" and never ask for
  the Run button. On github.io the button posts to the teacher's server, whose CORS allowlist rejects `*.github.io`
  (other students' forks fail the same way), so it would only show "Failed to fetch".
- Exactly one `public class` per cell, and it is the class named in the cell's last line. A non-public helper class is fine
  where the lesson's own starter has one (1.12's `Book` and `Author`).
- A markdown cell precedes every code cell, and a one-line `**Result:**` note follows it ("all predictions matched").
- Output that depends on `Math.random()` says "random values change every run".

**Sections** (headings are `##` or smaller)
1. `## 1. Overview`: link to the lesson through `{{ site.baseurl }}`, key idea, a table of the rules the homework uses,
   and a points table.
2. `## 2. Hacks & Practice Tasks`
   - `### Submission Safety Rules (Read First)`: the lesson's own rules verbatim, plus only the common rules it lacks
     (predict first, output visible, hand traces, explain lines, label tests, one public class, `##` headings).
   - `### Popcorn Hack (In-Class)`: concept, prediction table with a hand trace, code cell with its output, what I learned.
   - `### Homework Hack`: task, concept, "what the important lines do", hand-traced expected values, code cell with its output.
   - `### Submission Notes`: only where the lesson gives a paste-in block. Filled in, except the MCQ line.
   - `### Grading Plan (1 Point Total)`, in the lesson's own form (bullet rubric or table), with a "Where I show it"
     column or sentence for each point. The points add up to 1.0.
   - `#### Quick Validation Checklist`: the lesson's items, each tied to where the notebook meets it.

**Predictions and tests**
- Predictions are written *before* the code cell, with a hand trace, and the `**Result:**` line says whether they matched.
- Every homework has hand-traced expected values and PASS/FAIL checks, including edge cases (the lesson's required cases
  first, then overflow, zero, negative, and boundary values where they apply).
- Where the lesson leaves a choice open (for example 1.11's rarity cutoffs), I pick values and write them in a table.

**Unit 2 differences** (2.1 to 2.12)
- The lesson's front-matter template has no `lesson_part`; I still add it so every notebook has the same keys.
- No paste-in Submission Notes block and no MCQ points: the rubric is Popcorn 0.2 plus the homework parts and 0.1 for notebook quality.
- A written part (2.1's Part 1) goes in a markdown cell, in the lesson's pseudocode style.
- Where the lesson has a "Homework Quick Check", I answer it in a markdown table with the hand trace, then add a small
  code cell that prints the real answer.
- Where the Popcorn is "fix the bugs", the notebook shows the original `javac` error, then the fixed code cell with a comment naming each bug.
- Homework logic goes in a method with parameters so one run can also test edge cases (boundaries and both branches of an `if`).

**MCQ**
- MCQs are taken on the lesson page. I do not invent a score: the `MCQ N.M:` line in the Submission Notes stays
  `<paste your score line ...>` until the MCQ is taken. It is worth 0.2 in those lessons.

## Building and checking

Needs a JDK (`javac`, `java`). From the repo root:

```bash
python3 _notebooks/homework/_build/build_1_6.py     # builds the notebook, runs its Java, saves the output, audits it (exit 1 on failure)
source venv/bin/activate
make convert-single NOTEBOOK_FILE=_notebooks/homework/2025-09-21-csa-unit_01-1_6-hw.ipynb
make serve                                          # then open http://localhost:4500/csa/unit_01/1_6_hw (code, then its saved output)
```

- `_build/hwlib.py`: the shared helpers (`Notebook`, `safety_rules`, `submission_notes`, `java_run`, `java_compile_error`, `outputs_of`)
  and `audit`, which checks the conventions above.
- `_build/build_<lesson>.py`: one script per notebook; 1.5, 1.6, 1.10, 1.11, 1.12 and 2.1 to 2.5 are all built this way.
- Never hand-edit the generated `_posts/homework/*_IPYNB_2_.md`; edit the build script or notebook and convert again.

## Publishing

The fork's Pages site is built by `.github/workflows/jekyll-gh-pages.yml`, which runs `scripts/convert_notebooks.py` on all of
`_notebooks/`, so these notebooks are converted in CI. The workflow sets `baseurl: /sprinters-pages-fork` for the fork, so
internal links must use `{{ site.baseurl }}`. `create_assignments.yml` is guarded so it only runs in the teacher's repo.

The pages have no Run button. Every output is saved in the notebook, so they work on github.io with no backend.
