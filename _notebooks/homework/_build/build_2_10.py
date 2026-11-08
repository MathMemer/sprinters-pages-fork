"""Build CSA 2.10 Implementing String Algorithms homework (permalink /csa/unit_02/2_10_hw)."""
import json
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hwlib import Notebook, safety_rules, audit, outputs_of, java_run  # noqa: E402

TOPIC = 'String-Algorithms'
TITLE = 'CSA Unit 2.10 Implementing String Algorithms HW'
nb = Notebook(2, '10', TOPIC)
nb.front_matter(
    title=TITLE,
    description='Homework for 2.10 Implementing String Algorithms. Count vowels with a one-character substring window, test palindromes by building a reversed String, and trace a step-2 loop over a String.',
    permalink='/csa/unit_02/2_10_hw')

nb.md('''
## 1. Overview

This is my homework notebook for [2.10 Implementing String Algorithms]({{ site.baseurl }}/csa/unit_02/2_10). Each code cell below is Java code with the output from a real run (`javac` and `java` 21) saved under it, so the page reads the same without a Java server.

**Key idea:** a loop can visit every character of a String, and `substring` pulls one piece out at a time.

| Tool | Meaning | Example (`s = "java"`) |
| --- | --- | --- |
| `s.length()` | the number of characters | `4` |
| index | the position of a character, **starting at 0**; the last one is `length() - 1` | `j` is 0, `a` is 1, `v` is 2, `a` is 3 |
| `s.substring(a, b)` | the characters from index `a` up to **but not including** `b` | `s.substring(1, 3)` is `"av"` |
| one-character window | `s.substring(i, i + 1)` is the single character at index `i` | `s.substring(2, 3)` is `"v"` |
| `+` on Strings | builds a new String | `"a" + "b"` is `"ab"` |
| `a.equals(b)` | compares the **characters** of two Strings (not `==`, see 2.6) | `"java".equals("java")` is `true` |

**The loop bound.** The valid indexes are `0` to `length() - 1`, so the loop test is `i < s.length()`. The window `substring(i, i + 1)` is also safe at the last index, because the end index is allowed to equal `length()`. The bound `i <= s.length()` would let `i` reach `length()`, and `substring(length(), length() + 1)` is past the end of the String.

| Part | What I did | Points |
| --- | --- | --- |
| Popcorn Hack | Counted the vowels in a word with a one-character window and `\\|\\|` (`iterate` has 4) | 0.2 |
| Palindrome | Built a reversed String and compared with `.equals` | 0.5 |
| Quick check | Traced a loop that steps by 2 and stated the index range | 0.2 |
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
crash = java_run(r'''
public class OutOfBounds {
    public static void main(String[] args) {
        String word = "iterate";
        try {
            for (int i = 0; i <= word.length(); i++) {      // BUG: <= lets i reach length()
                String ch = word.substring(i, i + 1);
            }
            System.out.println("no error");
        } catch (StringIndexOutOfBoundsException e) {
            System.out.println("StringIndexOutOfBoundsException: " + e.getMessage());
        }
    }
}
''')
nb.md(f'''
### Popcorn Hack (In-Class)

Count the vowels in `word`. Use a one character window and a compound Boolean expression with `||`. Expected for `iterate`: 4.

**Concept:** visit each index `i` from 0 to `length() - 1`, take the one-character window `word.substring(i, i + 1)`, and count it when it equals `"a"`, `"e"`, `"i"`, `"o"`, or `"u"`. Characters are compared with `.equals`, joined with `||` (one `||` between each pair, so four in total for five vowels).

**My predictions (written before I ran the code):** the trace for `iterate` (7 letters, indexes 0 to 6).

| `i` | `substring(i, i + 1)` | A vowel? | `vowels` after |
| --- | --- | --- | --- |
| 0 | `i` | yes | 1 |
| 1 | `t` | no | 1 |
| 2 | `e` | yes | 2 |
| 3 | `r` | no | 2 |
| 4 | `a` | yes | 3 |
| 5 | `t` | no | 3 |
| 6 | `e` | yes | 4 |

The loop stops when `i` reaches 7 (`7 < 7` is false). Expected: `Vowels: 4`.

| `word` | Hand trace | Expected vowels |
| --- | --- | --- |
| `iterate` | above | `4` |
| `rhythm` | no a, e, i, o or u | `0` |
| `queue` | u, e, u, e | `4` |
| `a` (one letter) | index 0 only | `1` |
| `""` (empty) | `0 < 0` is false, so the loop never runs | `0` |

The rule counts the lowercase letters a, e, i, o and u only, as the lesson states, so an uppercase `A` would not be counted. All my test words are lowercase.

**The loop bound is derived from `length()`.** For `iterate`, `length()` is 7, so the last index is 6. If I wrote `i <= word.length()`, `i` would reach 7, and `substring(7, 8)` would fail. I ran that bug once to see the real error (it is caught and printed, so the program stops normally): `{crash}`.

**What the important lines do:** `word.substring(i, i + 1)` is the one-character window. The long `if` joins five `.equals` tests with `||`, so a vowel makes it true. `vowels++` counts it. The method `countVowels(word)` lets one run test five words, and `check` prints PASS or FAIL against my table.
''')
nb.runner('Popcorn Hack. Count the vowels with a one-character substring window and ||, tested on five words', r'''
public class VowelCounter {
    // Counts the vowels in word, one character at a time
    static int countVowels(String word) {
        int vowels = 0;

        for (int i = 0; i < word.length(); i++) {            // bound from length(): i never reaches length()
            String ch = word.substring(i, i + 1);            // the one-character window at index i

            // Compound condition: a, e, i, o or u (compare Strings with .equals)
            if (ch.equals("a") || ch.equals("e") || ch.equals("i") || ch.equals("o") || ch.equals("u")) {
                vowels++;
            }
        }
        return vowels;
    }

    // Prints one answer and checks it against my prediction
    static void check(String word, int expected) {
        int vowels = countVowels(word);
        System.out.println("Word: \"" + word + "\"");
        System.out.println("Vowels: " + vowels);
        System.out.println((vowels == expected ? "PASS: " : "FAIL: ") + "expected " + expected);
    }

    public static void main(String[] args) {
        check("iterate", 4);    // the lesson's case
        check("rhythm", 0);
        check("queue", 4);
        check("a", 1);
        check("", 0);           // boundary: the loop never runs
    }
}
''', output_note='all five predictions matched, and iterate printed Vowels: 4')
nb.md('**What I learned:** the window `substring(i, i + 1)` is only safe because `i` stops at `length() - 1`. The bound `i < word.length()` comes straight from the String, so it stays correct for any word, including the empty one.')

# ---------------------------------------------------------------- homework
nb.md('''
### Homework Hack

Two short tasks.

1. Finish the code below: `isPalindrome` returns `true` when a String reads the same backwards. Build the reversed String, then compare with `.equals`.
2. Answer the quick check.

#### Task 1: Palindrome

**Concept:** a palindrome reads the same forwards and backwards. To test it, build the reversed String, then compare it with the original. To reverse, go through the String from the first character to the last and add each character to the **front** of `rev`: `rev = s.substring(i, i + 1) + rev;`. The characters end up in the opposite order. `rev` is built at run time, so it is a different object from `s`, and `==` would compare references and be false even for a palindrome. `rev.equals(s)` compares the characters (the same lesson as 2.6).

**My predictions (written before I ran the code):** building `rev` for `"java"`, one pass at a time:

| `i` | `substring(i, i + 1)` | `rev` after `rev = char + rev` |
| --- | --- | --- |
| start | | `""` |
| 0 | `j` | `"j"` |
| 1 | `a` | `"aj"` |
| 2 | `v` | `"vaj"` |
| 3 | `a` | `"avaj"` |

`"avaj"` is not `"java"`, so `isPalindrome("java")` is `false`. For `"racecar"` the reversed String is `"racecar"` again, so it is `true`.

| `s` | `rev` | Same as `s`? | Expected |
| --- | --- | --- | --- |
| `racecar` | `racecar` | yes | `true` |
| `level` | `level` | yes | `true` |
| `java` | `avaj` | no | `false` |
| `abba` | `abba` | yes | `true` |
| `ab` | `ba` | no | `false` |
| `a` (one letter) | `a` | yes | `true` |
| `""` (empty) | `""` (the loop never runs) | yes | `true` |
| `Level` (capital L) | `leveL` | no, the comparison is case sensitive | `false` |

**What the important lines do:** `String rev = "";` is the starting String. The loop `for (int i = 0; i < s.length(); i++)` visits every index. `rev = s.substring(i, i + 1) + rev;` puts the next character in front. `return rev.equals(s);` compares the characters and returns the answer. `check` prints PASS or FAIL against my table, and the first three calls use the lesson's words and output format.
''')
nb.runner('Homework Hack. isPalindrome with a reversed String and .equals, tested on eight Strings', r'''
public class Palindrome {
    public static boolean isPalindrome(String s) {
        String rev = "";

        // Build rev by adding each character to the FRONT, so the order is reversed
        for (int i = 0; i < s.length(); i++) {          // bound from length(): i never reaches length()
            rev = s.substring(i, i + 1) + rev;
        }

        // .equals compares the characters; == would compare references and fail for a run-time String
        return rev.equals(s);
    }

    // Prints one answer and checks it against my prediction
    static void check(String s, boolean expected) {
        boolean result = isPalindrome(s);
        System.out.println(s + ": " + result);
        System.out.println((result == expected ? "PASS: " : "FAIL: ") + "\"" + s + "\" is " + expected);
    }

    public static void main(String[] args) {
        check("racecar", true);   // the three words the lesson lists
        check("level", true);
        check("java", false);

        check("abba", true);
        check("ab", false);
        check("a", true);         // one letter
        check("", true);          // boundary: the loop never runs
        check("Level", false);    // case sensitive
    }
}
''', output_note='all eight predictions matched, with racecar and level true and java false')

nb.md('''
#### Task 2: Homework quick check

**Question:** what does this print? Type the output exactly.

```java
String s = "loop";
String out = "";
for (int i = 0; i < s.length(); i += 2) {
    out += s.substring(i, i + 1);
}
System.out.println(out);
```

**My answer: `lo`.** The index range: `s.length()` is 4, so the test is `i < 4`, and `i` goes up by 2 each pass, so `i` takes only the values **0 and 2**. The next value, 4, fails the test, so the highest index used is 2. That stays inside the valid range 0 to 3, so there is no out-of-bounds error.

| `i` | `i < 4`? | `s.substring(i, i + 1)` | `out` after |
| --- | --- | --- | --- |
| 0 | true | `l` (index 0) | `"l"` |
| 2 | true | `o` (index 2; `substring(2, 3)`) | `"lo"` |
| 4 | **false** | the loop ends | `"lo"` |

The letters at indexes 1 and 3 (`o` and `p`) are skipped because the step is 2. I wrote the answer before running the check below.
''')
nb.runner('Homework quick check. Run to confirm the output and the index values used', r'''
public class StepByTwo {
    public static void main(String[] args) {
        String s = "loop";
        String out = "";

        for (int i = 0; i < s.length(); i += 2) {
            System.out.println("i is " + i + ", window is \"" + s.substring(i, i + 1) + "\"");
            out += s.substring(i, i + 1);
        }

        System.out.println(out);
    }
}
''', output_note='i took only the values 0 and 2, and the output is lo, as I answered')

nb.rubric('''
### Grading Plan (1 Point Total)

#### Classroom Rubric

- **0.2 points: Popcorn completion**
  I counted the vowels in `word` using a one character window (`word.substring(i, i + 1)`) and a compound condition with `||`, printing 4 for `iterate` (and passing four more words).

- **0.8 points: Homework completion**
  - **0.5 Palindrome:** `isPalindrome` builds the reversed String and compares with `.equals`, returning correct results for palindromes (`racecar`, `level`) and a non-palindrome (`java`), and for five more Strings.
  - **0.2 Quick check:** The traversal question is answered (`lo`) with the index range stated (`i` takes 0 and 2, inside the valid range 0 to 3).
  - **0.1 Notebook quality:** Every code cell executed with output visible, and a markdown cell before each code section explaining the concept.

#### Quick Validation Checklist

- Present: loop bound derived from `length()` (`i < word.length()` and `i < s.length()`)
- Present: `.equals` used for the String comparison (`rev.equals(s)`)
- Absent: any index that can reach `length()` (both loops use `<`; the `<=` bug is shown only as a caught, captured error)
- Test: `iterate` yields 4 vowels; `racecar` is a palindrome and `java` is not
''', points=[0.2, 0.5, 0.2, 0.1])

path = nb.write()
print('wrote', path.name, len(nb.cells), 'cells')

cells = json.load(open(path))['cells']
codes = [''.join(c['source']) for c in cells if c['cell_type'] == 'code']
outs = outputs_of(path)
allt = '\n'.join(''.join(c['source']) for c in cells)
nc = [re.sub(r'//.*', '', c) for c in codes]
extra = [
    ('3 code cells (popcorn, homework, quick check)', len(codes) == 3),
    ('vowel loop bound is i < word.length() and uses the one-character window',
     'for (int i = 0; i < word.length(); i++)' in nc[0] and 'word.substring(i, i + 1)' in nc[0]),
    ('vowel condition joins five .equals tests with exactly four ||', nc[0].count('.equals("') == 5 and re.search(r'if \((.*)\)', nc[0]).group(1).count('||') == 4),
    ('iterate -> Vowels: 4 (the lesson case)', 'Word: "iterate"\nVowels: 4\nPASS:' in outs[0]),
    ('vowels: all five PASS (including the empty String)', outs[0].count('PASS:') == 5),
    ('palindrome builds rev by adding each character to the front and compares with .equals',
     'rev = s.substring(i, i + 1) + rev;' in nc[1] and 'return rev.equals(s);' in nc[1]),
    ('palindrome bound is i < s.length()', 'for (int i = 0; i < s.length(); i++)' in nc[1]),
    ('no == comparison between Strings in the palindrome code', not re.search(r'rev\s*==|==\s*rev|s\s*==\s*rev', nc[1])),
    ('lesson outputs: racecar true, level true, java false', 'racecar: true' in outs[1] and 'level: true' in outs[1] and 'java: false' in outs[1]),
    ('palindrome: all eight PASS', outs[1].count('PASS:') == 8),
    ('quick check prints lo, with i = 0 and 2 only', outs[2].strip().splitlines()[-1] == 'lo' and 'i is 0' in outs[2] and 'i is 2' in outs[2] and 'i is 4' not in outs[2]),
    ('out-of-bounds bug shown as a captured exception message', 'StringIndexOutOfBoundsException' in allt),
]
ok = audit(path, {
    'layout': 'post', 'title': TITLE, 'categories': f'[Java, {TOPIC}]', 'lesson_language': 'Java',
    'lesson_topic': f'{TOPIC} HW', 'lesson_source': 'APCSA', 'lesson_type': 'lesson',
    'permalink': '/csa/unit_02/2_10_hw'}, expect_runners=3, extra=extra)
sys.exit(0 if ok else 1)
