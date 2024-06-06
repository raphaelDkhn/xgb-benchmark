import math
import argparse

def calculate_fri_step_list(num_steps, last_layer_degree_bound):
    """
    Calculate the FRI step list for a given number of steps.
    
    :param num_steps: Total number of steps in the trace.
    :param last_layer_degree_bound: The degree bound of the last layer, which is a fixed value.
    :return: A list of integers representing the FRI step list.
    """
    target_sum = math.log2(num_steps) + 4 - math.log2(last_layer_degree_bound)
    fri_step_list = []
    current_sum = 0
    step_range = [2, 3, 4]

    while current_sum < target_sum:
        remaining_sum = target_sum - current_sum
        possible_steps = [step for step in step_range if step <= remaining_sum]
        if possible_steps:
            step = max(possible_steps)
            fri_step_list.append(step)
            current_sum += step
        else:
            if remaining_sum > 0 and fri_step_list and remaining_sum < 2:
                fri_step_list[-1] += remaining_sum
            break

        if math.isclose(current_sum, target_sum, abs_tol=0.01):
            break

    return fri_step_list

def main():
    parser = argparse.ArgumentParser(description="Calculate the FRI step list based on number of steps.")
    parser.add_argument("num_steps", type=int, help="Total number of steps in the trace.")
    args = parser.parse_args()

    last_layer_degree_bound = 64
    fri_step_list = calculate_fri_step_list(args.num_steps, last_layer_degree_bound)
    print("FRI Step List:", fri_step_list)

if __name__ == "__main__":
    main()
