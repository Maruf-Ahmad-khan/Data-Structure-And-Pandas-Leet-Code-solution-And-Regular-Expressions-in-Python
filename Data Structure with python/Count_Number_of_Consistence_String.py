# class Solution:
#      from typing import List
#      def countConsistentStrings(self, allowed: str, words: List[str]) -> int:
#           allowed = set(allowed)
#           count = 0
#           for word in words:
#                for letter in word:
#                     if letter not in allowed:
#                          count += 1
#                          break
#           return len(words) - count
     
# def main()->None:
#      words = ["ad","bd","aaab","baa","badab"]
#      allowed = "ab"
#      sol = Solution()
#      sol.countConsistentStrings(words, allowed)
#      print(sol.countConsistentStrings(words, allowed))
          
# if __name__ == "__main__":
#      main() 
from typing import List

class Solution:
    def countConsistentStrings(self, allowed: str, words: List[str]) -> int:
        allowed_set = set(allowed)
        count = 0
        for word in words:
            consistent = True
            for letter in word:
                if letter not in allowed_set:
                    consistent = False
                    break
            if consistent:
                count += 1
        return count

def main() -> None:
    words = ["ad", "bd", "aaab", "baa", "badab"]
    allowed = "ab"
    sol = Solution()
    result = sol.countConsistentStrings(allowed, words)
    print(result)

if __name__ == "__main__":
    main()
