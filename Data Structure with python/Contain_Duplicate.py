class Solution:
     from typing import List
     def Contain_Duplicate(self, nums:List[int])->bool:
          # sort the arrays
          nums.sort()
          # check the condition
          for i in range(1, len(nums)):
               if nums[i] == nums[i - 1]:
                    return True
          return False
     
def main()->bool:
     sol = Solution()
     nums = [1,2,3,1]
     # ans = sol.Contain_Duplicate(nums)
     if sol.Contain_Duplicate(nums) == True:
          print("Duplicate Found ")
     else:
          print("Duplicate not Found ")
          
if __name__ == "__main__":
     main()
          
     