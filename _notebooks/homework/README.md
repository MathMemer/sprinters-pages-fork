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

Not generated yet: Unit 2 (2.1 to 2.12), Unit 3 (3.1, 3.3, 3.7, 3.8, 3.9), Unit 4 (4.2, 4.3, 4.6, 4.7, 4.8, 4.10,
4.13 to 4.15, 4.17). Unit 1 lessons whose text does **not** require a notebook, so they are skipped unless asked:
1.7, 1.8 ("a Jupyter notebook or Java file"), 1.9 (submits in the page), 1.13 to 1.15.

"Audited" means `hwlib.audit` passes (see below) and the notebook converts to a page with one Run button per code cell.
It does not mean the Run button was tested against a live Java backend.

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
- Added for the same look as the lesson pages: `description`, `lesson_source: APCSA`, `codemirror: true` (without it the
  editor and Run button do not load), and `menu: nav/csa_units/csaunit<U>.html`.
- `author` is my GitHub id, not the `yourGithubID` placeholder.
- No `assignment`, `team_teach` or `microblog`. The homework is submitted as a link on the teacher's lesson page, and those
  keys would make this page call the teacher's Spring backend.

**Code cells**
- Every runner starts with `// CODE_RUNNER: <challenge>` (with the colon) and its **last line is `ClassName.main(null);`**.
  The converter only makes a Run button for a Java cell that ends this way. Some lesson cells miss it, so they have no button.
- Exactly one `public class` per cell, and it is the class the runner calls. A non-public helper class is fine where the
  lesson's own starter has one (1.12's `Book` and `Author`).
- A markdown cell precedes every runner, and an `Output from my run` block follows it. The converter clears runner
  outputs, so the real output is saved in that block (from a real `javac` / `java` run).
- Output that depends on `Math.random()` says "random values change every run".

**Sections** (headings are `##` or smaller)
1. `## 1. Overview`: link to the lesson through `{{ site.baseurl }}`, key idea, a table of the rules the homework uses,
   and a points table.
2. `## 2. Hacks & Practice Tasks`
   - `### Submission Safety Rules (Read First)`: the lesson's own rules verbatim, plus only the common rules it lacks
     (predict first, output visible, hand traces, explain lines, label tests, one public class, `##` headings).
   - `### Popcorn Hack (In-Class)`: concept, prediction table with a hand trace, runner, output, what I learned.
   - `### Homework Hack`: task, concept, "what the important lines do", hand-traced expected values, runner, output.
   - `### Submission Notes`: only where the lesson gives a paste-in block. Filled in, except the MCQ line.
   - `### Grading Plan (1 Point Total)`, in the lesson's own form (bullet rubric or table), with a "Where I show it"
     column or sentence for each point. The points add up to 1.0.
   - `#### Quick Validation Checklist`: the lesson's items, each tied to where the notebook meets it.

**Predictions and tests**
- Predictions are written *before* the runner, with a hand trace, and the output block says whether they matched.
- Every homework has hand-traced expected values and PASS/FAIL checks, including edge cases (the lesson's required cases
  first, then overflow, zero, negative, and boundary values where they apply).
- Where the lesson leaves a choice open (for example 1.11's rarity cutoffs), I pick values and write them in a table.

**MCQ**
- MCQs are taken on the lesson page. I do not invent a score: the `MCQ N.M:` line in the Submission Notes stays
  `<paste your score line ...>` until the MCQ is taken. It is worth 0.2 in those lessons.

## Building and checking

Needs a JDK (`javac`, `java`). From the repo root:

```bash
python3 _notebooks/homework/_build/build_1_6.py     # builds the notebook, runs its Java, audits it (exit 1 on failure)
source venv/bin/activate
make convert-single NOTEBOOK_FILE=_notebooks/homework/2025-09-21-csa-unit_01-1_6-hw.ipynb
make serve                                          # then open http://localhost:4500/csa/unit_01/1_6_hw
```

- `_build/hwlib.py`: the shared helpers (`Notebook`, `safety_rules`, `submission_notes`, `java_run`, `java_compile_error`)
  and `audit`, which checks the conventions above.
- `_build/build_<lesson>.py`: one script per notebook; 1.6, 1.10, 1.11 and 1.12 are built this way.
  The 1.5 notebook was built earlier by a one-off script, and it passes the same audit.
- Never hand-edit the generated `_posts/homework/*_IPYNB_2_.md`; edit the build script or notebook and convert again.

## Publishing

The fork's Pages site is built by `.github/workflows/jekyll-gh-pages.yml`, which runs `scripts/convert_notebooks.py` on all of
`_notebooks/`, so these notebooks are converted in CI. The workflow sets `baseurl: /sprinters-pages-fork` for the fork, so
internal links must use `{{ site.baseurl }}`. `create_assignments.yml` is guarded so it only runs in the teacher's repo.

On github.io the Run button posts to the teacher's Java server, which may refuse the request. The saved
`Output from my run` blocks stay visible either way.
