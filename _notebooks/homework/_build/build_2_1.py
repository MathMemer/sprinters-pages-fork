"""Build CSA 2.1 Algorithms with Selection and Repetition homework (permalink /csa/unit_02/2_1_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, outputs_of  # noqa: E402

TOPIC = 'Algorithms-with-Selection-and-Repetition'
nb = Notebook(2, '1', TOPIC)
nb.front_matter(
    title='CSA Unit 2.01 Algorithms with Selection and Repetition HW',
    description='Homework for 2.01 Algorithms with Selection and Repetition. Trace a vending machine loop, write an everyday algorithm in pseudocode, and turn it into Java.',
    permalink='/csa/unit_02/2_1_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.01 Algorithms with Selection and Repetition]({{ site.baseurl }}/csa/unit_02/2_1). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** every algorithm in this unit is built from three blocks.

| Block | Meaning | Pseudocode | Java |
| --- | --- | --- | --- |
| Sequence | Steps run in order, one after another | numbered steps | statements top to bottom |
| Selection | The algorithm makes a choice | `IF condition` | `if` / `else` |
| Repetition | Steps repeat while a condition holds | `REPEAT UNTIL condition` or `WHILE condition` | `while` loop |

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Predicted the coins and change for the vending machine, then tested other prices and coins | 0.2 |
| Homework Part 1 | Wrote an everyday algorithm (cooking pasta) with 6 steps, one selection and one repetition, in pseudocode | 0.4 |
| Homework Part 2 | Turned it into Java with a `while` loop and an `if`, printing a line for each step | 0.3 |
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

With `price = 130` and `coin = 10`, how many "Inserted" lines will print, and how much change is given?

**Concept:** the `while` loop is the repetition: it keeps inserting a coin while `total < price`. The `if` after it is the selection: change is given only when `total > price`.

**My predictions (written before I ran the code):**

| `price` | `coin` | Hand trace | "Inserted" lines | Change |
| --- | --- | --- | --- | --- |
| `130` | `10` | totals go `10, 20, ... 130`, and `130 < 130` is false, so the loop stops | `13` | none: `130 > 130` is false, so "Exact amount. No change." |
| `130` | `20` | `20, 40, 60, 80, 100, 120, 140`, stops once `140 >= 130` | `7` | `140 - 130 = 10` cents |
| `100` | `30` | `30, 60, 90, 120`, stops once `120 >= 100` | `4` | `120 - 100 = 20` cents |

**What the important lines do:** `total = total + coin;` adds one coin, `inserted++;` counts it, and `while (total < price)` decides whether to insert another. I moved the loop into a method `insertCoins(price, coin)` so one run can test three different values; the first call uses the lesson's values.
''')
nb.runner('Popcorn Hack. Predict the number of coins and the change before pressing Run', r'''
public class PopcornMachine {
    // Runs the vending machine algorithm for one price and one coin size
    static void insertCoins(int price, int coin) {
        int total = 0;
        int inserted = 0;
        System.out.println("--- price " + price + ", coin " + coin + " ---");

        while (total < price) {              // repetition: keep inserting while the total is too low
            total = total + coin;
            inserted++;
            System.out.println("Inserted " + coin + " cents. Total: " + total);
        }
        System.out.println("Coins inserted: " + inserted);

        if (total > price) {                 // selection: change only if we overpaid
            System.out.println("Change: " + (total - price) + " cents");
        } else {
            System.out.println("Exact amount. No change.");
        }
    }

    public static void main(String[] args) {
        insertCoins(130, 10);   // the lesson's values
        insertCoins(130, 20);   // test: a bigger coin means fewer lines and some change
        insertCoins(100, 30);   // test: the coins overshoot the price
    }
}
''', output_note='all three predictions matched')
nb.md('**What I learned:** changing `coin` changes how many times the loop runs, and the `if` only gives change when the coins overshoot. Both blocks are driven by the same variable, `total`.')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

Two parts: write an everyday algorithm, then turn it into Java.

#### Part 1: My algorithm in pseudocode

**Concept:** an algorithm is ordered steps. This one has one **repetition** (step 3: wait for the water to boil) and one **selection** (step 5: drain the pasta only if it is soft). I used the pseudocode style from the lesson table (`REPEAT UNTIL`, `IF`, indented bodies).

```
Algorithm: Cook a pot of pasta
1. Fill the pot with water
2. Turn the stove on high
3. REPEAT UNTIL the water temperature >= 100
     wait one minute and check the temperature
4. Add the pasta to the pot
5. IF the pasta is soft
     drain the pasta
   ELSE
     cook two more minutes
6. Serve the pasta
```

| Step | Building block |
| --- | --- |
| 1, 2, 4, 6 | Sequence |
| 3 | Repetition (loops until the water is hot enough) |
| 5 | Selection (two ways: drain, or cook longer) |

#### Part 2: The same algorithm in Java

**Concept:** the `REPEAT UNTIL temperature >= 100` in step 3 becomes `while (waterTemp < 100)` (a `while` loop keeps going while its condition is true, so the condition flips). The `IF` in step 5 becomes `if` / `else`. Every step prints a line, so the output tells the story.

**My predictions and expected values (written before I ran the code):**

| Run | Start values | Hand trace | Expected |
| --- | --- | --- | --- |
| 1 | `waterTemp = 20`, `pastaMinutes = 10` | `20 -> 40 -> 60 -> 80 -> 100`, so 4 loop passes; `10 >= 10` is true | 4 "Minute" lines, then step 5 prints "drain it" |
| 2 | `waterTemp = 60`, `pastaMinutes = 6` | `60 -> 80 -> 100`, so 2 loop passes; `6 >= 10` is false | 2 "Minute" lines, then step 5 prints "cook two more minutes" |

**What the important lines do:** `waterTemp = waterTemp + 20;` heats the water by 20 degrees each minute, `minutes++;` counts the minutes, and the loop test `waterTemp < 100` stops it when the water is hot enough. Running the cook twice with different start values tests both branches of the `if`.
''')
nb.runner('Homework Hack. My algorithm in Java with one while loop and one if statement', r'''
public class PastaAlgorithm {
    // The whole algorithm, for a given starting water temperature and pasta cooking time
    static void cook(int startTemp, int pastaMinutes) {
        int waterTemp = startTemp;
        int minutes = 0;

        System.out.println("1. Fill the pot with water");
        System.out.println("2. Turn the stove on high");

        // Step 3: repetition. REPEAT UNTIL waterTemp >= 100 is the same as WHILE waterTemp < 100
        System.out.println("3. Wait until the water boils");
        while (waterTemp < 100) {
            waterTemp = waterTemp + 20;
            minutes++;
            System.out.println("   Minute " + minutes + ": water is " + waterTemp + " degrees");
        }

        System.out.println("4. Add the pasta to the pot");

        // Step 5: selection. Drain only if the pasta is soft
        if (pastaMinutes >= 10) {
            System.out.println("5. The pasta is soft: drain it");
        } else {
            System.out.println("5. The pasta is still firm: cook two more minutes");
        }

        System.out.println("6. Serve the pasta");
    }

    public static void main(String[] args) {
        System.out.println("=== Run 1: start at 20 degrees, pasta cooked 10 minutes ===");
        cook(20, 10);
        System.out.println("\n=== Run 2: start at 60 degrees, pasta cooked 6 minutes ===");
        cook(60, 6);
    }
}
''', output_note='both runs matched my hand trace and both branches of the if ran')
nb.md('**Does the Java match the written steps?** Yes. Steps 1, 2, 4 and 6 are sequence lines, step 3 is the `while` loop (4 passes in run 1, 2 in run 2), and step 5 is the `if` / `else` (drain in run 1, cook longer in run 2). Changing the start values changes the number of "Minute" lines and which step 5 message prints.')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I predicted the number of `Inserted` lines (13) and the change (none) before running, then verified them against the output, and also tested two other price and coin pairs.

- **0.8 points: Homework completion**
  - **0.4 Part 1 algorithm:** A written algorithm of six steps with one selection (step 5) and one repetition (step 3), in the pseudocode style used in the lesson table.
  - **0.3 Part 2 Java:** The same algorithm in the code cell with a `while` loop for the repetition and an `if` for the selection, printing a line per step.
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: prediction written before the Popcorn runner was executed
- Present: six or more numbered steps with one selection and one repetition (six steps: repetition in step 3, selection in step 5)
- Present: Java version whose printed output matches the written steps (steps 1 to 6 print in order)
- Test: changing `price` or `coin` changes the number of `Inserted` lines (13, 7 and 4 lines for the three tests)
''', points=[0.2, 0.4, 0.3, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
allt = '\n'.join(''.join(c['source']) for c in cells)
alg = re.search(r'Algorithm: Cook a pot of pasta\n(.*?)\n```', allt, re.S).group(1)
numbered = re.findall(r'^\d+\. ', alg, re.M)
out_pop = outputs_of(path)[0]
extra = [
    ('Popcorn has a while loop and an if', 'while (total < price)' in codes[0] and 'if (total > price)' in codes[0]),
    ('Popcorn output: 13 + 7 + 4 Inserted lines', out_pop.count('Inserted') == 24),
    ('Part 1 has at least 6 numbered steps', len(numbered) >= 6),
    ('Part 1 has a repetition (REPEAT UNTIL) and a selection (IF)', 'REPEAT UNTIL' in alg and 'IF ' in alg),
    ('Part 2 uses exactly one while loop and one if', len(re.findall(r'\bwhile \(', codes[1])) == 1 and len(re.findall(r'\bif \(', codes[1])) == 1),
    ('Part 2 prints a line for each of the 6 steps', all(f'"{n}. ' in codes[1] for n in range(1, 7))),
    ('Part 1 steps match Part 2 prints (6 numbered steps in both)', len(numbered) == 6),
    ('algorithm is my own (not the lesson laps example)', 'lapsDone' not in codes[1]),
]
ok = audit(path, {
    'layout': 'post', 'title': 'CSA Unit 2.01 Algorithms with Selection and Repetition HW',
    'categories': f'[Java, {TOPIC}]', 'lesson_language': 'Java', 'lesson_topic': f'{TOPIC} HW',
    'lesson_source': 'APCSA', 'lesson_type': 'lesson', 'permalink': '/csa/unit_02/2_1_hw'}, expect_runners=2, extra=extra)
sys.exit(0 if ok else 1)
