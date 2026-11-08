"""Build CSA 2.8 for Loops homework (permalink /csa/unit_02/2_8_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, outputs_of, java_run  # noqa: E402

TOPIC = 'For-Loops'
TITLE = 'CSA Unit 2.08 for Loops HW'
nb = Notebook(2, '8', TOPIC)
nb.front_matter(
    title=TITLE,
    description='Homework for 2.08 for Loops. Print the multiples of 5 with one for loop, compute a factorial, and count iterations from a loop header.',
    permalink='/csa/unit_02/2_8_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.08 for Loops]({{ site.baseurl }}/csa/unit_02/2_8). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** a `for` loop puts the three loop parts in one header, `for (initialise; test; update)`, in the order they run.

| Part | Runs | Example in `for (int i = 1; i <= 5; i++)` |
| --- | --- | --- |
| Initialise | once, before the first test | `int i = 1` |
| Test | before **every** pass; the body runs only if it is `true` | `i <= 5` |
| Update | after **every** pass of the body | `i++` |

It is the same loop as a `while`: `int i = 1; while (i <= 5) { ...; i++; }`.

**Counting iterations exactly:** for a header that starts at `first`, steps by `step`, and stops after `last` (using `<=`), the body runs `(last - first) / step + 1` times. With `<` the last value is **excluded**, which is the classic off-by-one.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Printed the multiples of 5 from 5 to 50 on one line with one `for` loop, then the count (10) | 0.2 |
| Factorial | Computed `n!` with a `for` loop: `5! = 120` (and `0! = 1`) | 0.5 |
| Quick check | Counted the iterations of a loop from its header without running it | 0.2 |
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
less_than = java_run(r'''
public class LessThanBug {
    public static void main(String[] args) {
        int printed = 0;
        for (int value = 5; value < 50; value += 5) {   // BUG: < leaves 50 out
            System.out.print(value + " ");
            printed++;
        }
        System.out.println();
        System.out.println("Printed " + printed + " numbers");
    }
}
''').replace('\n', ' / ')
nb.md(f'''
### Popcorn Hack (In-Class)

Print the multiples of 5 from 5 to 50 on one line, then print how many numbers were printed. Use one `for` loop and no `while`.

**Concept:** the loop variable starts at 5, the test keeps it going while it is `<= 50` (so 50 is included), and the update adds 5 each pass. The body prints the value and adds 1 to `printed`.

**My predictions (written before I ran the code):** the header is `for (int value = 5; value <= 50; value += 5)`.

| Pass | `value` at the test | `value <= 50`? | Body prints | `printed` after |
| --- | --- | --- | --- | --- |
| 1 | `5` | true | `5` | 1 |
| 2 | `10` | true | `10` | 2 |
| 3 to 9 | `15, 20, ... 45` | true | `15 ... 45` | 3 to 9 |
| 10 | `50` | true | `50` | 10 |
| (stop) | `55` | **false** | loop ends | 10 |

Iterations: `(50 - 5) / 5 + 1 = 10`. Expected output: `5 10 15 20 25 30 35 40 45 50` on one line, then `Printed 10 numbers`.

| Step, limit | Hand trace | Expected count |
| --- | --- | --- |
| `5`, `50` | above | `10` |
| `5`, `5` (boundary) | `5 <= 5` is true once, then `10 <= 5` is false | `1` |
| `5`, `4` (boundary) | `5 <= 4` is false at the first test | `0` |
| `7`, `50` | `7, 14, 21, 28, 35, 42, 49`, then `56` stops it | `7` |

**The off-by-one trap.** If I wrote `value < 50` instead of `value <= 50`, the 50 would be left out. I ran that buggy version once to check: it prints `{less_than}`, so it stops at 45 with a count of 9 and the lesson's expected count of 10 is not reached.

**What the important lines do:** `System.out.print(value + " ")` prints without ending the line, so everything stays on one line, and `System.out.println()` then ends it. `printed++` counts each pass. I put the loop in a method `multiples(step, limit, expectedCount)` so one run tests four cases, and each prints PASS or FAIL against my prediction.
''')
nb.runner('Popcorn Hack. Multiples of 5 from 5 to 50 on one line with one for loop, then the count', r'''
public class Multiples {
    // Prints the multiples of step up to limit on one line, then how many were printed
    static void multiples(int step, int limit, int expectedCount) {
        System.out.println("--- multiples of " + step + " up to " + limit + " ---");
        int printed = 0;

        // One for loop: initialise value, test value <= limit, update value += step
        for (int value = step; value <= limit; value += step) {
            System.out.print(value + " ");
            printed++;
        }

        System.out.println();
        System.out.println("Printed " + printed + " numbers");
        System.out.println((printed == expectedCount ? "PASS: " : "FAIL: ") + "expected " + expectedCount);
    }

    public static void main(String[] args) {
        multiples(5, 50, 10);   // the lesson's case: expected count 10
        multiples(5, 5, 1);     // boundary: exactly one pass
        multiples(5, 4, 0);     // boundary: the body never runs
        multiples(7, 50, 7);
    }
}
''', output_note='all four predictions matched, and the lesson case printed a count of 10')
nb.md('**What I learned:** the count comes from the header alone: `(last - first) / step + 1`. The `<=` is correct here because 50 must be included; `<` would silently drop it. A header whose first test is already false (`5 <= 4`) runs zero times.')

# ---------------------------------------------------------------- homework
exact13 = 6227020800
nb.md(f'''
### Homework Hack

Two short tasks.

1. Finish the code below: compute `n!` (n factorial) with a `for` loop. `5!` is `5 * 4 * 3 * 2 * 1 = 120`.
2. Answer the quick check.

#### Task 1: Factorial

**Concept:** `n!` is the product of every whole number from 1 to `n`. Start `result` at **1** (the identity for multiplication; starting at 0 would make every product 0), then multiply it by each value from 1 up to `n`. The header is `for (int i = 1; i <= n; i++)`, and `<=` is needed so `n` itself is multiplied in. For `n = 0` the test `1 <= 0` is false at once, so the loop never runs and `result` stays 1, which is exactly `0! = 1`.

**My predictions (written before I ran the code):** `5!`, one pass at a time:

| Pass | `i` | `result` after `result = result * i` |
| --- | --- | --- |
| start | | `1` |
| 1 | `1` | `1 * 1 = 1` |
| 2 | `2` | `1 * 2 = 2` |
| 3 | `3` | `2 * 3 = 6` |
| 4 | `4` | `6 * 4 = 24` |
| 5 | `5` | `24 * 5 = 120` |

| `n` | Hand trace | Expected `n!` |
| --- | --- | --- |
| `5` | above | `120` |
| `1` | one pass: `1 * 1` | `1` |
| `7` | `120 * 6 = 720`, then `720 * 7` | `5040` |
| `0` (boundary) | the loop never runs, `result` stays 1 | `1` |
| `12` | the largest `n` whose factorial fits in an `int` | `479001600` |

**Overflow (from Unit 1):** `13!` is `{exact13}`, which is more than the largest `int` (`2147483647`). An `int` wraps around: `{exact13} - 2^32 = {exact13 - 4294967296}`, so I predict `13!` computed in an `int` gives `{exact13 - 4294967296}`, not the true value.

**What the important lines do:** `int result = 1;` is the starting value. The `for` header runs `i` from 1 to `n`. `result = result * i;` is the body. The method `factorial(n)` returns the answer, and `main` checks each case against my prediction and prints PASS or FAIL. The last lines compute `13!` exactly in a `long` to show the `int` answer is wrong.
''')
nb.runner('Homework Hack. Factorial with a for loop, tested at 5, 1, 7, 0 and 12, plus the 13 overflow', r'''
public class Factorial {
    // n! computed with one for loop
    static int factorial(int n) {
        int result = 1;                      // multiplying by 1 changes nothing, so it is the right start
        for (int i = 1; i <= n; i++) {       // <= so that n itself is multiplied in
            result = result * i;
        }
        return result;
    }

    // Prints one factorial and checks it against my prediction
    static void show(int n, int expected) {
        int result = factorial(n);
        System.out.println(n + "! = " + result);
        System.out.println((result == expected ? "PASS: " : "FAIL: ") + n + "! is " + expected);
    }

    public static void main(String[] args) {
        show(5, 120);       // the lesson's case
        show(1, 1);
        show(7, 5040);
        show(0, 1);         // boundary: the loop never runs
        show(12, 479001600);

        // 13! no longer fits in an int, so the int answer wraps around
        long exact = 1;
        for (int i = 1; i <= 13; i++) {
            exact = exact * i;
        }
        System.out.println("13! as an int = " + factorial(13) + ", but the true value is " + exact);
    }
}
''', output_note='all five factorials matched, and 13! showed the int overflow I predicted')

nb.md('''
#### Task 2: Homework quick check

**Question:** how many times does the body run?

```java
for (int i = 10; i <= 50; i += 10) {
    System.out.println(i);
}
```

**My answer: 5**, worked out from the header alone, without running the loop:

| Part of the header | Value |
| --- | --- |
| Initialise | `i = 10` |
| Test | `i <= 50` |
| Update | `i += 10` |

`i` is `10, 20, 30, 40, 50` at the test, and each is `<= 50`, so the body runs five times. The next value, `60`, fails the test. By the formula: `(50 - 10) / 10 + 1 = 5`. The `<=` keeps 50 in; with `<` it would be 4.

I wrote the answer before running the check below, which counts the passes.
''')
nb.runner('Homework quick check. Run to count the iterations of the loop', r'''
public class IterationCount {
    public static void main(String[] args) {
        int iterations = 0;

        for (int i = 10; i <= 50; i += 10) {
            System.out.println("i is " + i);
            iterations++;
        }

        System.out.println("Iterations: " + iterations);
    }
}
''', output_note='five iterations, with i = 10, 20, 30, 40, 50, as I answered')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I printed the multiples of 5 from 5 to 50 on one line using a single `for` loop (no `while`), then printed the count, `Printed 10 numbers`.

- **0.8 points: Homework completion**
  - **0.5 Factorial:** A `for` loop computes `n!` correctly, with `5!` printing 120 (and `1!`, `7!`, `0!` and `12!` also passing).
  - **0.2 Quick check:** The iteration count question is answered (5) from the header without running the loop, using the values `10, 20, 30, 40, 50` and the formula `(50 - 10) / 10 + 1`.
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: one `for` loop and no `while` in the Popcorn answer
- Present: factorial verified for at least two values of n (five values pass: 5, 1, 7, 0 and 12)
- Absent: an off by one caused by `<=` where `<` was intended (`<=` is correct in both loops, and the `<` version is shown only as a captured bug)
- Test: `5!` prints 120 and `0!` prints 1
''', points=[0.2, 0.5, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
outs = outputs_of(path)
nc = [re.sub(r'//.*', '', c) for c in codes]
extra = [
    ('3 code cells (popcorn, homework, quick check)', len(codes) == 3),
    ('Popcorn: exactly one for loop and no while', len(re.findall(r'\bfor \(', nc[0])) == 1 and not re.search(r'\bwhile\b', codes[0])),
    ('Popcorn header is value = step; value <= limit; value += step', 'for (int value = step; value <= limit; value += step)' in nc[0]),
    ('Popcorn lesson output: 5 10 ... 50 on one line then Printed 10 numbers',
     '--- multiples of 5 up to 50 ---\n5 10 15 20 25 30 35 40 45 50 \nPrinted 10 numbers\nPASS:' in outs[0]),
    ('Popcorn: all four PASS (including counts 1 and 0 at the boundaries)', outs[0].count('PASS:') == 4),
    ('factorial uses one for loop with i <= n and result starts at 1', 'int result = 1;' in nc[1] and 'for (int i = 1; i <= n; i++)' in nc[1]),
    ('5! = 120 and 0! = 1 in the output', '5! = 120' in outs[1] and '0! = 1' in outs[1]),
    ('factorial verified for at least two values (all five PASS)', outs[1].count('PASS:') == 5),
    ('13! overflow shown with the predicted int value 1932053504 and true value 6227020800',
     '13! as an int = 1932053504, but the true value is 6227020800' in outs[1]),
    ('quick check: 5 iterations, i = 10..50', 'Iterations: 5' in outs[2] and all(f'i is {v}' in outs[2] for v in (10, 20, 30, 40, 50))),
    ('off-by-one demo captured (< leaves out 50, count 9)', 'Printed 9 numbers' in '\n'.join(''.join(c['source']) for c in cells)),
]
ok = audit(path, {
    'layout': 'post', 'title': TITLE, 'categories': f'[Java, {TOPIC}]', 'lesson_language': 'Java',
    'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_8_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
