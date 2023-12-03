import csv
import random


def generate_distributed_utilizations(number_of_tasks, total_utilization_needed, max_utilization_per_task=0.5, min_utilization_per_task=0.05):
    if number_of_tasks * max_utilization_per_task < total_utilization_needed:
        raise ValueError(
            "Total utilization needed cannot be achieved with the given parameters.")

    utilizations = []
    remaining_utilization = total_utilization_needed
    remaining_tasks = number_of_tasks

    while remaining_tasks > 1:
        # Generate a random utilization between 0 and max_utilization_per_task
        utilization = random.uniform(
            min_utilization_per_task, max_utilization_per_task)

        if (remaining_tasks-1)*max_utilization_per_task < remaining_utilization - utilization:
            # If the remaining tasks cannot be assigned a utilization of max_utilization_per_task, assign the remaining utilization to the last task
            continue

        utilizations.append(utilization)

        remaining_utilization -= utilization
        remaining_tasks -= 1

    # Add the remaining utilization to the last task
    for i in range(remaining_tasks):
        utilizations.append(remaining_utilization/remaining_tasks)

    # Shuffle the utilizations to randomize the order
    random.shuffle(utilizations)

    return utilizations


# create a new CSV file with utilization value as the filename
total_utilization_needed = random.uniform(3.0, 5.0)
utilization_str = f'{total_utilization_needed:.2f}'.replace('.', '_')
csv_file_path = f'./data/task_sets_util_{utilization_str}.csv'

header = ['id', 'criticality', 'period', 'wcet[0]', 'wcet[1]', 'utilization']

number_of_tasks = 10

# Generate distributed random utilizations with a maximum of 0.5 per task
task_set_utilizations = generate_distributed_utilizations(
    number_of_tasks, total_utilization_needed, max_utilization_per_task=0.4, min_utilization_per_task=0.05)

# create and write the tasks to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)

    for i in range(number_of_tasks):
        id = i
        criticality = random.randint(0, 1)
        period = random.randint(10, 100)
        utilization = task_set_utilizations[i]

        wcet1 = utilization * period
        wcet0 = random.uniform(0.0, wcet1)

        row_data = [id, criticality, period, wcet0, wcet1, utilization]
        csv_writer.writerow(row_data)

print(f'Task set created in CSV format: {csv_file_path}')

# print each utilization
print('Task set utilizations:')
for i in range(number_of_tasks):
    print(f'Task {i}: {task_set_utilizations[i]}')

print(f'Total utilization: {total_utilization_needed:.2f}')
