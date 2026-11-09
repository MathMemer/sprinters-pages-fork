"""Build CSA 2.12 Informal Run-Time Analysis homework (permalink /csa/unit_02/2_12_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, outputs_of  # noqa: E402

TOPIC = 'Run-Time-Analysis'
TITLE = 'CSA Unit 2.12 Informal Run-Time Analysis HW'
nb = Notebook(2, '12', TOPIC)
nb.front_matter(
    title=TITLE,
    description='Homework for 2.12 Informal Run-Time Analysis. Rewrite a loop to do 27 passes instead of 135, predict three execution counts and verify them with counters, and compare two nested loops by their counts.',
    permalink='/csa/unit_02/2_12_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.12 Informal Run-Time Analysis]({{ site.baseurl }}/csa/unit_02/2_12). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** to compare two pieces of code, **count how many times a statement runs**. Counting executions is a fair measure of work. Seconds are not, because they depend on the computer.

| Loop shape | How many passes | Example |
| --- | --- | --- |
| `for (i = a; i < b; i += s)` | `(b - a + s - 1) / s`, rounded up | `i = 0; i < 135; i += 5` is `27` |
| `for (i = a; i <= b; i += s)` | `(b - a) / s + 1`, rounded down, then plus one | `i = 3; i <= 18; i += 5` is `4` |
| Nested, inner bound **independent** of the outer variable | outer passes **times** inner passes | `3 * 4 = 12` |
| Nested, inner bound **depends** on the outer variable | add up the inner passes row by row | `0 + 1 + 2 + 3 = 6` |
| `while (n > 1) { n = n / 4; }` | how many times `n` can be divided by 4 before reaching 1 | `64, 16, 4, 1` is `3` |

**Two loops can print the same thing and do very different amounts of work.** A loop that tests every value and only acts on some of them does far more passes than one that jumps straight to the values it needs.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Rewrote a 135-pass loop as a 27-pass loop with identical output, and proved it with counters | 0.2 |
| Three counts | Predicted the three execution counts first, then verified them with counters | 0.5 |
| Quick check | Counted a nested loop (12) and compared it with the same loop without the step (36) | 0.2 |
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
nb.md('''
### Popcorn Hack (In-Class)

Rewrite the loop so it prints exactly the same numbers with far fewer passes. Keep the counter so you can prove it: the original does 135 passes.

**Concept:** the original loop visits **every** `k` from 0 to 134 (135 passes) but only prints the multiples of 5, so 108 of its 135 passes do nothing useful. The multiples of 5 are exactly 0, 5, 10, ..., 130, so the loop can **step by 5** and skip the others: `for (int k = 0; k < 135; k += 5)`. The `if` is no longer needed, because every `k` the loop reaches is a multiple of 5.

**My predictions (written before I ran the code):**

| Version | Header | Passes |
| --- | --- | --- |
| Original | `k = 0; k < 135; k++` | `135` (k is 0 to 134) |
| Rewritten | `k = 0; k < 135; k += 5` | k is 0, 5, 10, ..., 130, which is `130 / 5 + 1 =` **`27`** |

Both print `0 5 10 ... 130`, which is 27 numbers. So the rewrite does the same printing in `27 / 135`, one fifth of the passes.

| `limit` | `step` | Original passes | Rewritten passes `(limit + step - 1) / step` | Numbers printed |
| --- | --- | --- | --- | --- |
| `135` | `5` | `135` | `27` | 0 to 130 |
| `10` | `5` | `10` | `2` (k is 0 and 5; `10 < 10` is false) | `0 5` |
| `11` | `5` | `11` | `3` (k is 0, 5, 10) | `0 5 10` |
| `1` | `5` | `1` | `1` (k is 0 only) | `0` |
| `0` (boundary) | `5` | `0` | `0` | nothing |

**What the important lines do:** the first loop is the original, kept only so the program can prove the rewrite is the same. It counts its passes in `slowPasses` and builds what it printed into a String. The second loop is the rewrite: `k += step` jumps from multiple to multiple, and `passes++` counts its passes. The method `compare(limit, step, expectedPasses)` checks that both loops produce identical text **and** that the rewritten pass count matches my prediction.
''')
nb.runner('Popcorn Hack. A faster loop with identical output: 27 passes instead of 135, proved with counters', r'''
public class FasterLoop {
    // Runs the original loop and the rewritten loop, and proves they print the same numbers
    static void compare(int limit, int step, int expectedPasses) {
        // Original: visits every k and prints only the multiples of step
        int slowPasses = 0;
        String slow = "";
        for (int k = 0; k < limit; k++) {
            slowPasses++;
            if (k % step == 0) {
                slow = slow + k + " ";
            }
        }

        // Rewritten: jumps straight from one multiple to the next, so the if is not needed
        int passes = 0;
        String fast = "";
        for (int k = 0; k < limit; k += step) {
            passes++;
            fast = fast + k + " ";
        }

        System.out.println("--- limit " + limit + ", step " + step + " ---");
        System.out.println(fast);
        System.out.println("Passes: " + passes);                     // the lesson's goal for 135 is 27
        System.out.println("Original passes: " + slowPasses);        // the lesson says 135
        boolean ok = fast.equals(slow) && passes == expectedPasses;
        System.out.println((ok ? "PASS: " : "FAIL: ") + "identical output in " + expectedPasses + " passes");
    }

    public static void main(String[] args) {
        compare(135, 5, 27);    // the lesson's case
        compare(10, 5, 2);
        compare(11, 5, 3);
        compare(1, 5, 1);
        compare(0, 5, 0);       // boundary: neither loop runs
    }
}
''', output_note='all five predictions matched: identical output, and the lesson case took 27 passes against 135')
nb.md('**What I learned:** I did not just claim the rewrite is faster. The counters show 27 passes against 135, and comparing the printed text proves the output did not change. Dropping the `if` removed the wasted passes entirely.')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

Two short tasks.

1. Finish the code below: predict the three counts in the comments, then add counters to check yourself.
2. Answer the quick check.

#### Task 1: Predict, then count

**Concept:** for each loop I work out the number of times its `println` runs from the loop header alone, write the prediction down, and only **then** add a counter that is incremented next to the `println`.

**My predictions (written before I added the counters):**

**Loop 1:** `for (int i = 3; i <= 18; i += 5)`. The values of `i` are 3, 8, 13, 18, and the next, 23, fails `23 <= 18`. The `<=` keeps 18 in. By the formula, `(18 - 3) / 5 + 1 = 4`. **Prediction: 4.**

**Loop 2:** nested, and the inner bound depends on the outer variable (`j < i`).

| Outer `i` | Inner `j` values (`j < i`) | Inner passes |
| --- | --- | --- |
| 0 | none | 0 |
| 1 | 0 | 1 |
| 2 | 0, 1 | 2 |
| 3 | 0, 1, 2 | 3 |

The total is `0 + 1 + 2 + 3 =` **6.** **Prediction: 6.**

**Loop 3:** `while (n > 1) { n = n / 4; ... }` with `n = 64`.

| Pass | `n` at the test | `n > 1`? | `n` after `n = n / 4` |
| --- | --- | --- | --- |
| 1 | `64` | true | `16` |
| 2 | `16` | true | `4` |
| 3 | `4` | true | `1` |
| (stop) | `1` | **false** | |

The body runs **3** times. **Prediction: 3.**

**What the important lines do:** each `println` stays where it is. `count1++`, `count2++` and `count3++` sit right next to them, so each counter counts exactly the times that `println` runs. At the end the program prints the three counters and checks each against my prediction.
''')
nb.runner('Homework Hack. Predict each count first, then verify it with a counter next to each println', r'''
public class PredictCounts {
    // Compares a counter with the prediction I wrote before adding the counters
    static void check(String label, int actual, int predicted) {
        System.out.println(label + " count: " + actual);
        System.out.println((actual == predicted ? "PASS: " : "FAIL: ") + label + " predicted " + predicted);
    }

    public static void main(String[] args) {
        int count1 = 0;
        int count2 = 0;
        int count3 = 0;

        // Loop 1: how many times does the println run? Prediction: 4
        for (int i = 3; i <= 18; i += 5) {
            System.out.println("Loop 1: " + i);
            count1++;
        }

        // Loop 2: how many times does the println run? Prediction: 6
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < i; j++) {
                System.out.println("Loop 2: " + i + "," + j);
                count2++;
            }
        }

        // Loop 3: how many times does the println run? Prediction: 3
        int n = 64;
        while (n > 1) {
            n = n / 4;
            System.out.println("Loop 3: " + n);
            count3++;
        }

        check("Loop 1", count1, 4);
        check("Loop 2", count2, 6);
        check("Loop 3", count3, 3);
    }
}
''', output_note='all three counters matched my predictions: 4, 6 and 3')

nb.md('''
#### Task 2: Homework quick check

**Question:** how many times does `System.out.println(i + j)` execute?

```java
for (int i = 0; i < 6; i++) {
    for (int j = 0; j < 6; j += 3) {
        System.out.println(i + j);
    }
}
```

**My answer: 12.** The inner bound does not depend on `i`, so I multiply: the outer loop runs `i = 0, 1, 2, 3, 4, 5`, which is **6** passes. The inner loop runs `j = 0, 3` (then `6 < 6` is false), which is **2** passes. `6 * 2 = 12`.

**Comparing with counts.** Suppose `j` stepped by 1 instead of 3 (`j++`). Then the inner loop would run for `j = 0, 1, 2, 3, 4, 5`, which is 6 passes, and the total would be `6 * 6 = 36`. So `j += 3` does the work in `12 / 36`, one third of the passes. The comparison rests on the two counts (12 and 36), not on a guess about speed.

I wrote the answer before running the check below, which counts both versions.
''')
nb.runner('Homework quick check. Run to count both versions of the nested loop', r'''
public class NestedCounts {
    public static void main(String[] args) {
        int stepThree = 0;
        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 6; j += 3) {
                stepThree++;
            }
        }

        int stepOne = 0;
        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 6; j++) {
                stepOne++;
            }
        }

        System.out.println("passes with j += 3: " + stepThree);
        System.out.println("passes with j++:    " + stepOne);
        System.out.println("j += 3 does " + (stepOne / stepThree) + " times fewer passes");
    }
}
''', output_note='12 passes with j += 3 against 36 with j++, as I answered')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I rewrote the loop (`k += 5`, no `if`) to print the same numbers in far fewer passes, and used the counters to prove it against the original 135 passes (27 against 135, with identical output).

- **0.8 points: Homework completion**
  - **0.5 Three counts:** The three execution counts (4, 6 and 3) were predicted first from the loop headers, then verified with counters placed next to each `println`.
  - **0.2 Quick check:** The question is answered (12, with 6 outer passes times 2 inner passes) and compared with the counts that justify it (36 for the version that steps by 1).
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: prediction written before the counters were added (the predictions are in the markdown above the code, and the code comments carry them)
- Present: counters that report the actual number of passes (`passes`, `slowPasses`, `count1`, `count2`, `count3`)
- Absent: a claim about which version is faster with no count to support it (every comparison gives the counts: 27 against 135, and 12 against 36)
- Test: the rewritten Popcorn loop prints identical output with fewer passes
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
    ('rewritten loop steps by step and has no if', 'for (int k = 0; k < limit; k += step)' in nc[0]
     and 'if (' not in re.search(r'for \(int k = 0; k < limit; k \+= step\) \{.*?\n        \}', nc[0], re.S).group(0)),
    ('lesson case: Passes: 27 and Original passes: 135',
     '--- limit 135, step 5 ---' in outs[0] and 'Passes: 27\nOriginal passes: 135\nPASS:' in outs[0]),
    ('lesson case prints 0 5 10 ... 130', '0 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100 105 110 115 120 125 130 \n' in outs[0]),
    ('popcorn: all five PASS (identical output each time)', outs[0].count('PASS:') == 5),
    ('homework counters sit next to each println', all(f'count{n}++;' in nc[1] for n in (1, 2, 3))),
    ('homework predictions written in the comments: 4, 6, 3', all(f'Prediction: {v}' in codes[1] for v in (4, 6, 3))),
    ('homework counts: 4, 6, 3 with all PASS', 'Loop 1 count: 4' in outs[1] and 'Loop 2 count: 6' in outs[1] and 'Loop 3 count: 3' in outs[1] and outs[1].count('PASS:') == 3),
    ('loop 3 printed 16, 4, 1', 'Loop 3: 16\nLoop 3: 4\nLoop 3: 1\n' in outs[1]),
    ('quick check: 12 against 36, three times fewer', 'passes with j += 3: 12' in outs[2] and 'passes with j++:    36' in outs[2] and '3 times fewer' in outs[2]),
    ('every performance claim in the notebook comes with counts', '27' in allt and '135' in allt and '36' in allt),
]
ok = audit(path, {
    'layout': 'post', 'title': TITLE, 'categories': f'[Java, {TOPIC}]', 'lesson_language': 'Java',
    'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_12_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
