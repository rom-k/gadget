#!/usr/bin/python
# -*- coding: utf-8 -*-


class NumAndFormula(object):
    def __init__(self, num, formula=None):
        if formula is None:
            formula = str(num)
        self.n = num
        self.f = formula

    def __add__(self, other):
        return NumAndFormula(
            self.n + other.n,
            "(" + self.f + " + " + other.f + ")")

    def __sub__(self, other):
        return NumAndFormula(
            self.n - other.n,
            "(" + self.f + " - " + other.f + ")")

    def __mul__(self, other):
        return NumAndFormula(
            self.n * other.n,
            "(" + self.f + " * " + other.f + ")")

    def __div__(self, other):
        if (other.n == 0):
            raise Exception()
        return NumAndFormula(
            self.n / other.n,
            "(" + self.f + " / " + other.f + ")")


class Make10(object):
    def __init__(self, nums):
        self.nums = [x * 1.0 for x in nums]
        self.all_numforms = None

    def ShowGet10(self):
        if self.CanGet10():
            formulas_for_10 = [x.f for x in self.all_numforms if x.n == 10]
            formulas_for_10 = sorted(list(set(formulas_for_10)))
            print "Yes, you can get 10 from ", self.nums
            for formula in formulas_for_10:
                print "\t" + formula
        else:
            print "No, you can not get 10 from ", self.nums

    def CanGet10(self):
        return 10 in self.GetAll()

    def GetAll(self):
        self.CalcAll()
        return [x.n for x in self.all_numforms]

    def CalcAll(self):
        if self.all_numforms is None:
            numforms = [NumAndFormula(x) for x in self.nums]
            self.all_numforms = self.__calc(numforms)

    def __calc(self, numforms):
        if len(numforms) == 1:
            return numforms

        results = []
        for i, numform_i in enumerate(numforms):
            for j, numform_j in enumerate(numforms):
                if (i == j):
                    continue

                next_numforms = numforms[:]
                next_numforms.pop(i)
                next_numforms.pop(j if j < i else j - 1)

                new_numforms = [numform_i + numform_j,
                                numform_i - numform_j,
                                numform_i * numform_j]
                if (numform_j.n != 0):
                    new_numforms.append(numform_i / numform_j)

                for new_numform in new_numforms:
                    next_numforms.append(new_numform)
                    results.extend(self.__calc(next_numforms))
                    next_numforms.pop()

        return results


if __name__ == '__main__':
    import sys

    nums = [float(x) for x in sys.argv if x.isdigit()]
    if len(nums) == 0:
        nums = [1, 1, 5, 8]

    Make10(nums).ShowGet10()
