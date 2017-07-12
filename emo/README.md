TODO: pickle two sets:
1. singular nouns that differ from their plural form,
2. plural nouns that differ from their singular forms.

Classes for combining words into longer sequence for translation/replacement.


Plan:
1.	Translate sentence word by word, assigning a score based on completeness and maybe commonality of calcs.
2.	Translate sentence by phrase, and assign it a score based on the same criteria.  (If phrase translation
		always wins, drop 1, the word-calc translation)
3.	Transform original sentence into a sequence of syllables (or phonemes, whichever works better), and match
		this	against sequences of syllables or phonemes from the set of calc words.  Again, score it.

May the translation with the best score win!  That is, be remembered for learning.
