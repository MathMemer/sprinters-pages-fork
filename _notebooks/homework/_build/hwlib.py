"""Shared helpers for building the CSA homework notebooks in _notebooks/homework/.

Each build_<lesson>.py script describes one notebook with these helpers, runs the Java to
capture real output, writes the .ipynb, and audits it. See ../README.md for the conventions.

Needs a JDK (javac/java on PATH). Run from anywhere:  python3 _notebooks/homework/_build/build_1_6.py
"""
import json
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]        # repo root
OUT_DIR = ROOT / '_notebooks' / 'homework'
DATE = '2025-09-21'                                        # same date prefix as the teacher's lesson files
AUTHOR = 'MathMemer'                                       # GitHub id used in front matter

# Kernel metadata copied from the teacher's lesson notebooks.
META = {
    'kernelspec': {'display_name': 'Java', 'language': 'java', 'name': 'java'},
    'language_info': {'codemirror_mode': 'java', 'file_extension': '.jshell', 'mimetype': 'text/x-java-source',
                      'name': 'java', 'pygments_lexer': 'java', 'version': '21.0.9+10-LTS'},
}

# ------------------------------------------------------------------ java helpers


def _public_class(src):
    m = re.search(r'^public class (\w+)', src, re.M)
    if not m:
        raise ValueError('cell needs exactly one "public class Name" (the runner calls Name.main(null);)')
    return m.group(1)


def java_run(src, args=()):
    """Compile and run the cell's Java (without the trailer). Returns stdout without the final newline."""
    cls = _public_class(src)
    with tempfile.TemporaryDirectory() as d:
        (pathlib.Path(d) / f'{cls}.java').write_text(src)
        subprocess.run(['javac', f'{cls}.java'], cwd=d, check=True, capture_output=True, text=True)
        done = subprocess.run(['java', cls, *args], cwd=d, check=True, capture_output=True, text=True)
        return done.stdout.rstrip('\n')


def java_compile_error(src):
    """Compile source that is expected NOT to compile. Returns javac's message (first lines)."""
    cls = _public_class(src)
    with tempfile.TemporaryDirectory() as d:
        (pathlib.Path(d) / f'{cls}.java').write_text(src)
        done = subprocess.run(['javac', f'{cls}.java'], cwd=d, capture_output=True, text=True)
        if done.returncode == 0:
            raise AssertionError('expected a compile error but the code compiled')
        return done.stderr.strip()


# ------------------------------------------------------------------ notebook builder


class Notebook:
    def __init__(self, unit, lesson_no, slug_topic):
        """unit=1, lesson_no='5' -> csa-unit_01-1_5-hw ; slug_topic = categories/topic slug from the lesson."""
        self.unit = unit
        self.lesson_no = lesson_no
        self.topic = slug_topic
        self.cells = []
        self.n = 0
        self.points = []
        self.filename = f'{DATE}-csa-unit_{unit:02d}-{unit}_{lesson_no}-hw.ipynb'

    # --- raw cell helpers
    def _id(self, kind):
        self.n += 1
        return f'hw{self.unit}{self.lesson_no}-{kind}-{self.n}'

    @staticmethod
    def _lines(text):
        return text.strip('\n').splitlines(True)

    def front_matter(self, title, description, permalink, categories=None):
        cats = categories or f'[Java, {self.topic}]'
        text = f'''---
layout: post
title: {title}
description: {description}
categories: {cats}
lesson_language: Java
lesson_topic: {self.topic} HW
lesson_part: interactive
lesson_source: APCSA
lesson_type: lesson
codemirror: true
permalink: {permalink}
menu: nav/csa_units/csaunit{self.unit}.html
author: {AUTHOR}
---'''
        self.permalink = permalink
        self.cells.append({'cell_type': 'raw', 'id': self._id('frontmatter'), 'metadata': {}, 'source': self._lines(text)})

    def md(self, text):
        self.cells.append({'cell_type': 'markdown', 'id': self._id('md'), 'metadata': {}, 'source': self._lines(text)})

    def runner(self, challenge, src, show_output=True, output_note='all predictions matched', output_text=None,
               random_note=False):
        """Add a CODE_RUNNER cell (ends with ClassName.main(null);) and, after it, a visible output block."""
        cls = _public_class(src)
        body = f'// CODE_RUNNER: {challenge}\n' + src.rstrip('\n') + f'\n\n{cls}.main(null);\n'
        self.cells.append({'cell_type': 'code', 'execution_count': None, 'id': self._id('code'), 'metadata': {},
                           'outputs': [], 'source': self._lines(body)})
        if show_output:
            out = output_text if output_text is not None else java_run(src)
            note = f'{output_note}; random values change every run' if random_note else output_note
            self.md(f'**Output from my run** ({note}):\n\n```\n{out}\n```')

    def rubric(self, text, points):
        """Add the grading section. `points` are the leaf points; they must sum to 1.0 (lesson convention)."""
        assert abs(sum(points) - 1.0) < 1e-9, f'rubric points sum to {sum(points)}, not 1.0'
        self.points = points
        self.md(text)

    def write(self):
        path = OUT_DIR / self.filename
        nb = {'cells': self.cells, 'metadata': META, 'nbformat': 4, 'nbformat_minor': 5}
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n')
        return path


# ------------------------------------------------------------------ shared markdown blocks

# (regex that means "the lesson already says this", rule text). A common rule is added only when
# none of the lesson's own rules match its regex.
COMMON_RULES = [
    (r'predict', 'Write my predictions before running each code section'),
    (r'output|running|run each|execute', 'Execute every code cell and leave the output visible'),
    (r'hand', 'Show my work for hand-traced predictions'),
    (r'explain|comment', 'Explain what the important lines do; do not just copy code'),
    (r'label', 'Label each question or test clearly'),
    (r'main\(null\)|one (public )?class', 'One public class per cell, ending with `ClassName.main(null);`'),
    (r'##', 'Use `##` headings or smaller'),
]


def safety_rules(lesson_rules=()):
    """The lesson's own rules first (verbatim), then only the common rules the lesson does not already state."""
    rules = list(lesson_rules)
    joined = ' '.join(rules).lower()
    rules += [text for pattern, text in COMMON_RULES if not re.search(pattern, joined)]
    return '### Submission Safety Rules (Read First)\n\n' + '\n'.join(f'- {r}' for r in rules)


def submission_notes(lines):
    return ('### Submission Notes\n\nThe lesson asks for this text in the description box when I submit the link to this page. '
            'The MCQ score comes from the lesson page, so that line is filled in after I take the MCQ there.\n\n```\n'
            + '\n'.join(lines) + '\n```')


# ------------------------------------------------------------------ audit


def audit(path, template, expect_runners, extra=()):
    """Check a built notebook against the section 6 conventions. `template` = front matter values the lesson requires."""
    nb = json.load(open(path))
    cs = nb['cells']
    src = lambda c: ''.join(c['source'])
    allt = '\n'.join(src(c) for c in cs)
    fm = src(cs[0])
    keys = dict(l.split(': ', 1) for l in fm.split('\n')[1:-1] if ': ' in l)
    codes = [i for i, c in enumerate(cs) if c['cell_type'] == 'code']
    res = []

    def chk(name, ok):
        res.append((name, bool(ok)))

    chk('cell 0 is raw front matter', cs[0]['cell_type'] == 'raw' and fm.startswith('---') and fm.rstrip().endswith('---'))
    chk('front matter matches the lesson template', all(keys.get(k) == v for k, v in template.items()))
    chk('author is a GitHub id', keys.get('author') not in (None, 'yourGithubID'))
    chk('codemirror: true', keys.get('codemirror') == 'true')
    chk('no assignment/team_teach/microblog keys', not any(k in keys for k in ('assignment', 'team_teach', 'microblog')))
    chk(f'{expect_runners} code runners', len(codes) == expect_runners)
    chk('every code cell preceded by a markdown cell', all(cs[i - 1]['cell_type'] == 'markdown' for i in codes))
    chk('every code cell ends with ClassName.main(null);',
        all(re.match(r'^\w+\.main\(null\);$', src(cs[i]).strip().split('\n')[-1]) for i in codes))
    chk('CODE_RUNNER marker uses the colon form', all(src(cs[i]).startswith('// CODE_RUNNER: ') for i in codes))
    chk('exactly one public class per code cell',
        all(len(re.findall(r'^public class ', src(cs[i]), re.M)) == 1 for i in codes))
    chk('output block after every runner', all('Output from my run' in src(cs[i + 1]) or 'Compiler message' in src(cs[i + 1])
                                               for i in codes))
    chk('prediction/expected content before every runner',
        all(re.search(r'prediction|expected|trace|My ', src(cs[i - 1]), re.I) for i in codes))
    chk('no FAIL in saved outputs', 'FAIL:' not in ''.join(src(c) for c in cs if 'Output from my run' in src(c)))
    chk('Submission Safety Rules present', 'Submission Safety Rules (Read First)' in allt)
    chk('Grading Plan (1 Point Total) present', 'Grading Plan (1 Point Total)' in allt)
    chk('Quick Validation Checklist present', 'Quick Validation Checklist' in allt)
    body = allt.split('---', 2)[2] if allt.startswith('---') else allt
    chk('no heading above ##', not re.search(r'^# ', body, re.M))
    chk('internal links use {{ site.baseurl }}', not re.search(r'\]\(/csa/', allt))
    for name, ok in extra:
        chk(name, ok)
    bad = [n for n, o in res if not o]
    for n, o in res:
        print(('PASS ' if o else 'FAIL ') + n)
    print(f'\n{len(res) - len(bad)}/{len(res)} checks passed' + ('' if not bad else f'  FAILED: {bad}'))
    return not bad
