# Fibonnaci sequence using DynamicProgramming

class Fibonnaci:
    def __init__(self):
        self._memory = { 0:0, 1:1 }

    def using_recursion(self, n):
        """ Using plain recursion, we try to calculate the
        fibonnaci number at the nth position. For smaller numbers like upto 30,
        the difference is negligible, however as the number becomes larger e.g 50
        this method starts to fail due to stack overflow errors
        """
        if n<=1:
            return n
        else:
            return self.using_recursion(n-1) + self.using_recursion(n-2)

    def using_memoization(self, n):
        """
        If we just start to save the results in memory and use recursion, the time complexity
        decreases from exponential to polynomial. Try something like 100 and you will see the
        results immediatly as opposed to just using plain recursion
        """
        if n in self._memory:
            return self._memory[n]
        else:
            result = self.using_memoization(n-1) + self.using_memoization(n-2)
            self._memory[n] = result
            return result

if __name__ == '__main__':
    fibonacci = Fibonnaci()
    result = fibonacci.using_memoization(10)
    print (result)
