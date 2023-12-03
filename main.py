# open file './data/task_sets_util_3_31.csv'
import csv
import math

threshold_shutdown_slack = 50.0

file_name = "task_sets_util_3_31.csv"

file_path = f'./data/{file_name}'
task_sets = []

with open(file_path, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)

    # Print heading
    print(f'{"ID":^5}{"Criticality":^12}{"Period":^12}{"WCET0":^12}{"WCET1":^12}{"Utilization":^17}{"Shutdown Slack Time":^23}')

    print('-' * 100)  # separator line

    for row in csv_reader:
        task = {}
        task['id'] = int(row[0])
        task['criticality'] = int(row[1])
        task['period'] = float(row[2])
        task['wcet0'] = float(row[3])
        task['wcet1'] = float(row[4])
        task['utilization'] = float(row[5])
        task['shutdown_slack_time'] = 2*(task['period'] - task['wcet1'])

        task_sets.append(task)

        print(f'{task["id"]:^5}: {task["criticality"]:^12} {task["period"]:^12.2f} {task["wcet0"]:^12.2f} {task["wcet1"]:^12.2f} {task["utilization"]:^17.2f} {task["shutdown_slack_time"]:^23.2f}')


# format of each task set: [id, criticality, period, wcet0, wcet1, utilization]


high_criticality_non_shutdownable_tasks = []
high_criticality_shutdownable_tasks = []
low_criticality_non_shutdownable_tasks = []
low_criticality_shutdownable_tasks = []

for task in task_sets:
    shutdown_slack_time = task['shutdown_slack_time']
    if task['criticality'] == 0:
        if shutdown_slack_time < threshold_shutdown_slack:
            low_criticality_non_shutdownable_tasks.append(task)
        else:
            low_criticality_shutdownable_tasks.append(task)

    elif task['criticality'] == 1:
        if shutdown_slack_time < threshold_shutdown_slack:
            high_criticality_non_shutdownable_tasks.append(task)
        else:
            high_criticality_shutdownable_tasks.append(task)


def sort_by_period(tasks):
    return sorted(tasks, key=lambda k: k['period'])


high_criticality_non_shutdownable_tasks = sort_by_period(
    high_criticality_non_shutdownable_tasks)
high_criticality_shutdownable_tasks = sort_by_period(
    high_criticality_shutdownable_tasks)
low_criticality_non_shutdownable_tasks = sort_by_period(
    low_criticality_non_shutdownable_tasks)
low_criticality_shutdownable_tasks = sort_by_period(
    low_criticality_shutdownable_tasks)


non_shotdownable_tasks_utilization = 0

print('High Criticality Non-Shutdownable Tasks')
print('Task: Period, Shutdown Slack Time, Utilization')
utilization = 0
for task in high_criticality_non_shutdownable_tasks:
    print(
        f'{task["id"]}: {task["period"]:.2f} {task["shutdown_slack_time"]:.2f} {task["utilization"]:.2f}')
    utilization += task['utilization']
print(f'Total Utilization: {utilization:.2f}')
non_shotdownable_tasks_utilization += utilization

print('\nLow Criticality Non-Shutdownable Tasks')
print('Task: Period, Shutdown Slack Time, Utilization')
utilization = 0
for task in low_criticality_non_shutdownable_tasks:
    print(
        f'{task["id"]}: {task["period"]:.2f} {task["shutdown_slack_time"]:.2f} {task["utilization"]:.2f}')
    utilization += task['utilization']
print(f'Total Utilization: {utilization:.2f}')
non_shotdownable_tasks_utilization += utilization

print('\nHigh Criticality Shutdownable Tasks')
print('Task: Period, Shutdown Slack Time, Utilization')
utilization = 0
for task in high_criticality_shutdownable_tasks:
    print(
        f'{task["id"]}: {task["period"]:.2f} {task["shutdown_slack_time"]:.2f} {task["utilization"]:.2f}')
    utilization += task['utilization']
print(f'Total Utilization: {utilization:.2f}')

print('\nLow Criticality Shutdownable Tasks')
print('Task: Period, Shutdown Slack Time, Utilization')
utilization = 0
for task in low_criticality_shutdownable_tasks:
    print(
        f'{task["id"]}: {task["period"]:.2f} {task["shutdown_slack_time"]:.2f} {task["utilization"]:.2f}')
    utilization += task['utilization']
print(f'Total Utilization: {utilization:.2f}')


class Cores:
    def __init__(self, number_of_non_shutdownable_cores, number_of_shutdownable_cores):
        self.number_of_non_shutdownable_cores = number_of_non_shutdownable_cores
        self.number_of_shutdownable_cores = number_of_shutdownable_cores
        self.number_of_cores = number_of_non_shutdownable_cores + number_of_shutdownable_cores
        self.initialize_cores()

    def initialize_cores(self):
        self.cores = []
        for i in range(self.number_of_non_shutdownable_cores + self.number_of_shutdownable_cores):
            self.cores.append({'id': i, 'utilization': 0, 'tasks': [], 'type': 'non_shutdownable' if i <
                               number_of_non_shutdownable_cores else 'shutdownable'})

    def worst_fit_core(self, task):
        least_fit_utilization_core_id = None
        least_fit_utilization = 1
        for i, core in enumerate(self.cores):
            if core['utilization'] + task['utilization'] <= 1 and core['utilization'] < least_fit_utilization:
                least_fit_utilization_core_id = i
                least_fit_utilization = core['utilization']

        return least_fit_utilization_core_id

    def best_fit_core(self, task):
        best_fit_utilization_core_id = None
        best_fit_utilization = -1
        for i, core in enumerate(self.cores):
            if core['utilization'] + task['utilization'] <= 1 and core['utilization'] > best_fit_utilization:
                best_fit_utilization_core_id = i
                best_fit_utilization = core['utilization']

        return best_fit_utilization_core_id

    def add_task_to_core(self, task, core_id):
        self.cores[core_id]['utilization'] += task['utilization']
        self.cores[core_id]['tasks'].append(task)

    def add_core_and_reinitialize(self, core_type):
        if core_type == 'non_shutdownable':
            self.number_of_non_shutdownable_cores += 1
            self.initialize_cores()
        else:
            self.number_of_shutdownable_cores += 1
            for core in self.cores:
                if core['type'] == 'shutdownable':
                    # remove all tasks from shutdownable cores
                    core['tasks'] = []
                    core['utilization'] = 0

                else:
                    for task in core['tasks']:
                        if task['shutdown_slack_time'] > threshold_shutdown_slack:
                            # remove all shutdownable tasks from non-shutdownable cores
                            core['tasks'].remove(task)
                            core['utilization'] -= task['utilization']

        self.number_of_cores += 1
        self.cores.append({'id': self.number_of_cores - 1, 'utilization': 0, 'tasks': [],
                           'type': 'non_shutdownable' if core_type == 'non_shutdownable' else 'shutdownable'})

        print(f'Adding a new {core_type} core')
        self.print_cores()

    def print_cores(self):
        # print the format of each core: core id, utilization, and tasks ids
        print('-' * 50)  # separator line
        print(f'{"Core":<5}{"| Utilization":<10}{"| Type":<19}{"| Tasks"}')
        print('-' * 50)  # separator line
        for core in self.cores:
            # print core id, utilization, and tasks ids
            print(
                f'{core["id"]:<5}| {core["utilization"]:.2f}       |', core['type'], '|', end=' ')
            for task in core['tasks']:
                print(f'{task["id"]} {task["utilization"]}', end=' ,')
            print()


number_of_non_shutdownable_cores = math.ceil(
    non_shotdownable_tasks_utilization)
number_of_shutdownable_cores = 0

cores = Cores(number_of_non_shutdownable_cores, number_of_shutdownable_cores)

is_non_shutdownable_task_allocation_completed = False
is_shutdownable_task_allocation_completed = False

while not is_non_shutdownable_task_allocation_completed:
    print('/'*100)
    # print the algorithm is starting with the number of non shutdownable cores and shutdownable cores
    print('Algorithm is starting with', cores.number_of_non_shutdownable_cores,
          'non shutdownable cores and', cores.number_of_shutdownable_cores, 'shutdownable cores')

    is_non_shutdownable_task_allocation_completed = True
    print('-'*50)
    print('Adding high criticality non-shutdownable tasks')
    print('-'*50)
    for task in high_criticality_non_shutdownable_tasks:
        core_id = cores.worst_fit_core(task)
        if core_id is not None:
            cores.add_task_to_core(task, core_id)
            print('Task', task['id'], 'is added to core', core_id)
        else:
            is_non_shutdownable_task_allocation_completed = False
            print('Task', task['id'], 'cannot be added to any core')
            cores.add_core_and_reinitialize('non_shutdownable')
            break
        cores.print_cores()

    if is_non_shutdownable_task_allocation_completed == False:
        continue

    print('-'*50)
    print('Adding Low criticality non shutdownable tasks')
    print('-'*50)

    for task in low_criticality_non_shutdownable_tasks:
        core_id = cores.best_fit_core(task)
        if core_id is not None:
            cores.add_task_to_core(task, core_id)
            print('Task', task['id'], 'is added to core', core_id)
        else:
            is_non_shutdownable_task_allocation_completed = False
            print('Task', task['id'], 'cannot be added to any core')
            cores.add_core_and_reinitialize('non_shutdownable')
            break
        cores.print_cores()

    if is_non_shutdownable_task_allocation_completed == False:
        continue

    is_non_shutdownable_task_allocation_completed = True
    print('Non-Shutdownable Cores task allocation is done')


while not is_shutdownable_task_allocation_completed:
    is_shutdownable_task_allocation_completed = True
    print('-'*50)
    print('Adding high criticality shutdownable tasks')
    print('-'*50)

    for task in high_criticality_shutdownable_tasks:
        core_id = cores.worst_fit_core(task)
        if core_id is not None:
            cores.add_task_to_core(task, core_id)
            print('Task', task['id'], 'is added to core', core_id)
        else:
            is_shutdownable_task_allocation_completed = False
            print('Task', task['id'], 'cannot be added to any core')
            cores.add_core_and_reinitialize('shutdownable')
            break
        cores.print_cores()

    if is_shutdownable_task_allocation_completed == False:
        continue

    print('-'*50)
    print('Adding low criticality shutdownable tasks')
    print('-'*50)

    for task in low_criticality_shutdownable_tasks:
        core_id = cores.best_fit_core(task)
        if core_id is not None:
            cores.add_task_to_core(task, core_id)
            print('Task', task['id'], 'is added to core', core_id)
        else:
            is_shutdownable_task_allocation_completed = False
            print('Task', task['id'], 'cannot be added to any core')
            cores.add_core_and_reinitialize('shutdownable')
            break
        cores.print_cores()

    if is_shutdownable_task_allocation_completed == False:
        continue

    print('Shutdownable Cores task allocation is done')
    print('Algorithm is completed with', cores.number_of_non_shutdownable_cores,
          'non shutdownable cores and', cores.number_of_shutdownable_cores, 'shutdownable cores')
    print('/'*100)

    is_shutdownable_task_allocation_completed = True

# create a file './results/task_sets_util_3_31_results.csv'
results_file_name = file_name.replace('.csv', '_results.csv')
results_file_path = f'./results/{results_file_name}'

with open(results_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Core ID', 'Core Type', 'Utilization', 'Tasks IDs'])

    for core in cores.cores:
        csv_writer.writerow(
            [core['id'], core['type'], core['utilization'], [task['id'] for task in core['tasks']]])

print(f'Task set results created in CSV format: {results_file_path}')
