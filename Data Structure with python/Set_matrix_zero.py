class Solution:
    from typing import List

    def zero_matrix(self, matrix: List[List[int]]) -> None:
        row = len(matrix)
        col = len(matrix[0])
        zero_rows = set()
        zero_cols = set()

        # First pass to find all rows and columns that need to be zeroed
        for i in range(row):
            for j in range(col):
                if matrix[i][j] == 0:
                    zero_rows.add(i)
                    zero_cols.add(j)

        # Second pass to set the appropriate rows and columns to zero
        for i in range(row):
            for j in range(col):
                if i in zero_rows or j in zero_cols:
                    matrix[i][j] = 0

# Example matrix
matrix = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]

# Create an instance of the Solution class
sol = Solution()

# Apply the zero_matrix method
sol.zero_matrix(matrix)

# Print the modified matrix
for row in matrix:
    print(row)
