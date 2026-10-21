from hws import caching_fibonacci, sum_profit, generator_numbers

if __name__ == '__main__':
    fib = caching_fibonacci()

    print(fib(10))
    print(fib(15))

    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")
