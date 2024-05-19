class Solution:
     from typing import List
     def Rotate_matrix(self, matrix: List[List[int]])->None:
          n = len(matrix)
          for i in range(n):
               for j in range(i + 1, n):
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
          for i in matrix:
               i.reverse()
               
matrix = [[1,2,3],[4,5,6],[7,8,9]]
sol = Solution()
ans = sol.Rotate_matrix(matrix)
print('After Rotating the matrix is : \n')
for row in matrix:
     print(row)
          