#Question 1
import numpy as np

# Accept 12 student marks
marks = []

print("Enter 12 student marks:")
for i in range(12):
    mark = int(input(f"Mark {i+1}: "))
    marks.append(mark)

# Convert list to NumPy array
arr = np.array(marks)

# Display highest, lowest, average
print("\nHighest Mark :", np.max(arr))
print("Lowest Mark  :", np.min(arr))
print("Average Mark :", np.mean(arr))

# Reshape into 3 x 4 matrix
matrix = arr.reshape(3, 4)

print("\nReshaped Matrix (3 x 4):")
print(matrix)

# Row-wise sum
print("\nRow-wise Sum:")
print(np.sum(matrix, axis=1))

# Column-wise sum
print("\nColumn-wise Sum:")
print(np.sum(matrix, axis=0))

# QUESTION 2
class Node:
    def __init__(self, emp_id):
        self.emp_id = emp_id
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # Insert Employee
    def insert(self, emp_id):
        new_node = Node(emp_id)

        if self.head is None:
            self.head = new_node
            return

        temp = self.head
        while temp.next:
            temp = temp.next

        temp.next = new_node

    # Display Employees
    def display(self):
        if self.head is None:
            print("List is Empty")
            return

        temp = self.head
        while temp:
            print(temp.emp_id, end=" -> ")
            temp = temp.next
        print("None")

    # Search Employee
    def search(self, emp_id):
        temp = self.head

        while temp:
            if temp.emp_id == emp_id:
                return True
            temp = temp.next

        return False

    # Delete Employee
    def delete(self, emp_id):
        temp = self.head

        if temp and temp.emp_id == emp_id:
            self.head = temp.next
            return

        prev = None

        while temp and temp.emp_id != emp_id:
            prev = temp
            temp = temp.next

        if temp is None:
            print("Employee Not Found")
            return

        prev.next = temp.next

    # Count Employees
    def count(self):
        count = 0
        temp = self.head

        while temp:
            count += 1
            temp = temp.next

        return count

    # Reverse Linked List
    def reverse(self):
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev


# Main Program
ll = LinkedList()

while True:
    print("\n===== Employee Management =====")
    print("1. Insert")
    print("2. Display")
    print("3. Search")
    print("4. Delete")
    print("5. Count")
    print("6. Reverse")
    print("7. Exit")

    choice = int(input("Enter Choice: "))

    if choice == 1:
        emp_id = int(input("Enter Employee ID: "))
        ll.insert(emp_id)

    elif choice == 2:
        ll.display()

    elif choice == 3:
        emp_id = int(input("Enter Employee ID to Search: "))
        if ll.search(emp_id):
            print("Employee Found")
        else:
            print("Employee Not Found")

    elif choice == 4:
        emp_id = int(input("Enter Employee ID to Delete: "))
        ll.delete(emp_id)

    elif choice == 5:
        print("Total Employees:", ll.count())

    elif choice == 6:
        ll.reverse()
        print("Linked List Reversed")

    elif choice == 7:
        print("Exiting...")
        break

    else:
        print("Invalid Choice")
