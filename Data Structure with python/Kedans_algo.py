from typing import List
class Solution:
     def Sum(self, nums : List[int])-> int:
          maxi = nums[0]
          sum = 0
          for i in range(len(nums)):
               sum = sum + nums[i]
               maxi = max(sum, maxi)
               if sum < 0:
                    sum = 0
          return maxi
     
def main()->int:
     nums = [-2,1,-3,4,-1,2,1,-5,4]
     sol = Solution()
     sol.Sum(nums)
     print("The given sum is : ")
     print(sol.Sum(nums))
          
if __name__ == "__main__":
     main()