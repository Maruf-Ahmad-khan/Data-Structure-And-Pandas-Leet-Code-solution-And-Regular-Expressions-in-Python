class Solution:
     from typing import List
     def Linear_Search(self, nums: List[int], key: int)->int:
          for i in range(len(nums)):
               if nums[i] == key:
                    return i
          return - 1
          
     def main(self)->None:
          nums = [1,2,3,4,5]
          key = 3
          ans = self.Linear_Search(nums, key)
          print("Searched key is : ", ans)
          
if __name__ == "__main__":
     sol = Solution()
     sol.main()