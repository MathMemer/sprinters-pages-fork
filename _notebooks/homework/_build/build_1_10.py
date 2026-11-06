"""Build CSA 1.10 Calling Class Methods homework (permalink /csa/unit_01/1_10_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, submission_notes, audit, java_compile_error  # noqa: E402

nb = Notebook(1, '10', 'Class-Methods')
nb.front_matter(
    title='CSA Unit 1.10 Calling Class Methods HW',
    description='Homework for 1.10 Calling Class Methods. Predict which calls work, then fix a program that calls an instance method on a class name.',
    permalink='/csa/unit_01/1_10_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [1.10 Calling Class Methods]({{ site.baseurl }}/csa/unit_01/1_10). Every code cell below is a Java code runner. Press **Run** to execute it.

**Key idea:** a method marked `static` belongs to the class, so it is called on the class name. A method without `static` belongs to each object, so it needs an object first.

| Kind of method | How to call it | Example |
| --- | --- | --- |
| Class method (`static`) | `ClassName.method()` | `Robot.beep();` |
| Instance method (no `static`) | `objectName.method()` | `r.introduce();` |
| Static method through an object | Legal, but misleading | `r.beep();` works, but `Robot.beep();` is clearer |
| Instance method on a class name | Compile error | `Robot.introduce();` |

A `static` method has no particular object, so it cannot directly use an instance variable such as `name`.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Predicted WORKS or ERROR for four calls, ran them, and read the compiler message | 0.2 |
| MCQ | Taken on the lesson page; the score line goes in the Submission Notes | 0.2 |
| Homework Hack | Fixed the `Game` calls and explained the original error | 0.6 |
''')

nb.md('## 2. Hacks & Practice Tasks')
nb.md(safety_rules([
    'One class per cell, ending with `ClassName.main(null);`.',
    'Run each cell and leave the output showing.',
    'Write your own answers, not the sample code from the lesson.',
    'Include your MCQ score.',
    'Use `##` headings or smaller.',
]))

# ---------------------------------------------------------------- popcorn
ROBOT = r'''
public class Robot {
    String name;

    public Robot(String name) {
        this.name = name;
    }

    public void introduce() {
        System.out.println("I am " + name);
    }

    public static void beep() {
        System.out.println("Beep!");
    }

    // My predictions, written BEFORE I ran the code (Robot r = new Robot("R2"))
    static String call1 = "WORKS";  // Robot.beep();       class method on the class name
    static String call2 = "WORKS";  // r.beep();           static through an object: legal but misleading
    static String call3 = "ERROR";  // Robot.introduce();  instance method needs an object
    static String call4 = "WORKS";  // r.introduce();      instance method on an object

    public static void main(String[] args) {
        Robot r = new Robot("R2");
        System.out.println("Predictions: " + call1 + ", " + call2 + ", " + call3 + ", " + call4);

        Robot.beep();
        r.beep();
        // Robot.introduce();   // uncomment to see the compiler error
        r.introduce();
    }
}
'''
nb.md('''
### Popcorn Hack (In-Class)

2-minute challenge: decide whether each call works.

**Concept:** `static` methods are called on the class; instance methods need an object. Java also lets a `static` method be called through an object, but that hides the fact that no object is involved.

**My predictions (written before I ran the code):**

| Call | My prediction | Why |
| --- | --- | --- |
| `Robot.beep();` | WORKS | `beep()` is `static`, so the class name is the right way to call it |
| `r.beep();` | WORKS | Java allows a static call through an object, even though it is misleading |
| `Robot.introduce();` | ERROR | `introduce()` is an instance method; it uses `name`, and a class name is not an object |
| `r.introduce();` | WORKS | `r` is a `Robot` object, so the instance method has the object it needs |

**Which form is clearer for the call that works two ways?** `Robot.beep();`. It tells the reader that `beep()` is a class method and no particular robot is involved.
''')
nb.runner('Popcorn Hack. My WORKS / ERROR predictions are filled in, so run it and compare', ROBOT)

bad = ROBOT.replace('// Robot.introduce();   // uncomment to see the compiler error',
                    'Robot.introduce();   // uncommented to see the compiler error')
err = java_compile_error(bad)
nb.md(f'''
**Compiler message when I uncommented `Robot.introduce();`** (from `javac` 21):

```
{err}
```

**What I learned:** all four predictions matched. The compiler stops `Robot.introduce();` because `introduce()` reads `name`, which belongs to one robot, and a class name does not stand for any one robot.
''')

# ---------------------------------------------------------------- homework
GAME = r'''
public class Game {
    String player;

    public Game(String player) {
        this.player = player;
    }

    public void showPlayer() {
        System.out.println("Player: " + player);
    }

    public static void rules() {
        System.out.println("Each player gets one turn.");
    }

    public static void main(String[] args) {
        // ORIGINAL (does not compile):
        // Game.rules();
        // Game.showPlayer();

        // Corrected calls
        Game.rules();                    // class method: called on the class name
        Game match = new Game("Mia");    // instance method needs an object, so create one first
        match.showPlayer();              // called on the object

        // My explanation of the original error: showPlayer() is an instance method that prints this
        // object's player, so it needs a Game object. Game.showPlayer() used the class name, which is
        // not an object, so the call was invalid. rules() is static, so Game.rules() was already fine.
    }
}
'''
nb.md('''
### Homework Hack

**Task:** the original program does not compile. Write the corrected calls in `main`, make the program compile and run, and explain the original error in one or two sentences.

**Original code in `main`:**

```java
Game.rules();
Game.showPlayer();
```

**Concept:** `rules()` is `static`, so `Game.rules();` is correct. `showPlayer()` is an instance method, so `Game.showPlayer();` is the line that breaks.

**My predictions (written before I ran the code):**

| Line | My prediction | Why |
| --- | --- | --- |
| `Game.rules();` | Works, prints `Each player gets one turn.` | `rules()` is a class method |
| `Game.showPlayer();` | Compile error | `showPlayer()` is an instance method and `Game` is not an object |
| `Game match = new Game("Mia"); match.showPlayer();` | Works, prints `Player: Mia` | The object supplies `player` |

**What the important lines do:** `new Game("Mia")` runs the constructor and stores `"Mia"` in that object's `player`. `match.showPlayer()` then prints that object's `player`.
''')
nb.runner('Homework Hack. Corrected calls and my explanation of the original error', GAME,
          output_note='all three predictions matched')

orig = GAME.replace('        // Game.showPlayer();', '        Game.showPlayer();')
nb.md(f'''
**Compiler message for the original `Game.showPlayer();`** (from `javac` 21):

```
{java_compile_error(orig)}
```

**Explanation of the original error:** `showPlayer()` is an instance method, so it needs a `Game` object. Calling it on the class name `Game` gave it no object, so the compiler rejected it. `Game.rules()` was already fine because `rules()` is `static`.
''')

nb.md(submission_notes([
    'Lesson: CSA 1.10 Calling Class Methods',
    'MCQ 1.10: <paste your score line, such as 4/5 | answers: B,C,A,D,C>',
    'Popcorn: four call predictions made, cell runs and prints',
    'Homework: rules() called as a class method (yes)',
    'Homework: Game object created and showPlayer() called on it (yes)',
    'Homework: program compiles and runs (yes)',
    'Homework: explanation of the original error = showPlayer() is an instance method that needs a Game object, '
    'so calling it on the class name Game was invalid.',
]))

nb.rubric('''
### Grading Plan (1 Point Total)

| Part | Points | What earns the points | Where I show it |
| :--- | :--- | :--- | :--- |
| Popcorn | 0.2 | Four WORKS/ERROR predictions made and the cell runs. | Popcorn Hack: prediction table, `Robot` runner, output |
| MCQ | 0.2 | 4 or 5 correct. 0.15 for 3, 0.1 if every question was answered. | Taken on the lesson page; score line goes in the Submission Notes |
| Homework: class method call | 0.1 | `rules()` is called as a class method. | `Game.rules();` in the `Game` runner |
| Homework: object call | 0.2 | A `Game` object is created and `showPlayer()` is called on it. | `Game match = new Game("Mia"); match.showPlayer();` |
| Homework: compiles and runs | 0.15 | The corrected program compiles and prints output. | Output block under the `Game` runner |
| Homework: explanation | 0.15 | Explanation says `showPlayer()` is an instance method that needs an object, so the class-name call was invalid. | "Explanation of the original error" |
| **Total** | **1.0** | | |

### Quick Validation Checklist

- Each cell ends with `ClassName.main(null);` and shows output.
- MCQ score in the notes (paste it into the Submission Notes after taking the MCQ).
- `rules()` is called as a static method.
- `showPlayer()` is called on a `Game` object.
- The program compiles and runs.
- One- or two-sentence explanation of why `Game.showPlayer()` was invalid.
''', points=[0.2, 0.2, 0.1, 0.2, 0.15, 0.15])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
allt = '\n'.join(''.join(c['source']) for c in cells)
extra = [
    ('no "?" placeholders left in the Popcorn predictions', 'static String call1 = "?"' not in codes[0] and '"?"' not in codes[0]),
    ('Popcorn predictions are all WORKS or ERROR', len(re.findall(r'call\d = "(WORKS|ERROR)"', codes[0])) == 4),
    ('rules() called as a class method (uncommented)', re.search(r'^\s+Game\.rules\(\);', codes[1], re.M) is not None),
    ('showPlayer() called on a Game object', re.search(r'new Game\("\w+"\)', codes[1]) and re.search(r'^\s+match\.showPlayer\(\);', codes[1], re.M)),
    ('original bad call is only in a comment', not re.search(r'^\s+Game\.showPlayer\(\);', codes[1], re.M)),
    ('explanation present', 'My explanation of the original error:' in codes[1] and 'instance method' in codes[1]),
    ('MCQ line is left as a placeholder (not invented)', 'MCQ 1.10: <paste your score line' in allt),
    ('compiler errors captured from javac', allt.count('cannot be referenced from a static context') >= 2),
]
ok = audit(path, {
    'layout': 'post', 'title': 'CSA Unit 1.10 Calling Class Methods HW', 'categories': '[Java, Class-Methods]',
    'lesson_language': 'Java', 'lesson_topic': 'Class-Methods HW', 'lesson_part': 'interactive',
    'lesson_type': 'lesson', 'permalink': '/csa/unit_01/1_10_hw'}, expect_runners=2, extra=extra)
sys.exit(0 if ok else 1)
