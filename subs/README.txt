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
### Runtime 
When running this script on a large corpus, such as the corpus-en.txt 
file provided, nearly all the runtime goes to reading the file and
counting words.  Since the script will converge on the correct answer
as soon as it has tried matching the encoded words agains most of their
originals, I was tempted to read in only part of the corpus, run the 
matching algorithm, then read in more and run it again only if there
were still unknown letters and words.  That would not have saved me
anything, though, because even after that entire corpus was matched
against, there are still two unmached words and 3 unknown letters.
Why?  Because ...

Other Notes
-----------
Input files are assumed to be encoded in UTF-8, a la Project Gutenberg.
Outputting non-ASCII characters to a terminal screen can cause Python
to throw UnicodeEncodeError messages.  Mac and KDE terminals do not
have this problem, but I wrote this code mostly using VIM on a PC,
so it defines a specialized print function (uprint) that checks the 
output file encoding (by defulat, the encoding of sys.stdout), and 
tries to compensate.

