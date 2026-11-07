"""Build CSA 2.4 Nested if Statements homework (permalink /csa/unit_02/2_4_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, outputs_of  # noqa: E402

TOPIC = 'Nested-If-Statements'
TITLE = 'CSA Unit 2.04 Nested `if` Statements HW'
nb = Notebook(2, '4', TOPIC)
nb.front_matter(
    title=TITLE,
    description='Homework for 2.04 Nested if Statements. Extend an else-if chain to five letter grades, write a nested if for member discounts, and trace a quick check.',
    permalink='/csa/unit_02/2_4_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.04 Nested `if` Statements]({{ site.baseurl }}/csa/unit_02/2_4). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** to choose between three or more cases, chain decisions with `else if`, or put one `if` inside another. Java checks the conditions from top to bottom and runs only the **first** branch whose condition is `true`.

| Pattern | Java | Use it when |
| --- | --- | --- |
| `else if` chain | `if (a) { ... } else if (b) { ... } else { ... }` | The cases are alternatives and only one should run |
| Nested `if` | `if (a) { if (b) { ... } else { ... } }` | The second question only matters when the first answer is `true` |

**Order matters in a chain.** Each branch only sees values the earlier branches rejected, so I test the highest cutoff first. If `>= 60` came before `>= 90`, a 95 would print D, and the A branch could never run (an unreachable branch).

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Extended the chain to A, B, C, D and F and tested 90, 75, 61 and 40 (plus the boundaries) | 0.2 |
| Nested discount | Wrote a nested `if` for member discounts | 0.5 |
| Case coverage | Tested non-members, members under $100 and members at or above $100 | 0.2 |
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

Add branches so the program prints the right letter for every average: A (90 and up), B (80 to 89), C (70 to 79), D (60 to 69), F (below 60). Test with 90, 75, 61, and 40.

**Concept:** an `else if` chain with the highest cutoff first. A value reaches `>= 80` only after `>= 90` was false, so the B branch already means "80 to 89" without writing `< 90`.

**My predictions (written before I ran the code):**

| Average | Hand trace | Prints |
| --- | --- | --- |
| `90` | `90 >= 90` is true | A |
| `75` | `>= 90` false, `>= 80` false, `>= 70` true | C |
| `61` | `>= 90`, `>= 80`, `>= 70` false, `>= 60` true | D |
| `40` | every test is false, so the `else` runs | F |
| `89.9` (boundary) | `>= 90` false, `>= 80` true | B |
| `80` (boundary) | `>= 90` false, `>= 80` true | B |
| `70` (boundary) | `>= 80` false, `>= 70` true | C |
| `60` (boundary) | `>= 70` false, `>= 60` true | D |
| `59.9` (boundary) | every test is false | F |

**What the important lines do:** each `else if` is only checked when every test above it was `false`. The final `else` has no condition: it catches everything below 60. I wrapped the chain in a method `evaluate(average, expectedLetter)` so one run can test all nine values, and each branch also stores its letter so the program can print PASS or FAIL against my prediction.
''')
nb.runner('Popcorn Hack. The chain extended with C, D and F, tested at 90, 75, 61, 40 and the boundaries', r'''
public class GradeEvaluator {
    // Prints the grade message for one average and checks it against the letter I predicted
    static void evaluate(double myAverage, String expectedLetter) {
        System.out.println("Current average: " + myAverage);
        String letter;

        // Highest cutoff first, so each branch only sees averages the branches above it rejected
        if (myAverage >= 90) {
            System.out.println("You have an A average.");
            letter = "A";
        } else if (myAverage >= 80) {
            System.out.println("You have a B average.");
            letter = "B";
        } else if (myAverage >= 70) {
            System.out.println("You have a C average.");
            letter = "C";
        } else if (myAverage >= 60) {
            System.out.println("You have a D average.");
            letter = "D";
        } else {
            System.out.println("You have an F average.");
            letter = "F";
        }

        System.out.println((letter.equals(expectedLetter) ? "PASS: " : "FAIL: ") + myAverage + " is " + expectedLetter);
    }

    public static void main(String[] args) {
        // The four values the lesson asks for
        evaluate(90, "A");
        evaluate(75, "C");
        evaluate(61, "D");
        evaluate(40, "F");

        // My boundary tests
        evaluate(89.9, "B");
        evaluate(80, "B");
        evaluate(70, "C");
        evaluate(60, "D");
        evaluate(59.9, "F");
    }
}
''', output_note='all nine predictions matched, so no branch is unreachable')
nb.md('**What I learned:** the order of the tests is part of the logic. Because each branch runs only when the ones above it were false, the highest cutoff must come first. The boundaries (80, 70, 60) land in the higher grade because each test uses `>=`.')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

Two short tasks.

1. Finish the code below with a **nested if**: members get a discount, and members who spend $100 or more get a bigger one.
2. Answer the quick check.

#### Task 1: Member discount

**Concept:** the "spend $100" question only matters for members, so it goes **inside** the `if (isMember)` branch. A non-member never reaches the inner `if`, so `discount` keeps its starting value of `0`. A flat chain would have to repeat `isMember` in every condition.

| Who | Rule | Discount |
| --- | --- | --- |
| Non-member | the outer `if` is false | `0` (stays at its start value) |
| Member, total under $100 | outer true, inner `total >= 100` false | `0.10` (10%) |
| Member, total $100 or more | outer true, inner true | `0.20` (20%) |

**My predictions (written before I ran the code):**

| `isMember` | `total` | Hand trace | Discount | You pay |
| --- | --- | --- | --- | --- |
| `true` | `120.0` | member, `120 >= 100` | `20.0%` | `120 - 24 =` `$96.0` |
| `true` | `100.0` | member, boundary `100 >= 100` is true | `20.0%` | `100 - 20 =` `$80.0` |
| `true` | `80.0` | member, `80 >= 100` is false | `10.0%` | `80 - 8 =` `$72.0` |
| `false` | `200.0` | not a member, so the inner `if` never runs | `0.0%` | `$200.0` |
| `false` | `50.0` | not a member | `0.0%` | `$50.0` |

**What the important lines do:** `double discount = 0;` is the default for non-members. The outer `if (isMember)` decides whether any discount applies. The inner `if (total >= 100)` picks 20% or 10%. `total - total * discount` takes the discount off. I put the logic in a method `checkout(isMember, total, expectedDiscount)` so one run covers every case, and it prints PASS or FAIL against my prediction.
''')
nb.runner('Homework Hack. Nested if for member discounts, tested for non-members, members under $100 and members at or above $100', r'''
public class Discount {
    static void check(String label, boolean passed) {
        System.out.println((passed ? "PASS: " : "FAIL: ") + label);
    }

    // Applies the member discount rules for one purchase
    static void checkout(boolean isMember, double total, double expectedDiscount) {
        double discount = 0;

        if (isMember) {
            // Nested: only members are asked whether they spent $100 or more
            if (total >= 100) {
                discount = 0.20;
            } else {
                discount = 0.10;
            }
        }
        // A non-member never reaches the inner if, so discount stays 0

        System.out.println("Member: " + isMember + ", total: $" + total);
        System.out.println("Discount: " + (discount * 100) + "%");
        System.out.println("You pay: $" + (total - total * discount));
        check("discount is " + (expectedDiscount * 100) + "%", Math.abs(discount - expectedDiscount) < 1e-9);
    }

    public static void main(String[] args) {
        System.out.println("--- Member spending 120 (expected: 20.0% and $96.0) ---");
        checkout(true, 120.0, 0.20);

        System.out.println("\n--- Member spending exactly 100 (boundary) ---");
        checkout(true, 100.0, 0.20);

        System.out.println("\n--- Member spending 80 (under 100) ---");
        checkout(true, 80.0, 0.10);

        System.out.println("\n--- Non-member spending 200 (no discount) ---");
        checkout(false, 200.0, 0.0);

        System.out.println("\n--- Non-member spending 50 ---");
        checkout(false, 50.0, 0.0);
    }
}
''', output_note='every case matched my predictions, and the non-member who spent $200 got no discount')

nb.md('''
#### Task 2: Homework quick check

**Question:** what does this print when `temp` is 75? Type the exact word.

```java
if (temp > 85) {
    System.out.println("Hot");
} else if (temp > 70) {
    System.out.println("Warm");
} else if (temp > 50) {
    System.out.println("Cool");
} else {
    System.out.println("Cold");
}
```

**My answer: `Warm`.** Hand trace: `75 > 85` is `false`, so `Hot` is skipped. `75 > 70` is `true`, so `Warm` prints, and the rest of the chain (`Cool`, `Cold`) is skipped because only the first true branch runs.

I wrote the answer before running the check below.
''')
nb.runner('Homework quick check. Run to confirm the word printed for temp 75', r'''
public class TempCheck {
    public static void main(String[] args) {
        int temp = 75;
        if (temp > 85) {
            System.out.println("Hot");
        } else if (temp > 70) {
            System.out.println("Warm");
        } else if (temp > 50) {
            System.out.println("Cool");
        } else {
            System.out.println("Cold");
        }
    }
}
''', output_note='Warm, as I answered')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I added branches covering A, B, C, D and F and tested with 90, 75, 61 and 40 (and the boundaries 89.9, 80, 70, 60 and 59.9).

- **0.8 points: Homework completion**
  - **0.5 Nested discount:** A nested `if` gives members a discount, and gives members spending $100 or more the larger discount (20% against 10%).
  - **0.2 Case coverage:** Non-members ($200 and $50), members under $100 ($80) and members at or above $100 ($120 and exactly $100) are each tested.
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: all five grade branches tested with the four listed values (90, 75, 61 and 40 print A, C, D and F; 80 to 89 prints B)
- Present: nested structure, not a flat chain, for the member discount (`if (total >= 100)` is inside `if (isMember)`)
- Absent: an unreachable branch caused by condition order (the cutoffs run from 90 down to 60, and all nine tests pass)
- Test: a non-member spending $200 receives no discount (Discount: 0.0%, You pay: $200.0)
''', points=[0.2, 0.5, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
outs = outputs_of(path)
nocomment = [re.sub(r'//.*', '', c) for c in codes]
extra = [
    ('3 code cells (popcorn, homework, quick check)', len(codes) == 3),
    ('Popcorn chain has cutoffs 90, 80, 70, 60 in descending order and a final else',
     re.findall(r'else if \(myAverage >= (\d+)\)', nocomment[0]) == ['80', '70', '60'] and 'myAverage >= 90' in nocomment[0] and '} else {' in nocomment[0]),
    ('Popcorn output: 90->A, 75->C, 61->D, 40->F',
     all(f'PASS: {a} is {l}' in outs[0] for a, l in (('90.0', 'A'), ('75.0', 'C'), ('61.0', 'D'), ('40.0', 'F')))),
    ('Popcorn boundaries tested (89.9, 80, 70, 60, 59.9)', all(f'PASS: {a} is' in outs[0] for a in ('89.9', '80.0', '70.0', '60.0', '59.9'))),
    ('homework is a NESTED if (inner test inside if (isMember))',
     re.search(r'if \(isMember\) \{\s*\n\s*if \(total >= 100\)', nocomment[1]) is not None),
    ('homework is not a flat chain (no else-if on isMember)', 'else if (isMember' not in nocomment[1]),
    ('lesson example: member spending 120 -> 20.0% and $96.0', 'Discount: 20.0%\nYou pay: $96.0' in outs[1]),
    ('non-member spending 200 receives no discount', 'Member: false, total: $200.0\nDiscount: 0.0%\nYou pay: $200.0' in outs[1]),
    ('three kinds of customer covered (non-member, member <100, member >=100)',
     'Discount: 10.0%' in outs[1] and 'Discount: 20.0%' in outs[1] and 'Discount: 0.0%' in outs[1]),
    ('quick check prints exactly Warm', outs[2].strip() == 'Warm'),
]
ok = audit(path, {
    'layout': 'post', 'title': TITLE, 'categories': f'[Java, {TOPIC}]', 'lesson_language': 'Java',
    'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_4_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
