Garbled Email
=============
My solution to problem C, "Garbled Email", in the 2013 Google Code Jam, round 1B.

Unfortunately, I did not do this in the allowed 2.5 hour time window. In fact, it took me many more hours once the competition was over to get it working. But, I did complete it without looking at anyone else's analysis or implementation.

See my ["Garbled Email" blog post][blog] for a more in-depth discussion of my solution.

[blog]: http://www.offermann.us/2013/05/google-code-jam-ungarbling-a-garbled-email.html

Usage
-----
(See `inputs` directory for input files.)

    $ garbled_email.py <input_file>
    Case #1: 0
    Case #2: 2
    Case #3: 1
    Case #4: 1


Problem
-------
[Link to problem on Google Code Jam page.](https://code.google.com/codejam/contest/2434486/dashboard#s=p2)

Gagan just got an email from her friend Jorge. The email contains important information, but unfortunately it was corrupted when it was sent: all of the spaces are missing, and after the removal of the spaces, some of the letters have been changed to other letters! All Gagan has now is a string S of lower-case characters.

You know that the email was originally made out of words from the dictionary described below. You also know the letters were changed after the spaces were removed, and that the difference between the indices of any two letter changes is not less than 5. So for example, the string "code jam" could have become "codejam", "dodejbm", "zodejan" or "cidejab", but not "kodezam" (because the distance between the indices of the "k" change and the "z" change is only 4).

What is the minimum number of letters that could have been changed?

Dictionary
----------
In order to solve this problem, you'll need an extra file: a special dictionary that you can find at https://code.google.com/codejam/contest/static/garbled_email_dictionary.txt. It is not a dictionary from any natural language, though it does contain some English words. Each line of the dictionary contains one word. The dictionary file should be 3844492 bytes in size, contain 521196 words, start with the word "a", and end with the word "zymuznh".

When you're submitting the code you used to solve this problem, you shouldn't include the dictionary. As usual, however, you must submit all code you used to solve the problem.

Note that if you are using Windows and want to look at the dictionary file, you should avoid Notepad, and instead use WordPad or another piece of software, or else all the words might appear on the same line.

Input
-----
The first line of the input gives the number of test cases, T. T test cases follow. Each test case consists of a single line containing a string S, consisting of lower-case characters a-z.

Output
------
For each test case, output one line containing "Case #x: y", where x is the case number (starting from 1) and y is the minimum number of letters that could have been changed in order to make S.

Limits
------
S is valid: it is possible to make it using the method described above.

### Small dataset
* 1 ≤ T ≤ 20.
* 1 ≤ length of S ≤ 50.

###Large dataset
* 1 ≤ T ≤ 4.
* 1 ≤ length of S ≤ 4000.

Sample
------
### Input 

    4
    codejam
    cxdejax
    cooperationaabea
    jobsinproduction
    
### Output

    Case #1: 0
    Case #2: 2
    Case #3: 1
    Case #4: 1

Explanation
-----------
"code" and "jam" both appear in the dictionary. Although "cooperation" is an English word, it doesn't appear in the dictionary; "aabea" does.
