"""Build CSA 2.2 Boolean Expressions homework (permalink /csa/unit_02/2_2_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, java_compile_error  # noqa: E402

TOPIC = 'Boolean-Expressions'
nb = Notebook(2, '2', TOPIC)
nb.front_matter(
    title='CSA Unit 2.02 Boolean Expressions HW',
    description='Homework for 2.02 Boolean Expressions. Fix two bugs, write four relational expressions, and answer two quick checks with the reasoning shown.',
    permalink='/csa/unit_02/2_2_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.02 Boolean Expressions]({{ site.baseurl }}/csa/unit_02/2_2). Every code cell below is a Java code runner. Press **Run** to execute it.

**Key idea:** a Boolean expression is a yes or no question that Java answers with `true` or `false`. Relational operators compare two values.

| Operator | Question it asks | Example (`x = 7`) | Result |
| --- | --- | --- | --- |
| `==` | Equal? | `x == 7` | `true` |
| `!=` | Not equal? | `x != 7` | `false` |
| `<` | Less than? | `x < 7` | `false` |
| `>` | Greater than? | `x > 7` | `false` |
| `<=` | Less than or equal? | `x <= 7` | `true` |
| `>=` | Greater than or equal? | `x >= 7` | `true` |

**Two classic mistakes:** `=` stores a value but `==` compares, and there is no `=>` operator (it is written `>=`, with the `>` first). `%` gives a remainder, so `n % 2 != 0` is true for an odd number.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Fixed two bugs: one that did not compile and one that printed the wrong answer | 0.2 |
| Four expressions | Wrote the four Boolean expressions for the speed check and printed them | 0.5 |
| Quick checks | Answered both with the reasoning shown | 0.2 |
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
BUGGY = r'''
public class BonusCheck {
    public static void main(String[] args) {
        int score = 120;
        int target = 100;

        // Bug 1: this line does not compile
        boolean bonus = score => target;

        // Bug 2: this should ask whether score is EXACTLY equal to target
        boolean exact = score != target;

        System.out.println("Bonus unlocked: " + bonus);
        System.out.println("Exact score: " + exact);
    }
}
'''
err = java_compile_error(BUGGY).splitlines()
nb.md(f'''
### Popcorn Hack (In-Class)

This program has two bugs. One stops it from compiling, the other prints the wrong answer. Fix both so it prints `Bonus unlocked: true` and `Exact score: false`.

**Concept:** there is no `=>` operator in Java, and `!=` asks the opposite question from `==`.

**My predictions (written before I ran the code):**

| Bug | What is wrong | My fix | Why |
| --- | --- | --- | --- |
| Bug 1: `score => target` | `=>` is not a Java operator, so the compiler stops | `score >= target` | "greater than or equal" is written `>=` |
| Bug 2: `score != target` | `!=` means "not equal", but the question is "exactly equal" | `score == target` | `==` compares for equality |

| Line | Hand trace | Expected output |
| --- | --- | --- |
| `bonus` | `120 >= 100` is true | `Bonus unlocked: true` |
| `exact` | `120 == 100` is false | `Exact score: false` |

**Compiler message for the original code** (from `javac` 21, so I can see Bug 1):

```
{chr(10).join(err[:3])}
```
''')
nb.runner('Popcorn Hack. Both bugs fixed, each with a comment naming it', r'''
public class BonusCheck {
    public static void main(String[] args) {
        int score = 120;
        int target = 100;

        // Bug 1 fixed: "=>" is not an operator; "greater than or equal" is ">="
        boolean bonus = score >= target;

        // Bug 2 fixed: "exactly equal" needs "==", not "!="
        boolean exact = score == target;

        System.out.println("Bonus unlocked: " + bonus);
        System.out.println("Exact score: " + exact);
    }
}
''', output_note='both lines match my expected output')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

1. Complete the runner: write the four Boolean expressions described in the comments and print them.
2. Answer the two quick checks under it.

#### Part 1: Four Boolean expressions

**Concept:** each expression asks one yes or no question about `speed`, `limit` and `age`. I put them in a method `report(...)` so I can test more than the lesson's one set of values: the lesson values first, then two edge cases (speed exactly at the limit and exactly 18 years old; a driver under the limit).

| Question | My expression | Why |
| --- | --- | --- |
| 1. Over the limit? | `speed > limit` | strictly greater |
| 2. Exactly the limit? | `speed == limit` | `==` compares |
| 3. At least 18? | `age >= 18` | "at least" includes 18 |
| 4. Speed is odd? | `speed % 2 != 0` | an odd number leaves remainder 1 when divided by 2 |

**My predictions (written before I ran the code):**

| Test | `speed`, `limit`, `age` | speeding | exactLimit | adult | oddSpeed |
| --- | --- | --- | --- | --- | --- |
| Lesson values | `68, 65, 17` | `true` (`68 > 65`) | `false` | `false` (`17 >= 18`) | `false` (`68 % 2 = 0`) |
| Edge: at the limit | `65, 65, 18` | `false` (`65 > 65`) | `true` | `true` (`18 >= 18`) | `true` (`65 % 2 = 1`) |
| Under the limit | `60, 65, 30` | `false` | `false` | `true` | `false` (`60 % 2 = 0`) |

**What the important lines do:** each `boolean` variable holds the answer to one question. `speed % 2 != 0` is the odd test, because `%` gives the remainder. The `report` method prints the four lines in the lesson's format, and its extra arguments are my expected values so it can print PASS or FAIL.
''')
nb.runner('Homework Hack. Four Boolean expressions for the speed check, printed for three test cases', r'''
public class SpeedCheck {
    // Evaluates the four expressions for one driver and checks them against what I expected
    static void report(int speed, int limit, int age,
                       boolean expSpeeding, boolean expExact, boolean expAdult, boolean expOdd) {
        // 1. true when the driver is over the limit
        boolean speeding = speed > limit;

        // 2. true when the driver is going exactly the limit
        boolean exactLimit = speed == limit;

        // 3. true when the driver is at least 18
        boolean adult = age >= 18;

        // 4. true when speed is an odd number (use %)
        boolean oddSpeed = speed % 2 != 0;

        System.out.println("speeding: " + speeding);
        System.out.println("exactLimit: " + exactLimit);
        System.out.println("adult: " + adult);
        System.out.println("oddSpeed: " + oddSpeed);

        boolean allMatch = speeding == expSpeeding && exactLimit == expExact
                && adult == expAdult && oddSpeed == expOdd;
        System.out.println((allMatch ? "PASS: " : "FAIL: ") + "all four match my expected values");
    }

    public static void main(String[] args) {
        System.out.println("--- Lesson values: speed 68, limit 65, age 17 ---");
        report(68, 65, 17, true, false, false, false);

        System.out.println("\n--- Edge case: speed 65, limit 65, age 18 ---");
        report(65, 65, 18, false, true, true, true);

        System.out.println("\n--- Under the limit: speed 60, limit 65, age 30 ---");
        report(60, 65, 30, false, false, true, false);
    }
}
''', output_note='every PASS check matched my predictions')

nb.md('''
#### Part 2: Homework quick checks

**Concept:** type the value Java produces. The trick in both is knowing which operator runs first and what type each side has.

| Question | My answer | Reasoning (hand trace) |
| --- | --- | --- |
| 1. `int n = 15; System.out.println(n % 5 == 0);` | `true` | `%` runs before `==`. `15 % 5` is `0` (5 goes into 15 exactly three times), and `0 == 0` is `true`. |
| 2. `int a = 9; int b = 2; System.out.println(a / b == 4.5);` | `false` | `a / b` is integer division: `9 / 2` is `4`, not `4.5`. Then `4 == 4.5` is `false`. |

I wrote the answers before running the check below.
''')
nb.runner('Homework quick checks. Run to confirm the two answers', r'''
public class QuickChecks {
    public static void main(String[] args) {
        // Question 1: 15 % 5 is 0, and 0 == 0
        int n = 15;
        System.out.println("Question 1: " + (n % 5 == 0));

        // Question 2: 9 / 2 is integer division, so it is 4, and 4 == 4.5 is false
        int a = 9;
        int b = 2;
        System.out.println("Question 2: " + (a / b == 4.5));
    }
}
''', output_note='both answers matched')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I fixed both bugs so the program compiles and prints `Bonus unlocked: true` and `Exact score: false`.

- **0.8 points: Homework completion**
  - **0.5 Four expressions:** The four Boolean expressions from the runner comments are written correctly (`speed > limit`, `speed == limit`, `age >= 18`, `speed % 2 != 0`) and printed, and they were also tested on two more cases.
  - **0.2 Quick checks:** Both quick check questions answered with the reasoning shown (`true` and `false`, with a hand trace for each).
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: all four expressions print a `true` or `false` value
- Present: both Popcorn bugs fixed, with a comment naming each one
- Absent: `=` used where `==` was intended
- Test: output reads `Bonus unlocked: true` and `Exact score: false`
''', points=[0.2, 0.5, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
allt = '\n'.join(''.join(c['source']) for c in cells)
nocomment = [re.sub(r'//.*', '', c) for c in codes]
extra = [
    ('3 runners (popcorn, homework, quick checks)', len(codes) == 3),
    ('Popcorn: no "=>" left and ">=" and "==" used', '=>' not in nocomment[0] and '>=' in nocomment[0] and 'score == target' in nocomment[0]),
    ('Popcorn: comments name Bug 1 and Bug 2', 'Bug 1' in codes[0] and 'Bug 2' in codes[0]),
    ('Popcorn output reads the required lines', 'Bonus unlocked: true' in allt and 'Exact score: false' in allt),
    ('four expressions written (no leftover "= false; // TODO")', 'TODO' not in codes[1] and all(e in codes[1] for e in ('speed > limit', 'speed == limit', 'age >= 18', 'speed % 2 != 0'))),
    ('no assignment "=" used as a comparison in any condition', not any(re.search(r'if \([^=!<>]*[^=!<>]=[^=]', c) for c in nocomment)),
    ('quick check answers true and false shown', 'Question 1: true' in allt and 'Question 2: false' in allt),
    ('original compiler error captured for Bug 1', 'error:' in allt),
]
ok = audit(path, {
    'layout': 'post', 'title': 'CSA Unit 2.02 Boolean Expressions HW', 'categories': f'[Java, {TOPIC}]',
    'lesson_language': 'Java', 'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_2_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
