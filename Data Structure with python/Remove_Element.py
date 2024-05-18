# Input: nums = [3,2,2,3], val = 3
# Output: 2, nums = [2,2,_,_]
# Explanation: Your function should return k = 2, with the first two elements of nums being 2.
# It does not matter what you leave beyond the returned k (hence they are underscores).

class Solution:
     from typing import List
     def RemoveElement(self, nums:List[int], val:int)->int:
          # count for keep tracking
          count = 0
          # loop to iterate indexes of nums List
          for i in range(len(nums)):
               # check the condition if the currecnt element is not equal to val
               if nums[i] != val:
                    # update count with current element
                    nums[count] = nums[i]
                    count += 1
          return count
     
def main()->int:
     nums = [3,2,2,3]
     val = 3
     sol = Solution()
     ans = sol.RemoveElement(nums, val)
     print("element is : \n", ans)
     
if __name__ == "__main__":
     main()
                    