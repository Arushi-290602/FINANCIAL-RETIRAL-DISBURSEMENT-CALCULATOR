import csv

def write_dict_to_csv(data_dict, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the keys (headings) and values column-wise
        for key, value in data_dict.items():
            writer.writerow([key,value])
            #writer.writerow(([value]))