from typing import List
class Solution:
     def sort_Colors(self, nums: List[int])->None:
          low = 0
          mid = 0
          height = len(nums) - 1
          while mid <= height:
               if nums[mid] == 0:
                    nums[low], nums[mid] = nums[mid], nums[low]
                    low += 1
                    mid += 1
               elif nums[mid] == 1:
                    mid += 1
                    
               else:
                    nums[mid], nums[height] = nums[height], nums[mid]
                    height -= 1
                    
def main():
     nums = [2, 0, 2, 1, 1, 0]
     sol = Solution()
     sol.sort_Colors(nums)
     print("The sort colors are : ")
     print(nums)
     
if __name__ == "__main__":
     main()
                    
          