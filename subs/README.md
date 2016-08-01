subs/README.txt for subs_cipher.py
Sprax Lines  July 2016

The Script
----------
The subs_cipher.py script contains a class (SubCipher) and a main-function
driver that uses this class to infer and reverse a simple substitution
cipher.  Given a small sample of enciphered English text and a large corpus
of more or less similar English text, it derives the forward cipher map and
decrypts the sample text, writing each to separate files.

Input and Output
----------------
Usage: `python3 subs_cipher.py [cipher_file [corpus_file [verbosity]]]`
```
Where:
    The cipher_file contains text (at least mostly English) in which
    every lower [upper[ case ASCII letter has been replaced by the
    lower [upper] case substitution-cipher value for that letter;
    the corpus_file contains (mostly English) text whose word distribution
    is not too dissimilar from that of the encoded text;
    and verbosity is a number that controls how much trace is output.
Two new files are written:
1)  cipher_text.key will contain the discovered forward mapping of letter
    to cipher, and
2)  cipher_text.decoded will contain the deciphered contents the
    cipher_text file.
Verbosity levels:
    0   Only the forward cipher key and decoded text,
        plus warnings if anything unexpected happens.
    1   Insertions and deletions to the key, and the reasons/scores.
    2   Decoded words not found in the corpus
    3   All decoded words
    4   Messages pertaining to the queue of cipher words being matched
    6   Every partially decoded cipher word, every time a possible
        change to the cipher key is evaluated (very verbose).
```
How It Works
------------
### Strategy
The overall strategy has three phases:
1) Map all words and letters to their counts in the corpus and cipher texts.
2) Bootstrap the decoding by forward matching a few most common corpus words
to their likely encodings in the cipher text, based on frequency alone.  The
words I chose for this purpose are "I", "a", "the", and "and".  Experiments
show that to succeed on the actual given corpus and encrypted text, it is
enough to bootstrap on "the" and nothing else.
3) Given the current best guess at the cipher map, try to guess more
map entries by matching partially decoded cipher words with corpus
words, and update the map with whatever bindings results in the most
matched whole words.

### Phase 3 Algorithm
1. Partially order all the encoded words by how many unmapped letters each
one contains.  In fact, put them all in a priority queue (min heap).
2. Focus on the encoded words that contain exactly one unmapped letter each.
Taking each one of these single-unknown cipher words in descending order of
frequency, try to match it against all corpus words of the same length (or at
least against all the most common ones), also in descending order of frequency.
Whenever a corpus word's letters match all the previously guessed keys for
this cipher word's letters, evaluate the map that would result from adding the
implied new key mapping.  (That is, if the unguessed letter is at index j of
the cipher word, try adding corpus_word[j] -> cipher_word[j] to the existing
map.)  A simple way to score the map is to count the letters in all the cipher
words that would match whole corpus words when decoded with this map.
If multiple corpus words match this single-unknown cipher word, keep the first
one that gives the maximal score.
3. If this maximal score is greater than score of the old best-guess map,
then accept this new letter-to-cipher binding and go on to the next entry
in the queue.
4. As this process of inverse-map guessing and evaluation consumes the
queue, it adds keys to the map.  This, by definition, reduces the
number of unmapped letters in the words remaining in the queue.  Thus
their priorities should change.  One could re-evaluate all the entries
and re-heapify the queue every time the map changes, but in practice,
lazily re-evaluating each entry only when it is popped seems adequate.
Cipher words with zero remaining unmapped letters are discarded,
naturally, and the heap will re-order itself soon enough.
5. Repeat steps (2) through (4) until there are no more single-unknown
cipher words in the queue.
6. Using the resulting cipher map, decode the encrypted text.

Limitations and Possible Enhancements
-------------------------------------
### Robustness
The algorithm as a whole succeeds even if you comment out everything in
the bootstrapping phase except for finding the word "the".  You could
probably replace the find_the() method with a lot of random key-guessing
and map-scoring, and still succeed, but then you would be throwing out the
some of the most salient information in the corpus.)
All of this indicates to me that this approach is fairly robust.

Nevertheless, the current implementation has its shortcomings.
The way the comparison queue is set up, each encoded word in the
cipher text will be compared with possibly matching corpus words
at most once.  At the time of that matching, the scores resulting from
each potential letter-to-cipher match will depend in part on whatever
bindings are already present in the current best-guess
map.  These already guessed bindings may be incorrect, and indeed
they will be replaced if a different binding is found to yield a higher
score.  When such a binding is replaced, however, there is no
back-tracking; word matches that depended on the erroneous bindings
are not expressly tossed out or individually re-evaluated.  Nor is
the priority of every entry in the queue re-computed on whenever the
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
given corpus, whereas "in is" occurs 3 times.  Thus if you already
believe that i -> h, then you may subjectively evaluate "hr hj" as
approximately 213 times more likely to encode "is in" than it is
to encode "in is".  That gives you s -> r and n -> j.

#### Weighting and Confidence Measures
The scoring function simply counts all the letters in each decoded
word that matches a corpus word, when decoded using the cipher key
under evaluation.  All letters have the same weight, namely 1,
and this weight cannot be divided up among various possible matches
according to frequencies or any other measure of confidence.  For
example, the partially decoded word "the_" could match "them", "then",
or "they."  But instead of awarding 1/3 of a point to each of the
letters 'm', 'n', and 'y', or dividing that point up according to the
relative counts of each of these three words (in the corpus or the cipher
text), one of these letters will win the whole point, the others nothing.

### Speed
When running this script on a large corpus, such as the corpus-en.txt
file provided, nearly all the runtime goes to reading the file and
counting words.  Since the script will converge on the correct answer
as soon as it has tried matching the encoded words against most of their
originals, I was tempted to read in only part of the corpus, run the
matching algorithm, then read in more of the corpus and re-run the
inverse matching phase only if there were still unknown letters and words.
That would not have saved me anything, though, because even after matching
the encoded words against that entire corpus, the decoded word
'simplification' is still unmatched, and more importantly, the letters
j, q, and z do not appeared in any of the decoded words.  Thus the map
remains incomplete.
(I also wrote code to guess these remaining 3 letters based solely on
frequency, but with a count of 0 in the cipher text, these letters have
no meaningful frequencies.  Rather than confuse the issue, I left that
code out.  Better to match j, q, and z to nothing than to make an
uninformed guess.)

#### Faster Data Structures
I know from experience that a well-coded trie can beat a hashmap at
rejecting non-matching words.  Instead of multiplying and adding up
every letter in the match-candidate to derive a hash code for addressing
words in a large table, the trie uses the candidate's letters directly as
indexes into a compact, hopefully cache-resident table.  But I think
that would be overkill for a problem of the given size characteristics.

### Space
The corpus Counter stores the original string and its count for every
word in the corpus, even if the count is only 1.  Right now, the count
information is used mainly to set the order in which to try matching
corpus words to partially decoded cipher words.  That is important,
but the solver would probably still succeed if single-occurrence words
were jettisoned.

Other Notes
-----------
Input files are assumed to be encoded in UTF-8, a la Project Gutenberg.
Outputting non-ASCII characters to a terminal screen can cause Python
to throw UnicodeEncodeError messages.  Mac and KDE terminals do not
have this problem, but I wrote this code mostly using VIM on a PC.
To handle that problem, it defines a specialized print function (uprint)
that checks the output file encoding (by default, the encoding of sys.stdout),
and tries to compensate.
