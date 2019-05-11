# credit to https://github.com/quillyBeans/VisualConvexHull for the convexhull code, which is under the MIT license
# This uses the O(nlogn) algorithm discussed in class by sorting by x-coordinate to create an x-monotone chain
# and then creating the upper and lower hulls.
# note that, if we assumed the input was the simple polygon in counterclockwise or clockwise direction, we could
# just run Melkman's algorithm in O(n) time. But it's better to do this for robustness bc it will still work if
# someone inputs a self-intersecting sequence/chain of points.
def convexHull(pointsList):
    lowerHull = []
    upperHull = []
    if len(pointsList) <= 0:
        return pointsList
    #have to sort list first
    pointsList.sort(key=lambda tup: tup[0])
    n = len(pointsList)
    j = 0
    #then calculate lower hull
    for idx in range(n):
        #checking for counter clockwise-ness
        while len(lowerHull) >= 2 and \
                cross(lowerHull[j - 2], lowerHull[j - 1], pointsList[idx]) <= 0:
            lowerHull.pop()
            j -= 1
        lowerHull.append(pointsList[idx])
        j += 1

    j = 0
    idx = n - 1
    #then upper hull from reverse of pointsList
    for i in range(n):
        while len(upperHull) >= 2 and \
                cross(upperHull[j - 2], upperHull[j - 1], pointsList[idx]) <= 0:
            upperHull.pop()
            j -= 1
        upperHull.append(pointsList[idx])
        idx -= 1
        j += 1

    #pop lowerhull b/c it contains the 1st point then combine with upper and return
    lowerHull.pop()
    return lowerHull + upperHull

def cross(O, A, B):
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])