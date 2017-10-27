#!/usr/bin/env python3
'''Text similarity (between words, phrases, or short sentences) using NLTK'''

import heapq
import string
import time
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

def cosine_sim_quanda(one_quanda, other_quanda, get_question=second, get_answer=third, q_weight=0.5, vectorizer=VECTORIZER):
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

def unit_clip(value):
    ''' Clip value to [0, 1] '''
    if value > 1:
        return 1
    if value < 0:
        return 0
    return value

def unit_clip_verbose(value):
    ''' Verbosely clip value to [0, 1] '''
    if value > 1:
        print("unit_clip_verbose: {} -> 1".format(value))
        return 1
    if value < 0:
        print("unit_clip_verbose: {} -> 0".format(value))
        return 0
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


def nearest_known(saved_texts, input_text, similarity_func, threshold):
    '''find text in saved_texts most similar to input_text, if similarity >= threshold'''
    idx, sim = nearest_other_idx(saved_texts, input_text, similarity_func, threshold)
    if idx < 0:
        print("No saved text found more similar than %f" % threshold)
    else:
        print("Nearest at %f (%d) %s" % (sim, idx, saved_texts[idx]))

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
def similarity_dict(train_quats, question, answer=None, excludes=None, q_weight=1.0, sim_func=cosine_sim_txt,
                    min_sim_val=0):
    '''
    Returns a dict mapping train_quats' indexes to their similarity with this_text,
        provide their similarity value >= min_sim_val
        similarity_func:    function returning the similariy between two texts (as in sentences)
        min_sim_val:        similarity threshold
    '''
    if excludes is None:
        excludes = []
    sim_dict = {}
    for idx, quat in enumerate(train_quats):
        if idx in excludes:
            continue
        try:
            # print("SIM_WEIGHTED_QAS(", question, answer, quat[1], quat[2], q_weight, sim_func, ")")
            # # pdb.set_trace()
            sim = sim_weighted_qas(question, answer, quat.question, quat.answer, q_weight=q_weight, sim_func=sim_func)
            if  sim >= min_sim_val:
                if sim > 1:
                    sim = 1
                sim_dict[idx] = sim
        except ValueError as ex:
            print("Continuing past error at idx: {}  ({})  ({})".format(idx, ex, all_quats[idx]))
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

def find_nearest_quats(train_quats, question, answer=None, excludes=None, q_weight=1.0, sim_func=cosine_sim_txt, max_count=5, min_sim_val=0, max_sim_val=1):
    '''
    Find the N most similar texts to this_text and return a list of (index, similarity) pairs in
    descending order of similarity.
        train_quats:        The training sentences or question-answer-tuples or whatever is to be compared.
        question:           a plain text question
        answer:             a plain text answer (default None)
        excludes:           list of IDs to exclude from the comparison; e.g. this_text.id if excluding self comparison.
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
        max_count           maximum size of returned dict
        max_sim_val:        the initial value of max, or the maximum similariy found so far.
    '''
    assert q_weight >= 0.0
    sim_dict = similarity_dict(train_quats, question, answer, excludes, q_weight=q_weight, sim_func=sim_func, min_sim_val=min_sim_val)
    return nlargest_items_by_value(sim_dict, max_count)

def find_nearest_qas_lists(train_quats, trial_quats, find_nearest_qas=find_nearest_quats, q_weight=1.0, max_count=5,
                           min_sim_val=0.0, id_eq_index=False):
    '''
    For each question-and-answer tuple in quats, find a list of indexes of the most similar Q and A's.
    Returns list of lists of items as in: [[(index, similariy), ...], ...]
        similarity_func:    function returning the similariy between two texts (as in sentences)
        vocab:              the set of all known words
    '''
    assert q_weight >= 0.0
    nearests = len(trial_quats)*[None]
    for idx, trial_quat in enumerate(trial_quats):
        # consistency check:
        idn = trial_quat.id
        assert isinstance(idn, int)
        if id_eq_index:
            # print("DBG LMSTL: ", trial_quat)
            if idx > 0 and idx + 100 != idn:
                print("ERROR:", (idx + 100), "!=", trial_quat.id, "at", trial_quat)
                raise IndexError
        nearests[idx] = find_nearest_qas(train_quats, trial_quat.question, trial_quat.answer, [idx], q_weight=q_weight,
                                         max_count=max_count, min_sim_val=min_sim_val)
    return nearests

def find_ranked_qa_lists_inclusive(train_quats, trial_quats, find_nearest_qas=find_nearest_quats, q_weight=1.0, sim_func=cosine_sim_txt, max_count=5,
                                   min_sim_val=0.0):
    return [find_nearest_qas(train_quats, trial_quat, None, q_weight, sim_func,
                             max_count, min_sim_val) for trial_quat in trial_quats]

def find_ranked_qa_lists(train_quats, trial_quats, find_nearest_qas=find_nearest_quats, q_weight=1.0, max_count=6, min_sim_val=1.0/6):
    '''
    Returns list of most similar lists.  For each object in quats, compute the similarity with all
    (other) objects in quats, and save at most max_count indices and similarity measures in descending
    order of similarity, where similiary >= min_sim_val.  If exclude_self is false, compare each object
    with itself as well as the others (sanity check)
    '''
    ranked_lists = None
    beg_time = time.time()
    # import pdb; pdb.set_trace()
    ranked_lists = find_nearest_qas_lists(train_quats, trial_quats, find_nearest_qas, q_weight, max_count, min_sim_val, id_eq_index=False)
    seconds = time.time() - beg_time
    print("Finding all similarity lists (train %d, trial %d, nears %d) took %.1f seconds" % (len(train_quats), len(trial_quats), max_count, seconds))
    return ranked_lists

def show_most_sim_texts_list(texts, sim_lists=None):
    '''print already-found similarity lists'''
    if sim_lists is None:
        sim_lists = find_ranked_qa_lists(train_quats, trial_quats, find_nearest_qas=find_nearest_quats)     # use defaults
    for idx, txt in enumerate(texts):
        most_sim_list = sim_lists[idx]
        print("  %3d.  %s" % (idx, txt))
        for oix, sim in most_sim_list:
            print("        %3d   %.5f   %s" % (oix, sim, texts[oix]))
        print()
    return sim_lists

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
        if len(trial_quat) > 3 and trial_quat[3]:
            try:
                gold = int(trial_quat[3])
                assert isinstance(gold, int)
            except ValueError as ex:
                print("ERROR on: ", trial_quat, ex)
                continue
            gold_scored += 1
            # ms = sim_list[0]
            # msi = ms[0]
            # sim = ms[1]
            # print("DBG_F: Q_%d <==> Q_%d (%s <==> %s) first, %.4f (%s : %s)" % (int(qax[0]), msi, qax[1],
            #       trial_quats[msi][1], sim, remove_stop_words(normalize(qax[1])), remove_stop_words(normalize(trial_quats[msi][1]))))
            for idx, item in enumerate(sim_list):
                # print("DC: %d  item(%d, %f)" % (idx, item[0], item[1]))
                train_quat = train_quats[item[0]]
                if gold == train_quat[0]:      # compare idn to idn (not idx)
                    # print("DBG_G: Q_%d <==> Q_%d (%s <==> %s) at %d, %.4f (%s : %s)\n" % (int(qax[0]), item[0], qax[1], quats[item[0]][1],
                    #       idx, item[1], remove_stop_words(normalize(qax[1])), remove_stop_words(normalize(quats[item[0]][1]))))
                    dist_counts[idx] += 1
                    break
    # save the number of gold standard matches as the last count in the list
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
        print("DBG SDC LOOP:", idx, dist_counts[idx])
        score += weight * dist_counts[idx]
    # print("DBG_SDC: score(%.4f) / %d == %f" % (score, gold_scored, score/gold_scored))
    return 100 * score / gold_scored

def score_most_sim_lists(train_quats, trial_quats, sim_lists, weights=None):
    '''Sum up gold-standard accuracy score'''
    if weights is None:
        weights = [1.0, 0.8, 0.6, 0.4, 0.2, 0.1]
    dist_counts = distance_counts(train_quats, trial_quats, sim_lists, len(weights))
    return score_distance_counts(dist_counts, weights)

def save_most_sim_qa_lists_tsv(train_quats, trial_quats, path, sim_lists, min_sim_val=0, sort_most_sim=True):
    '''Save ranked most-similar lists to TSV file'''
    isorted = None
    sim_oix = []
    if sort_most_sim:
        # TODO: replace with zip
        for idx, sim_list in enumerate(sim_lists):
            # print("QUAT:", idx, quats[idx])
            # print("SIM_LIST:", sim_list)
            len_lst = len(sim_list)
            max_oix = sim_list[0][0] if len_lst > 0 else -1
            max_sim = sim_list[0][1] if len_lst > 1 else 0
            sum_sim = sum([y[1] for y in sim_list])
            sim_oix.append((max_sim, sum_sim, -idx, -max_oix))
        # TODO: sorted with 2 keys?? FIXME: should sort on all keys!!
        isorted = [-tup[2] for tup in sorted(sim_oix, reverse=True)]
    else:
        isorted = range(len(trial_quats))
    # print("ISORTED ", len(isorted), ": ", isorted)

    out = text_fio.open_out_file(path)
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
                except Exception as ex:
                    print("ERROR AT MIX {}: idx {}  qax {},  err: {}\n".format(mix, idx, qax, ex))

                    pass    # raise IndexError
        # if sort_most_sim:
        #     print("TUP {:3}:\t {}".format(mix, sim_oix[idx]))
        print(file=out)
        mix += 1
    if path != '-':
        out.close()

# VECTORIZER (default):                  (size=201, count=6) took 96.1 seconds; score 0.8583
# VECT_MOST_STOPS (DEFAULT-QUERY_WORDS): (size=201, count=6) took 96.3 seconds; score 0.6635
# TODO: Why do the query words make the score worse?
# TEST: >>> sim_score_save(fair, sim_func=sim_wosc_nltk.sentence_similarity)
def sim_score_save(all_quats, ntrain=200, outpath="simlists.tsv", find_nearest_qas=find_nearest_quats,
                   q_weight=1.0, max_count=6, min_sim_val=0.15, sort_most_sim=False):
    '''Compute similarities using sim_func, score them against gold standard, and save
    the list of similarity lists to TSV for further work.  Many default values are
    assumed, and the score is returned, not saved.'''
    size = len(all_quats)
    beg_time = time.time()
    sim_lists = find_ranked_qa_lists(all_quats, all_quats, find_nearest_qas, q_weight=q_weight,
                                     max_count=max_count, min_sim_val=min_sim_val)
    score = score_most_sim_lists(all_quats, all_quats, sim_lists)
    save_most_sim_qa_lists_tsv(all_quats, all_quats, path, sim_lists, min_sim_val=min_sim_val, sort_most_sim=sort_most_sim)
    seconds = time.time() - beg_time
    print("sim_score_save(size=%d, count=%d) took %.1f seconds; score %.4f" % (size, max_count,
                                                                               seconds, score))
    return score, sim_lists

def match_trials_to_trained(train_quats, trial_quats, outpath="matched_ttt.tsv", find_nearest_qas=find_nearest_quats,
                            q_weight=1.0, max_count=6, min_sim_val=0, sort_most_sim=False):
    '''Compute similarities using sim_func, score them against gold standard, and save
    the list of similarity lists to TSV for further work.  Many default values are
    assumed, and the score is returned, not saved.'''
    beg_time = time.time()
    sim_lists = find_ranked_qa_lists(train_quats, trial_quats, find_nearest_qas, q_weight=q_weight,
                                     max_count=max_count, min_sim_val=min_sim_val)
    score = score_most_sim_lists(train_quats, trial_quats, sim_lists)
    save_most_sim_qa_lists_tsv(train_quats, trial_quats, path, sim_lists, min_sim_val=min_sim_val, sort_most_sim=sort_most_sim)
    seconds = time.time() - beg_time
    print("match_trials_to_trained(n_train=%d, n_trial=%d, count=%d) took %.1f seconds; score %.4f" % (
        len(train_quats), len(trial_quats), max_count, seconds, score))
    return score, sim_lists


# TODO: use kwargs for a bag of parameters.
def match_quats_to_model(model, trial_quats, outpath="matched_qtm.tsv", q_weight=1.0, max_count=6, min_sim_val=0):
    '''Compute similar Q&A's using a model, score them against a gold standard, and save
    the list of best matches to text file for further work.  The model object must implement:
        find_nearest_quats(quat, q_weight, max_count)
        get_dev_quat(index)
        get_all_quats()
    assumed, and the score is returned, not saved.'''
    beg_time = time.time()
    sim_lists = find_ranked_qa_lists(model, trial_quats, q_weight=q_weight, max_count=max_count, min_sim_val=min_sim_val)
    train_quats = model.get_all_quats()
    score = score_most_sim_lists(train_quats, trial_quats, sim_lists)
    save_most_sim_qa_lists_tsv(train_quats, trial_quats, path, sim_lists, min_sim_val=min_sim_val, sort_most_sim=sort_most_sim)
    seconds = time.time() - beg_time
    print("match_trials_to_trained(n_train=%d, n_trial=%d, count=%d) took %.1f seconds; score %.4f" % (
        len(train_quats), len(trial_quats), max_count, seconds, score))
    return score, sim_lists


###############################################################################
# >>> quats = sc.csv_read_qa("simsilver.tsv", delimiter="\t")
# >>> score, msl = sn.sim_score_save(quats, "simlists_sort.tsv", min_sim_val=0.00)
# Finding all similarity lists (size=309, count=6) took 218.1 seconds
# sim_score_save(size=309, count=6) took 218.1 seconds; score 0.5941
###############################################################################
def test_fair():
    '''test similariy of QA pairs containing many stop words, including "fair"'''
    fair = qa_csv.csv_read_qa('fair.txt', delimiter='\t')
    score = sim_score_save(fair)
    print("sim_score_save(fair) => %.3f" % score)

if __name__ == '__main__':
    test_fair()
