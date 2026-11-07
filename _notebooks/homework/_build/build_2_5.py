"""Build CSA 2.5 Compound Boolean Expressions homework (permalink /csa/unit_02/2_5_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, outputs_of  # noqa: E402

TOPIC = 'Compound-Boolean-Expressions'
TITLE = 'CSA Unit 2.05 Compound Boolean Expressions HW'
nb = Notebook(2, '5', TOPIC)
nb.front_matter(
    title=TITLE,
    description='Homework for 2.05 Compound Boolean Expressions. Fix a discount rule, write the leap year rule as one compound expression, and trace two quick checks.',
    permalink='/csa/unit_02/2_5_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.05 Compound Boolean Expressions]({{ site.baseurl }}/csa/unit_02/2_5). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** `&&`, `||` and `!` combine yes or no questions into one bigger question.

| Operator | Name | True when | Example (`x = 5`, `y = 4`) |
| --- | --- | --- | --- |
| `!a` | NOT | `a` is false | `!(x > 3)` is `false` |
| `a && b` | AND | both are true | `x > 3 && y == 4` is `true` |
| `a \\|\\| b` | OR | at least one is true | `x > 9 \\|\\| y == 4` is `true` |

**Precedence:** `!` is done first, then `&&`, then `||`. So `a || b && c` means `a || (b && c)`. I still write the parentheses, because a reader should not have to remember the precedence table.

**Short circuit:** `&&` stops as soon as the left side is `false` (the answer must be false), and `||` stops as soon as the left side is `true`. The right side is then **not evaluated at all**.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Fixed the discount rule and tested the lesson's two cases plus four more | 0.2 |
| Leap year rule | Wrote it as one compound Boolean expression | 0.5 |
| Boundary tests | Tested 1900, 2000, 2024 and 2023 (plus two more) | 0.2 |
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

The discount rule is: seniors (65 and up) get a discount, and so do students who are also members. Fix the condition so `age = 20, isStudent = true, isMember = false` prints `No discount`, and `age = 20, isStudent = true, isMember = true` prints `Discount!`.

**Concept:** the rule is "senior **or** (student **and** member)".

**What was wrong with the original condition**, `age >= 65 || isStudent && isMember == false`:

| Problem | What I found |
| --- | --- |
| Reversed member check | `isMember == false` is true for people who are **not** members, so non-member students got the discount and members did not. This is the logic bug that breaks both of the lesson's test cases. |
| Grouping not written out | Java already groups `&&` before `||`, so the original meant `age >= 65 \\|\\| (isStudent && isMember == false)`. The grouping was right but hidden. I add parentheses so the rule can be read without remembering the precedence table. |

**My predictions (written before I ran the code):**

| `age` | `isStudent` | `isMember` | Hand trace | Prints |
| --- | --- | --- | --- | --- |
| `20` | `true` | `false` | `20 >= 65` false; `(true && false)` false; `false \\|\\| false` | No discount |
| `20` | `true` | `true` | `20 >= 65` false; `(true && true)` true; `false \\|\\| true` | Discount! |
| `65` | `false` | `false` | `65 >= 65` true, so `\\|\\|` short-circuits and the right side is skipped | Discount! |
| `70` | `true` | `false` | senior, so true (right side skipped) | Discount! |
| `64` | `false` | `true` | `64 >= 65` false; `(false && true)` false | No discount |
| `20` | `false` | `false` | `20 >= 65` false; `(false && false)` false | No discount |

**What the important lines do:** `age >= 65 || (isStudent && isMember)` is true for a senior, or for someone who is both a student and a member. I put it in a method `decide(...)` so one run can test all six customers, and each case prints PASS or FAIL against my prediction.
''')
nb.runner('Popcorn Hack. The compound condition fixed and tested on six customers', r'''
public class DiscountRule {
    // Prints the discount decision for one customer and checks it against my prediction
    static void decide(int age, boolean isStudent, boolean isMember, String expected) {
        String result;

        // Fix 1: the member check was reversed (isMember == false), so it is just isMember.
        // Fix 2: parentheses make the grouping explicit: a senior, OR (a student who is also a member).
        if (age >= 65 || (isStudent && isMember)) {
            result = "Discount!";
        } else {
            result = "No discount";
        }

        System.out.println("age " + age + ", student " + isStudent + ", member " + isMember + ": " + result);
        System.out.println((result.equals(expected) ? "PASS: " : "FAIL: ") + "expected " + expected);
    }

    public static void main(String[] args) {
        // The two cases the lesson lists
        decide(20, true, false, "No discount");
        decide(20, true, true, "Discount!");

        // My extra cases: seniors, a non-student member, and a customer who qualifies for nothing
        decide(65, false, false, "Discount!");
        decide(70, true, false, "Discount!");
        decide(64, false, true, "No discount");
        decide(20, false, false, "No discount");
    }
}
''', output_note='all six predictions matched')
nb.md('**What I learned:** the original grouping was already correct, but the reversed member check was the real bug, and it broke both test cases. The parentheses do not change what Java does here; they change whether a reader can trust the rule at a glance.')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

Two short tasks.

1. Finish the code below: a year is a leap year when it is divisible by 4 and not by 100, or when it is divisible by 400.
2. Answer the quick check.

#### Task 1: Leap year

**Concept:** the rule is `(divisible by 4 AND not divisible by 100) OR divisible by 400`. `year % 4 == 0` tests "divisible by 4" (the remainder is 0). Century years such as 1900 are divisible by 4 and by 100, so the first part is false for them, and only the `% 400` part can rescue them (2000 is a leap year, 1900 is not). The parentheses group the `&&` part so the rule reads exactly like the sentence.

**My expression:** `(year % 4 == 0 && year % 100 != 0) || year % 400 == 0`

**My predictions (written before I ran the code):**

| `year` | `year % 4 == 0` | `year % 100 != 0` | left side (`&&`) | `year % 400 == 0` | Leap year? |
| --- | --- | --- | --- | --- | --- |
| `2024` | true (`2024 % 4 = 0`) | true (`24`) | true | false | **yes** |
| `1900` | true (`1900 % 4 = 0`) | false (`1900 % 100 = 0`) | false | false (`300`) | **no** |
| `2000` | true | false (`2000 % 100 = 0`) | false | true (`2000 % 400 = 0`) | **yes** |
| `2023` | false (`2023 % 4 = 3`) | true | false | false | **no** |
| `1600` (extra) | true | false | false | true | **yes** |
| `2100` (extra) | true | false | false | false (`100`) | **no** |

**What the important lines do:** `year % 4 == 0 && year % 100 != 0` is the "ordinary leap year" part, and `|| year % 400 == 0` adds the "century leap year" exception. I put the rule in a method `report(year, expected)` so one run tests all six years, and each prints PASS or FAIL against my prediction. The message format matches the lesson (`2024 is a leap year.`).
''')
nb.runner('Homework Hack. Leap year rule as one compound Boolean expression, tested on six years', r'''
public class LeapYear {
    // Prints whether one year is a leap year and checks it against my prediction
    static void report(int year, boolean expectedLeap) {
        // Divisible by 4 and not by 100, or divisible by 400 (parentheses make the grouping explicit)
        boolean isLeap = (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;

        if (isLeap) {
            System.out.println(year + " is a leap year.");
        } else {
            System.out.println(year + " is not a leap year.");
        }
        System.out.println((isLeap == expectedLeap ? "PASS: " : "FAIL: ") + year + " leap year is " + expectedLeap);
    }

    public static void main(String[] args) {
        // The four years the lesson lists
        report(2024, true);
        report(1900, false);
        report(2000, true);
        report(2023, false);

        // My extra century years
        report(1600, true);
        report(2100, false);
    }
}
''', output_note='all six predictions matched; 1900 is not a leap year and 2000 is')

nb.md('''
#### Task 2: Homework quick checks

**Question 1:** what is the value of `!(x > 3) || y == 4` when `x = 5` and `y = 4`? Type true or false.

**My answer: `true`.** Hand trace: `x > 3` is `5 > 3`, which is `true`. `!(true)` is `false`. `y == 4` is `4 == 4`, which is `true`. So the whole expression is `false || true`, which is `true`.

**Question 2:** with `a = false`, does Java evaluate `b` in `a && b`? Type yes or no.

**My answer: `no`.** Hand trace: `&&` is only true when both sides are true. Once the left side `a` is `false`, the answer is already `false`, so Java skips `b`. This is short-circuit evaluation.

I wrote both answers before running the check below. To **prove** question 2 instead of just claiming it, `noisy()` prints a line when it runs. If `b` is skipped, that line must not appear for `false && noisy()`. As a control, `true && noisy()` must run it.
''')
nb.runner('Homework quick checks. Run to confirm both answers, with a side-effect method that proves the short circuit', r'''
public class QuickChecks {
    // Stands in for "b": it prints a line whenever Java actually evaluates it
    static boolean noisy() {
        System.out.println("   noisy() was evaluated");
        return true;
    }

    public static void main(String[] args) {
        // Question 1: !(5 > 3) is false, y == 4 is true, so false || true
        int x = 5;
        int y = 4;
        System.out.println("Question 1: " + (!(x > 3) || y == 4));

        // Question 2: a is false, so a && noisy() never calls noisy()
        boolean a = false;
        System.out.println("Question 2, a is false:");
        boolean result = a && noisy();
        System.out.println("   result = " + result + " (no 'evaluated' line above, so b was skipped)");

        // Control: a is true, so Java must evaluate noisy() to decide
        a = true;
        System.out.println("Control, a is true:");
        result = a && noisy();
        System.out.println("   result = " + result);
    }
}
''', output_note='Question 1 is true, and noisy() ran only in the control, so b is skipped when a is false')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I fixed the reversed member check and wrote the grouping out with parentheses, and tested the two lesson cases (20/true/false prints `No discount`, 20/true/true prints `Discount!`) plus four more.

- **0.8 points: Homework completion**
  - **0.5 Leap year rule:** The condition `(year % 4 == 0 && year % 100 != 0) || year % 400 == 0` implements divisible by 4 and not by 100, or divisible by 400, in a single Boolean expression.
  - **0.2 Boundary tests:** The rule is tested against 1900, 2000, 2024 and 2023 (and the extra 1600 and 2100); all PASS.
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: parentheses that make the grouping explicit (in the discount rule and in the leap year rule)
- Present: all four leap year test values checked (2024, 1900, 2000, 2023)
- Absent: a condition that relies on default precedence to be readable (every `&&` inside an `||` is parenthesized)
- Test: 1900 is not a leap year and 2000 is (the output shows `1900 is not a leap year.` and `2000 is a leap year.`)
''', points=[0.2, 0.5, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
outs = outputs_of(path)
nocomment = [re.sub(r'//.*', '', c) for c in codes]
extra = [
    ('3 code cells (popcorn, homework, quick checks)', len(codes) == 3),
    ('Popcorn uses explicit parentheses and no "== false"',
     'age >= 65 || (isStudent && isMember)' in nocomment[0] and '== false' not in nocomment[0]),
    ('Popcorn lesson cases: 20/true/false -> No discount, 20/true/true -> Discount!',
     'age 20, student true, member false: No discount' in outs[0] and 'age 20, student true, member true: Discount!' in outs[0]),
    ('Popcorn: all six cases PASS', outs[0].count('PASS:') == 6),
    ('leap year is one compound expression with && inside || and parentheses',
     '(year % 4 == 0 && year % 100 != 0) || year % 400 == 0' in nocomment[1]),
    ('all four lesson years checked', all(f'{y} ' in outs[1] for y in ('2024', '1900', '2000', '2023'))),
    ('1900 is not a leap year and 2000 is', '1900 is not a leap year.' in outs[1] and '2000 is a leap year.' in outs[1]),
    ('leap year: all six PASS', outs[1].count('PASS:') == 6),
    ('quick check Q1 prints true', 'Question 1: true' in outs[2]),
    ('short circuit proven: noisy() runs only in the control', outs[2].count('noisy() was evaluated') == 1
     and outs[2].index('Control') < outs[2].index('noisy() was evaluated')),
    ('every && inside an || is parenthesized in all conditions',
     not re.search(r'\|\|\s*\w+\s*&&|&&\s*\w+\s*\|\|', ' '.join(nocomment))),
]
ok = audit(path, {
    'layout': 'post', 'title': TITLE, 'categories': f'[Java, {TOPIC}]', 'lesson_language': 'Java',
    'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_5_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
