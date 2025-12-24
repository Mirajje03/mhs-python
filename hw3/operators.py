import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

class FileWriteMixin:
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))

class DisplayMixin:
    def __str__(self):
        return str(self.data)

class AccessorMixin:
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = np.asarray(value)

    @property
    def shape(self):
        return self._data.shape


class Matrix(NDArrayOperatorsMixin, FileWriteMixin, DisplayMixin, AccessorMixin):
    def __init__(self, data):
        self._data = np.asarray(data)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        inputs = tuple(x.data if isinstance(x, Matrix) else x for x in inputs)
        
        if out:
            kwargs['out'] = tuple(x.data if isinstance(x, Matrix) else x for x in out)
        
        result = getattr(ufunc, method)(*inputs, **kwargs)
        
        if method == 'at':
            return None
        
        if isinstance(result, np.ndarray):
            return Matrix(result)
        return result


if __name__ == "__main__":
    np.random.seed(0)
    
    array1 = np.random.randint(0, 10, (10, 10))
    array2 = np.random.randint(0, 10, (10, 10))
    
    m1 = Matrix(array1)
    m2 = Matrix(array2)
    
    result_add = m1 + m2
    result_mul = m1 * m2
    result_matmul = m1 @ m2
    
    result_add.save_to_file("matrix+.txt")
    result_mul.save_to_file("matrix*.txt")
    result_matmul.save_to_file("matrix@.txt")
