# txt
TODO:
ML/DL for human-readable, human-compiler-like index


SOV paraphrasis

Sentence Similarity:
    String equality
    Token list equality (from conservative, not-very-lossy clean-up)
    Token list similarity (1 - distance), minimally weighted
    Token list with replacements: case-folding, stemming, etc.
    Feature list similarity
    *Bag of words?  
    Pariphrasis
    Word2Vec
    *Grammar

Hierarchy:
  Text
    Paragraph
      Sentence
        Statement
          features include: what kind of question it may answer.
        Question
          Query (factual, 3rd person)
            features:
              kind of question: Are/Is, How, What, When, Where, Which, Who, Why
          Request/Command/exhortation (2nd person, explicit or implied)
