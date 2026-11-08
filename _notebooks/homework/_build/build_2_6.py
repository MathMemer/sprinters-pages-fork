"""Build CSA 2.6 Comparing Boolean Expressions homework (permalink /csa/unit_02/2_6_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, outputs_of, java_run  # noqa: E402

TOPIC = 'Comparing-Boolean-Expressions'
TITLE = 'CSA Unit 2.06 Comparing Boolean Expressions HW'
nb = Notebook(2, '6', TOPIC)
nb.front_matter(
    title=TITLE,
    description='Homework for 2.06 Comparing Boolean Expressions. Rewrite a condition with De Morgan\'s Law, fix a String comparison, and prove two expressions equivalent with a truth table.',
    permalink='/csa/unit_02/2_6_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.06 Comparing Boolean Expressions]({{ site.baseurl }}/csa/unit_02/2_6). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** two Boolean expressions are **equivalent** when they give the same value for every possible input. A truth table lists every combination, so it can prove equivalence.

**De Morgan's Laws** move a `!` inside a group and flip the operator:

| Original | Equivalent |
| --- | --- |
| `!(a && b)` | `!a \\|\\| !b` |
| `!(a \\|\\| b)` | `!a && !b` |
| `!!a` | `a` |

**Flip rules for comparisons** remove a `!` from in front of one:

| Original | Equivalent |
| --- | --- |
| `!(x < y)` | `x >= y` |
| `!(x > y)` | `x <= y` |
| `!(x <= y)` | `x > y` |
| `!(x >= y)` | `x < y` |
| `!(x == y)` | `x != y` |

**Comparing objects:** `==` on two `String` variables asks "are they the same object in memory?", not "do they have the same characters?". To compare the characters, call `a.equals(b)`.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Rewrote `!(age >= 18 \\|\\| !member)` with no `!` and compared it with the original on every input | 0.2 |
| String comparison fix | Replaced `==` with `.equals` so a password built at run time still matches | 0.5 |
| Second check | Added the length check (fewer than 8 characters) with no `!` | 0.2 |
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

The condition below works but is hard to read. Rewrite it without any `!` so it still prints the same result for every `age` and `member` combination. Test with `(15, true)`, `(20, false)`, and `(20, true)`.

```java
if (!(age >= 18 || !member)) {
    System.out.println("Youth member rate");
} else {
    System.out.println("Standard rate");
}
```

**Concept:** remove the `!` in two steps: De Morgan's Law first, then the flip rules.

| Step | Expression | Rule used |
| --- | --- | --- |
| Start | `!(age >= 18 \\|\\| !member)` | the original |
| 1 | `!(age >= 18) && !(!member)` | De Morgan: `!(a \\|\\| b)` becomes `!a && !b` |
| 2 | `age < 18 && member` | flip rule: `!(age >= 18)` is `age < 18`, and `!(!member)` is `member` |

**My rewrite:** `age < 18 && member`. In words: "a youth rate for members under 18".

**My predictions (written before I ran the code): the truth table over every input.** `A` is `age >= 18`.

| `age` | `member` | `A` | `!(A \\|\\| !member)` | `age < 18 && member` | Prints |
| --- | --- | --- | --- | --- | --- |
| `15` | `true` | false | `!(false \\|\\| false)` = true | true | Youth member rate |
| `15` | `false` | false | `!(false \\|\\| true)` = false | false | Standard rate |
| `20` | `true` | true | `!(true \\|\\| false)` = false | false | Standard rate |
| `20` | `false` | true | `!(true \\|\\| true)` = false | false | Standard rate |
| `17` (boundary) | `true` | false | true | true | Youth member rate |
| `18` (boundary) | `true` | true | false | false | Standard rate |

The two columns match on every row, so the rewrite is equivalent.

**What the important lines do:** `rewritten` is the new condition with no `!`. I kept `original` in the same cell only so the program can compare the two on every input and print PASS or FAIL; it is not part of the answer.
''')
nb.runner('Popcorn Hack. The condition rewritten with no ! and compared with the original on six inputs', r'''
public class Simplify {
    // The original condition. Kept only so the program can check my rewrite against it
    static boolean original(int age, boolean member) {
        return !(age >= 18 || !member);
    }

    // My rewrite with no ! at all: De Morgan, then flip the comparison
    static boolean rewritten(int age, boolean member) {
        return age < 18 && member;
    }

    // Prints the rate for one customer and checks it against the original and against my prediction
    static void rate(int age, boolean member, String expected) {
        String result;
        if (age < 18 && member) {
            result = "Youth member rate";
        } else {
            result = "Standard rate";
        }

        System.out.println("age " + age + ", member " + member + " -> " + result);
        boolean sameAsOriginal = original(age, member) == rewritten(age, member);
        System.out.println((result.equals(expected) && sameAsOriginal ? "PASS: " : "FAIL: ")
                + "matches my prediction and the original condition");
    }

    public static void main(String[] args) {
        // The three pairs the lesson lists
        rate(15, true, "Youth member rate");
        rate(20, false, "Standard rate");
        rate(20, true, "Standard rate");

        // The rest of the truth table, and the boundary at 18
        rate(15, false, "Standard rate");
        rate(17, true, "Youth member rate");
        rate(18, true, "Standard rate");
    }
}
''', output_note='all six inputs matched my truth table and the original condition')
nb.md('**What I learned:** I did not have to guess that the rewrite was right. The truth table covers every input, and the two columns match on every row. The boundary rows (17 and 18) matter because they are where `age < 18` and `age >= 18` change places.')

# ---------------------------------------------------------------- homework
ORIGINAL = r'''
public class PasswordCheck {
    public static void main(String[] args) {
        String saved = new String("open-sesame");
        String typed = new String("open-sesame");

        if (typed == saved) {
            System.out.println("Welcome back!");
        } else {
            System.out.println("Wrong password.");
        }
    }
}
'''
orig_out = java_run(ORIGINAL)
nb.md(f'''
### Homework Hack

Two short tasks.

1. Finish the code below: the password checker has a bug because it uses `==` on Strings. Fix it, then add the second check described in the comment.
2. Answer the quick check.

#### Task 1: The password checker

**The bug.** In the starter, `typed` and `saved` both hold `"open-sesame"`, yet the check says the password is wrong. I ran the original code to see:

```
{orig_out}
```

`==` on two `String` variables compares **references**: it asks whether they are the same object. `new String("open-sesame")` makes two separate objects, so `==` is `false` even though the characters are identical. `typed.equals(saved)` compares the **characters**, so it is `true`. A real password comes from a form and is built at run time, so it is never the same object as the saved one; `==` would reject every correct password.

**Fix 1:** `typed.equals(saved)`.

**Fix 2 (the second check):** print `Too short` if `typed` has fewer than 8 characters, otherwise `Length OK`, with no `!` anywhere. `typed.length() < 8` already asks "is it shorter than 8?", so no `!` is needed.

**My predictions (written before I ran the code):**

| What is typed | Same characters as `open-sesame`? | Length | Prints |
| --- | --- | --- | --- |
| `new String("open-sesame")` | yes | 11 | Welcome back! / Length OK |
| `"open-"` + `"sesame"` (joined at run time) | yes (`.equals` compares characters) | 11 | Welcome back! / Length OK |
| `open-sesam` (one letter short) | no | 10 | Wrong password. / Length OK |
| `abcdefgh` (boundary: exactly 8) | no | 8 | Wrong password. / Length OK (`8 < 8` is false) |
| `abcdefg` (boundary: 7) | no | 7 | Wrong password. / Too short |

**What the important lines do:** `new String("open-sesame")` makes a separate String object, as a password read at run time would be. `typed.equals(saved)` compares characters. `typed.length() < 8` is the length test. The `login` method runs both checks for one typed password, so one run covers every row, and it prints PASS or FAIL against my prediction.
''')
nb.runner('Homework Hack. .equals instead of ==, plus a length check with no !, tested on five passwords', r'''
public class PasswordCheck {
    // Runs both checks for one typed password and compares them with my predictions
    static void login(String typed, String expectedWelcome, String expectedLength) {
        String saved = new String("open-sesame");   // a separate object, like a password read at run time
        String welcome;
        String length;

        // TODO 1 fixed: Strings are compared by their characters with .equals, not by reference with ==
        if (typed.equals(saved)) {
            welcome = "Welcome back!";
        } else {
            welcome = "Wrong password.";
        }

        // TODO 2: fewer than 8 characters. "< 8" asks the question directly, so no ! is needed
        if (typed.length() < 8) {
            length = "Too short";
        } else {
            length = "Length OK";
        }

        System.out.println("Typed: " + typed);
        System.out.println(welcome);
        System.out.println(length);
        boolean allMatch = welcome.equals(expectedWelcome) && length.equals(expectedLength);
        System.out.println((allMatch ? "PASS: " : "FAIL: ") + "both checks match my prediction");
    }

    public static void main(String[] args) {
        // A copy made with new String: different object, same characters
        login(new String("open-sesame"), "Welcome back!", "Length OK");

        // A password assembled by concatenation at run time: still matches with .equals
        String firstHalf = "open-";
        login(firstHalf + "sesame", "Welcome back!", "Length OK");

        // A wrong password, and the two boundaries of the length check
        login("open-sesam", "Wrong password.", "Length OK");
        login("abcdefgh", "Wrong password.", "Length OK");
        login("abcdefg", "Wrong password.", "Too short");
    }
}
''', output_note='all five predictions matched, including the password assembled by concatenation')

nb.md('''
#### Task 2: Homework quick check

**Question:** are `!(a && !b)` and `!a || b` equivalent? Type true or false.

**My answer: `true`.** Two ways to show it.

**By De Morgan's Law:** `!(a && !b)` becomes `!a || !(!b)`, and `!(!b)` is just `b`, so it is `!a || b`.

**By truth table** (all four input combinations):

| `a` | `b` | `!b` | `a && !b` | `!(a && !b)` | `!a` | `!a \\|\\| b` | Same? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| true | true | false | false | true | false | true | yes |
| true | false | true | true | false | false | false | yes |
| false | true | false | false | true | true | true | yes |
| false | false | true | false | true | true | true | yes |

I wrote the answer before running the check below, which prints the same table.
''')
nb.runner('Homework quick check. Run to confirm the truth table for !(a && !b) and !a || b', r'''
public class EquivalenceCheck {
    // Prints one row of the truth table for both expressions
    static boolean row(boolean a, boolean b) {
        boolean left = !(a && !b);
        boolean right = !a || b;
        System.out.println("a=" + a + ", b=" + b + ":  !(a && !b) = " + left + ",  !a || b = " + right);
        return left == right;
    }

    public static void main(String[] args) {
        boolean r1 = row(true, true);
        boolean r2 = row(true, false);
        boolean r3 = row(false, true);
        boolean r4 = row(false, false);
        System.out.println("Equivalent: " + (r1 && r2 && r3 && r4));
    }
}
''', output_note='all four rows match, so the expressions are equivalent')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I rewrote the condition as `age < 18 && member` (no `!`) and confirmed identical results for the three listed pairs (15/true, 20/false, 20/true) and for every other input in the truth table.

- **0.8 points: Homework completion**
  - **0.5 String comparison fix:** The password check uses `.equals` rather than `==`, and works for a String built at run time (the `new String` copy and the concatenated password both print `Welcome back!`).
  - **0.2 Second check:** The length check from the runner comment is implemented with no `!` (`typed.length() < 8`) and tested at the boundaries (7 characters prints `Too short`, 8 prints `Length OK`).
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: `.equals` used for every String content comparison (`typed.equals(saved)`)
- Present: truth table covering all input combinations (the Popcorn table has every `age`/`member` combination, and the quick check lists all four `a`/`b` rows)
- Absent: `==` comparing String contents (the fixed code uses `.equals`; the original `==` is shown only as captured output)
- Test: a password assembled by concatenation still matches (`"open-"` + `"sesame"` prints `Welcome back!`)
''', points=[0.2, 0.5, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
outs = outputs_of(path)
allt = '\n'.join(''.join(c['source']) for c in cells)
strip = lambda s: re.sub(r'"(?:[^"\\]|\\.)*"', '""', re.sub(r'//.*', '', s))   # drop comments and string literals
rewritten_body = re.search(r'static boolean rewritten\(.*?\n    \}', codes[0], re.S).group(0)
extra = [
    ('3 code cells (popcorn, homework, quick check)', len(codes) == 3),
    ('Popcorn rewrite has no !', '!' not in strip(rewritten_body) and 'if (age < 18 && member)' in codes[0]),
    ('Popcorn lesson pairs: 15/true Youth, 20/false Standard, 20/true Standard',
     'age 15, member true -> Youth member rate' in outs[0] and 'age 20, member false -> Standard rate' in outs[0]
     and 'age 20, member true -> Standard rate' in outs[0]),
    ('Popcorn: all six inputs PASS (rewrite equals the original)', outs[0].count('PASS:') == 6),
    ('Popcorn truth table lists all four age/member combinations plus both boundaries',
     all(f'| `{a}` | `{m}` |' in allt for a, m in (('15', 'true'), ('15', 'false'), ('20', 'true'), ('20', 'false')))),
    ('homework uses .equals and never == between Strings', 'typed.equals(saved)' in codes[1] and 'typed == saved' not in codes[1]),
    ('homework length check has no !', '!' not in strip(codes[1])),
    ('concatenated password still matches', 'Typed: open-sesame\nWelcome back!' in outs[1] and outs[1].count('Welcome back!') == 2),
    ('length boundaries: 8 -> Length OK, 7 -> Too short', 'Typed: abcdefgh\nWrong password.\nLength OK' in outs[1] and 'Typed: abcdefg\nWrong password.\nToo short' in outs[1]),
    ('homework: all five PASS', outs[1].count('PASS:') == 5),
    ('original == bug shown as captured output (Wrong password.)', 'Wrong password.' in allt.split('#### Task 1')[1].split('**The bug.**')[1].split('**Fix 1')[0]),
    ('quick check: four rows and Equivalent: true', outs[2].count('a=') == 4 and 'Equivalent: true' in outs[2]),
]
ok = audit(path, {
    'layout': 'post', 'title': TITLE, 'categories': f'[Java, {TOPIC}]', 'lesson_language': 'Java',
    'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_6_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
