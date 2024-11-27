def recursive_sum(n):
    if n <= 1:
        return 0
    return (n - 1) + recursive_sum(n - 1)


# when n is too large, recursive function cause error
def big_integers_sum(n):
    return (n * (n - 1)) // 2


def main():
    while True:
        user_input = input("Insert a number n or 'Exit': ")
        if user_input.lower() == "exit":
            print("Bye!")
            break
        try:
            n = int(user_input)
            if n < 0:
                raise ValueError

            if n < 500:  # recursive function for small numbers
                result = recursive_sum(n)
            else:  # big_integers_sum function for large numbers
                result = big_integers_sum(n)

            print(f"The sum of integers before {n} is: {result}\n")
        except ValueError:
            print("Invalid input. Please enter integer (>= 0) or 'Exit' to quit.\n")


main()
