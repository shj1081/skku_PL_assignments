import random


def RandomStats():

    # Generate 200 random numbers between 0 and 100
    random_numbers = [random.randint(0, 100) for _ in range(200)]

    # 5 categories: 1-20, 21-40, 41-60, 61-80, 81-100
    categories = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
    counts = [0, 0, 0, 0, 0]

    # Count the number of random numbers in each category
    for number in random_numbers:
        for category, (low, high) in enumerate(categories):
            if low <= number <= high:
                counts[category] += 1
                break

    # Print the random numbers (20*10) and the category counts
    for i in range(0, 200, 20):
        print(" ".join(f"{num:4}" for num in random_numbers[i : i + 20]))
    print("-" * 50)
    for i, (low, high) in enumerate(categories):
        print(f"{low:3} - {high:<3}: {'*' * counts[i]:<20}  {counts[i]:2}")


RandomStats()
