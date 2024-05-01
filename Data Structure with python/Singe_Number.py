class Solution:
     from typing import List
     def getSingleElemet(self, nums: List[int])->int:
          xor = 0
          for i in range(len(nums)):
               xor ^= nums[i]
          return xor
     def main(self)->None:
          nums = [3,1,1,2,2]
          ans = self.getSingleElemet(nums)
          print(f"The single element is found {ans}")
if __name__ == "__main__":
     sol = Solution()
     sol.main()