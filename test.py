

class A:
    __value = 10

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        self.__value = val

    @classmethod
    def get_value(cls):
        return cls.value


class B(A):

    def __init__(self, valueb):
        super().__init__(self.value)
        self.value2 = valueb

    def show(self):
        return self.value


a = A(20)
print(a.value)
a.value = 25
b = B(30)
print(b.value)
a.value = 100
print(b.value)
