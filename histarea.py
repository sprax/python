# Python script to calculate the area of "water"
# that would be trapped by a histogram. 

# default values:
defProgramName  = "histarea"
INT_MIN = -2147483648


def histarea(histogram, length):
    '''Calculates the area of "fluid" that would be trapped in poured onto
    a histogram from above.'''

    area, height = 0, 0
    if (length > 2):
        maxFromLeft = []
        maxHeight = INT_MIN;
        # Don't skip the last entry.
        for j in range(length):
            height = histogram[j]
            if (maxHeight < height):
                maxHeight = height
            maxFromLeft.append(maxHeight)
        maxHeight = INT_MIN;
        for j in range(length-1, 0, -1):   # Do skip the first entry.
            height = histogram[j]
            if (maxHeight < height):
                maxHeight = height
            if (maxHeight > maxFromLeft[j]):
                area += maxFromLeft[j] - height;
            else:
                area += maxHeight - height;
    return area;

def main_histarea():
    # programName  = argv[0] ? argv[0] : defProgramName;

    histogram = [-1, 2, 32, -4, 4, 44, 2, 38, 0]
    length = len(histogram)
    area = histarea(histogram, length);

    print( "Area from histogram:", area );
    for j in range(length):
        print( histogram[j]),
    print();

if __name__ == '__main__':
    main_histarea()

