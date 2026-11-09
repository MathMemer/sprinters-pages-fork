"""Build CSA 2.11 Nested Iteration homework (permalink /csa/unit_02/2_11_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, outputs_of, java_run  # noqa: E402

TOPIC = 'Nested-Iteration'
TITLE = 'CSA Unit 2.11 Nested Iteration HW'
nb = Notebook(2, '11', TOPIC)
nb.front_matter(
    title=TITLE,
    description='Homework for 2.11 Nested Iteration. Print a number triangle with nested loops, count the pairs whose sum is even, and count how many times an inner loop body runs.',
    permalink='/csa/unit_02/2_11_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.11 Nested Iteration]({{ site.baseurl }}/csa/unit_02/2_11). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** a loop inside a loop is **nested iteration**. For **every single pass** of the outer loop, the inner loop starts over and runs completely.

| Part | Runs | Example: `for (i = 0; i < 3; i++)` around `for (j = 0; j < 4; j++)` |
| --- | --- | --- |
| Outer loop | 3 times | `i` is 0, 1, 2 |
| Inner loop | 4 times **for each** outer pass | `j` is 0, 1, 2, 3, then restarts at 0 |
| Inner body | outer passes times inner passes | 3 times 4 = **12** |

**Rows and columns:** think of the outer loop as the rows and the inner loop as the columns. The inner body runs once for every cell of the grid. A `println` placed **after** the inner loop (inside the outer loop) ends each row.

**When the inner bound depends on the outer variable** (for example `j <= i`), the number of inner passes changes from row to row, which is what makes a triangle instead of a rectangle.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Printed a right triangle of numbers, each row counting up to its row number | 0.2 |
| Even-sum pairs | Counted the pairs `(a, b)` with `1 <= a < b <= n` and an even sum (2 for `n = 4`) | 0.5 |
| Quick check | Counted how many times the inner body runs, with the arithmetic shown | 0.2 |
| Notebook quality | Every cell run with output visible, and a markdown cell before each code section | 0.1 |
''')

nb.md('## 2. Hacks & Practice Tasks')
nb.md(safety_rules([
    'Write your prediction before you run each code section',
    'Execute every code cell and leave the output visible',
    'Show your work for any hand-traced prediction',
    'Do not just copy code; explain what each line does',
    'Label each question clearly',
]))

# ---------------------------------------------------------------- popcorn
bad_println = java_run(r'''
public class PrintlnInside {
    public static void main(String[] args) {
        for (int i = 1; i <= 4; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.println(j);          // BUG: println inside the inner loop
            }
        }
    }
}
''').replace('\n', ' ')
nb.md(f'''
### Popcorn Hack (In-Class)

Print a right triangle of numbers where each row counts up to the row number:

```
1
1 2
1 2 3
1 2 3 4
```

**Concept:** the outer loop counts the **rows** (`i` from 1 to `rows`). The inner loop prints the **numbers in one row**, `j` from 1 up to `i`, so its bound is tied to the outer variable: row 1 has one number, row 3 has three. After the inner loop finishes, `System.out.println()` ends the row.

**My predictions (written before I ran the code):** `rows = 4`.

| Outer `i` | Inner `j` runs | Inner passes | Row printed |
| --- | --- | --- | --- |
| 1 | 1 | 1 | `1` |
| 2 | 1, 2 | 2 | `1 2` |
| 3 | 1, 2, 3 | 3 | `1 2 3` |
| 4 | 1, 2, 3, 4 | 4 | `1 2 3 4` |

The inner body runs `1 + 2 + 3 + 4 = 10` times in total (`rows * (rows + 1) / 2`).

| `rows` | Expected output | Inner body runs |
| --- | --- | --- |
| `4` | the four rows above | `10` |
| `1` | `1` | `1` |
| `0` (boundary) | nothing: `1 <= 0` is false, so the outer loop never runs | `0` |
| `5` | the four rows plus `1 2 3 4 5` | `15` |

**A classic mistake.** If the `println` is inside the inner loop instead of after it, every number ends up on its own line and the rows never form. I ran that bug once to check: it prints `{bad_println}` (each value on its own line, joined here with `/`).

**What the important lines do:** the outer `for (int i = 1; i <= rows; i++)` is the row counter. The inner `for (int j = 1; j <= i; j++)` prints the numbers. `if (j > 1)` prints a space *between* numbers, so no row ends with a stray space. `System.out.println()` after the inner loop ends the row. The method `triangle(rows, expected)` builds the same text as a String so it can print PASS or FAIL against my prediction.
''')
nb.runner('Popcorn Hack. A number triangle with nested loops, tested for 4, 1, 0 and 5 rows', r'''
public class NumberTriangle {
    // Prints a triangle with the given number of rows and checks it against my prediction
    static void triangle(int rows, String expected) {
        System.out.println("--- rows " + rows + " ---");
        String shown = "";

        for (int i = 1; i <= rows; i++) {            // outer loop: one pass per row
            for (int j = 1; j <= i; j++) {           // inner loop: its bound depends on the row number
                if (j > 1) {
                    System.out.print(" ");
                    shown = shown + " ";
                }
                System.out.print(j);
                shown = shown + j;
            }
            System.out.println();                    // after the inner loop: ends the row
            shown = shown + "\n";
        }

        System.out.println((shown.equals(expected) ? "PASS: " : "FAIL: ") + rows + " rows match my prediction");
    }

    public static void main(String[] args) {
        triangle(4, "1\n1 2\n1 2 3\n1 2 3 4\n");    // the lesson's case
        triangle(1, "1\n");
        triangle(0, "");                            // boundary: the outer loop never runs
        triangle(5, "1\n1 2\n1 2 3\n1 2 3 4\n1 2 3 4 5\n");
    }
}
''', output_note='all four predictions matched, and the four-row triangle is the one the lesson shows')
nb.md('**What I learned:** the inner bound `j <= i` is what makes it a triangle; with a fixed bound it would be a rectangle. Where the `println` sits decides whether the numbers form rows.')

# ---------------------------------------------------------------- homework
bad_pairs = java_run(r'''
public class SameStart {
    public static void main(String[] args) {
        int n = 4;
        int pairs = 0;
        for (int a = 1; a <= n; a++) {
            for (int b = a; b <= n; b++) {      // BUG: starts at a, so it counts a == b
                if ((a + b) % 2 == 0) {
                    pairs++;
                }
            }
        }
        System.out.println("Even-sum pairs: " + pairs);
    }
}
''')
nb.md(f'''
### Homework Hack

Two short tasks.

1. Finish the code below: count the pairs `(a, b)` with `1 <= a < b <= n` whose sum is even. For `n = 4` the pairs are (1,3) and (2,4), so the answer is 2.
2. Answer the quick check.

#### Task 1: Even-sum pairs

**Concept:** the outer loop picks `a` from 1 to `n`. For each `a`, the inner loop picks `b` from **`a + 1`** to `n`. Starting `b` at `a + 1` does two jobs at once: it guarantees `a < b` (so no pair has `a == b`), and it makes each pair appear **once** (the pair (1,3) comes up as `a = 1, b = 3`, but never again as `a = 3, b = 1`). The `if ((a + b) % 2 == 0)` counts the pairs whose sum has no remainder when divided by 2.

**My predictions (written before I ran the code):** `n = 4`.

| `a` | `b` (from `a + 1` to 4) | Pairs examined | Even sums |
| --- | --- | --- | --- |
| 1 | 2, 3, 4 | (1,2), (1,3), (1,4) | (1,3) |
| 2 | 3, 4 | (2,3), (2,4) | (2,4) |
| 3 | 4 | (3,4) | none |
| 4 | none (`5 <= 4` is false) | none | none |

So 6 pairs are examined (`n(n - 1) / 2 = 4 * 3 / 2`), and 2 have an even sum: **2**, as the lesson says.

A sum is even only when `a` and `b` are **both odd or both even**, so the answer is the number of same-parity pairs: `C(odds, 2) + C(evens, 2)`.

| `n` | Odd numbers, even numbers | Same-parity pairs | Pairs examined `n(n-1)/2` | Expected even-sum pairs |
| --- | --- | --- | --- | --- |
| `4` | 1,3 and 2,4 | 1 + 1 | `6` | `2` |
| `5` | 1,3,5 and 2,4 | 3 + 1 | `10` | `4` |
| `6` | 1,3,5 and 2,4,6 | 3 + 3 | `15` | `6` |
| `1` (boundary) | 1 and none | 0 + 0 | `0` | `0` |
| `2` | 1 and 2 | 0 + 0 (the only pair, (1,2), sums to 3) | `1` | `0` |
| `3` | 1,3 and 2 | 1 + 0 | `3` | `1` |
| `7` | 1,3,5,7 and 2,4,6 | 6 + 3 | `21` | `9` |
| `10` | 1,3,5,7,9 and 2,4,6,8,10 | 10 + 10 | `45` | `20` |

**A classic mistake.** If the inner loop starts at `b = a` instead of `b = a + 1`, it also counts the pairs with `a == b` ((1,1), (2,2), (3,3), (4,4), all with even sums). I ran that bug once for `n = 4`: it prints `{bad_pairs}` instead of 2.

**What the important lines do:** `for (int b = a + 1; b <= n; b++)` is the inner loop, bounded by the outer variable. `checked++` counts every pair examined, and `(a + b) % 2 == 0` counts the even sums. The method `countEvenPairs(n, expected)` checks both numbers against my table. The pairs-checked count must equal `n(n - 1) / 2`: if a pair were counted twice or with `a == b`, it would not.
''')
nb.runner('Homework Hack. Count the pairs with an even sum using nested loops, tested for eight values of n', r'''
public class EvenPairs {
    // Counts the pairs (a, b) with 1 <= a < b <= n whose sum is even
    static void countEvenPairs(int n, int expectedPairs) {
        int pairs = 0;
        int checked = 0;

        for (int a = 1; a <= n; a++) {                 // outer loop: the first number of the pair
            for (int b = a + 1; b <= n; b++) {         // inner loop: starts at a + 1, so a < b and no pair repeats
                checked++;
                if ((a + b) % 2 == 0) {                // even sum
                    pairs++;
                }
            }
        }

        int expectedChecked = n * (n - 1) / 2;
        System.out.println("n = " + n);
        System.out.println("Even-sum pairs: " + pairs);
        System.out.println("Pairs checked: " + checked + " (n(n-1)/2 = " + expectedChecked + ")");
        boolean ok = pairs == expectedPairs && checked == expectedChecked;
        System.out.println((ok ? "PASS: " : "FAIL: ") + "n = " + n + " gives " + expectedPairs);
    }

    public static void main(String[] args) {
        countEvenPairs(4, 2);     // the lesson's case
        countEvenPairs(5, 4);
        countEvenPairs(6, 6);
        countEvenPairs(1, 0);     // boundary: the inner loop never runs
        countEvenPairs(2, 0);
        countEvenPairs(3, 1);
        countEvenPairs(7, 9);
        countEvenPairs(10, 20);
    }
}
''', output_note='all eight predictions matched, and no pair was counted twice or with a == b')

nb.md('''
#### Task 2: Homework quick check

**Question:** how many times does `total++` run?

```java
int total = 0;
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 4; j++) {
        total++;
    }
}
```

**My answer: 12.** The arithmetic: the outer loop runs `i = 0, 1, 2`, which is **3** passes. For each outer pass the inner loop starts over and runs `j = 0, 1, 2, 3`, which is **4** passes. The inner body is run `3 * 4 = 12` times.

| Outer `i` | Inner `j` values | Inner passes | `total` after |
| --- | --- | --- | --- |
| 0 | 0, 1, 2, 3 | 4 | 4 |
| 1 | 0, 1, 2, 3 | 4 | 8 |
| 2 | 0, 1, 2, 3 | 4 | 12 |

I wrote the answer before running the check below, which prints the running total after each outer pass.
''')
nb.runner('Homework quick check. Run to confirm how many times the inner body runs', r'''
public class InnerCount {
    public static void main(String[] args) {
        int total = 0;

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 4; j++) {
                total++;
            }
            System.out.println("after outer pass i = " + i + ": total = " + total);
        }

        System.out.println("total = " + total);
    }
}
''', output_note='the total after each outer pass is 4, 8 and 12, as I answered')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I printed a right triangle of numbers where each row counts up to the row number (rows `1`, `1 2`, `1 2 3`, `1 2 3 4`), and tested 1, 0 and 5 rows as well.

- **0.8 points: Homework completion**
  - **0.5 Even sum pairs:** The nested loop counts the pairs with `1 <= a < b <= n` whose sum is even, printing 2 for `n = 4` (and passing seven more values of `n`).
  - **0.2 Quick check:** The inner body count question is answered (12) with the arithmetic shown (3 outer passes times 4 inner passes).
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: inner loop bound related to the outer variable where the task requires it (`j <= i` in the triangle, `b = a + 1` in the pairs)
- Present: `println` placed after the inner loop so rows break correctly
- Absent: a pair counted twice or counted with `a == b` (the pairs-checked count equals `n(n-1)/2` every time, and the `b = a` bug is shown only as captured output)
- Test: `n = 4` gives 2 pairs and `n = 5` gives 4
''', points=[0.2, 0.5, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
outs = outputs_of(path)
allt = '\n'.join(''.join(c['source']) for c in cells)
nc = [re.sub(r'//.*', '', c) for c in codes]
extra = [
    ('3 code cells (popcorn, homework, quick check)', len(codes) == 3),
    ('triangle: nested for loops with the inner bound j <= i', 'for (int i = 1; i <= rows; i++)' in nc[0] and 'for (int j = 1; j <= i; j++)' in nc[0]),
    ('triangle: println placed after the inner loop (inside the outer loop)',
     re.search(r'for \(int j = 1; j <= i; j\+\+\) \{.*?\n            \}\n            System\.out\.println\(\);', nc[0], re.S) is not None),
    ('lesson triangle printed exactly', '--- rows 4 ---\n1\n1 2\n1 2 3\n1 2 3 4\nPASS:' in outs[0]),
    ('triangle: all four PASS (including 0 rows)', outs[0].count('PASS:') == 4),
    ('pairs: inner loop starts at a + 1 and never at a', 'for (int b = a + 1; b <= n; b++)' in nc[1] and 'b = a;' not in nc[1]),
    ('pairs: condition is (a + b) % 2 == 0', '(a + b) % 2 == 0' in nc[1]),
    ('lesson cases: n=4 -> 2, n=5 -> 4, n=6 -> 6',
     all(f'n = {n}\nEven-sum pairs: {v}\n' in outs[1] for n, v in ((4, 2), (5, 4), (6, 6)))),
    ('pairs: all eight PASS, checked count equals n(n-1)/2 each time', outs[1].count('PASS:') == 8),
    ('quick check: totals 4, 8, 12 and total = 12', all(f'total = {v}' in outs[2] for v in (4, 8, 12))),
    ('mistakes shown as captured output (println inside, b = a)',
     'Even-sum pairs: 6' in allt and re.search(r'prints `1 1 2 1 2 3 1 2 3 4`', allt) is not None),
]
ok = audit(path, {
    'layout': 'post', 'title': TITLE, 'categories': f'[Java, {TOPIC}]', 'lesson_language': 'Java',
    'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_11_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
