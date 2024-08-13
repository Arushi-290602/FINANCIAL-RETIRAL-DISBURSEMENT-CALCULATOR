import csv
from future_value import fv_calc, pv_calc
from phase_wise01 import phase_dict

def bucket_wise_calc(growth_rate, no_of_yrs, cv, no_of_phases, phase_dur, b2_growth_rate):
    bucket_wise_final_val = 0  # Ensure it starts from zero
    ob = [0] * no_of_phases
    deduct_from_b3 = [0] * no_of_phases
    amt_at_start = [0] * no_of_phases
    cb = [0] * no_of_phases
    phases = [0] * no_of_phases

    for i in range(no_of_phases, 0, -1):
        phases[i - 1] = i
        if i == no_of_phases:
            cb[i - 1] = fv_calc(cv, growth_rate, no_of_yrs)
            deduct_from_b3[i - 1] = phase_dict[i - 1]
            amt_at_start[i - 1] = pv_calc(cb[i - 1], b2_growth_rate, phase_dur)
            ob[i - 1] = deduct_from_b3[i - 1] + amt_at_start[i - 1]
        else:
            cb[i - 1] = ob[i]
            amt_at_start[i - 1] = pv_calc(cb[i - 1], b2_growth_rate, phase_dur)
            deduct_from_b3[i - 1] = phase_dict[i - 1]
            ob[i - 1] = deduct_from_b3[i - 1] + amt_at_start[i - 1]

        bucket_wise_final_val += ob[i - 1]  # Accumulate the value
        print(f"ob:{ob} deduct from b3{deduct_from_b3} amt_at start:{amt_at_start} cb:{cb} phases: {phases}")

    return ob, deduct_from_b3, amt_at_start, cb, phases


def write_bucket_wise_calc_results_to_csv(results, filename):
    # Prepare the data for writing to CSV
    data = {
        'ob': results[0],
        'deduct_from_b3': results[1],
        'amt_at_start': results[2],
        'cb': results[3],
        'phases': results[4]
    }

    # Write the results to a CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerows([dict(zip(data.keys(), values)) for values in zip(*data.values())])

    print(f"Results have been written to '{filename}'.")

# Example usage:
#results = bucket_wise_calc(5, 45, 10000000, 5, 7, 9)
#write_bucket_wise_calc_results_to_csv(results, "bucket_trial.csv")
#if results:
    #ob_phase_1 = results[0][0]  # Accessing the first element of 'ob' list
    #print(f"Opening balance of phase 1: {ob_phase_1}")
