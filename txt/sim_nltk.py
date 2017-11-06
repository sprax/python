#!/usr/bin/env python3
'''Text similarity (between words, phrases, or short sentences) using NLTK'''

import functools
import heapq
import string
import time
import cProfile
import pstats
import io
# import pdb
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import qa_csv
import text_fio

STEMMER = nltk.stem.porter.PorterStemmer()
TRANS_NO_PUNCT = str.maketrans('', '', string.punctuation)
STOP_WORDS = nltk.corpus.stopwords.words('english')

# Most question words can also be used in qualifiers.  It's not the word, but the useage we want.
QUERY_WORDS = ['how', 'what', 'when', 'where', 'which', 'who', 'why']
MOST_STOPS = [word for word in STOP_WORDS if word not in QUERY_WORDS]

def stem_tokens(tokens, stemmer=STEMMER):
    '''list of stems, one per input tokens'''
    return [stemmer.stem(item) for item in tokens]

def normalize(text, translation=TRANS_NO_PUNCT):
    '''remove punctuation, lowercase, stem'''
    return stem_tokens(nltk.word_tokenize(text.translate(translation).lower()))

VECTORIZER = TfidfVectorizer(tokenizer=normalize, stop_words='english')
VECT_NO_STOPS = TfidfVectorizer(tokenizer=normalize)
VECT_MOST_STOPS = TfidfVectorizer(tokenizer=normalize, stop_words=MOST_STOPS)

def remove_stop_words(tokens, stop_words=STOP_WORDS):
    '''filter out stop words'''
    return [tok for tok in tokens if tok not in stop_words]

def ident(obj):
    '''identify function: just returns its argument'''
    return obj

def first(obj):
    '''first: returns the first item from an indexible, or failing that, just the object'''
    try:
        return obj.__getitem__(0)
    except TypeError:
        return obj

def second(obj):
    '''second: returns second item from an indexible, or failing that, just the object'''
    try:
        return obj.__getitem__(1)
    except TypeError:
        return obj

def third(obj):
    '''third: returns third item from an indexible, or failing that, just the object'''
    try:
        return obj.__getitem__(2)
    except TypeError:
        return obj

def cosine_sim_txt(txt_1, txt_2, vectorizer=VECTORIZER):
    '''dot-product (projection) similarity'''
    tfidf = vectorizer.fit_transform([txt_1, txt_2])
    return ((tfidf * tfidf.T).A)[0, 1]

def sim_weighted_qas(qst_1, ans_1, qst_2, ans_2, q_weight=0.5, sim_func=cosine_sim_txt):
    '''dot-product (projection) similarity combining similarities of questions and, if available, answers'''
    assert q_weight > 0.0 and q_weight <= 1.0
    # print("SIM_WEIGHTED_QAS(", qst_1, ans_1, qst_2, ans_2, q_weight, sim_func, ")")
    q_sim = sim_func(qst_1, qst_2)
    if q_weight < 1.0:
        if ans_1 and ans_2:
            try:
                a_sim = sim_func(ans_1, ans_2)
                return (q_sim - a_sim) * q_weight + a_sim
            except ValueError as vex:
                print("Error on answers (%s|%s): %s" % (ans_1, ans_2, vex))
                raise vex
    return q_sim

def cosine_sim_quanda(one_quanda, other_quanda, get_question=second, get_answer=third,
                      q_weight=0.5, vectorizer=VECTORIZER):
    '''dot-product (projection) similarity combining similarities of questions and, if available, answers'''
    assert q_weight > 0 and q_weight <= 1
    q_sim = cosine_sim_txt(get_question(one_quanda), get_question(other_quanda), vectorizer)
    if q_weight >= 1.0:
        return q_sim

    ans_1 = get_answer(one_quanda)
    ans_2 = get_answer(other_quanda)
    if ans_1 and ans_2:
        try:
            a_sim = cosine_sim_txt(ans_1, ans_2, vectorizer)
            return (q_sim - a_sim) * q_weight + a_sim
        except ValueError as vex:
            print("Error on answers (%s|%s): %s" % (ans_1, ans_2, vex))
    return q_sim

def cosine_sim_quanda_2(one_quanda, other_quanda, get_question=second, get_answer=third,
                        q_weight=0.5, vectorizer=VECT_NO_STOPS):
    '''dot-product (projection) similarity combining similarities of questions
    and, if available, answers'''
    assert q_weight > 0.0 and q_weight <= 1.0
    if q_weight >= 1.0:
        print("Degenerate q_weight: ", q_weight)
        return cosine_sim_txt(get_question(one_quanda), get_question(other_quanda), vectorizer)
    # print("DBG CSQ:  Q(%s)  A(%s)" % (get_question(other_quanda), get_answer(other_quanda)))
    qst_1 = get_question(one_quanda)
    qst_2 = get_question(other_quanda)
    ans_1 = get_answer(one_quanda)
    ans_2 = get_answer(other_quanda)
    try:
        tfidf = vectorizer.fit_transform([qst_1, qst_2, ans_1, ans_2])
        q_sim = ((tfidf * tfidf.T).A)[0, 1]
        a_sim = ((tfidf * tfidf.T).A)[2, 3]
        return (q_sim - a_sim) * q_weight + a_sim
    except ValueError as vex:
        print("Error, probably on answers (%s|%s): %s" % (ans_1, ans_2, vex))
    return 0.0

def cosine_sim_quanda_ms(one_quanda, other_quanda, get_question=second, get_answer=third,
                         q_weight=0.5, vectorizer=VECT_MOST_STOPS):
    '''Returns weighted Q & A similarity between two question-answer pairs'''
    return cosine_sim_quanda_2(one_quanda, other_quanda, get_question, get_answer,
                               q_weight, vectorizer)


def clip(value, loval=0, hival=1):
    ''' Clip value to [loval, hival], no frills. '''
    if value < loval:
        return loval
    if value > hival:
        return hival
    return value

def clip_verbose(value, loval=0, hival=1):
    ''' Verbosely clip value to [loval, hival] '''
    if value < loval:
        print("clip_verbose: {} -> {}".format(value, loval))
        return loval
    if value > hival:
        print("clip_verbose: {} -> {}".format(value, hival))
        return hival
    return value

def prob_clip_verbose(value, where="prob_clip_verbose", loval=0.000001, hival=0.99999, verbose=False):
    ''' Verbosely clip value to [loval, hival] '''
    if value != 0 and value < loval:
        if verbose:
            print("{} -> 0 \t\t at: {}".format(value, where))
        return 0
    if value != 1 and value > hival:
        if verbose:
            print("{} -> {} \t at: {}".format(value, hival, where))
        return hival
    return value


def prob_clip(value, loval=0.000001, hival=0.99999):
    ''' clip value to probability based on [loval, hival] '''
    if value != 0 and value < loval:
        return 0
    if value != 1 and value > hival:
        return hival
    return value


def unit_clip(value):
    '''
    Clip value to [0, 1], redundant with clip.
    TODO: Make semantics comply with naive assumptions/"ordinary language"?
    '''
    if value < 0:
        return 0
    if value > 1:
        return 1
    return value





def smoke_test():
    '''Tests that basic sentence similarity functionality works, or at least does not blow-up'''
    sent_1 = 'a little bird'
    sent_2 = 'a little bird chirps'
    sent_3 = 'a big dog barks a lot'
    print("cosine_sim_txt(%s, %s) == %f" % (sent_1, sent_1, cosine_sim_txt(sent_1, sent_1)))
    print("cosine_sim_txt(%s, %s) == %f" % (sent_1, sent_2, cosine_sim_txt(sent_1, sent_2)))
    print("cosine_sim_txt(%s, %s) == %f" % (sent_1, sent_3, cosine_sim_txt(sent_1, sent_3)))
    questions = ['How is that fair?!', 'What is fair?!', 'When is the fair?', 'Where is the fair?',
                 'Who is fair?', 'Why is that fair?']
    for qst in questions:
        print("remove_stop_words(normalize(%s)) -> " % qst, remove_stop_words(normalize(qst)))


def nearest_known(known_texts, input_text, similarity_func, threshold):
    '''find text in known_texts most similar to input_text, if similarity >= threshold'''
    idx, sim = nearest_other_idx(known_texts, input_text, similarity_func, threshold)
    if idx < 0:
        print("No saved text found more similar than %f" % threshold)
    else:
        print("Nearest at %f (%d) %s" % (sim, idx, known_texts[idx]))

def nearest_other_idx(other_texts, this_text, similarity_func, max_sim_val):
    '''
    Find the text in the other_texts array most similar to this_text and return its index.
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
        max_sim_val:        the initial value of max, or the maximum similariy found so far.
    '''
    max_sim_idx = -9999
    for idx, other_text in enumerate(other_texts):
        sim = similarity_func(this_text, other_text)
        if  max_sim_val < sim:
            max_sim_val = sim
            max_sim_idx = idx
    return  max_sim_idx, max_sim_val

def list_nearest_other_idx(texts, similarity_func=cosine_sim_txt):
    '''
    For each text in texts, find the index of the most similar other text.
    Returns the list of indexes.  The mapping is not necessarily 1-1, that is,
    two texts may share a most similar other text.
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
    '''
    nearests = len(texts)*[None]
    for idx, txt in enumerate(texts):
        max_idx_0, max_sim_0 = nearest_other_idx(texts[:idx], txt, similarity_func, -1)
        max_idx_1, max_sim_1 = nearest_other_idx(texts[idx+1:], txt, similarity_func, max_sim_0)
        nearests[idx] = 1 + idx + max_idx_1 if max_sim_1 > max_sim_0 else max_idx_0
    return nearests

def show_nearest_neighbors(texts, nearest_indexes=None):
    '''print the most similar pairs'''
    if nearest_indexes is None:
        nearest_indexes = list_nearest_other_idx(texts)
    for idx, txt in enumerate(texts):
        nearest_idx = nearest_indexes[idx]
        nearest_txt = texts[nearest_idx]
        print("  %3d.  T  %s\n  %3d.  O  %s\n" % (idx, txt, nearest_idx, nearest_txt))

###############################################################################
def similarity_dict(train_quats, trial_quat, q_weight=1.0, sim_func=cosine_sim_txt,
                    min_sim_val=0):
    '''
    Returns a dict mapping train_quats' indexes to their similarity with this_text,
        provide their similarity value >= min_sim_val
        similarity_func:    function returning the similariy between two texts (as in sentences)
        min_sim_val:        similarity threshold
    '''
    sim_dict = {}
    for idx, train_quat in enumerate(train_quats):
        if train_quat is trial_quat:
            continue
        try:
            sim = sim_weighted_qas(train_quat.question, train_quat.answer,
                                   trial_quat.question, trial_quat.answer, q_weight=q_weight, sim_func=sim_func)
            # sim = unit_clip_verbose(sim)
            sim = prob_clip_verbose(sim, where="(%d x %d)" % (train_quat.id, trial_quat.id), verbose=False)
            if  sim >= min_sim_val:
                sim_dict[idx] = sim
        except ValueError as ex:
            print("Continuing past error at idx: {}  ({})  ({})".format(idx, ex, train_quats[idx]))
            raise ex
    return  sim_dict

def nlargest_items_by_value(dict_with_comparable_values, count=10):
    '''Returns a list of the maximally valued N items (key, value)-tuples) in descending order by value.'''
    return heapq.nlargest(count, dict_with_comparable_values.items(), key=lambda item: (item[1], -item[0]))

def nlargest_keys_by_value(dict_with_comparable_values, count=10):
    '''Returns a list of the keys to the greatest values, in descending order by value.'''
    return heapq.nlargest(count, dict_with_comparable_values, key=dict_with_comparable_values.get)

def nlargest_values(dict_with_comparable_values, count=10):
    '''Returns a list of the greatest values in descending order.  Duplicates permitted.'''
    return heapq.nlargest(count, dict_with_comparable_values.values())

def find_nearest_quats(train_quats, trial_quat, q_weight=1.0, sim_func=cosine_sim_txt, max_count=5, min_sim_val=0):
    '''
    Find the N most similar texts to this_text and return a list of (index, similarity) pairs in
    descending order of similarity.
        train_quats:        The training sentences or question-answer-tuples or whatever is to be compared.
        trial_quat:         The trial object to be compared with the training objects; must have .question attribute.
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
        max_count           maximum size of returned dict
    '''
    assert q_weight >= 0.0
    sim_dict = similarity_dict(train_quats, trial_quat, q_weight=q_weight, sim_func=sim_func,
                               min_sim_val=min_sim_val)
    return nlargest_items_by_value(sim_dict, max_count)

def find_nearest_qas_lists(train_quats, trial_quats, find_nearest_qas, sim_func,
                           q_weight=1.0, max_count=5, min_sim_val=0.0, id_eq_index=False,
                           verbose=True):
    '''
    For each question-and-answer tuple in trial_quats, find a list of indexes of the most similar Q and A's in train_quats.
    Returns list of lists of items as in: [[(index, similariy), ...], ...]
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
    '''
    assert q_weight >= 0.0
    ntrain, ntrial = len(train_quats), len(trial_quats)
    nearests = ntrial*[None]
    beg_time = prv_time = time.time()
    for idx, trial_quat in enumerate(trial_quats):
        try:
            # consistency check:
            idn = trial_quat.id
            assert isinstance(idn, int)
            if id_eq_index:
                # print("DBG LMSTL: ", trial_quat)
                if idx > 0 and idx + 100 != idn:
                    print("ERROR:", (idx + 100), "!=", trial_quat.id, "at", trial_quat)
                    raise IndexError
            nearests[idx] = find_nearest_qas(train_quats, trial_quat, q_weight=q_weight,
                                             max_count=max_count, min_sim_val=min_sim_val,
                                             sim_func=sim_func)
            if verbose:
                time_gone = time.time() - beg_time
                time_left = time_gone * (ntrial/(idx + 1) - 1)
                sim_tuple = nearests[idx][0]
                max_squat = train_quats[sim_tuple[0]]
                max_simil = sim_tuple[1]
                print("(Time & ETR %4.1f %4.1f)  %d  %d -> %d (%.3f) %s -> %s" % (time_gone, time_left,
                      trial_quat.id, trial_quat.label, max_squat.id, max_simil, trial_quat.question,
                      max_squat.question))
        except KeyboardInterrupt:
            int_time = time.time()
            print("KeyboardInterrupt in find_nearest_qas_lists at %d/%d trials on %d train_quats after %d seconds." % (idx, ntrial, ntrain, int_time - beg_time))
            if int_time - prv_time < 2:
                print("That's 2 interrupts in less than 2 seconds -- breaking out of loop in find_nearest_qas_lists!")
                break;
            prv_time = int_time
    return nearests

def find_nearest_qas_lists_self(train_quats, trial_quats, find_nearest_qas,
                                sim_func=cosine_sim_txt, q_weight=1.0, max_count=5, min_sim_val=0.0):
    '''Find similars including self.'''
    return [find_nearest_qas(train_quats, trial_quat, q_weight, sim_func,
                             max_count, min_sim_val) for trial_quat in trial_quats]

def find_ranked_qa_lists(train_quats, trial_quats, find_nearest_qas, sim_func, q_weight=1.0, max_count=6, min_sim_val=1.0/6):
    '''
    Returns list of most similar lists.  For each object in quats, compute the similarity with all
    (other) objects in quats, and save at most max_count indices and similarity measures in descending
    order of similarity, where similiary >= min_sim_val.  If exclude_self is false, compare each object
    with itself as well as the others (sanity check)
    '''
    ranked_lists = None
    beg_time = time.time()
    # import pdb; pdb.set_trace()
    ranked_lists = find_nearest_qas_lists(train_quats, trial_quats, find_nearest_qas, sim_func,
                                          q_weight=q_weight, max_count=max_count, min_sim_val=min_sim_val,
                                          id_eq_index=False)
    seconds = time.time() - beg_time
    print("Finding all similarity lists (train %d, trial %d, nears %d) took %.1f seconds" % (len(train_quats), len(trial_quats), max_count, seconds))
    return ranked_lists


def distance_counts(train_quats, trial_quats, sim_lists, max_dist):
    '''
    Returns a list of miss-distance counts: how many missed the gold standard by 0 (exact match),
    how many missed it by one (as in the gold standard got the second highest similarity score)
    how many missed it by two, on up to max_dist.  The total number of items with a gold standard
    is added as the last element in the list.
    '''
    dist_counts = (max_dist + 1) * [0]
    gold_scored = 0
    for trial_quat, sim_list in zip(trial_quats, sim_lists):
        try:
            gold = int(trial_quat.label)
            assert isinstance(gold, int)
        except ValueError as ex:
            print("ERROR on: ", trial_quat, ex)
            continue
        gold_scored += 1
        # ms = sim_list[0]
        # msi = ms[0]
        # sim = ms[1]
        # print("DBG_F: Q_%d <==> Q_%d (%s <==> %s) first, %.4f (%s : %s)" % (int(qax.id), msi, qax.question,
        #       trial_quats[msi][1], sim, remove_stop_words(normalize(qax.question)), remove_stop_words(normalize(trial_quats[msi][1]))))
        for idx, item in enumerate(sim_list):
            # print("DC: %d  item(%d, %f)" % (idx, item.id, item[1]))
            train_quat = train_quats[item[0]]
            if gold == train_quat.id:      # compare idn to idn (not idx)
                # print("DBG_G: Q_%d <==> Q_%d (%s <==> %s) at %d, %.4f (%s : %s)\n" % (
                #                              int(qax.id), item[0], qax.question, quats[item[0]][1],
                #       idx, item[1], remove_stop_words(normalize(qax.question)),
                # remove_stop_words(normalize(quats[item[0]][1]))))
                dist_counts[idx] += 1
                break
    # save the number of gold standard matches as the last count in the list
    assert gold_scored > 0
    dist_counts[max_dist] = gold_scored
    return dist_counts

def score_distance_counts(dist_counts, weights):
    '''Compute a score from miss-distance counts.  The perfect score would be 1.0'''
    assert len(weights) > 0 and weights[0] == 1.0
    assert len(weights) < len(dist_counts)
    gold_scored = dist_counts[-1]
    # print("DBG SDC DCS:", dist_counts)
    # print("DBG SDC WTS:", weights)
    assert gold_scored > 0
    score = dist_counts[0]                  # number of exact matches
    for idx, weight in enumerate(weights[1:], 1):
        assert weight <= weights[idx - 1]
        # print("DBG SDC LOOP:", idx, dist_counts[idx])
        score += weight * dist_counts[idx]
    # print("DBG_SDC: score(%.4f) / %d == %f" % (score, gold_scored, score/gold_scored))
    return 100 * score / gold_scored

def score_most_sim_lists(train_quats, trial_quats, sim_lists, weights=None):
    '''Sum up gold-standard accuracy score'''
    if weights is None:
        weights = [1.0, 0.6667, 0.5, 0.375, 0.25, 0.1667]
    dist_counts = distance_counts(train_quats, trial_quats, sim_lists, len(weights))
    return score_distance_counts(dist_counts, weights)

def save_most_sim_qa_lists_tsv(train_quats, trial_quats, sim_lists, ntrain=None,
                               outpath="simlists.tsv", min_sim_val=0, sort_most_sim=True):
    '''Save ranked most-similar lists to TSV file'''
    if sort_most_sim:
        sim_oix = []
        for idx, sim_list in enumerate(sim_lists):
            # print("QUAT:", idx, quats[idx])
            # print("SIM_LIST:", sim_list)
            len_lst = len(sim_list)
            # max_oix = sim_list[0][0] if len_lst > 0 else -1
            max_sim = sim_list[0][1] if len_lst > 1 else 0
            sum_sim = sum([y[1] for y in sim_list])
            sim_oix.append((max_sim, sum_sim, -idx))
        # Sort on tuple keys
        isorted = [-tup[2] for tup in sorted(sim_oix, reverse=True)]

        # HACK for separating training and test data if they were mixed.
        if ntrain:
            # Partition training from trial indices
            print("LEN_TRAIN ", ntrain, "LEN(sim_list)", len(sim_lists), "\n")
            print("BEFORE:   ", isorted, "\n")
            sort_lo = [idx for idx in isorted if idx < ntrain]
            print("AFTER LO: ", sort_lo, "\n")
            sort_hi = [idx for idx in isorted if idx >= ntrain]
            print("AFTER HI: ", sort_hi, "\n")
            isorted = sort_lo + sort_hi
    else:
        isorted = range(len(trial_quats))
    # print("ISORTED ", len(isorted), ": ", isorted)

    out = text_fio.open_out_file(outpath)
    mix = 0
    for idx in isorted:
        qax = trial_quats[idx]
        idn = qax.id
        most_sim_list = sim_lists[idx]
        lqax, ansr = len(qax), 'N/A'
        if lqax < 3:
            print("MISSING ANSWER at:", idx, qax.id, qax.question, "ANSWER:", ansr, sep="\t")
        else:
            ansr = qax.answer
            gold = qax.label
        print(idn, gold, qax.question, ansr, sep="\t", file=out)
        for oix, sim in most_sim_list:  # Note: oix = other index, i.e., the index of the gold standard other QAS
            if sim >= min_sim_val:
                try:
                    # print("IDX: ", idx, " OIX: ", oix, " SIM: ", sim)
                    quox = train_quats[oix]
                    sidn = quox.id
                    sgld = quox.label
                    stxt = quox.question
                    sans = quox.answer
                    print("\t%3d\t%.5f\t%s\t%s\t%s" % (sidn, sim, stxt, sans, sgld), file=out)
                except IndexError as ex:
                    print("ERROR AT MIX {}: idx {}  qax {},  err: {}\n".format(mix, idx, qax, ex))
                    # raise IndexError

        # if sort_most_sim:
        #     print("TUP {:3}:\t {}".format(mix, sim_oix[idx]))
        print(file=out)
        mix += 1
    if outpath != '-':
        out.close()

# VECTORIZER (default):                  (size=201, count=6) took 96.1 seconds; score 0.8583
# VECT_MOST_STOPS (DEFAULT-QUERY_WORDS): (size=201, count=6) took 96.3 seconds; score 0.6635
# TODO: Why do the query words make the score worse?
# TEST: >>> match_tat(fair, sim_func=sim_wosc_nltk.sentence_similarity)
def match_tat(all_quats, ntrain=None, outpath="simlists.tsv",
              find_nearest_qas=find_nearest_quats, sim_func=None,
              q_weight=1.0, max_count=6, min_sim_val=0, sort_most_sim=False):
    '''       Match Training And Test Quats.
    Compute similarities between all quats, training and test, score them against
    gold standard, and save the list of similarity lists to TSV for further work.
    Many default values are assumed, and the score is returned, not saved.'''
    size = len(all_quats)
    beg_time = time.time()
    if sim_func is not None:
        # import pdb; pdb.set_trace()
        find_nearest_qas = functools.partial(find_nearest_qas, sim_func=sim_func)
    sim_lists = find_ranked_qa_lists(all_quats, all_quats, find_nearest_qas, sim_func,
                                     q_weight=q_weight, max_count=max_count, min_sim_val=min_sim_val)
    score = score_most_sim_lists(all_quats, all_quats, sim_lists)
    save_most_sim_qa_lists_tsv(all_quats, all_quats, sim_lists, ntrain=ntrain,
                               outpath=outpath, min_sim_val=min_sim_val, sort_most_sim=sort_most_sim)
    seconds = time.time() - beg_time
    print("match_tat(size=%d, count=%d) took %.1f seconds; score %.4f\n" % (size, max_count,
                                                                            seconds, score))
    return score, sim_lists

# >>> scorem, mslm = sn.moby_tat() # Fri Oct 27 01:03:09 EDT 2017
# Finding all similarity lists (train 418, trial 418, nears 6) took 399.6 seconds
# match_tat(size=418, count=6) took 399.6 seconds; score 82.8708
def moby_tat(quats=None, nproto=200, ntrain=0, inpath="simsilver.tsv", outpath="moby_simlists.txt",
             find_qas=find_nearest_quats, sim_func=None, q_weight=1.0,
             max_count=6, min_sim_val=0, sort_most_sim=False, reload=False):
    '''Test match_tat on moby_dick or other specified quats.'''
    if quats is None or reload:
        quats = qa_csv.csv_read_qa(inpath)
    if ntrain > 0:
        used_quats = quats[0:ntrain] + quats[nproto:nproto+ntrain]
    else:
        used_quats = quats
    score, slists = match_tat(used_quats, ntrain=ntrain, outpath=outpath,
                              find_nearest_qas=find_qas, sim_func=sim_func,
                              q_weight=q_weight, max_count=max_count,
                              min_sim_val=min_sim_val, sort_most_sim=sort_most_sim)
    return score, slists, used_quats

###############################################################################
def match_ttt(train_quats, trial_quats, outpath="matched_ttt.tsv",
              find_nearest_qas=find_nearest_quats, sim_func=None,
              q_weight=1.0, max_count=6, min_sim_val=0, sort_most_sim=False):
    '''       Match Trial To Training Quats.
    Compute similarities using sim_func, score them against gold standard, and save
    the list of similarity lists to TSV for further work.  Many default values are
    assumed, and the score is returned, not saved.'''
    beg_time = time.time()
    # if sim_func is not None:
    #     # import pdb; pdb.set_trace()
    #     find_nearest_qas = functools.partial(find_nearest_qas, sim_func=sim_func)
    # import pdb; pdb.set_trace()
    sim_lists = find_ranked_qa_lists(train_quats, trial_quats, find_nearest_qas, sim_func,
                                     q_weight=q_weight, max_count=max_count, min_sim_val=min_sim_val)
    score = score_most_sim_lists(train_quats, trial_quats, sim_lists)
    save_most_sim_qa_lists_tsv(train_quats, trial_quats, sim_lists,
                               outpath=outpath, min_sim_val=min_sim_val, sort_most_sim=sort_most_sim)
    seconds = time.time() - beg_time
    print("match_ttt(n_train=%d, n_trial=%d, count=%d) took %.1f seconds; score %.4f" % (
        len(train_quats), len(trial_quats), max_count, seconds, score))
    return score, sim_lists


def moby_ttt(quats=None, nproto=200, ntrain=0, inpath="simsilver.tsv", outpath="moby_matched.txt",
             find_qas=find_nearest_quats, sim_func=None,
             q_weight=1.0, max_count=6, min_sim_val=0, sort_most_sim=False,
             reload=False, swap=False, profile=False):
    '''Test match_tat on moby_dick or other specified quats.'''
    if quats is None or reload:
        quats = qa_csv.csv_read_qa(inpath)
    if ntrain > 0:
        train_quats = quats[:ntrain]
        trial_quats = quats[nproto:nproto + ntrain]
    else:
        train_quats = quats[:nproto]
        trial_quats = quats[nproto:]
    if swap:
        train_quats, trial_quats = trial_quats, train_quats

    if profile:
        pro = cProfile.Profile()
        pro.enable()
    score, ms_lists = match_ttt(train_quats, trial_quats, outpath=outpath,
                                find_nearest_qas=find_qas, sim_func=sim_func,
                                q_weight=q_weight, max_count=max_count,
                                min_sim_val=min_sim_val, sort_most_sim=sort_most_sim)
    if profile:
        pro.disable()
        sio = io.StringIO()
        pst = pstats.Stats(pro, stream=sio).sort_stats('cumulative')
        pst.print_stats(30)
        print(sio.getvalue())
    return score, ms_lists, train_quats, trial_quats


# TODO: use kwargs for a bag of parameters.
def match_quats_to_model(model, trial_quats, outpath="matched_qtm.tsv", q_weight=1.0, max_count=6, min_sim_val=0):
    '''Compute similar Q&A's using a model, score them against a gold standard, and save
    the list of best matches to text file for further work.  The model must implement:
        rank_qa_lists(trial_quats, q_weight, max_count, min_sim_val)
        get_dev_quat_by_index(index)
        get_dev_quat_by_id(id)
        get_all_quats()
    assumed, and the score is returned, not saved.'''
    beg_time = time.time()
    sim_lists = model.rank_qa_lists(model, trial_quats, q_weight=q_weight, max_count=max_count, min_sim_val=min_sim_val)
    train_quats = model.get_all_quats()
    score = score_most_sim_lists(train_quats, trial_quats, sim_lists)
    save_most_sim_qa_lists_tsv(train_quats, trial_quats, sim_lists,
                               outpath=outpath, min_sim_val=min_sim_val)
    seconds = time.time() - beg_time
    print("match_ttt(n_train=%d, n_trial=%d, count=%d) took %.1f seconds; score %.4f\n" % (
        len(train_quats), len(trial_quats), max_count, seconds, score))
    return score, sim_lists


###############################################################################
# >>> quats = sc.csv_read_qa("simsilver.tsv", delimiter="\t")
# >>> score, msl = sn.match_tat(quats, "simlists_sort.tsv", min_sim_val=0.00)
# Finding all similarity lists (size=309, count=6) took 218.1 seconds
# match_tat(size=309, count=6) took 218.1 seconds; score 0.5941
###############################################################################
def test_fair():
    '''test similariy of QA pairs containing many stop words, including "fair"'''
    fair = qa_csv.csv_read_qa('fair.txt', delimiter='\t')
    score = match_tat(fair)
    print("match_tat(fair) => %.3f" % score)

if __name__ == '__main__':
    test_fair()
