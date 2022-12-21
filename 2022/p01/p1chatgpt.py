# Below code has been generated with ChatGPT from OpenAI by providing it with the problem statement.
# It was almost right (a slight modification has been added to the input reading from stdin).
# It can be run with "python p1chatgpt.py < in.txt".

# Read the calorie counts from the input
calorie_counts = []
while True:
    try:
        if line := input():
          calorie_counts.append(int(line))
        else:
            calorie_counts.append(0)
    except EOFError:
        break

# Group the calorie counts by Elf
elf_calorie_counts = []
current_elf_calorie_counts = []
for calorie_count in calorie_counts:
    if calorie_count == 0:
        elf_calorie_counts.append(current_elf_calorie_counts)
        current_elf_calorie_counts = []
    else:
        current_elf_calorie_counts.append(calorie_count)
elf_calorie_counts.append(current_elf_calorie_counts)

# Find the Elf with the highest total calorie count
highest_calorie_count = 0
highest_calorie_count_elf = None
for i, elf_calories in enumerate(elf_calorie_counts):
    calorie_count = sum(elf_calories)
    if calorie_count > highest_calorie_count:
        highest_calorie_count = calorie_count
        highest_calorie_count_elf = i

# Print the result
print(f"Elf {highest_calorie_count_elf + 1} is carrying the most Calories, with a total of {highest_calorie_count} Calories.")
