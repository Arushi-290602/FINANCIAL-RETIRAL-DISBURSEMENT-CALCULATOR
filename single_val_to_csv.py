import csv
def write_single_value_to_csv(heading, value, filename="output.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the heading in the first column and value in the second column
        writer.writerow([heading, value])