import csv

# Define the file name
phase_dict = {}

def phase_wise(yrs, phase_dur, no_of_phases,rate):
    rate=rate/100
    filename = 'streamlit_mly_req.csv'
    output_filename = 'output_requirements.csv'
    yearly_requirement = {}

    # Open the file in read mode
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            year = int(row["Year"])
            annual_amount = float(row["Annual req"])
            yearly_requirement[year] = annual_amount


    total_years = yrs + (no_of_phases * phase_dur) + 1
    all_phases = []
    ob = [0] * total_years
    bal_amt = [0] * total_years
    cb = [0] * total_years
    yly_req = [0] * total_years
    yr = [0] * total_years

    cnt = yrs + 1

    for i in range(no_of_phases):
        cnt1 = cnt + (i * phase_dur)
        phase = i + 1

        for j in range(phase_dur - 1, -1, -1):
            year = cnt1 + j
            idx = cnt1 + j
            yr[idx] = year
            yly_req[idx] = yearly_requirement.get(year, 0)
            print("yly",yly_req[idx])
            if j == phase_dur - 1:
                cb[idx] = 0
                bal_amt[idx] = 0
                ob[idx] = yly_req[idx]
            else:
                cb[idx] = ob[idx + 1]
                bal_amt[idx] = cb[idx] / (1 + rate)
                ob[idx] = yly_req[idx] + bal_amt[idx]

        phase_data = list(zip([phase] * phase_dur, yr[cnt1:cnt1 + phase_dur], ob[cnt1:cnt1 + phase_dur], yly_req[cnt1:cnt1 + phase_dur], bal_amt[cnt1:cnt1 + phase_dur], cb[cnt1:cnt1 + phase_dur]))
        all_phases.extend(phase_data)
        phase_dict[i]=ob[idx]

    print(phase_dict)
    return all_phases

#yrs = 10
#phase_dur = 7
#no_of_phases = 5

#all_phases = phase_wise(yrs, phase_dur, no_of_phases)

def write_phases_to_csv(all_phases, output_filename):
    with open(output_filename, mode='w', newline='') as file:
        fieldnames = ['phase', 'year', 'ob', 'yly req', 'bal_amt', 'cb']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data rows
        for row in all_phases:
            writer.writerow({
                'phase': row[0],
                'year': row[1],
                'ob': row[2],
                'yly req': row[3],
                'bal_amt': row[4],
                'cb': row[5]
            })

    # Print results
    for row in all_phases:
        print(
            f"Phase: {row[0]}, Year: {row[1]}, OB: {row[2]:.2f}, YLY Req: {row[3]:.2f}, Bal Amt: {row[4]:.2f}, CB: {row[5]:.2f}"
        )

# Example usage
