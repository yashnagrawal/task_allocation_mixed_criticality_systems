# Task Set Allocation Algorithm

## Overview

This code implements an algorithm for allocating tasks in a real-time system to a set of processing cores, considering task criticality and shutdownable/non-shutdownable nature. The tasks are read from a CSV file, and the allocation results are written to another CSV file. Additionally, a script (make_task_sets.py) is provided to generate random task sets with distributed utilizations for testing purposes.

## Files

1. 'main.py': This script reads task information from a CSV file, performs task allocation on processing cores, and writes the allocation results to a new CSV file. It also includes a Cores class to manage the state of processing cores and task allocation logic.
2. 'make_task_sets.py': This script generates random task sets with distributed utilizations for testing purposes.

## Usage

### main.py

1. Execute the script with the following command:
   `python3 main.py`
2. Output File: The results will be saved in a CSV file with a name like task_sets_util_3_31_results.csv in the results directory.

### make_task_sets.py

1. Adjust Parameters: Modify the parameters in the script, such as total_utilization_needed, max_utilization_per_task, min_utilization_per_task, and number_of_tasks to generate task sets according to your requirements.

2. Run Script: Execute make_task_sets.py. The script will generate a random task set with the specified parameters and save it to a CSV file in the data directory.

3. Generated Task Set: The generated task set will have a file name like task_sets_util_3_15.csv based on the total utilization, and the utilizations of individual tasks will be printed to the console.
