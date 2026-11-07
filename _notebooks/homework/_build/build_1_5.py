"""Build CSA 1.5 Casting and Range homework (permalink /csa/unit_01/1_5_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, audit, outputs_of  # noqa: E402

TOPIC = 'Casting-and-Range'
nb = Notebook(1, '5', TOPIC)
nb.front_matter(
    title='CSA Unit 1.5 Casting and Range HW',
    description='Homework for 1.05 Casting and Range of Variables. Predict casting results, then write three casting methods and test their edge cases.',
    permalink='/csa/unit_01/1_5_hw')

nb.md(r'''
## 1. Overview

This is my homework notebook for [1.05 Casting and Range of Variables]({{ site.baseurl }}/csa/unit_01/1_5). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** Java does integer math when both sides are `int`, so the decimals are lost. A cast like `(double)` or `(int)` changes the type of one value so the math comes out the way I want. An `int` also has a fixed range, so a result past the end wraps around (overflow).

| Rule | Example | Result |
| --- | --- | --- |
| Both operands `int` | `7 / 2` | `3` (truncated, not 3.5) |
| Cast first, then divide | `(double) 7 / 2` | `3.5` |
| Narrowing cast truncates toward zero | `(int) 5.9` and `(int) -5.9` | `5` and `-5` |
| Round a non-negative number | `(int)(x + 0.5)` | `(int)(5.5 + 0.5)` is `6` |
| Round a negative number | `(int)(x - 0.5)` | `(int)(-5.5 - 0.5)` is `-6` |
| Overflow wraps around | `Integer.MAX_VALUE + 1` | `-2147483648` |

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Predicted five casting results before running them, then checked them | 0.2 |
| Homework Hack | Wrote `averageAsDouble`, `percentScore`, and `nearestInteger`, with tests and edge cases | 0.8 |
''')

nb.md(r'''
## 2. Code Examples

These are the lesson's three examples, with one value changed in each so I have to predict a new answer. I wrote my prediction before pressing Run, and my notes say what each important line does.

> **Fix for Example C:** in the lesson page, Example C is missing its closing `OverflowAndCastingDemo.main(null);` line, so the page shows it as plain text with no Run button. I added the line so the cell runs as a complete program, and its output is saved below it.
''')

nb.md(r'''
### A. Simple: Understanding Integer Division

**Concept:** `/` on two `int` values is integer division: it drops the decimal part. `%` gives the remainder. Casting one operand to `double` makes the whole division a `double` division.

**What I changed:** `b` from `2` to `4`.

**My predictions (before running):**

| Line | My prediction | Hand trace |
| --- | --- | --- |
| `a / b` | `1` | `7 / 4` is `1` remainder `3`, and the `.75` is dropped |
| `a % b` | `3` | `7 - 1 * 4 = 3` |
| `(double)a / b` | `1.75` | `a` becomes `7.0`, then `7.0 / 4 = 1.75` |
| `a / (double)b` | `1.75` | `b` becomes `4.0`, then `7 / 4.0 = 1.75` |

**What the lines do:** `int a = 7, b = 4;` stores two whole numbers. `(double)a` casts first (higher precedence than `/`), so the division uses `double` math.
''')

nb.runner('', r'''
// A. Simple: Understanding Integer Division
public class IntegerDivisionDemo {
    public static void main(String[] args) {
        int a = 7, b = 4;   // changed from the lesson's 7 and 2

        System.out.println("Both operands are int:");
        System.out.println(a / b);           // 1 (truncated, not 1.75)
        System.out.println(a % b);           // 3 (remainder)

        System.out.println("\nCast one operand to double before operation:");
        System.out.println((double)a / b);   // 1.75 (division on doubles)
        System.out.println(a / (double)b);   // 1.75 (division on doubles)
    }
}
''', output_note='all four predictions matched')

nb.md(r'''
### B. Intermediate: Casting and Rounding

**Concept:** `(int)` on a `double` truncates toward zero, so it does not round. To round a non-negative number, add `0.5` before casting. To round a negative number, subtract `0.5` before casting.

**What I changed:** `d` from `5.7` to `2.5` (exactly halfway), and `neg` to `-2.5`.

**My predictions (before running):**

| Line | My prediction | Hand trace |
| --- | --- | --- |
| `(int)d` | `2` | Truncate `2.5`: cut off `.5` |
| `(int)(d + 0.5)` | `3` | `2.5 + 0.5 = 3.0`, then `(int)3.0 = 3` |
| `(int)neg` | `-2` | Truncate toward zero: `-2.5` becomes `-2`, not `-3` |
| `(int)(neg - 0.5)` | `-3` | `-2.5 - 0.5 = -3.0`, then `(int)-3.0 = -3` |

**What the lines do:** the cast has to wrap the whole `(d + 0.5)` expression in parentheses. Without them, `(int)d + 0.5` would truncate first and then add `0.5`.
''')

nb.runner('', r'''
// B. Intermediate: Casting and Rounding
public class CastingAndRoundingDemo {
    public static void main(String[] args) {
        double d = 2.5;   // changed from the lesson's 5.7: exactly halfway

        System.out.println("Positive number:");
        int truncated = (int)d;
        System.out.println("Truncate 2.5: " + truncated);  // 2
        int rounded = (int)(d + 0.5);
        System.out.println("Round 2.5: " + rounded);       // 3

        System.out.println("\nNegative number:");
        double neg = -2.5;
        int negTruncated = (int)neg;
        System.out.println("Truncate -2.5: " + negTruncated);  // -2
        int negRounded = (int)(neg - 0.5);
        System.out.println("Round -2.5: " + negRounded);       // -3
    }
}
''', output_note='all four predictions matched')

nb.md(r'''
### C. Complex: Overflow and Mixed-Type Expressions

**Concept:** An `int` holds `-2147483648` to `2147483647`. Going past either end wraps around to the other end (overflow), and Java gives no error. In a mixed expression, where the cast is placed decides when the division happens.

**What I changed:** `x` and `y` from `10` and `3` to `17` and `5`. I also added the missing `OverflowAndCastingDemo.main(null);` line so this cell runs on its own.

**My predictions (before running):**

| Line | My prediction | Hand trace |
| --- | --- | --- |
| `Max + 1` | `-2147483648` | `MAX_VALUE + 1` wraps to `MIN_VALUE` |
| `Min - 1` | `2147483647` | `MIN_VALUE - 1` wraps to `MAX_VALUE` |
| `(double)(x / y)` | `3.0` | `17 / 5` is `3` (int division first), then cast to `3.0` |
| `(double)x / y` | `3.4` | Cast first: `17.0 / 5 = 3.4` |
| Verification line | `17 == (3*5) + 2`, then `17 == 17` | `(x/y)*y + (x%y)` is `15 + 2`, which rebuilds `x` |

**What the lines do:** `(double)(x / y)` casts the *result* of an int division, so the decimals are already gone. `(double)x / y` casts `x` first, so the decimals survive.
''')

nb.runner('', r'''
// C. Complex: Overflow and Mixed-Type Expressions
public class OverflowAndCastingDemo {
    public static void main(String[] args) {
        System.out.println("Understanding int range:");
        int max = Integer.MAX_VALUE;  // 2147483647
        int min = Integer.MIN_VALUE;  // -2147483648

        System.out.println("Max int: " + max);
        System.out.println("Min int: " + min);

        System.out.println("\nOverflow wraps around:");
        int overflow = max + 1;
        System.out.println("Max + 1: " + overflow);  // -2147483648 (wraps to MIN)

        int underflow = min - 1;
        System.out.println("Min - 1: " + underflow); // 2147483647 (wraps to MAX)

        System.out.println("\nMixed-type calculations:");
        int x = 17, y = 5;   // changed from the lesson's 10 and 3

        System.out.println("Order matters with casting:");
        double result1 = (double)(x / y);    // 3.0 (int division first, then cast)
        double result2 = (double)x / y;      // 3.4 (cast first, then double division)

        System.out.println("(double)(17/5) = " + result1);   // 3.0
        System.out.println("(double)17/5 = " + result2);     // 3.4

        System.out.println("\nVerification: x == (x/y)*y + (x%y)");
        System.out.println(x + " == (" + (x/y) + "*" + y + ") + " + (x%y));
        System.out.println(x + " == " + ((x/y)*y + (x%y)));
    }
}
''', output_note='all five predictions matched')

nb.md(r'''
## 3. Hacks & Practice Tasks

### Submission Safety Rules (Read First)

- Include my predictions before running each code section
- Execute all code cells and leave output visible
- Show my work for hand-traced predictions
- Test edge cases (especially for overflow)
- Do not just copy code; explain what each line does
- Label each question clearly
- One class per cell, ending with `ClassName.main(null);`
- Use `##` headings or smaller
''')

nb.md(r'''
### Popcorn Hack (In-Class)

5-minute challenge: predict and verify casting results.

**Concept:** A division of two `int` values is done as integer division and drops the decimal part. Casting one side to `double` first keeps the decimals. Casting a `double` to `int` cuts off everything after the decimal point (it truncates toward zero, it does not round). `Integer.MAX_VALUE` is the largest `int`, so adding 1 overflows and wraps to the smallest `int`.

**My predictions (written before I ran the code):**

| Q | Expression | My prediction | Hand trace |
| --- | --- | --- | --- |
| Q1 | `int a = 10, b = 4; a / b` | `2` | Both are `int`: `10 / 4 = 2` remainder `2`, the `.5` is dropped |
| Q2 | `(double)a / b` | `2.5` | `a` becomes `10.0`, then `10.0 / 4 = 2.5` |
| Q3 | `double d = 7.8; (int)d` | `7` | Casting truncates toward zero, it does not round |
| Q4 | `(int)(d + 0.5)` | `8` | `7.8 + 0.5 = 8.3`, then truncating `8.3` gives `8` |
| Q5 | `int x = Integer.MAX_VALUE; x + 1` | `-2147483648` | `2147483647 + 1` is one past the largest `int`, so it wraps to the smallest |
''')

nb.runner('', r'''
public class PopcornCasting {
    public static void main(String[] args) {
        // Q1: int a = 10, b = 4; a / b
        // My prediction: 2 (both operands are int, so the decimal part is dropped)
        int a = 10, b = 4;
        System.out.println("Q1: " + (a / b));

        // Q2: (double)a / b
        // My prediction: 2.5 (a becomes 10.0 first, so the division keeps decimals)
        System.out.println("Q2: " + ((double) a / b));

        // Q3: (int) 7.8
        // My prediction: 7 (casting a double to int truncates toward zero, it does not round)
        double d = 7.8;
        System.out.println("Q3: " + ((int) d));

        // Q4: (int)(d + 0.5)
        // My prediction: 8 (adding 0.5 before truncating rounds a positive number)
        System.out.println("Q4: " + ((int) (d + 0.5)));

        // Q5: Integer.MAX_VALUE + 1
        // My prediction: -2147483648 (int overflow wraps around to the smallest int)
        int x = Integer.MAX_VALUE;
        System.out.println("Q5: " + (x + 1));
    }
}
''', output_note='all five predictions matched')

nb.md(r'''
**What I learned:** Q1 and Q3 lose information (the decimal part), Q2 and Q4 show two ways to get the answer I wanted, and Q5 shows that a result can be wrong without any error message.
''')

nb.md(r'''
### Homework Hack

**Task:** Write three methods that demonstrate casting and type conversion:

1. **averageAsDouble(int a, int b)**: the average of two integers as a double, preserving decimal values
2. **percentScore(int correct, int total)**: a percentage (0.0 to 100.0) from whole numbers
3. **nearestInteger(double value)**: round a double to the nearest integer, handling both positive and negative numbers

**Concept:** each method needs one casting idea.

| Method | Casting idea |
| --- | --- |
| `averageAsDouble` | Cast to `double` **before** adding, so `a + b` cannot overflow and the division is not integer division |
| `percentScore` | `100.0 * correct` forces `double` math; return `0.0` when `total` is `0` |
| `nearestInteger` | The CED technique: a cast truncates, so add `0.5` for positive values and subtract `0.5` for negative values before casting |

**What each important line does:**

| Line | What it does |
| --- | --- |
| `return ((double) a + b) / 2.0;` | `(double) a` makes the sum a `double`, so `a + b` cannot overflow and `/ 2.0` keeps the `.5` |
| `if (total == 0) { return 0.0; }` | Stops a divide by zero before it happens (edge case) |
| `return (100.0 * correct) / total;` | `100.0` is a `double`, so the whole expression is `double` math |
| `if (value >= 0) { return (int) (value + 0.5); }` | Rounds non-negative values: `5.5` becomes `6.0`, which casts to `6` |
| `return (int) (value - 0.5);` | Rounds negative values: `-5.5` becomes `-6.0`, which casts to `-6` |
| `check(label, passed)` | Prints `PASS` or `FAIL` so each test is labeled clearly |

**My hand-traced expected values (written before I ran the code):**

| Call | Hand trace | Expected |
| --- | --- | --- |
| `averageAsDouble(5, 10)` | `(5.0 + 10) / 2.0 = 15.0 / 2.0` | `7.5` |
| `averageAsDouble(4, 4)` | `8.0 / 2.0` | `4.0` |
| `averageAsDouble(-3, 2)` | `(-3.0 + 2) / 2.0 = -1.0 / 2.0` (negative edge case) | `-0.5` |
| `averageAsDouble(MAX, MAX)` | `(2147483647.0 + 2147483647) / 2.0`. An `int` sum would overflow to `-2` (overflow edge case) | `2147483647.0` |
| `percentScore(7, 10)` | `100.0 * 7 = 700.0`, then `700.0 / 10` | `70.0` |
| `percentScore(4, 5)` | `400.0 / 5` | `80.0` |
| `percentScore(0, 5)` / `(5, 5)` | `0.0 / 5` and `500.0 / 5` (boundary edge cases) | `0.0` / `100.0` |
| `percentScore(3, 0)` | the guard returns before dividing (division by zero edge case) | `0.0` |
| `percentScore(MAX, MAX)` | `100.0 * MAX` is a `double`, so no overflow; an `int` `100 * MAX` would overflow | `100.0` |
| `nearestInteger(5.5)` / `(-5.5)` | `5.5 + 0.5 = 6.0`; `-5.5 - 0.5 = -6.0` | `6` / `-6` |
| `nearestInteger(2.4)` / `(-2.4)` | `2.9` truncates to `2`; `-2.9` truncates to `-2` | `2` / `-2` |
| `nearestInteger(0.0)` | `0.0 >= 0`, so `0.0 + 0.5 = 0.5`, which truncates to `0` (boundary edge case) | `0` |
''')

nb.runner('', r'''
public class CastingHomework {

    // Average of two ints as a double. Cast BEFORE adding so a + b cannot overflow
    // and the division is done on doubles, which keeps the .5.
    public static double averageAsDouble(int a, int b) {
        return ((double) a + b) / 2.0;
    }

    // Percentage from whole numbers. 100.0 makes the whole expression double math.
    // Edge case: total == 0 would divide by zero, so return 0.0 instead.
    public static double percentScore(int correct, int total) {
        if (total == 0) {
            return 0.0;
        }
        return (100.0 * correct) / total;
    }

    // Round to the nearest int. A cast truncates toward zero, so add 0.5 for
    // positive values and subtract 0.5 for negative values before casting.
    public static int nearestInteger(double value) {
        if (value >= 0) {
            return (int) (value + 0.5);
        }
        return (int) (value - 0.5);
    }

    static void check(String label, boolean passed) {
        System.out.println((passed ? "PASS: " : "FAIL: ") + label);
    }

    static boolean close(double actual, double expected) {
        return Math.abs(actual - expected) < 1e-9;
    }

    public static void main(String[] args) {
        System.out.println("--- averageAsDouble ---");
        System.out.println("averageAsDouble(5, 10) = " + averageAsDouble(5, 10));
        check("averageAsDouble(5, 10) is 7.5", close(averageAsDouble(5, 10), 7.5));
        check("averageAsDouble(4, 4) is 4.0", close(averageAsDouble(4, 4), 4.0));
        check("averageAsDouble(-3, 2) is -0.5 (negative)", close(averageAsDouble(-3, 2), -0.5));
        check("averageAsDouble(MAX, MAX) does not overflow",
                close(averageAsDouble(Integer.MAX_VALUE, Integer.MAX_VALUE), 2147483647.0));

        System.out.println("--- percentScore ---");
        System.out.println("percentScore(7, 10) = " + percentScore(7, 10));
        check("percentScore(7, 10) is 70.0", close(percentScore(7, 10), 70.0));
        check("percentScore(4, 5) is 80.0", close(percentScore(4, 5), 80.0));
        check("percentScore(0, 5) is 0.0 (boundary)", close(percentScore(0, 5), 0.0));
        check("percentScore(5, 5) is 100.0 (boundary)", close(percentScore(5, 5), 100.0));
        check("percentScore(3, 0) is 0.0 (division by zero)", close(percentScore(3, 0), 0.0));
        check("percentScore(MAX, MAX) is 100.0 (no overflow)",
                close(percentScore(Integer.MAX_VALUE, Integer.MAX_VALUE), 100.0));

        System.out.println("--- nearestInteger ---");
        System.out.println("nearestInteger(5.5) = " + nearestInteger(5.5));
        check("nearestInteger(5.5) is 6", nearestInteger(5.5) == 6);
        check("nearestInteger(-5.5) is -6", nearestInteger(-5.5) == -6);
        check("nearestInteger(2.4) is 2", nearestInteger(2.4) == 2);
        check("nearestInteger(-2.4) is -2", nearestInteger(-2.4) == -2);
        check("nearestInteger(0.0) is 0 (boundary)", nearestInteger(0.0) == 0);
    }
}
''', output_note='every test passed, and every value matched my hand trace')

nb.rubric(r'''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I made predictions for all five questions and verified them with working Java code. The output matches the expected results (Popcorn Hack section, Q1 to Q5).

- **0.8 points: Homework completion**
  - **0.25 averageAsDouble:** Uses casting to prevent integer division. The tests verify it returns the proper decimal average (`averageAsDouble(5, 10)` is `7.5`).
  - **0.25 percentScore:** Casts to double before multiplication or division. Handles the division by zero edge case (`percentScore(3, 0)` is `0.0`).
  - **0.25 nearestInteger:** Implements rounding for both positive and negative numbers using the CED technique (`nearestInteger(5.5)` is `6` and `nearestInteger(-5.5)` is `-6`).
  - **0.05 Edge cases:** At least one edge case per method: overflow and negative values for `averageAsDouble`, zero division and boundaries for `percentScore`, negative and zero values for `nearestInteger`.

#### Quick Validation Checklist

- Present: All code cells executed with output visible
- Present: Predictions written before code for the Popcorn Hack
- Present: Three working methods with correct casting
- Present: Test cases that demonstrate understanding
- Present: Comments explaining casting logic
- Absent: Integer division where floating-point is needed
- Test: averageAsDouble(5, 10) = 7.5
- Test: percentScore(7, 10) = 70.0
- Test: nearestInteger(5.5) = 6 and nearestInteger(-5.5) = -6
''', points=[0.2, 0.25, 0.25, 0.25, 0.05])


path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
allt = '\n'.join(''.join(c['source']) for c in cells)
outs = outputs_of(path)
extra = [
    ('Popcorn predictions Q1-Q5 present', all(f'| Q{n} |' in allt for n in range(1, 6))),
    ('Popcorn output matches the five predictions', outs[3].split() == ['Q1:', '2', 'Q2:', '2.5', 'Q3:', '7', 'Q4:', '8', 'Q5:', '-2147483648']),
    ('Example C ends with its main(null) call', codes[2].rstrip().endswith('OverflowAndCastingDemo.main(null);')),
    ('three methods present', all(re.search(rf'static \w+ {m}\(', allt) for m in ('averageAsDouble', 'percentScore', 'nearestInteger'))),
    ('required tests pass', all(t in outs[4] for t in ('PASS: averageAsDouble(5, 10) is 7.5', 'PASS: percentScore(7, 10) is 70.0',
                                                       'PASS: nearestInteger(5.5) is 6', 'PASS: nearestInteger(-5.5) is -6'))),
    ('division by zero guard + test', 'total == 0' in allt and 'percentScore(3, 0)' in allt),
    ('overflow edge case tested', 'MAX, MAX' in allt),
]
ok = audit(path, {
    'layout': 'post', 'title': 'CSA Unit 1.5 Casting and Range HW', 'categories': f'[Java, {TOPIC}]',
    'lesson_language': 'Java', 'lesson_topic': f'{TOPIC} HW', 'lesson_part': 'interactive', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_01/1_5_hw'}, expect_runners=5, extra=extra)
sys.exit(0 if ok else 1)
