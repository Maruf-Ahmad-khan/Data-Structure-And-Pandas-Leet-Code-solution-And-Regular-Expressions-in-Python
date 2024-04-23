from typing import List
def TwoSum(nums: List[int], target: int)->List[int]:
     mp = {}
     for i, num in  enumerate(nums):
          complement = target - num
          if complement in mp:
               return [mp[complement], i]
          mp[num] = i
     return [-1, -1]

if __name__ == "__main__":
     nums = [2,7,11,15]
     target = 9
     num = TwoSum(nums, target)
     print("The two sum of the given array is : \n", num)