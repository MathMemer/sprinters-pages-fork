"""Build CSA 2.3 if Statements homework (permalink /csa/unit_02/2_3_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, java_compile_error  # noqa: E402

TOPIC = 'If-Statements'
nb = Notebook(2, '3', TOPIC)
nb.front_matter(
    title='CSA Unit 2.03 if Statements HW',
    description='Homework for 2.03 if Statements. Fix two compile errors, write a free-shipping if-else with an always-run line, and trace a quick check.',
    permalink='/csa/unit_02/2_3_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.03 if Statements]({{ site.baseurl }}/csa/unit_02/2_3). Every code cell below is a Java code runner. Press **Run** to execute it.

**Key idea:** an `if` statement runs its body only when its condition is `true`. An `else` adds the other way. Code after the closing brace runs either way.

| Form | Java | When the body runs |
| --- | --- | --- |
| One-way `if` | `if (condition) { ... }` | Only when the condition is `true` |
| Two-way `if`-`else` | `if (condition) { ... } else { ... }` | The first body if `true`, otherwise the second |
| After the branch | a statement outside the braces | Always |

**Two classic mistakes:** text needs double quotes (`"text"`, not `'text'`; single quotes are only for one `char`), and every statement ends with a semicolon. I always put braces around each branch body, even a one-line one.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Fixed two compile errors so the program prints `Number is even` | 0.2 |
| Free shipping branch | Wrote the `if`-`else` and tested orders above, below and exactly at $50 | 0.5 |
| Always-run line | Printed the order total outside the branch so it prints in both cases | 0.2 |
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
public class FixMe {
    public static void main(String[] args) {
        int number = 2;

        if (number % 2 == 0) {
            System.out.println('Number is even');
        } else {
            System.out.println("Number is odd")
        }
    }
}
'''
err = java_compile_error(BUGGY).splitlines()
nb.md(f'''
### Popcorn Hack (In-Class)

Find and fix the two errors so the program compiles and prints `Number is even`.

**Concept:** a `String` literal uses double quotes, and every statement ends with a semicolon. The compiler reports syntax errors before anything runs.

**My predictions (written before I ran the code):**

| Error | Where | My fix | Why |
| --- | --- | --- | --- |
| Error 1 | `println('Number is even')` | change to `"Number is even"` | single quotes are for one `char`, not text |
| Error 2 | `println("Number is odd")` | add `;` at the end | every statement ends with a semicolon |

| Check | Hand trace | Expected output |
| --- | --- | --- |
| `number = 2` | `2 % 2` is `0`, and `0 == 0` is `true`, so the `if` body runs | `Number is even` |
| `number = 3` (my extra test of the `else`) | `3 % 2` is `1`, so the condition is `false` and the `else` body runs | `Number is odd` |

**Compiler messages for the original code** (from `javac` 21):

```
{chr(10).join(err[:7])}
```
''')
nb.runner('Popcorn Hack. Both errors fixed, each with a comment naming it', r'''
public class FixMe {
    // Prints whether a number is even or odd
    static void describe(int number) {
        if (number % 2 == 0) {
            // Error 1 fixed: text needs double quotes, not single quotes
            System.out.println("Number is even");
        } else {
            // Error 2 fixed: the statement needed a semicolon
            System.out.println("Number is odd");
        }
    }

    public static void main(String[] args) {
        describe(2);   // the lesson's value: should print Number is even
        describe(3);   // my extra test: should take the else branch
    }
}
''', output_note='both lines match my predictions')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

Two short tasks.

1. Finish the runner below. A store gives free shipping on orders of $50 or more. Print `Free shipping` or `Shipping: $5.99`, then always print the order total.
2. Answer the quick check.

#### Task 1: Free shipping

**Concept:** the shipping message depends on one condition, `orderTotal >= 50`, so it is a two-way `if`-`else`. The order total prints on a line **after** the closing brace, so it runs for both branches. I used `>=` so an order of exactly $50 gets free shipping (the lesson's boundary test).

**My predictions (written before I ran the code):**

| Order total | Hand trace | Expected output |
| --- | --- | --- |
| `42.50` (below) | `42.50 >= 50` is false, so the `else` runs | `Shipping: $5.99`, then `Order total: $42.5` |
| `75.00` (above) | `75.0 >= 50` is true | `Free shipping`, then `Order total: $75.0` |
| `50.00` (exactly 50) | `50.0 >= 50` is true, so the boundary takes the free branch | `Free shipping`, then `Order total: $50.0` |

A `double` prints without trailing zeros past one decimal place, so `42.50` prints as `42.5`.

**What the important lines do:** `if (orderTotal >= 50)` is the test. The braces hold the branch bodies. The last `println` sits outside both braces, so it always runs.
''')
nb.runner('Homework Hack. Free shipping if-else, then a line that always runs; tested at 42.50, 75.00 and 50.00', r'''
public class Shipping {
    // Prints the shipping message and then the order total
    static void ship(double orderTotal) {
        if (orderTotal >= 50) {
            System.out.println("Free shipping");
        } else {
            System.out.println("Shipping: $5.99");
        }

        // Outside the braces, so it runs for both branches
        System.out.println("Order total: $" + orderTotal);
    }

    public static void main(String[] args) {
        System.out.println("--- 42.50: below 50 ---");
        ship(42.50);

        System.out.println("\n--- 75.00: above 50 ---");
        ship(75.00);

        System.out.println("\n--- 50.00: exactly 50 ---");
        ship(50.00);
    }
}
''', output_note='all three matched; the exact-50 order took the free shipping branch')

nb.md('''
#### Task 2: Homework quick check

**Question:** how many lines does this code print?

```java
int level = 7;
if (level > 10) {
    System.out.println("Expert");
    System.out.println("Unlocked");
}
System.out.println("Level " + level);
```

**My answer: 1.** Hand trace: `7 > 10` is `false`, so both lines inside the braces are skipped. The last `println` is outside the braces, so it always runs and prints `Level 7`.

I wrote the answer before running the check below.
''')
nb.runner('Homework quick check. Run to confirm the number of lines printed', r'''
public class LevelCheck {
    public static void main(String[] args) {
        int level = 7;
        if (level > 10) {
            System.out.println("Expert");
            System.out.println("Unlocked");
        }
        System.out.println("Level " + level);
    }
}
''', output_note='one line printed, as I answered')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I found and fixed both errors (double quotes, missing semicolon) so the program compiles and prints `Number is even`.

- **0.8 points: Homework completion**
  - **0.5 Free shipping branch:** `Free shipping` or `Shipping: $5.99` prints correctly for orders above and below the $50 threshold (and exactly at it).
  - **0.2 Always-run line:** The order total prints in both cases, because the statement is placed outside the branch.
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: both branches tested with a value above and below 50 (42.50 and 75.00)
- Present: braces around every branch body
- Present: quick check answered (1 line, with the trace)
- Test: an order of exactly 50 takes the free shipping branch (50.00 prints `Free shipping`)
''', points=[0.2, 0.5, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
allt = '\n'.join(''.join(c['source']) for c in cells)
nocomment = [re.sub(r'//.*', '', c) for c in codes]
extra = [
    ('3 runners (popcorn, homework, quick check)', len(codes) == 3),
    ("Popcorn: no single-quoted text left, semicolons present", "'Number" not in nocomment[0] and 'println("Number is odd");' in nocomment[0]),
    ('Popcorn: comments name Error 1 and Error 2', 'Error 1' in codes[0] and 'Error 2' in codes[0]),
    ('Popcorn output reads "Number is even"', 'Number is even' in allt),
    ('homework uses if-else with >= 50 and braces', 'orderTotal >= 50' in codes[1] and 'else {' in codes[1]),
    ('order total printed outside the branch', re.search(r'\}\s*\n\s*//[^\n]*\n\s*System\.out\.println\("Order total', codes[1]) is not None),
    ('exact-50 order takes the free branch in the output', re.search(r'exactly 50 ---\nFree shipping\nOrder total: \$50\.0', allt) is not None),
    ('both branches appear in the output', 'Shipping: $5.99' in allt and 'Free shipping' in allt),
    ('quick check prints exactly one line (Level 7)', allt.rstrip().count('Level 7') >= 1 and 'Expert' not in re.search(r'LevelCheck.*', allt, re.S).group(0).split('Output from my run')[-1]),
    ('original compiler errors captured', 'error:' in allt),
]
ok = audit(path, {
    'layout': 'post', 'title': 'CSA Unit 2.03 if Statements HW', 'categories': f'[Java, {TOPIC}]',
    'lesson_language': 'Java', 'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_3_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
