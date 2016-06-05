# MinHeap implementation

def Parent(i): return i//2
def Left(i):   return 2*i
def Right(i):  return 2*i+1


def Heapify(A, i, n):
        # print(i)
        l = Left(i)
        r = Right(i)
        if l <= n and A[l] > A[i]: 
            largest = l
        else: 
            largest = i
        if r <= n and A[r] > A[largest]:
            largest = r
        if largest != i:
            A[i], A[largest] = A[largest], A[i]
            Heapify(A, largest, n)
        # print(A)
        return A

def HeapLength(A): return len(A)-1
def BuildHeap(A): # build a heap A from an unsorted array
        n = HeapLength(A)
        for i in range(n//2, -1, -1):
            Heapify(A,i,n)

def HeapSort(A): # use a heap to build sorted array from the end
    BuildHeap(A)
    # print(A)
    HeapSize=HeapLength(A)
    for i in range(HeapSize,0,-1):
        A[0], A[i] = A[i], A[0] # largest element is a root of heap, put it at the end of array
        HeapSize=HeapSize-1 # shrink heap size by 1 to get next largest element
        Heapify(A,0,HeapSize)


def test_heap():
    L = [888, -1, 2, -2, 3, -3, 4, 4, -7, 11, -11, 9999]
    print("Python user MaxHeap: Starting from this array:", L)
    BuildHeap(L)
    print('Python user MaxHeap: Heapified (root is max):  {}'.format(L))
    HeapSort(L)
    print('Python user MaxHeap: HeapSorted (ascending):   %s' % L)

    print('Java; MaxHeapified (root (first item) is max):  9999 11 888 4 3 2 4 -2 -7 -1 -11 -3')
    print('Java: sortAscend: (order is min to max value):  -11 -7 -3 -2 -1 2 3 4 4 11 888 9999')
    


if __name__ == '__main__':
    test_heap()