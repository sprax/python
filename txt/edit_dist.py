
''' try out editdistance '''
import editdistance

def edit_dist(seq_a, seq_b):
    '''try editdistance function'''
    dist = editdistance.eval(seq_a, seq_b)
    print("{:>5} = editdistance({}, {})".format(dist, seq_a, seq_b))

def main():
    '''Compute edit distances between strings and other sequences'''
    edit_dist('banana', 'bandana')
    edit_dist('banana', 'bahamas')
    edit_dist(['one', 'two'], ['one', 'three'])
    edit_dist(['one', 'two', 'three'], ['one', 'eleven', 'three'])

if __name__ == '__main__':
    main()
