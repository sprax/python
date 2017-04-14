
import editdistance


def edit_dist(seqA, seqB):
    dist = editdistance.eval(seqA, seqB)
    print("editdistance.eval({}, {}) = {}".format(seqA, seqB, dist))

edit_dist('banana', 'bandana')
edit_dist('banana', 'bahamas')
edit_dist(['one', 'two'], ['one', 'three'])
edit_dist(['one', 'two', 'three'], ['one', 'eleven', 'three'])
