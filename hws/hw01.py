def caching_fibonacci():
    """
    create a cache and a fibonacci function that uses it (closure)
    :return: function fibonacci(n)
    """
    cache = dict()

    def fibonacci(n):
        """
        calculate the n-th Fibonacci number, reusing cached values instead of recalculating them
        :param n: position in the Fibonacci sequence
        :return: Fibonacci number
        """
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        elif cache.get(n):
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci
