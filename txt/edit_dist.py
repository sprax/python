
import editdistance


def edit_dist(seqA, seqB):
    dist = editdistance.eval(seqA, seqB)
    print("{:>5} = editdistance({}, {})".format(dist, seqA, seqB))

def main():
    '''Compute edit distances between strings and other sequences'''
    edit_dist('banana', 'bandana')
    edit_dist('banana', 'bahamas')
    edit_dist(['one', 'two'], ['one', 'three'])
    edit_dist(['one', 'two', 'three'], ['one', 'eleven', 'three'])

if __name__ == '__main__':
    main()
