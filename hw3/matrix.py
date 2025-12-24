import numpy as np

class Matrix:
    def __init__(self, data):
        if isinstance(data, np.ndarray):
            self.data = data.tolist()
        else:
            self.data = data

        self.rows = len(self.data)
        self.cols = len(self.data[0])

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimensions do not match for addition")
        
        result_data = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result_data)

    def __mul__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimensions do not match for element multiplication")
        
        result_data = [
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result_data)

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Dimensions do not match for matmul")
        
        result_data = [
            [sum(a * b for a, b in zip(row, col)) for col in zip(*other.data)]
            for row in self.data
        ]
        return Matrix(result_data)

    def __str__(self):
        return '\n'.join(['\t'.join(map(str, row)) for row in self.data])

def save_matrix(matrix, filename):
    with open(filename, 'w') as f:
        f.write(str(matrix))

if __name__ == "__main__":
    np.random.seed(0)
    
    array1 = np.random.randint(0, 10, (10, 10))
    array2 = np.random.randint(0, 10, (10, 10))
    
    m1 = Matrix(array1)
    m2 = Matrix(array2)
    
    result_add = m1 + m2
    result_mul = m1 * m2
    result_matmul = m1 @ m2
    
    save_matrix(result_add, "matrix+.txt")
    save_matrix(result_mul, "matrix*.txt")
    save_matrix(result_matmul, "matrix@.txt")
