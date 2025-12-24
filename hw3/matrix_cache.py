import numpy as np

class HashMixin:
    def __hash__(self):
        return int(np.sum(self.data))

class Matrix(HashMixin):
    _matmul_cache = {}

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
        key = (hash(self), hash(other))
        if key in self._matmul_cache:
            return self._matmul_cache[key]

        if self.cols != other.rows:
            raise ValueError("Dimensions do not match for matmul")
        
        result_data = [
            [sum(a * b for a, b in zip(row, col)) for col in zip(*other.data)]
            for row in self.data
        ]
        result = Matrix(result_data)
        self._matmul_cache[key] = result
        return result

    def __str__(self):
        return '\n'.join(['\t'.join(map(str, row)) for row in self.data])

def save_matrix(matrix, filename):
    with open(filename, 'w') as f:
        f.write(str(matrix))

if __name__ == "__main__":
    A = Matrix([[1, 2], [3, 4]]) 
    C = Matrix([[2, 1], [4, 3]]) 
    
    B = Matrix([[5, 0], [0, 5]])
    D = B 

    AB = A @ B
    
    true_matmul_data = [[sum(a * b for a, b in zip(row, col)) for col in zip(*D.data)] for row in C.data]
    CD = Matrix(true_matmul_data)

    save_matrix(A, "A.txt")
    save_matrix(B, "B.txt")
    save_matrix(C, "C.txt")
    save_matrix(D, "D.txt")
    save_matrix(AB, "AB.txt")
    save_matrix(CD, "CD.txt")
    
    with open("hash.txt", "w") as f:
        f.write(str(hash(CD)))
