import numpy as np

scores = np.array([
    [78, 85, 90, 88],
    [92, 81, 76, 95],
    [89, 90, 91, 87],
    [65, 70, 72, 68],
    [99, 95, 98, 100]
])

# 1
student_avg = np.mean(scores, axis=1)
print(f"Average of each student: {student_avg}")

# 2
exam_avg = np.mean(scores, axis=0)
print(f"Average of each exam: {exam_avg}")

# 3
centered_scores = scores - exam_avg
print(f"Scores after subtracting exam averages:\n{centered_scores}")

# 4
best_student = np.argmax(student_avg) + 1
print(f"Best student number: {best_student}")