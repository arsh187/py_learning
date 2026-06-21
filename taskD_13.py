Question 1: Reshape the Matrix

# Reshape the Matrix

matrix = [
    [1, 2],
    [3, 4]
]

r = 1
c = 4

m = len(matrix)
n = len(matrix[0])

# Check if reshape is possible
if m * n != r * c:
    print("Reshape not possible. Original Matrix:")
    for row in matrix:
        print(*row)
else:
    # Flatten the matrix
    flat = []
    for row in matrix:
        for num in row:
            flat.append(num)

    # Create reshaped matrix
    reshaped = []
    index = 0

    for i in range(r):
        new_row = []
        for j in range(c):
            new_row.append(flat[index])
            index += 1
        reshaped.append(new_row)

    print("Reshaped Matrix:")
    for row in reshaped:
        print(*row)

#Question 2: Diamond Pattern

# Diamond Pattern

n = int(input("Enter N: "))

# Upper Half
for i in range(1, n + 1):
    spaces = n - i
    stars = 2 * i - 1

    print(" " * spaces + "*" * stars)

# Lower Half
for i in range(n - 1, 0, -1):
    spaces = n - i
    stars = 2 * i - 1

    print(" " * spaces + "*" * stars)
