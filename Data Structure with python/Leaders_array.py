# There is an integer array ‘a’ of size ‘n’.
# An element is called a Superior Element if it is greater than all the elements present to its right.
# You must return an array all Superior Elements in the array ‘a’.

# Note:

# The last element of the array is always a Superior Element. 


# Example

# Input: a = [1, 2, 3, 2], n = 4

# Output: 2 3
from typing import List
class Solution:
     def Superior_Element(self, arr: List[int])->int:
          # Create an empty list
          ans = []
          # Assign the lenght of the array
          n = len(arr) - 1
          # assign max_ele 
          max_ele = arr[n - 1]
          # add lenght of the array to the ans 
          ans.append(arr[n - 1])
          # Run a reverse for loop for comparision
          for i in range(n - 2, - 1, - 1):
               # Compare the last two elements
               if arr[i] > max_ele:
                    # add arr[i] current element to the empty list ans
                    ans.append(arr[i])
                    # update max_ele with arr[i] the current element
                    max_ele = arr[i]
          return ans
     
def main()->None:
     arr = [1, 2, 3, 2]
     sol = Solution()
     print(sol.Superior_Element(arr))
     
if __name__ == "__main__":
     main()