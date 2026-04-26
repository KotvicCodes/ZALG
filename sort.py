#

#! SelectionSort()
def selection_sort(a):
    array = a[:]

    for i in range(len(array)):
        leastIndex = i

        for j in range(i + 1, len(array)):
            if array[j] < array[leastIndex]:
                leastIndex = j

        swap(array, i, leastIndex)
    return array


#! InsertionSort()
def insertion_sort(a:list):
    array = a[:]

    for i in range(1, len(array)):
        currentEl = array[i]

        for j in reversed(range(i)):
            if currentEl > array[j]:
                array.insert(j+1, currentEl)
                del(array[i+1])
                break

            elif j == 0:
                array.insert(0, currentEl)
                del(array[i+1])
    return array


#! BubbleSort()
def bubble_sort(a:list):
    array = a[:]

    for i in reversed(range(len(array))):
        for j in range(0, i):
            if array[j+1] < array[j]:
                swap(array, j, j+1)
    return array


#! ShakerSort()
def shaker_sort(a):
    array = a[:]

    i = 0
    step = 1
    highestIndex = len(array) - 1
    lowestIndex = 0
    swapped = False

    while True:
        if (step == 1 and i+1 > highestIndex) or (step == -1 and i-1 < lowestIndex):

            if not swapped: # check whether anything swapped during last go
                return array

            if highestIndex <= lowestIndex:
                return array
            swapped = False

            if step == 1:
                highestIndex = highestIndex - 1
            else: # step == -1
                lowestIndex = lowestIndex + 1
            step *= -1

        if step == 1 and array[i] > array[i+1]:
            swap(array, i, i+1)
            swapped = True
        elif step == -1 and array[i] < array[i-1]:
            swap(array, i, i-1)
            swapped = True
        i = i + step


#! MergeSort()
#* Main
def merge_sort(a):
    array = a[:]

    if len(array) <= 1:
        return array
    
    mid = len(array) // 2
    left = merge_sort(array[:mid])
    right = merge_sort(array[mid:])

    return merge(left, right)

#* Helper
def merge(left, right):
    array = []
    i = 0
    j = 0

    # compare elements
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            array.append(left[i])
            i += 1
        elif left[i] > right[j]:
            array.append(right[j])
            j += 1

    # add remaining elements
    array.extend(left[i:])
    array.extend(right[j:])

    return array


#! QuickSort()
def quick_sort(a):
    array = a[:]

    if len(array) <= 1:
        return array

    pivotIndex = len(array) // 2
    pivot = array[pivotIndex]

    i = 0
    j = len(array) - 1
    iLocked = False
    jLocked = False

    # compare elements with pivot
    while i <= j:
        if not iLocked:
            if array[i] >= pivot:
                iLocked = True
            else:
                i += 1

        if not jLocked:
            if array[j] <= pivot:
                jLocked = True
            else:
                j -= 1

        # swap
        if iLocked and jLocked and i <= j:
            swap(array, i, j)
            i += 1
            j -= 1
            iLocked = False
            jLocked = False

    left = quick_sort(array[:j + 1])
    right = quick_sort(array[i:])

    return left + array[j + 1:i] + right


#! Swap (2 Elements by index in a list)
def swap(a: list, i: int, j: int):
    """swaps a[i] and a[j] in a (list)"""
    firstEl = a[i]
    a[i] = a[j]
    a[j] = firstEl


#! Tests
def simple_test(sort_function, a):
    import random
    def single(a):
        r = sort_function(a)
        if r != sorted(a):
            print(f"{sort_function.__name__} error for: {a} with result: {r}")
            return False
        return True
    
    if not single(a):                       # original order
        return False
    if not single(sorted(a, reverse=True)): # descending order
        return False
    if not single(sorted(a)):               # ascending order
        return False
    for _ in range(10):
        shuffle_a = a[:]
        random.shuffle(shuffle_a)
        if not single(shuffle_a):           # random order
            return False
    return True
 
def sort_test():
    algorithms = [selection_sort, insertion_sort, bubble_sort, shaker_sort, merge_sort, quick_sort]
    a = [100, 2, 45, 13, 2, 90, 1, 3, 27]
    b = [100, 2, 45, 13, 2, 90, 1, 3, 27]
    c = [10]
    d = []
    for algorithm in algorithms:
        test_ok = simple_test(algorithm, a)
        assert a == b, f"{algorithm.__name__} modified original array!"
        if test_ok:
            test_ok = simple_test(algorithm, c)
        if test_ok:
            test_ok = simple_test(algorithm, d)
        if test_ok:
            print(f"Test on {algorithm.__name__} OK")
 
if __name__ == "__main__":
    sort_test()