# # Rearrange Array Elements by Sign
# Input: nums = [3,1,-2,-5,2,-4]
# Output: [3,-2,1,-5,2,-4]
from typing import List
class Solution:
     def Rearrange_array_element(self, nums: List[int])->int:
          n = len(nums)
          posInd , negInd = 0, 1
          ans = [0] * n
          for num in nums:
               if num < 0:
                    ans[negInd] = num
                    negInd = 2 + negInd
               else:
                    ans[posInd] = num
                    posInd = 2 + posInd
          return ans

def main()->int:
     sol = Solution()
     nums = [3,1,-2,-5,2,-4]
     ans = sol.Rearrange_array_element(nums)
     print("The List after rearranging : \n")
     print(ans)
     
if __name__ == "__main__":
     main()
     