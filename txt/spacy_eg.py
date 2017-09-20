
import spacy
dir(spacy)
# help(spacy.tokenizer)

NLP = spacy.load('en')
# dir(NLP)

es = 'I shot an elephant in my pajamas'
doc = NLP(es)
doc
# I shot an elephant in my pajamas

[i for i in doc]
# [I, shot, an, elephant, in, my, pajamas]

[i.pos for i in doc]
# [93, 98, 88, 90, 83, 82, 90]

[i.pos_ for i in doc]
# ['PRON', 'VERB', 'DET', 'NOUN', 'ADP', 'ADJ', 'NOUN']

[i.tag_ for i in doc]
# ['PRP', 'VBD', 'DT', 'NN', 'IN', 'PRP$', 'NNS']

[i.lemma_ for i in doc]
# ['-PRON-', 'shoot', 'an', 'elephant', 'in', '-PRON-', 'pajama']

[i.dep_ for i in doc]
# ['nsubj', 'ROOT', 'det', 'dobj', 'prep', 'poss', 'pobj']
