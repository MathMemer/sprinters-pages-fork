"""Build CSA 2.7 while Loops homework (permalink /csa/unit_02/2_7_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, outputs_of, java_run  # noqa: E402

TOPIC = 'While-Loops'
TITLE = 'CSA Unit 2.07 while Loops HW'
nb = Notebook(2, '7', TOPIC)
nb.front_matter(
    title=TITLE,
    description='Homework for 2.07 while Loops. Write a countdown, double an amount until it reaches a goal, and trace how many times a loop body runs.',
    permalink='/csa/unit_02/2_7_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.07 while Loops]({{ site.baseurl }}/csa/unit_02/2_7). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** a `while` loop repeats its body **while its condition is true**. The condition is tested *before* every pass, so the body can run zero times.

A loop has three parts, and all three must be present and in the right place:

| Part | What it does | Where it goes |
| --- | --- | --- |
| Initialise | Gives the control variable its starting value | before the loop |
| Test | The condition in `while (...)`; the loop continues while it is `true` | in the parentheses |
| Update | Changes the control variable so the loop moves toward stopping | **inside** the body |

**Two classic bugs:** a missing or misplaced update makes an **infinite loop** (the condition never becomes false), and a wrong comparison (`>` where `>=` is needed) makes an **off-by-one** loop that runs one pass too few or too many.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Wrote the countdown from 5 to 1, then `Liftoff!`, ending because of its condition | 0.2 |
| Doubling loop | Doubled `amount` until it reached `goal`, counting the doublings (1600 and 4) | 0.5 |
| Quick check | Counted the passes of a loop and listed the control variable's values | 0.2 |
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
off_by_one = java_run(r'''
public class OffByOne {
    public static void main(String[] args) {
        int count = 5;
        while (count > 1) {          // BUG: should be >= 1
            System.out.println(count);
            count--;
        }
        System.out.println("Liftoff!");
    }
}
''').replace('\n', ' ')
nb.md(f'''
### Popcorn Hack (In-Class)

Write a countdown. Starting from `start`, print each number down to 1, then print `Liftoff!`. The loop must end because of its condition.

**Concept:** the control variable `count` starts at `start`. The loop keeps going while there is still a number to print (`count >= 1`), and each pass moves `count` down by one, so the condition eventually becomes false by itself. No `break` is needed.

**My predictions (written before I ran the code):** the control variable's value each time the test runs, for `start = 5`:

| Test number | `count` at the test | `count >= 1`? | What happens |
| --- | --- | --- | --- |
| 1 | `5` | true | print `5`, then `count` becomes `4` |
| 2 | `4` | true | print `4`, then `3` |
| 3 | `3` | true | print `3`, then `2` |
| 4 | `2` | true | print `2`, then `1` |
| 5 | `1` | true | print `1`, then `0` |
| 6 | `0` | **false** | the loop ends; `Liftoff!` prints |

So the output is `5 4 3 2 1` and then `Liftoff!`, from five passes.

| `start` | Passes | Prints |
| --- | --- | --- |
| `5` | 5 | `5 4 3 2 1 Liftoff!` |
| `1` | 1 | `1 Liftoff!` |
| `0` (boundary) | 0: `0 >= 1` is false at the very first test | `Liftoff!` only |
| `-3` | 0 | `Liftoff!` only |

**The off-by-one trap.** If I wrote `count > 1` instead of `count >= 1`, the test would fail at `count = 1`, and the `1` would never print. I ran that buggy version once to check (it is bounded, so it stops): it prints `{off_by_one}`, missing the `1`.

**What the important lines do:** `int count = start;` initialises. `while (count >= 1)` tests. `count--;` is the update, **inside** the body. The method `countdown(start, expected)` lets one run test four starting values, and it builds the printed sequence as a String so it can print PASS or FAIL against my prediction.
''')
nb.runner('Popcorn Hack. The countdown with a while loop, tested for start 5, 1, 0 and -3', r'''
public class Countdown {
    // Counts down from start to 1, then prints Liftoff!, and checks the sequence against my prediction
    static void countdown(int start, String expected) {
        System.out.println("--- start " + start + " ---");
        String shown = "";

        int count = start;               // initialise the control variable
        while (count >= 1) {             // test: continue while there is still a number to print
            System.out.println(count);
            shown = shown + count + " ";
            count--;                     // update: inside the body, moving toward the stopping condition
        }

        System.out.println("Liftoff!");
        shown = shown + "Liftoff!";
        System.out.println((shown.equals(expected) ? "PASS: " : "FAIL: ") + "printed " + expected);
    }

    public static void main(String[] args) {
        countdown(5, "5 4 3 2 1 Liftoff!");   // the lesson's value
        countdown(1, "1 Liftoff!");
        countdown(0, "Liftoff!");             // boundary: the body never runs
        countdown(-3, "Liftoff!");
    }
}
''', output_note='all four predictions matched, and the loop ended because of its condition each time')
nb.md('**What I learned:** the loop stops by itself because `count--` keeps moving `count` toward the point where `count >= 1` is false. With `start = 0` the test is false before the first pass, so a `while` loop can run zero times.')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

Two short tasks.

1. Finish the code below: keep doubling `amount` until it is at least `goal`, counting how many doublings it took.
2. Answer the quick check.

#### Task 1: Doubling until the goal

**Concept:** the loop must continue **while the goal has not been reached**, so the test is `amount < goal`. Each pass doubles `amount` and adds 1 to `doublings`. Both updates go **inside** the body: if `amount` were never changed, the condition would stay true forever.

**My predictions (written before I ran the code):** the lesson's values, `amount = 100`, `goal = 1000`:

| Test | `amount` at the test | `amount < 1000`? | Body | `doublings` after |
| --- | --- | --- | --- | --- |
| 1 | `100` | true | `amount = 200`, `doublings++` | 1 |
| 2 | `200` | true | `amount = 400` | 2 |
| 3 | `400` | true | `amount = 800` | 3 |
| 4 | `800` | true | `amount = 1600` | 4 |
| 5 | `1600` | **false** | loop ends | 4 |

So the output is `Amount: 1600` and `Doublings: 4`.

| `amount` | `goal` | Hand trace | Expected |
| --- | --- | --- | --- |
| `100` | `1000` | above | `1600`, 4 doublings |
| `1000` | `1000` (boundary) | `1000 < 1000` is false at the first test | `1000`, 0 doublings |
| `1` | `1000` | `1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024` | `1024`, 10 doublings |
| `100` | `101` | `100 < 101` is true once: `200` | `200`, 1 doubling |

**What the important lines do:** `while (amount < goal)` is the test. `amount = amount * 2;` is the update that makes progress toward the goal, and `doublings++;` counts the pass. Both are inside the braces. The method `doubleUntil(...)` lets one run test four cases, and prints PASS or FAIL against my prediction. The first call uses the lesson's values and prints the two lines the lesson expects.
''')
nb.runner('Homework Hack. Double the amount until it reaches the goal, counting the doublings', r'''
public class Doubling {
    // Doubles amount until it is at least goal, counting the doublings
    static void doubleUntil(int amount, int goal, int expectedAmount, int expectedDoublings) {
        int doublings = 0;                // initialise the counter
        System.out.println("--- amount " + amount + ", goal " + goal + " ---");

        while (amount < goal) {           // test: keep going while the goal has not been reached
            amount = amount * 2;          // update 1: moves amount toward the goal
            doublings++;                  // update 2: counts this pass
        }

        System.out.println("Amount: " + amount);          // the lesson expects 1600 for 100 and 1000
        System.out.println("Doublings: " + doublings);    // the lesson expects 4
        boolean ok = amount == expectedAmount && doublings == expectedDoublings;
        System.out.println((ok ? "PASS: " : "FAIL: ") + "expected " + expectedAmount + " after " + expectedDoublings + " doublings");
    }

    public static void main(String[] args) {
        doubleUntil(100, 1000, 1600, 4);     // the lesson's values
        doubleUntil(1000, 1000, 1000, 0);    // boundary: already at the goal, so the body never runs
        doubleUntil(1, 1000, 1024, 10);
        doubleUntil(100, 101, 200, 1);
    }
}
''', output_note='all four cases matched, and the lesson case printed Amount 1600 and Doublings 4')

nb.md('''
#### Task 2: Homework quick check

**Question:** how many times does the body of this loop run?

```java
int i = 0;
while (i < 10) {
    i = i + 3;
}
```

**My answer: 4.** Hand trace, listing the control variable's value at each test:

| Test | `i` at the test | `i < 10`? | Body runs? | `i` after |
| --- | --- | --- | --- | --- |
| 1 | `0` | true | yes (pass 1) | `3` |
| 2 | `3` | true | yes (pass 2) | `6` |
| 3 | `6` | true | yes (pass 3) | `9` |
| 4 | `9` | true | yes (pass 4) | `12` |
| 5 | `12` | **false** | no, the loop ends | `12` |

The values `0, 3, 6, 9` are all less than 10, so there are four passes. `12` is the first value that fails the test. I wrote the answer before running the check below, which counts the passes.
''')
nb.runner('Homework quick check. Run to count the passes and list the control variable values', r'''
public class LoopCount {
    public static void main(String[] args) {
        int i = 0;
        int passes = 0;

        while (i < 10) {
            System.out.println("Pass " + (passes + 1) + ": i is " + i + " at the test");
            i = i + 3;
            passes++;
        }

        System.out.println("The test saw i = " + i + " and the loop stopped");
        System.out.println("Passes: " + passes);
    }
}
''', output_note='four passes, with i = 0, 3, 6, 9, as I answered')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I wrote a countdown that prints each number down to 1 and then `Liftoff!`, and it ends because the condition (`count >= 1`) becomes false, not because of a `break`. It is tested for 5, 1, 0 and -3.

- **0.8 points: Homework completion**
  - **0.5 Doubling loop:** The loop doubles `amount` until it reaches `goal` and counts the doublings, printing `Amount: 1600` and `Doublings: 4` (and passing three more cases).
  - **0.2 Quick check:** The iteration count question is answered (4 passes) with the values of the control variable listed (`0, 3, 6, 9`, then `12` ends the loop).
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: initialise, test and update all present and in the right place (`int count = start;`, `while (count >= 1)`, `count--;` inside the body; the same for `amount` and `doublings`)
- Present: countdown ends because of its condition, not a `break`
- Absent: an update placed outside the loop body
- Test: output reads `Amount: 1600` and `Doublings: 4`
''', points=[0.2, 0.5, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
outs = outputs_of(path)
nc = [re.sub(r'//.*', '', c) for c in codes]
extra = [
    ('3 code cells (popcorn, homework, quick check)', len(codes) == 3),
    ('countdown loop: test count >= 1 with the update count-- inside the body',
     re.search(r'while \(count >= 1\) \{[^{}]*count--;[^{}]*\}', nc[0]) is not None),
    ('no break anywhere', not any(re.search(r'\bbreak\b', c) for c in nc)),
    ('countdown output for start 5 is 5 4 3 2 1 then Liftoff!', '--- start 5 ---\n5\n4\n3\n2\n1\nLiftoff!\nPASS:' in outs[0]),
    ('start 0 prints only Liftoff! (the body never runs)', '--- start 0 ---\nLiftoff!\nPASS:' in outs[0]),
    ('countdown: all four PASS', outs[0].count('PASS:') == 4),
    ('doubling loop: test, both updates inside the body',
     re.search(r'while \(amount < goal\) \{[^{}]*amount = amount \* 2;[^{}]*doublings\+\+;[^{}]*\}', nc[1]) is not None),
    ('lesson output: Amount: 1600 and Doublings: 4', '--- amount 100, goal 1000 ---\nAmount: 1600\nDoublings: 4\nPASS:' in outs[1]),
    ('doubling: all four PASS (including the boundary 1000/1000)', outs[1].count('PASS:') == 4),
    ('quick check: 4 passes with i = 0, 3, 6, 9 and the loop stopped at 12',
     'Passes: 4' in outs[2] and all(f'i is {v} at the test' in outs[2] for v in (0, 3, 6, 9)) and 'i = 12' in outs[2]),
    ('off-by-one demo shows the missing 1 (bounded run)', '5 4 3 2 Liftoff!' in '\n'.join(''.join(c['source']) for c in cells)),
]
ok = audit(path, {
    'layout': 'post', 'title': TITLE, 'categories': f'[Java, {TOPIC}]', 'lesson_language': 'Java',
    'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_7_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
