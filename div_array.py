import random

def divide_into_random_subarrays(arr, n):
    if n <= 0:
        return []

    # If n is greater than the length of the array, return each element as its own subarray
    if n >= len(arr):
        return [[item] for item in arr]
    
    # Shuffle the array to ensure randomness
    random.shuffle(arr)
    
    # Generate n - 1 random split points (we need n partitions, so we need n-1 splits)
    split_points = sorted(random.sample(range(1, len(arr)), n - 1))
    
    # Use the split points to create the subarrays
    subarrays = [arr[i:j] for i, j in zip([0] + split_points, split_points + [len(arr)])]
    
    return subarrays


# print(divide_into_random_subarrays([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],4))