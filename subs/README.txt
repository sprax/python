subs/README.txt for subs_cipher.py
Sprax Lines  July 2016

The Script
----------
The subs_cipher.py script contains a class (SubCipher) and a main-function
driver that uses this class to infer and reverse a simple substituion
cipher.  Given a small sample of enciphered English text and a large corpus
of more or less similar English text, it derives the forward cipher key and
decrypts the sample text, writing each to separate files.  

Input and Output
----------------
Depending on the verbosity setting

How It Works
------------


Limitations and Possible Enhancements
-------------------------------------
### Robustness
The way the comparison queue is set up, each encoded word in the 
cipher text will be scored against possibly matching corpus words
matches only once, and the relative scores then will be based 
partly on the already existing key assignments in whatever 
cipher mapping was current at that time.  But these keys
assignments change as more encoded words are processed.  
On a smaller sample size, it might be important to re-try 
previously matched words when any bindings they assumed are
later changed.  Not re-trying them meas that some information is lost.  

### Speed
When running this script on a large corpus, such as the corpus-en.txt 
file provided, nearly all the runtime goes to reading the file and
counting words.  Since the script will converge on the correct answer
as soon as it has tried matching the encoded words agains most of their
originals, I was tempted to read in only part of the corpus, run the 
matching algorithm, then read in more and run it again only if there
were still unknown letters and words.  That would not have saved me
anything, though, because even after matching the encoded words against
that entire corpus, the decoded word 'simplification' is still unmatched,
and more importantly, the letters j, q, and z do not appeared in any of
the decoded words, and so the key is incomplete.  (I also wrote code to
guess these remaining 3 letters based solely on frequency, but with a 
count of 0 in the cipher text, these letters have no meaningful
frequencies.  Rather than confuse the issue, I left that code out.
Better to match j, q, and z to nothing than to make an uninformed guess.)

### Space
The corpus Counter stores the original string and its count for every 
word in the corpus, even if the count is only 1.  Right now, the count 
information is used mainly to set the order in which to try matching 
corpus words to partially decoded cipher words.  That is important,
but the solver would probably still succeed in single-occurence words
were jettisoned.  

Other Notes
-----------
Input files are assumed to be encoded in UTF-8, a la Project Gutenberg.
Outputting non-ASCII characters to a terminal screen can cause Python
to throw UnicodeEncodeError messages.  Mac and KDE terminals do not
have this problem, but I wrote this code mostly using VIM on a PC,
so it defines a specialized print function (uprint) that checks the 
output file encoding (by defulat, the encoding of sys.stdout), and 
tries to compensate.

