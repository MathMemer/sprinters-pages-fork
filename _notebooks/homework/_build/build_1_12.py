"""Build CSA 1.12 Classes & Objects homework (permalink /csa/unit_01/1_12_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, submission_notes, audit  # noqa: E402

nb = Notebook(1, '12', 'Classes-and-Objects')
nb.front_matter(
    title='CSA Unit 1.12 Classes and Objects HW',
    description='Homework for 1.12 Classes and Objects. Finish a Book class, then show aliasing, separate objects, and an Object method with an Author class.',
    permalink='/csa/unit_01/1_12_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [1.12 Classes & Objects]({{ site.baseurl }}/csa/unit_01/1_12). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** a class is a blueprint (fields and methods). An object is one instance of that class, made with `new`. A variable holds a **reference** to an object, not the object itself.

| Idea | Example | What happens |
| --- | --- | --- |
| Make an object | `Author a1 = new Author();` | A new `Author` is created and `a1` refers to it |
| Alias | `Author a2 = a1;` | Copies the reference, so `a1` and `a2` are two names for one object |
| Separate objects | `Author b1 = new Author(); Author b2 = new Author();` | Two different objects, even if their fields match |
| `==` on objects | `b1 == b2` | Compares references, so it is `false` for two different objects |
| Inherited from `Object` | `a1.getClass()` | Every class gets methods like `toString()`, `equals()`, `hashCode()`, `getClass()` |

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Finished `Book` with `printInfo()`, made one `Book`, set its fields, and called it | 0.2 |
| MCQ | Taken on the lesson page; the score line goes in the Submission Notes | 0.2 |
| Homework Hack | Predicted aliasing, then showed an aliased pair, a separate pair, and one `Object` method | 0.6 |
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
nb.md('''
### Popcorn Hack (In-Class)

2-minute challenge:

1. Finish `Book` by adding `printInfo()`.
2. Create one `Book` object, set its fields, and call `printInfo()`.

**Concept:** `Book` describes the data (`title`, `pages`) and behavior (`printInfo()`). `new Book()` makes one object, and `book.title = ...` sets a field on that object.

**My prediction (written before I ran the code):** one line, `Title: The Hobbit, Pages: 310`. The class has no constructor, so the fields start empty (`null` and `0`) until `main` sets them.

**What the important lines do:** `void printInfo()` reads this object's own `title` and `pages`. `Book book = new Book();` creates the object. The two assignment lines fill in its fields before `printInfo()` runs.

**Note on "one class per cell":** this task needs two classes (`Book` and the class with `main`), as the lesson's starter does. There is still exactly one `public` class, and it is the one named in the cell's last line.
''')
nb.runner('Popcorn Hack. Finished printInfo(), one Book created, fields set, and called', r'''
class Book {
    String title;
    int pages;

    // Prints this book's title and page count
    void printInfo() {
        System.out.println("Title: " + title + ", Pages: " + pages);
    }
}

public class MainPopcorn {
    public static void main(String[] args) {
        Book book = new Book();
        book.title = "The Hobbit";
        book.pages = 310;
        book.printInfo();
    }
}
''', output_note='matched my prediction')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

**Task:** finish the `Author` class and `main`. Predict the aliasing results before running, show an aliased pair and a separate pair, and call one method inherited from `Object`.

**Concept:** `Author a2 = a1;` does not copy the object, it copies the reference. A change made through `a2` is visible through `a1`. Two separate `new Author()` calls make two objects, so `==` is `false` even when both names are `"Grace"`.

**My predictions (written before I ran the code):**

| Question | My prediction | Why |
| --- | --- | --- |
| Aliased pair: set `a2.name = "Ada"`, then print `a1` and `a2` | `Ada and Ada` | `a1` and `a2` refer to the same object, so both see the new name |
| `a1 == a2` | `true` | Same reference |
| Separate pair: both named `"Grace"`, print `b1 == b2` | `false` | `==` compares references, and these are two different objects |
| `a1.getClass()` | `class Author` | `getClass()` is inherited from `Object` and reports the object's class |

**What the important lines do:** `Author a2 = a1;` makes the alias. `a2.name = "Ada";` changes the one shared object. `b1` and `b2` each come from their own `new Author()`. `a1.getClass()` is a method `Author` never wrote; it comes from `Object`.
''')
nb.runner('Homework Hack. Predictions first, then an aliased pair, a separate pair, and one Object method', r'''
class Author {
    String name;

    // Prints this author's name
    void printName() {
        System.out.println("Author: " + name);
    }
}

public class HomeworkClassesObjects {
    // My predictions, written BEFORE I ran the code
    static String predictAliased = "Ada and Ada";  // a1 and a2 are two names for one object
    static String predictSeparate = "false";       // b1 == b2 compares references; these are two objects

    public static void main(String[] args) {
        System.out.println("Predictions: aliased=" + predictAliased + ", separate=" + predictSeparate);

        // Aliased pair: a2 = a1 copies the reference, so both point at the same object
        Author a1 = new Author();
        Author a2 = a1;
        a2.name = "Ada";            // set the name through a2
        a1.printName();             // a1 sees it too
        a2.printName();
        String aliasedResult = a1.name + " and " + a2.name;
        System.out.println("a1 == a2: " + (a1 == a2));
        System.out.println("Aliased matched my prediction: " + aliasedResult.equals(predictAliased));

        // Separate pair: two new objects with the same name
        Author b1 = new Author();
        Author b2 = new Author();
        b1.name = "Grace";
        b2.name = "Grace";
        String separateResult = String.valueOf(b1 == b2);
        System.out.println("b1 == b2: " + separateResult);
        System.out.println("Separate matched my prediction: " + separateResult.equals(predictSeparate));

        // A method inherited from Object: Author never defined getClass()
        System.out.println("getClass() on an Author: " + a1.getClass());
    }
}
''', output_note='both predictions matched')

nb.md('**What I learned:** the same name can mean the same object (aliasing) or just an equal value on two different objects. `==` answers the first question, not the second. `getClass()` works on `Author` even though I never wrote it, because every class inherits from `Object`.')

nb.md(submission_notes([
    'Lesson: CSA 1.12 Classes & Objects',
    'MCQ 1.12: <paste your score line, such as 4/5 | answers: B,C,A,D,A>',
    'Popcorn: Book class finished, one Book object created and printInfo() called',
    'Homework: two Author objects created, aliasing predicted before running (yes)',
    'Homework: one Object-inherited method named and demonstrated = getClass()',
]))

nb.rubric('''
### Grading Plan (1 Point Total)

| Part | Points | What earns the points | Where I show it |
| :--- | :--- | :--- | :--- |
| Popcorn | 0.2 | `Book` finished, one object created, `printInfo()` called, and the cell runs. | Popcorn Hack: `Book` cell and its output |
| MCQ | 0.2 | 4 or 5 correct. 0.15 for 3, 0.1 if every question was answered. | Taken on the lesson page; score line goes in the Submission Notes |
| Homework: class/object usage | 0.2 | `Author` class and objects created correctly with `new`. | `Author` class, `new Author()` four times in the homework cell |
| Homework: aliasing prediction | 0.25 | Prediction written before running, and the aliased pair's shared value is correctly demonstrated. | Prediction table and `predictAliased`; `a1`/`a2` both print `Ada` |
| Homework: separate objects | 0.1 | Separate pair correctly shown as two different objects (`==` is `false`). | `b1 == b2` prints `false` |
| Homework: `Object` method | 0.05 | One method inherited from `Object` is called and its result printed. | `a1.getClass()` prints `class Author` |
| **Total** | **1.0** | | |

### Quick Validation Checklist

- Each cell ends with `ClassName.main(null);` and shows output.
- MCQ score in the notes (paste it into the Submission Notes after taking the MCQ).
- `Book` popcorn hack has one object with fields set and `printInfo()` called.
- Homework has both an aliased pair and a separate pair of `Author` objects.
- Predictions were written before running, not after.
- One `Object`-inherited method is named and demonstrated.
''', points=[0.2, 0.2, 0.2, 0.25, 0.1, 0.05])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
allt = '\n'.join(''.join(c['source']) for c in cells)
extra = [
    ('no "?" placeholders left', not any('"?"' in c for c in codes)),
    ('Book has printInfo() and one Book is created with fields set',
     'void printInfo()' in codes[0] and 'new Book()' in codes[0] and 'book.title =' in codes[0] and 'book.pages =' in codes[0]
     and 'book.printInfo();' in codes[0]),
    ('aliased pair (a2 = a1) present', 'Author a2 = a1;' in codes[1]),
    ('separate pair (two new Author()) present', len(re.findall(r'Author b\d = new Author\(\);', codes[1])) == 2),
    ('predictions declared before main logic', codes[1].index('predictAliased') < codes[1].index('Author a1')),
    ('b1 == b2 is printed', 'b1 == b2' in codes[1]),
    ('one Object-inherited method called (getClass)', 'a1.getClass()' in codes[1]),
    ('MCQ line is left as a placeholder (not invented)', 'MCQ 1.12: <paste your score line' in allt),
]
ok = audit(path, {
    'layout': 'post', 'title': 'CSA Unit 1.12 Classes and Objects HW', 'categories': '[Java, Classes-and-Objects]',
    'lesson_language': 'Java', 'lesson_topic': 'Classes-and-Objects HW', 'lesson_part': 'interactive',
    'lesson_type': 'lesson', 'permalink': '/csa/unit_01/1_12_hw'}, expect_runners=2, extra=extra)
sys.exit(0 if ok else 1)
