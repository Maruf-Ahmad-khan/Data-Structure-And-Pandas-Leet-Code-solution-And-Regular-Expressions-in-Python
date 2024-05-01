class Solution:
     from typing import List
     def B_Search(self, nums:List[int], start:int, end:int, key:int)->int:
          if start > end:
               return -1
          mid = (start + end) // 2
          if nums[mid] == key:
               return mid
          if nums[mid] < key:
               start = mid + 1
               return self.B_Search(nums, start, end, key)
          else:
               end = mid - 1
               return self.B_Search(nums, start, end, key)
          
sol = Solution()
nums = [10,20,30,40,50]
start = 0
end = len(nums) - 1
key = 40
ans = sol.B_Search(nums, start, end, key)
print(f"The key is found at : {ans}")