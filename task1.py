#Question 1 

from flask import Flask, render_template_string
import matplotlib.pyplot as plt

app = Flask(__name__)

students = ["Arun", "Bala", "Charan", "Divya", "Elan"]
marks = [85, 72, 90, 65, 78]
attendance = [95, 88, 92, 80, 85]

# 1. Line Graph
plt.figure(figsize=(6,4))
plt.plot(students, marks, marker='o', label="Marks")
plt.title("Student Marks Analysis")
plt.xlabel("Students")
plt.ylabel("Marks")
plt.legend()
plt.grid(True)
plt.savefig("static/line_graph.png")
plt.close()

# 2. Scatter Plot
plt.figure(figsize=(6,4))
plt.scatter(students, attendance, label="Attendance")
plt.title("Student Attendance")
plt.xlabel("Students")
plt.ylabel("Attendance (%)")
plt.legend()
plt.grid(True)
plt.savefig("static/scatter_plot.png")
plt.close()

# 3. Bar Chart
import numpy as np

x = np.arange(len(students))
width = 0.35

plt.figure(figsize=(6,4))
plt.bar(x - width/2, marks, width, label="Marks")
plt.bar(x + width/2, attendance, width, label="Attendance")
plt.xticks(x, students)
plt.title("Marks vs Attendance")
plt.xlabel("Students")
plt.ylabel("Values")
plt.legend()
plt.savefig("static/bar_chart.png")
plt.close()

# 4. Histogram
plt.figure(figsize=(6,4))
plt.hist(marks, bins=5, edgecolor='black', label="Marks Distribution")
plt.title("Histogram of Marks")
plt.xlabel("Marks")
plt.ylabel("Frequency")
plt.legend()
plt.savefig("static/histogram.png")
plt.close()

# Flask Route
@app.route("/")
def home():
    return render_template_string("""
    <h1>Student Performance Dashboard</h1>
    <img src="/static/line_graph.png" width="600">
    """)

if __name__ == "__main__":
    app.run(debug=True)

#question 2 - 560. Subarray Sum Equals K

class Solution:
    def subarraySum(self, nums, k):
        count = 0
        prefix_sum = 0
        hashmap = {0: 1}

        for num in nums:
            prefix_sum += num

            if prefix_sum - k in hashmap:
                count += hashmap[prefix_sum - k]

            hashmap[prefix_sum] = hashmap.get(prefix_sum, 0) + 1

        return count

# LC Question - 238. Product of Array Except Self  

class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)

        answer = [1] * n

        prefix = 1
        for i in range(n):
            answer[i] = prefix
            prefix *= nums[i]

        suffix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= suffix
            suffix *= nums[i]

        return answer

