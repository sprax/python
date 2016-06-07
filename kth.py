
def add_if_not_exists(possibles, newt):
    if newt not in possibles:
        possibles.append(newt)


def find_next(arr, possibles):
    min = 9999999
    selx = 0
    sely = 0
    for (x,y) in possibles:
        if(arr[x][y] < min):
            min = arr[x][y]
            selx = x
            sely = y
            possibles.remove((selx,sely))
        if selx+1 < len(arr):
            add_if_not_exists(possibles, (selx+1,sely))
        if sely+1 < len(arr):
            add_if_not_exists(possibles, (selx,sely+1))
    return (selx,sely)


def find_kth(arr, k):
    possibles = [(0,0)]
    for idx in range(0,k):
        print(idx)
        (x,y) = find_next(arr, possibles)
        print (x,y)
        print (arr[x][y])


if __name__ == '__main__':
    arr = [ [ 1, 2, 3 ],
            [ 4, 5, 6 ],
            [ 7, 8, 9 ] ]
    find_kth(arr, 4)
