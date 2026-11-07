"""Build CSA 1.6 Compound Assignment Operators homework (permalink /csa/unit_01/1_6_hw)."""
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit  # noqa: E402

nb = Notebook(1, '6', 'Compound-Assignment-Operators')
nb.front_matter(
    title='CSA Unit 1.6 Compound Assignment Operators HW',
    description='Homework for 1.06 Compound Assignment Operators. Rewrite long-form code with compound operators, then simulate a bank account with at least three operators.',
    permalink='/csa/unit_01/1_6_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [1.06 Compound Assignment Operators]({{ site.baseurl }}/csa/unit_01/1_6). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** a compound assignment operator updates a variable using its own old value. `x += 5` means `x = x + 5`, but it is shorter and the variable name is written once.

| Operator | Long form | What it does |
| --- | --- | --- |
| `x += y` | `x = x + y` | Add `y` to `x` |
| `x -= y` | `x = x - y` | Subtract `y` from `x` |
| `x *= y` | `x = x * y` | Multiply `x` by `y` |
| `x /= y` | `x = x / y` | Divide `x` by `y` (integer division if both are `int`) |
| `x %= y` | `x = x % y` | Keep the remainder of `x / y` |
| `x++` | `x = x + 1` | Add exactly 1 |
| `x--` | `x = x - 1` | Subtract exactly 1 |

**Scope note:** the AP CSA exam uses only the post-form `x++` and `x--` as statements, so this notebook never uses the prefix forms `++x` and `--x`.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Rewrote long-form game-score code with compound operators and checked it gives the same result | 0.2 |
| Homework Hack | Option A, Bank Account Manager: 7 events, 7 different compound operators, a print after every operation | 0.8 |
''')

nb.md('## 2. Hacks & Practice Tasks')
nb.md(safety_rules([
    'Include print statements after EACH compound operation to show the result',
    'Test your code by running it and verifying output',
    'Use meaningful variable names that reflect the scenario',
    'Include comments explaining the purpose of each operation',
    'Only use post-form (x++, x--) for increment/decrement, not prefix',
    'Do not use external libraries',
]))

# ---------------------------------------------------------------- popcorn
nb.md('''
### Popcorn Hack (In-Class)

3-minute challenge: transform verbose code into compound operators.

**Task:** rewrite the lesson's game code (score 1000, health 100, enemies 0) using compound assignment and increment operators.

**Concept:** each long-form line `v = v op value;` becomes `v op= value;`. Adding exactly 1 becomes `v++`. The code must give the same final numbers as the long form.

**My predictions (hand-traced before I ran the code):**

| Step | Long form | Compound form | Hand trace | Value |
| --- | --- | --- | --- | --- |
| 1 | `playerScore = playerScore + 250;` | `playerScore += 250;` | `1000 + 250` | score `1250` |
| 2 | `playerHealth = playerHealth - 15;` | `playerHealth -= 15;` | `100 - 15` | health `85` |
| 3 | `enemiesDefeated = enemiesDefeated + 1;` | `enemiesDefeated++;` | `0 + 1` | enemies `1` |
| 4 | `playerScore = playerScore * 2;` | `playerScore *= 2;` | `1250 * 2` | score `2500` |
| 5 | `playerHealth = playerHealth * 4;` | `playerHealth *= 4;` | `85 * 4` | health `340` |
| 6 | `playerHealth = playerHealth / 5;` | `playerHealth /= 5;` | `340 / 5` | health `68` |

**What the important lines do:** `+=` adds to the variable in place, `++` adds exactly one, and `*=` then `/=` is the two-step "80% effectiveness" healing (multiply by 4, then divide by 5). The second half of the cell runs the long form on separate variables so the program can check that both forms agree.
''')
nb.runner('Popcorn Hack. Rewrite the long-form game code with compound operators and check it matches', r'''
public class PopcornCompound {
    public static void main(String[] args) {
        int playerScore = 1000;
        int playerHealth = 100;
        int enemiesDefeated = 0;

        // += adds the points straight into playerScore (long form: playerScore = playerScore + 250)
        playerScore += 250;
        System.out.println("Step 1, enemy worth 250: score = " + playerScore);

        // -= subtracts the damage (long form: playerHealth = playerHealth - 15)
        playerHealth -= 15;
        System.out.println("Step 2, 15 damage: health = " + playerHealth);

        // ++ adds exactly one, so it is the clearest choice for counting
        enemiesDefeated++;
        System.out.println("Step 3, enemy defeated: enemies = " + enemiesDefeated);

        // *= doubles the score for the boss battle
        playerScore *= 2;
        System.out.println("Step 4, boss battle doubles the score: score = " + playerScore);

        // *= then /= is the "80%" healing potion: multiply by 4, then divide by 5
        playerHealth *= 4;
        System.out.println("Step 5, potion step one (times 4): health = " + playerHealth);
        playerHealth /= 5;
        System.out.println("Step 6, potion step two (divide by 5): health = " + playerHealth);

        // Same steps in the long form, on separate variables, to check the answers match
        int longScore = 1000;
        int longHealth = 100;
        int longEnemies = 0;
        longScore = longScore + 250;
        longHealth = longHealth - 15;
        longEnemies = longEnemies + 1;
        longScore = longScore * 2;
        longHealth = longHealth * 4;
        longHealth = longHealth / 5;

        System.out.println("Final: Score " + playerScore + ", Health " + playerHealth + ", Enemies " + enemiesDefeated);
        System.out.println("Same as the long form? "
                + (playerScore == longScore && playerHealth == longHealth && enemiesDefeated == longEnemies));
    }
}
''')
nb.md('**What I learned:** every compound operator is just the long form with the variable written once. `/=` on `int` values drops the remainder, so `340 / 5` is exact here but would truncate for other numbers.')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

**Task:** create a simulation program for ONE scenario. The program must use at least three different compound assignment operators and show each state change with a print statement after every operation.

I chose **Option A: Bank Account Manager** and wrote my own events and numbers.

**Requirements (from the lesson), and how my program meets them:**

| Requirement | How I meet it |
| --- | --- |
| At least 3 different compound operators | Seven: `+=`, `-=`, `*=`, `/=`, `%=`, `++`, `--` |
| At least 5 state-changing events | Seven events (paycheck, rent, interest, transfer, promo, dinner, statement day) |
| Print the value after each operation | A `println` follows every compound operation |
| Comments explaining each operator choice | Every operation has a comment saying why that operator fits |
| Test and verify output | Hand-traced values below, then PASS/FAIL checks at the end |

**Concept:** I used whole dollars (`int`) so every result prints exactly. The 2% interest is `balance += balance / 50`, which uses integer division, so it drops cents. That is a real property of `/` on `int` values, and it is why the interest is `13` and not `13.0`.

**My hand-traced expected values (written before I ran the code):**

| Event | Operation | Hand trace | Expected |
| --- | --- | --- | --- |
| 1 | `balance += 800;` `transactions++;` | `500 + 800` | balance `1300`, transactions `1` |
| 2 | `balance -= 650;` `transactions++;` | `1300 - 650` | balance `650`, transactions `2` |
| 3 | `balance += balance / 50;` | `650 / 50 = 13`, so `650 + 13` | balance `663` |
| 4 | `freeTransfersLeft--;` `balance -= 40;` `transactions++;` | `3 - 1`, `663 - 40` | transfers `2`, balance `623`, transactions `3` |
| 5 | `rewardPoints *= 3;` | `10 * 3` | points `30` |
| 6 | `share /= 4;` `balance -= share;` `transactions++;` | `120 / 4 = 30`, `623 - 30` | share `30`, balance `593`, transactions `4` |
| 7 | `daysSinceStatement += 5;` `daysSinceStatement %= 30;` | `28 + 5 = 33`, `33 % 30` | days `3` (wraps) |
''')
nb.runner('Homework Hack. Bank Account Manager: at least three compound operators, a print after each operation', r'''
public class BankAccountManager {
    static void check(String label, boolean passed) {
        System.out.println((passed ? "PASS: " : "FAIL: ") + label);
    }

    public static void main(String[] args) {
        // Whole dollars keep every result exact
        int balance = 500;
        int transactions = 0;
        int freeTransfersLeft = 3;
        int rewardPoints = 10;
        int daysSinceStatement = 28;

        System.out.println("=== BANK ACCOUNT MANAGER ===");
        System.out.println("Start: balance = $" + balance);

        // Event 1: += adds the paycheck to the balance, ++ counts exactly one transaction
        System.out.println("\nEvent 1: paycheck deposited");
        balance += 800;
        System.out.println("balance = $" + balance);
        transactions++;
        System.out.println("transactions = " + transactions);

        // Event 2: -= takes the rent out, ++ counts the transaction
        System.out.println("\nEvent 2: rent paid");
        balance -= 650;
        System.out.println("balance = $" + balance);
        transactions++;
        System.out.println("transactions = " + transactions);

        // Event 3: += adds interest; balance / 50 is 2% with integer division, so cents are dropped
        System.out.println("\nEvent 3: 2% interest applied");
        balance += balance / 50;
        System.out.println("balance = $" + balance);

        // Event 4: -- uses up one free transfer, -= sends the money, ++ counts the transaction
        System.out.println("\nEvent 4: $40 sent to a friend");
        freeTransfersLeft--;
        System.out.println("freeTransfersLeft = " + freeTransfersLeft);
        balance -= 40;
        System.out.println("balance = $" + balance);
        transactions++;
        System.out.println("transactions = " + transactions);

        // Event 5: *= triples the reward points for a promotion
        System.out.println("\nEvent 5: triple-points promotion");
        rewardPoints *= 3;
        System.out.println("rewardPoints = " + rewardPoints);

        // Event 6: /= splits a $120 dinner bill four ways, -= takes our share, ++ counts it
        System.out.println("\nEvent 6: dinner bill split four ways");
        int share = 120;
        share /= 4;
        System.out.println("share = $" + share);
        balance -= share;
        System.out.println("balance = $" + balance);
        transactions++;
        System.out.println("transactions = " + transactions);

        // Event 7: += moves the calendar forward, %= wraps the counter back into a 30-day cycle
        System.out.println("\nEvent 7: five days pass");
        daysSinceStatement += 5;
        System.out.println("daysSinceStatement before wrap = " + daysSinceStatement);
        daysSinceStatement %= 30;
        System.out.println("daysSinceStatement after wrap = " + daysSinceStatement);

        System.out.println("\n=== FINAL SUMMARY ===");
        System.out.println("Balance: $" + balance);
        System.out.println("Transactions: " + transactions);
        System.out.println("Free transfers left: " + freeTransfersLeft);
        System.out.println("Reward points: " + rewardPoints);
        System.out.println("Days since statement: " + daysSinceStatement);

        System.out.println("\n=== CHECKS (compared with my hand trace) ===");
        check("balance is 593", balance == 593);
        check("transactions is 4", transactions == 4);
        check("freeTransfersLeft is 2", freeTransfersLeft == 2);
        check("rewardPoints is 30", rewardPoints == 30);
        check("daysSinceStatement wrapped to 3", daysSinceStatement == 3);
    }
}
''', output_note='every check passed and every value matched my hand trace')

nb.md('''
**Why I chose each operator:** `+=` and `-=` are for money coming in and going out, `*=` for a multiplier (triple points), `/=` for splitting evenly, `%=` for a counter that must stay inside a range, and `++` / `--` only when exactly one is added or removed. I used only the post-form `x++` and `x--`.
''')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I transformed all the long-form expressions into compound operators. The code runs without errors and the output matches the hand-traced values (score 2500, health 68, enemies 1).

- **0.8 points: Homework completion**
  - **0.25 Operator variety:** The Bank Account Manager uses seven different compound operators (`+=`, `-=`, `*=`, `/=`, `%=`, `++`, `--`), each chosen for its context (see "Why I chose each operator").
  - **0.25 State tracking:** Five variables (`balance`, `transactions`, `freeTransfersLeft`, `rewardPoints`, `daysSinceStatement`) change meaningfully across seven events.
  - **0.2 Output and documentation:** A print statement shows the value after every operation, and a comment explains why each operator was chosen.
  - **0.1 Correctness:** Every operator gives the correct result; the PASS checks match my hand trace, and the program runs without errors.

#### Quick Validation Checklist

- Present: All code executed with output visible
- Present: At least 3 different compound operators used (seven)
- Present: At least 5 print statements showing state changes (every operation has one)
- Present: Comments explaining operator choices
- Absent: Prefix increment/decrement operators (`++x`, `--x`)
- Test: All operators produce mathematically correct results (five PASS checks)
- Test: Variables change in expected ways through the scenario
- Verify: Output shows a clear progression of state changes (Event 1 to Event 7)
''', points=[0.2, 0.25, 0.25, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

# ---------------------------------------------------------------- audit
import json  # noqa: E402
cells = json.load(open(path))['cells']
code_src = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
hw = code_src[1]
ops = set(re.findall(r'\+=|-=|\*=|/=|%=|\+\+|--', re.sub(r'//.*', '', hw)))
events = len(re.findall(r'Event \d:', hw)) // 1
extra = [
    ('homework uses at least 3 different compound operators', len(ops) >= 3),
    ('homework has at least 5 events', len(set(re.findall(r'Event (\d):', hw))) >= 5),
    ('no prefix ++x / --x anywhere', not any(re.search(r'(\+\+|--)[A-Za-z_]', re.sub(r'//.*', '', s)) for s in code_src)),
    ('no import statements (no external libraries)', not any('import ' in s for s in code_src)),
]
ok = audit(path, {
    'layout': 'post', 'title': 'CSA Unit 1.6 Compound Assignment Operators HW',
    'categories': '[Java, Compound-Assignment-Operators]', 'lesson_language': 'Java',
    'lesson_topic': 'Compound-Assignment-Operators HW', 'lesson_part': 'interactive', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_01/1_6_hw'}, expect_runners=2, extra=extra)
sys.exit(0 if ok else 1)
