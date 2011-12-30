# -*- coding: utf-8 -*-

import copy
import operator

def main(n):
    if not type(n) is int:
        raise TypeError
    return reduce(operator.mul, xrange(1,n+1))

class MyLong(object):
    """ 10進数で4桁ごとに値を保持するオリジナル型

    >>> foo = MyLong('123456789')
    >>> print foo
    123456789
    >>> foo.value
    [1, 2345, 6789]
    >>> a = MyLong("10000")
    >>> a.value
    [1, 0]
    >>> a
    10000ML
    >>> a+a
    20000ML
    >>> b = MyLong("123456789")
    >>> a+b
    123466789ML
    >>> a*b
    1234567890000ML
    >>> MyLong.factorial(10)
    3628800ML
    >>> MyLong.factorial(20)
    2432902008176640000ML
    >>> MyLong.factorial(30).value
    [2, 6525, 2859, 8121, 9105, 8636, 3084, 8000, 0]
    """

    def __init__(self, value):
        """ 初期化
         * リスト: 4桁ずつの値リストとして扱う
         * 文字列: 数値文字列として扱う
         * 数値: 与えられた数値と同じ数として扱う
        """
        if isinstance(value, list) and self._is_valid(value):
            self.value = value
        elif isinstance(value, basestring):
            vals = []
            while value:
                if value:
                    vals.append(int(value[-4:]))
                    value = value[:-4]
            self.value = list(reversed(vals))
        elif isinstance(value, int) or isinstance(value, long):
            vals = []
            while value:
                value, val = value / 10000, value % 10000
                vals.append(val)
            self.value = list(reversed(vals))
        else:
            raise ValueError

    def _is_valid(self, val):
        """ self.value 値として妥当かチェック """
        if not isinstance(val, list):
            return False
        for v in val:
            if not isinstance(v, int):
                return False
            if v<0 or v>=10000:
                return False
        return True

    def __str__(self):
        return str(self.value[0]) + "".join(["%04d" % v for v in self.value[1:]])

    def __repr__(self):
        return "%sML" % str(self)

    def __len__(self):
        return len(self.value)

    def __add__(self, other):
        result = []
        nd = max(len(self), len(other))
        lhs = copy.copy(self.value)
        rhs = copy.copy(other.value)
        car = 0
        for i in xrange(nd):
            try:
                a = lhs.pop()
            except IndexError:
                a = 0
            try:
                b = rhs.pop()
            except IndexError:
                b = 0
            sum, car = (a+b+car) % 10000, (a+b+car) / 10000
            result.append(sum)
        if car:
            result.append(car)
        return MyLong(list(reversed(result)))

    def __mul__(self, other):
        lhs = copy.copy(self.value)
        rhs = copy.copy(other.value)

        # 筆算の各段の計算
        car = 0
        lines = []
        for i, a in enumerate(reversed(rhs)):
            lines.append([])
            for b in reversed(lhs):
                mul, car = (a*b+car) % 10000, (a*b+car) / 10000
                lines[i].append(mul)
            if car:
                lines[i].append(car)
            lines[i].reverse()
            # 次の計算のための桁揃え
            for ii in xrange(i):
                lines[i].append(0)

        # 集計（各段の和をとる）
        return reduce(operator.add, [MyLong(l) for l in lines])

    @classmethod
    def factorial(cls, n):
        """ 階乗計算 """
        return reduce(operator.mul, [cls(i) for i in xrange(1, n+1)])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # for i in range(1, 10):
    #     print main(i)
