import math


# helper function to check if a number is prime
def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True


# check all numbers until the nth prime number is found
def find_nth_prime_ver1(n):
    count = 0  # Count of prime numbers
    num = 2  # first prime number

    while count < n:
        if is_prime(num):
            count += 1
            if count == n:
                return num
        num += 1


# find the nth prime number using the sieve of eratosthenes method
def find_nth_prime_ver2(n):

    if n < 10:
        # when n is small, limit the range to a fixed number (for efficiency)
        limit = 30
    else:
        # prime number theorem: p_n ~ n * (ln(n) + ln(ln(n)))
        limit = int(n * (math.log(n) + math.log(math.log(n)))) + 1

    # eratosthenes sieve method
    sieve = [True] * limit
    sieve[0], sieve[1] = False, False

    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit, i):
                sieve[j] = False

    # list of prime numbers
    primes = [idx for idx, is_prime in enumerate(sieve) if is_prime]

    # may return None if n is too large
    return primes[n - 1] if len(primes) >= n else None


while True:
    try:
        n = int(input("What is the prime number at rank: "))
        if n <= 0:
            raise ValueError

        # prime_number_ver1 = find_nth_prime_ver1(n)
        # print(f"The prime number is {prime_number_ver1}")

        prime_number_ver2 = find_nth_prime_ver2(n)
        print(f"The prime number is {prime_number_ver2}")

    except ValueError:
        print("Rank should be a positive integer")
