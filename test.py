# import numpy as np
def moveZeroes(nums) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    maxloops = len(nums)
    i = 0
    while i<=maxloops:
        if nums[i]==0:
            # print(nums[i])
            nums.pop(i)
            nums.append(0)
        else:
            i += 1
            # print(i, nums)
    return nums

nums = [0,0,1]
res = moveZeroes(nums)
print(res)