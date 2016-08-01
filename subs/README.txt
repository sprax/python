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
The overall strategy has three parts:
1) Map all words and letters to their counts in the corpus and cipher texts.  
2) Bootstrap the decoding by forward matching a few most common corpus words
to their likely encodings in the cipher text, based on frequency alone.  The
words I chose for this purpose are "I", "a", "the", and "and".  Experiments
show that for actual given corpus and encrypted texts, "the" alone would have
been sufficient.
3) Given the current best guess at the cipher key, gather all the encoded
words that contain exactly one letter whose inverse mapping has not yet been
guessed.  Taking each of these single-unknown cipher words in descending
order of frequency, try to match it against all (or at least the most common)
corpus words of the same length, also in descending order of frequency.
Whenever a corpus word's letters match all the previously guessed keys of
this cipher word, evaluate the map that would result from adding the implied
new key mapping.  (That is, if the unguessed letter is at index j of the
cipher word, try adding corpus_word[j] -> cipher_word[j] to the existing map.)
A simple way to score the map is to count the letters in all the cipher words
that would match whole corpus words when decoded with this map.  If multiple
corpus words match the single-unknown cipher words, keep the first one that 
gives the maximal score.  If this maximal score is greater than score of the
old best-guess map, then accept this new binding and go on to the next
single-unknown cipher word.  





Limitations and Possible Enhancements
-------------------------------------
### Robustness
The way the comparison queue is set up, each encoded word in the 
cipher text will be compared with possibly matching corpus words
at most once, and at that time, the scores resulting from each
potential letter-to-cipher match will depend in part on whatever
letter-to-cipher bindings are already present in the current best-guess
map.  These already guessed bidings may be incorrect, and indeed 
they will be replaced if a different binding is found to yield a higher
score.  When such a binding is replaced, however, there is no
back-tracking; word matches that depended on the erroneous bindings
are not expressly tossed out or individually re-evaluated.  Nor is
the priority of every entry in the queue re-computed on wheneve the
current cipher map is "corrected" by deleting and replacing an
existing key.  Instead, the queue just greedily processes forward.
On a smaller sample size, it might be important to re-try previously
matched cipher words containing any letter whose inverse cipher key
is corrected.

#### Higher Order Syntax: Letter and Word Order

##### Letter Order
The current decrypting methods look only at individual letter and 
word frequencies, taking no account of any prescriptive or statistical
constraints on their order.  In English, for example, many words begin
with the letter B followed by a vowel, but no words begin with 'bb',
'bc', 'bf', or 'bg', and very few words begin with 'bd' or 'bh' (they
are mostly loan words).  It would be straightforward to count the
occurrences of all adjacent letter pairs found in the corpus, create
separate weighted graphs for the beginnings, interiors, and ends of
words, and add these statistical constraints to the scoring mechanism:
basically, multiply any possible decoding of a cipher word by its
syntactic probability as measured only from the corpus.  

##### Word Order
Likewise, word order within sentences is constrained.  Some adjacent
word pairs (or higher-order engrams) are much more frequent than
others.  For example, the word pair "is in" occurs 639 times in the
given corpus, whereas "in is" occors 3 times.  Thus if you already
believe that i -> h, then you may subjectively evaluate "hr hj" as
approximately 213 times more likely to encode "is in" than to encode
"in is".  That gives gives s -> r and n -> j.

#### Weighting and Confidence Measures
The scoring function simply counts all the letters in each decoded
word that matches a corpus word, when decoded using the cipher key
under evaluation.  All letters have the same weight, namely 1,
and this weight cannot be devided up among various possible matches
according to frequencies or any other measure of confidence.  For 
example, the partially decoded word "the_" could match "them", "then",
or "they."  But instead of awarding 1/3 of a point to each letter 'm',
'n', and 'y', or dividing that point up according to the relative 
counts of each of these three words (in the corpus or the cipher text),
one of these letters will win the whole point, the others get nothing.


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

#### Faster Data Structures
I know from experience that a well-coded trie can beat a hashmap at
rejecting non-matching words.  Instead of multiplying and adding up
every letter in the match candidate to derive a hash code into a 
large table, the trie uses the candidate's letters directly as
indicies into a compact, hopefully cache-resident table.  But I think
that would be overkill for a problem of the given size characteristics.

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

