from typing import List

class Solution:
    def Maximum_Count(self, num: List[int]) -> int:
        count = 0
        maxi = 0
        for i in range(len(num)):
            if num[i] == 1:
                count = 1 + count
                maxi = max(count, maxi)
            else:
                count = 0
        return maxi
    
    def main(self) -> None:
        num = [1, 2, 3, 1, 1, 1]
        maxi = self.Maximum_Count(num)
        print(maxi)
        
if __name__ == "__main__":
    sol = Solution()
    sol.main()
