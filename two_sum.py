class Solution(object):
    def twoSum(self, nums, target):
        d = dict()
        for indx, num in enumerate(nums):
            if num in d:
                return [d[num], indx]
            else:
                d[target - num] = indx
