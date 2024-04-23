from typing import List
class Solution:
     def Majority_Elements(self, nums : List[int])->int:
          count = 0
          ele = None
          for num in nums:
               if count == 0:
                    count = 1
                    ele = num
               
               elif num == ele:
                    count += 1
                    
               else:
                    count -= 1
                    
          count_1 = 0
          for num in nums:
               if num == ele:
                    count_1 += 1
                    
          if count_1 > (len(nums) // 2):
               return ele
          return - 1
     
def main()->int:
     nums = [3, 2, 3]
     sol = Solution()
     ans = sol.Majority_Elements(nums)
     print("The majority Elements are : \n")
     print(ans)
     
if __name__ == "__main__":
     main()