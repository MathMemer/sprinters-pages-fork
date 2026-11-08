"""Build CSA 2.9 Implementing Selection and Iteration Algorithms homework (permalink /csa/unit_02/2_9_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, outputs_of  # noqa: E402

TOPIC = 'Selection-and-Iteration-Algorithms'
TITLE = 'CSA Unit 2.09 Implementing Selection and Iteration Algorithms HW'
nb = Notebook(2, '9', TOPIC)
nb.front_matter(
    title=TITLE,
    description='Homework for 2.09 Implementing Selection and Iteration Algorithms. Finish a prime test by counting divisors, count the even digits of a number with % 10 and / 10, and trace a conditional sum.',
    permalink='/csa/unit_02/2_9_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.09 Implementing Selection and Iteration Algorithms]({{ site.baseurl }}/csa/unit_02/2_9). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** most algorithms in this unit put an `if` inside a loop. The loop visits each value, and the `if` decides what to do with it. A few patterns cover most problems:

| Pattern | Idea | Skeleton |
| --- | --- | --- |
| Counting | add 1 each time a test passes | `if (test) { count++; }` |
| Summing (accumulator) | add each value that passes into a running total | `if (test) { total += value; }` |
| Divisibility | a remainder of 0 means it divides evenly | `n % d == 0` |
| Divisor counting | count every `d` from 1 to `n` that divides `n` | `for (int d = 1; d <= n; d++) { if (n % d == 0) { divisors++; } }` |
| Pulling apart digits | `% 10` reads the last digit, `/ 10` removes it | `while (n > 0) { digit = n % 10; n = n / 10; }` |

A number is **prime** when its only divisors are 1 and itself, so it has **exactly 2** divisors.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Finished `isPrime` with the divisor counting pattern and tested six values (plus more) | 0.2 |
| Even digit count | Counted the even digits of a number with `% 10` and `/ 10` (2847 gives 3) | 0.5 |
| Quick check | Traced a loop that sums the multiples of 4 and named the pattern | 0.2 |
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

A number is **prime** when its only divisors are 1 and itself. Finish `isPrime` using the divisor counting pattern. Expected: 2, 13, and 97 print `true`; 1, 15, and 100 print `false`.

**Concept:** count how many whole numbers from 1 to `n` divide `n` evenly (`n % d == 0`). A prime has exactly 2 divisors (1 and itself); a composite has more. Numbers below 2 are never prime, so a guard `if (n < 2) return false;` comes first. Without it, `1` would have exactly 1 divisor, and `0` and negative numbers would have none, which only works by accident.

**My predictions (written before I ran the code):** divisors counted for each `n`.

| `n` | Divisors found (`d` where `n % d == 0`) | Count | `isPrime(n)` |
| --- | --- | --- | --- |
| `2` | 1, 2 | 2 | `true` |
| `13` | 1, 13 | 2 | `true` |
| `97` | 1, 97 | 2 | `true` |
| `1` | 1 | 1 | `false` (the guard `n < 2` returns first) |
| `15` | 1, 3, 5, 15 | 4 | `false` |
| `100` | 1, 2, 4, 5, 10, 20, 25, 50, 100 | 9 | `false` |
| `4` | 1, 2, 4 | 3 | `false` |
| `91` (7 times 13) | 1, 7, 13, 91 | 4 | `false` |
| `0` and `-5` | none (the loop `d <= n` never runs) | 0 | `false` (the guard) |

**What the important lines do:** `for (int d = 1; d <= n; d++)` tries every candidate divisor from 1 up to and including `n` (the `<=` matters, because `n` is a divisor of itself). `if (n % d == 0)` is the divisibility test and `divisors++` counts a hit. `divisors == 2` is true only for primes. I split the counting into `countDivisors(n)` so the program can print the count next to each answer and check it against my table.
''')
nb.runner('Popcorn Hack. isPrime finished with the divisor counting pattern and tested on nine values', r'''
public class PrimeCheck {
    // Counts the divisors of n from 1 to n
    static int countDivisors(int n) {
        int divisors = 0;
        for (int d = 1; d <= n; d++) {    // <= so that n counts as a divisor of itself
            if (n % d == 0) {             // divisibility test
                divisors++;
            }
        }
        return divisors;
    }

    public static boolean isPrime(int n) {
        if (n < 2) {                      // guard: 0, 1 and negatives are not prime
            return false;
        }
        int divisors = countDivisors(n);
        return divisors == 2;             // exactly 1 and itself
    }

    // Prints one answer and checks the divisor count and the result against my table
    static void report(int n, boolean expectedPrime, int expectedDivisors) {
        boolean prime = isPrime(n);
        int found = countDivisors(n);
        System.out.println(n + ": " + prime + "   (divisors counted: " + found + ")");
        boolean ok = prime == expectedPrime && found == expectedDivisors;
        System.out.println((ok ? "PASS: " : "FAIL: ") + n + " matches my prediction");
    }

    public static void main(String[] args) {
        // The six values the lesson lists
        report(2, true, 2);
        report(13, true, 2);
        report(97, true, 2);
        report(1, false, 1);
        report(15, false, 4);
        report(100, false, 9);

        // My extra cases
        report(4, false, 3);
        report(91, false, 4);
        report(0, false, 0);
    }
}
''', output_note='all nine predictions matched, including every divisor count')
nb.md('**What I learned:** 91 looks prime but is 7 times 13, and only the divisor count catches it (4 divisors, not 2). The guard `n < 2` handles 0, 1 and negatives explicitly instead of relying on how the counting loop happens to behave for them.')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

Two short tasks.

1. Finish the code below: count how many digits of `n` are even. For 2847 the answer is 3 (2, 8, 4).
2. Answer the quick check.

#### Task 1: Count the even digits

**Concept:** to pull a number apart without converting it to a String, use two operations. `n % 10` is the **last digit** (the remainder after dividing by 10), and `n / 10` **removes** the last digit (integer division drops the remainder). A `while (n > 0)` loop repeats until no digits are left. Inside, the `if` counts the digit when `digit % 2 == 0`. The digit is read **before** `n` is shortened, in the same pass, so the final digit is never skipped.

**My predictions (written before I ran the code):** the trace for `2847`.

| Pass | `n` at the test | `n > 0`? | `digit = n % 10` | even? | `evenDigits` | `n = n / 10` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `2847` | true | `7` | no | 0 | `284` |
| 2 | `284` | true | `4` | yes | 1 | `28` |
| 3 | `28` | true | `8` | yes | 2 | `2` |
| 4 | `2` | true | `2` | yes | 3 | `0` |
| (stop) | `0` | **false** | | | 3 | |

| `n` | Hand trace | Expected even digits |
| --- | --- | --- |
| `2847` | above | `3` |
| `1357` | digits 7, 5, 3, 1 are all odd | `0` |
| `2000` | digits 0, 0, 0, 2 are all even (0 is even) | `4` |
| `8` (one digit) | one pass: the last digit is also the first | `1` |
| `7` (one digit) | one pass, odd | `0` |
| `1234567890` | digits 0, 9, 8, 7, 6, 5, 4, 3, 2, 1: the even ones are 0, 8, 6, 4, 2 | `5` |
| `0` (special case) | the loop `0 > 0` is false and never runs, so the loop alone would say 0, but the number 0 has one even digit | `1` |

**The `0` special case.** The loop only runs while `n > 0`, so `0` is skipped entirely. The digit 0 is even, so the right answer is 1, and I add one line before the loop: `if (n == 0) { evenDigits = 1; }`. The lesson's tests (2847, 1357, 2000) don't need it, but a correct method should handle it.

**What the important lines do:** `int rest = n;` makes a working copy so the loop can shorten it without changing `n`. `rest % 10` reads the last digit, `digit % 2 == 0` is the evenness test, and `rest = rest / 10` drops the digit I just read. The method `countEvenDigits(n)` holds the loop; `check` prints PASS or FAIL against my table.
''')
nb.runner('Homework Hack. Count the even digits of a number with % 10 and / 10, tested on seven numbers', r'''
public class EvenDigits {
    // Counts the even digits of n without converting it to a String
    static int countEvenDigits(int n) {
        int evenDigits = 0;
        int rest = n;                       // a working copy, so n itself is not changed

        if (n == 0) {                       // special case: the loop below never runs for 0, but 0 is an even digit
            evenDigits = 1;
        }

        while (rest > 0) {
            int digit = rest % 10;          // the last digit
            if (digit % 2 == 0) {           // even digits only
                evenDigits++;
            }
            rest = rest / 10;               // remove the digit just read
        }
        return evenDigits;
    }

    // Prints one answer and checks it against my prediction
    static void check(int n, int expected) {
        int result = countEvenDigits(n);
        System.out.println("Number: " + n);
        System.out.println("Even digits: " + result);
        System.out.println((result == expected ? "PASS: " : "FAIL: ") + n + " has " + expected + " even digits");
    }

    public static void main(String[] args) {
        check(2847, 3);          // the lesson's case
        check(1357, 0);
        check(2000, 4);          // the three values the lesson lists
        check(8, 1);             // one digit
        check(7, 0);
        check(1234567890, 5);
        check(0, 1);             // special case
    }
}
''', output_note='all seven predictions matched, and 2847 printed 3 even digits')

nb.md('''
#### Task 2: Homework quick check

**Question:** what does this print?

```java
int total = 0;
for (int i = 1; i <= 12; i++) {
    if (i % 4 == 0) {
        total += i;
    }
}
System.out.println(total);
```

**My answer: 24.** The loop visits `i = 1, 2, ..., 12`, and the `if` keeps only the multiples of 4, because `i % 4 == 0` means a remainder of 0 when dividing by 4.

| `i` | `i % 4 == 0`? | `total` after |
| --- | --- | --- |
| 1, 2, 3 | no | 0 |
| 4 | yes | `0 + 4 = 4` |
| 5, 6, 7 | no | 4 |
| 8 | yes | `4 + 8 = 12` |
| 9, 10, 11 | no | 12 |
| 12 | yes | `12 + 12 = 24` |

**The pattern is a conditional accumulator** (a running sum with a filter): the loop visits every value, the `if` is the filter, and `total += i` adds the ones that pass into the running total, which starts at 0. It is the summing pattern from the overview with a divisibility test as the condition.

I wrote the answer before running the check below, which prints each value that passes the filter.
''')
nb.runner('Homework quick check. Run to confirm the total and which values were added', r'''
public class ConditionalSum {
    public static void main(String[] args) {
        int total = 0;
        for (int i = 1; i <= 12; i++) {
            if (i % 4 == 0) {
                System.out.println("added " + i + ", total is now " + (total + i));
                total += i;
            }
        }
        System.out.println(total);
    }
}
''', output_note='4, 8 and 12 were added, and the total is 24, as I answered')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I completed `isPrime` using the divisor counting pattern, with 2, 13 and 97 printing `true` and 1, 15 and 100 printing `false` (and 4, 91 and 0 also passing).

- **0.8 points: Homework completion**
  - **0.5 Even digit count:** The loop counts the even digits of `n` with `% 10` and `/ 10`, printing 3 for 2847 (and passing six more numbers, including single digits and 2000).
  - **0.2 Quick check:** The quick check is answered (24, with a trace) and the pattern used is named: a conditional accumulator, a running sum with a filter.
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: `isPrime` correct for all six listed test values (2, 13, 97 true; 1, 15, 100 false)
- Present: digit loop uses `% 10` and `/ 10` rather than String conversion
- Absent: a loop that misses the final digit (the digit is read before `n` is shortened, and the one-digit tests 8 and 7 pass)
- Test: 2847 yields 3 even digits and 1 is not prime
''', points=[0.2, 0.5, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
outs = outputs_of(path)
nc = [re.sub(r'//.*', '', c) for c in codes]
extra = [
    ('3 code cells (popcorn, homework, quick check)', len(codes) == 3),
    ('isPrime uses the divisor counting pattern (loop 1..n, n % d == 0, divisors == 2)',
     'for (int d = 1; d <= n; d++)' in nc[0] and 'if (n % d == 0)' in nc[0] and 'divisors == 2' in nc[0] and 'if (n < 2)' in nc[0]),
    ('the six lesson values print the expected results',
     all(f'\n{n}: {v}   (divisors' in '\n' + outs[0] for n, v in (('2', 'true'), ('13', 'true'), ('97', 'true'), ('1', 'false'), ('15', 'false'), ('100', 'false')))),
    ('prime: all nine PASS', outs[0].count('PASS:') == 9),
    ('digit loop uses % 10 and / 10', 'rest % 10' in nc[1] and 'rest / 10' in nc[1] and 'while (rest > 0)' in nc[1]),
    ('no String conversion of the number', not re.search(r'String\.valueOf|Integer\.toString|\.charAt|toCharArray|"" \+ n', nc[1])),
    ('2847 -> 3 even digits (the lesson case)', 'Number: 2847\nEven digits: 3\nPASS:' in outs[1]),
    ('2000 -> 4 and 1357 -> 0', 'Number: 2000\nEven digits: 4' in outs[1] and 'Number: 1357\nEven digits: 0' in outs[1]),
    ('final digit not missed: one-digit 8 -> 1 and 7 -> 0', 'Number: 8\nEven digits: 1' in outs[1] and 'Number: 7\nEven digits: 0' in outs[1]),
    ('digits: all seven PASS (including 0)', outs[1].count('PASS:') == 7),
    ('quick check total is 24 after adding 4, 8, 12',
     outs[2].strip().splitlines()[-1] == '24' and all(f'added {v}' in outs[2] for v in (4, 8, 12))),
    ('quick check names the pattern', 'conditional accumulator' in '\n'.join(''.join(c['source']) for c in cells)),
]
ok = audit(path, {
    'layout': 'post', 'title': TITLE, 'categories': f'[Java, {TOPIC}]', 'lesson_language': 'Java',
    'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_9_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
