"""Build CSA 1.11 Math Class homework (permalink /csa/unit_01/1_11_student_hw).

The teacher's own separate homework page already owns /csa/unit_01/1_11_hw, so this one uses _student_hw.
"""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, submission_notes, audit  # noqa: E402

PERMALINK = '/csa/unit_01/1_11_student_hw'
nb = Notebook(1, '11', 'Math-Class')
nb.front_matter(
    title='CSA Unit 1.11 Math Class HW',
    description='Homework for 1.11 Math Class. Predict Math results, build a random range 10 to 20, and finish a loot-drop program with Math.random().',
    permalink=PERMALINK)

nb.md('''
## 1. Overview

This is my homework notebook for [1.11 Math Class]({{ site.baseurl }}/csa/unit_01/1_11). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** the `Math` class has static methods, so I call them on the class name with no object: `Math.abs(-8)`.

| Method | Returns | Example | Result |
| --- | --- | --- | --- |
| `Math.abs(x)` | same type as `x` | `Math.abs(-8)` | `8` |
| `Math.pow(base, exp)` | `double` | `Math.pow(3, 2)` | `9.0` |
| `Math.sqrt(x)` | `double` | `Math.sqrt(36)` | `6.0` |
| `Math.random()` | `double`, from `0.0` up to but not including `1.0` | `Math.random()` | for example `0.4271...` |

**Random whole number from `min` through `max` (inclusive):** `(int)(Math.random() * (max - min + 1)) + min`.

| Step | `min = 10`, `max = 20` | Lowest case | Highest case |
| --- | --- | --- | --- |
| `Math.random()` | `0.0` to just under `1.0` | `0.0` | `0.9999` |
| `* (max - min + 1)` | times `11` | `0.0` | `10.9989` |
| `(int)` | truncates | `0` | `10` |
| `+ min` | plus `10` | `10` | `20` |

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack #1 | Predicted three `Math` values and wrote a distance expression | 0.1 |
| Popcorn Hack #2 | Built a random 10 to 20 range and ran it more than once | 0.1 |
| MCQ | Taken on the lesson page; the score line goes in the Submission Notes | 0.2 |
| Homework Hack | Finished the loot-drop program with `Math.random()` for the rarity roll and the gold value | 0.6 |
''')

nb.md('## 2. Hacks & Practice Tasks')
nb.md(safety_rules([
    'One class per cell, ending with `ClassName.main(null);`.',
    'Run each cell and leave the output showing.',
    'Write your own answers, not the sample code from the lesson.',
    'Include your MCQ score.',
    'Use `##` headings or smaller.',
]))

# ---------------------------------------------------------------- popcorn 1
nb.md('''
### Popcorn Hack #1 (In-Class)

2-minute challenge: predict without running.

**Concept:** `Math.abs` keeps the type of its argument, so an `int` gives an `int`. `Math.pow` and `Math.sqrt` always return a `double`, so their results print with `.0`. The distance between `(0, 0)` and `(3, 4)` is `sqrt((3 - 0)^2 + (4 - 0)^2)`.

**My predictions (written before I ran the code):**

| Expression | My prediction | Why |
| --- | --- | --- |
| `Math.abs(-8)` | `8` | Absolute value drops the sign; the argument is an `int`, so the result is an `int` |
| `Math.pow(3, 2)` | `9.0` | `3 * 3 = 9`, and `pow` returns a `double` |
| `Math.sqrt(36)` | `6.0` | `6 * 6 = 36`, and `sqrt` returns a `double` |
| Distance `(0, 0)` to `(3, 4)` | `5.0` | `sqrt(3^2 + 4^2) = sqrt(9 + 16) = sqrt(25)` |
''')
nb.runner('Popcorn Hack #1. My predictions are filled in, so run it and compare', r'''
public class PopcornMath {
    // My predictions, written BEFORE I ran the code
    static String guess1 = "8";    // Math.abs(-8)
    static String guess2 = "9.0";  // Math.pow(3, 2)
    static String guess3 = "6.0";  // Math.sqrt(36)

    public static void main(String[] args) {
        System.out.println("Predictions: " + guess1 + ", " + guess2 + ", " + guess3);
        System.out.println("Actual:");
        System.out.println(Math.abs(-8));
        System.out.println(Math.pow(3, 2));
        System.out.println(Math.sqrt(36));

        // Distance between (0, 0) and (3, 4): sqrt((3 - 0)^2 + (4 - 0)^2)
        double distance = Math.sqrt(Math.pow(3 - 0, 2) + Math.pow(4 - 0, 2));
        System.out.println("Distance: " + distance);
    }
}
''')

# ---------------------------------------------------------------- popcorn 2
nb.md('''
### Popcorn Hack #2 (In-Class)

**Task:** generate a random integer from 10 through 20, inclusive. Run it several times and confirm it never prints 9 or 21.

**Concept:** `Math.random()` is never `1.0`, so `Math.random() * 11` is below `11`, and `(int)` of that is at most `10`. Adding `min` gives `10` to `20`. Multiplying by `(max - min + 1)` (not `max - min`) is what lets `20` appear.

**My predictions (written before I ran the code):**

| Question | My prediction | Why |
| --- | --- | --- |
| Smallest roll | `10` | `(int)(0.0 * 11) + 10` |
| Largest roll | `20` | `(int)(0.9999 * 11) = 10`, then `+ 10` |
| Can `9` or `21` appear? | No | The formula cannot go below `10` or above `20` |

**What the important lines do:** `randomBetween(min, max)` holds the formula so I can reuse it. Five rolls in one run, plus running the cell again, test more than once.
''')
nb.runner('Popcorn Hack #2. Random 10 to 20: run it several times and check it never leaves the range', r'''
public class PopcornRange {
    // Random whole number from min through max, inclusive
    static int randomBetween(int min, int max) {
        return (int)(Math.random() * (max - min + 1)) + min;
    }

    public static void main(String[] args) {
        int min = 10;
        int max = 20;

        int roll1 = randomBetween(min, max);
        int roll2 = randomBetween(min, max);
        int roll3 = randomBetween(min, max);
        int roll4 = randomBetween(min, max);
        int roll5 = randomBetween(min, max);

        System.out.println("Roll 1 (10-20): " + roll1);
        System.out.println("Roll 2 (10-20): " + roll2);
        System.out.println("Roll 3 (10-20): " + roll3);
        System.out.println("Roll 4 (10-20): " + roll4);
        System.out.println("Roll 5 (10-20): " + roll5);

        boolean allInRange = roll1 >= min && roll1 <= max && roll2 >= min && roll2 <= max
                && roll3 >= min && roll3 <= max && roll4 >= min && roll4 <= max
                && roll5 >= min && roll5 <= max;
        System.out.println((allInRange ? "PASS: " : "FAIL: ") + "all five rolls are between 10 and 20");
    }
}
''', output_note='all rolls stayed inside 10 to 20', random_note=True)

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

**Task:** finish the loot-drop program. It rolls a random rarity roll from 1 to 100, turns the roll into `Common`, `Rare`, or `Legendary`, and then picks a random gold value from a range that depends on the rarity. Both random values must come from `Math.random()`.

The lesson does not give the cutoffs, so I chose them and wrote them down:

| Rarity | Roll | Chance | Gold range |
| --- | --- | --- | --- |
| Common | `1` to `70` | 70% | `5` to `20` |
| Rare | `71` to `95` | 25% | `25` to `75` |
| Legendary | `96` to `100` | 5% | `100` to `500` |

**Concept:** the rarity roll and the gold value both use the random-range formula `(int)(Math.random() * (max - min + 1)) + min`. The rarity decides which `min` and `max` the gold roll gets.

**What the important lines do:** `rarityFor(roll)` is an `if` / `else if` / `else` chain from the table. `goldFor(rarity)` picks the gold range for that rarity. `goldInRange` re-checks the answer so each drop prints PASS or FAIL.

**My predictions and expected values (written before I ran the code):**

| Test | Hand trace | Expected |
| --- | --- | --- |
| `rarityFor(1)` and `rarityFor(70)` | both are `<= 70` | `Common` |
| `rarityFor(71)` and `rarityFor(95)` | above 70, at most 95 | `Rare` |
| `rarityFor(96)` and `rarityFor(100)` | above 95 | `Legendary` |
| Any rarity roll | formula with `min = 1`, `max = 100` | `1` to `100` |
| Any gold value | formula with that rarity's `min` and `max` | inside the table range |
''')
nb.runner('Homework Hack. Loot drop with Math.random(): run it a few times', r'''
public class RandomLoot {
    // Random whole number from min through max, inclusive
    static int randomBetween(int min, int max) {
        return (int)(Math.random() * (max - min + 1)) + min;
    }

    // Rarity from the roll: 1-70 Common, 71-95 Rare, 96-100 Legendary
    static String rarityFor(int roll) {
        if (roll <= 70) {
            return "Common";
        } else if (roll <= 95) {
            return "Rare";
        } else {
            return "Legendary";
        }
    }

    // Gold depends on rarity: Common 5-20, Rare 25-75, Legendary 100-500
    static int goldFor(String rarity) {
        if (rarity.equals("Common")) {
            return randomBetween(5, 20);
        } else if (rarity.equals("Rare")) {
            return randomBetween(25, 75);
        } else {
            return randomBetween(100, 500);
        }
    }

    static boolean goldInRange(String rarity, int gold) {
        if (rarity.equals("Common")) {
            return gold >= 5 && gold <= 20;
        } else if (rarity.equals("Rare")) {
            return gold >= 25 && gold <= 75;
        }
        return gold >= 100 && gold <= 500;
    }

    static void check(String label, boolean passed) {
        System.out.println((passed ? "PASS: " : "FAIL: ") + label);
    }

    // One extra random drop with its range checks
    static void drop(int number) {
        int roll = randomBetween(1, 100);
        String rarity = rarityFor(roll);
        int gold = goldFor(rarity);
        System.out.println("Drop " + number + ": roll " + roll + ", " + rarity + ", gold " + gold);
        check("roll is between 1 and 100", roll >= 1 && roll <= 100);
        check("gold is in the " + rarity + " range", goldInRange(rarity, gold));
    }

    public static void main(String[] args) {
        // The drop the lesson asks for
        int rarityRoll = randomBetween(1, 100);
        String rarity = rarityFor(rarityRoll);
        int gold = goldFor(rarity);

        System.out.println("Loot Drop!");
        System.out.println("Rarity Roll: " + rarityRoll);
        System.out.println("You got: " + rarity + " item");
        System.out.println("Gold Value: " + gold);

        // Boundary tests: these do not depend on luck
        System.out.println("\n--- Boundary tests ---");
        check("roll 1 is Common", rarityFor(1).equals("Common"));
        check("roll 70 is Common", rarityFor(70).equals("Common"));
        check("roll 71 is Rare", rarityFor(71).equals("Rare"));
        check("roll 95 is Rare", rarityFor(95).equals("Rare"));
        check("roll 96 is Legendary", rarityFor(96).equals("Legendary"));
        check("roll 100 is Legendary", rarityFor(100).equals("Legendary"));

        // Tested more than once: five more random drops
        System.out.println("\n--- Five more random drops ---");
        drop(1);
        drop(2);
        drop(3);
        drop(4);
        drop(5);
    }
}
''', output_note='every check passed', random_note=True)

nb.md('**What I learned:** I only wrote the random-range formula once, in `randomBetween`, and used it for the rarity roll and for the gold. The boundary tests check the rarity cutoffs exactly (70 and 71, 95 and 96), and the five extra drops show the random values always stay in range.')

nb.md(submission_notes([
    'Lesson: CSA 1.11 Math Class',
    'MCQ 1.11: <paste your score line, such as 4/5 | answers: B,D,A,C,B>',
    'Popcorn 1: three Math values predicted, plus a distance expression, cell runs and prints',
    'Popcorn 2: random integer from 10-20 generated and tested',
    'Homework: rarity roll printed and in range 1-100 (yes)',
    'Homework: gold value printed and in the correct range for the rarity (yes)',
    'Homework: Math.random() used for both values (yes)',
]))

nb.rubric('''
### Grading Plan (1 Point Total)

| Part | Points | What earns the points | Where I show it |
| :--- | :--- | :--- | :--- |
| Popcorn 1 | 0.1 | Three `Math` predictions and a distance expression, cell runs. | Popcorn Hack #1: prediction table, `PopcornMath` cell |
| Popcorn 2 | 0.1 | Random 10-20 range built correctly and tested more than once. | Popcorn Hack #2: five rolls, PASS check, and I ran it again |
| MCQ | 0.2 | 4 or 5 correct. 0.15 for 3, 0.1 if every question was answered. | Taken on the lesson page; score line goes in the Submission Notes |
| Homework: rarity range | 0.2 | Rarity roll is between 1 and 100 and maps to the correct name. | `randomBetween(1, 100)`, `rarityFor`, and the boundary tests |
| Homework: gold range | 0.2 | Gold value stays within the correct range for the rolled rarity. | `goldFor` and the `goldInRange` checks on every drop |
| Homework: uses `Math.random()` and runs | 0.2 | `Math.random()` is used for both values, and the program runs and prints the required output. | `randomBetween` is the only place values are generated; output block |
| **Total** | **1.0** | | |

### Quick Validation Checklist

- Each cell ends with `ClassName.main(null);` and shows output.
- MCQ score in the notes (paste it into the Submission Notes after taking the MCQ).
- Rarity roll is between 1 and 100.
- Gold value stays within the correct range for that rarity.
- `Math.random()` is used, not hardcoded numbers.
- The program was tested more than once.
''', points=[0.1, 0.1, 0.2, 0.2, 0.2, 0.2])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
allt = '\n'.join(''.join(c['source']) for c in cells)
extra = [
    ('3 code cells (2 popcorn + homework)', len(codes) == 3),
    ('no "?" placeholders left', not any('"?"' in c for c in codes)),
    ('distance uses Math.sqrt and Math.pow', 'Math.sqrt(Math.pow(3 - 0, 2) + Math.pow(4 - 0, 2))' in codes[0]),
    ('random range formula uses (max - min + 1)', '(max - min + 1)' in codes[1] and '(max - min + 1)' in codes[2]),
    ('Math.random() used in homework', 'Math.random()' in codes[2]),
    ('no hardcoded loot values left as 0 / "?"', 'rarityRoll = 0;' not in codes[2] and 'gold = 0;' not in codes[2]),
    ('boundary tests present (70/71, 95/96)', all(f'rarityFor({n})' in codes[2] for n in (1, 70, 71, 95, 96, 100))),
    ('MCQ line is left as a placeholder (not invented)', 'MCQ 1.11: <paste your score line' in allt),
    ('permalink does not collide with the teacher 1_11_hw page', PERMALINK != '/csa/unit_01/1_11_hw'),
]
ok = audit(path, {
    'layout': 'post', 'title': 'CSA Unit 1.11 Math Class HW', 'categories': '[Java, Math-Class]',
    'lesson_language': 'Java', 'lesson_topic': 'Math-Class HW', 'lesson_part': 'interactive',
    'lesson_type': 'lesson', 'permalink': PERMALINK}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
