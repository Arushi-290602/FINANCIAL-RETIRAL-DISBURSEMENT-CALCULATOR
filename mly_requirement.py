import csv
from future_value import fv_calc
class Input_One:
    def __init__(self, mly_req, years):
        self.mly_req = mly_req
        self.years = years

def mly_req_func(mly_req, years, annual_inflation, csv_filename):


    mly_req=float(mly_req)
    monthly_requirement_table = []
    for i in range(years + 1, 53):

        fv = fv_calc(mly_req,annual_inflation,i-1)
        annual_req = (12 * fv)

        row = {"Year": i, "Monthly Requirement (Present Value)": mly_req, "Annual inflation": annual_inflation, "FV(monthly req)": fv, "Annual req": annual_req}
        monthly_requirement_table.append(row)

    fieldnames = ["Year", "Monthly Requirement (Present Value)", "Annual inflation", "FV(monthly req)", "Annual req"]

    # Open a file in write mode
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data rows
        writer.writerows(monthly_requirement_table)

    print(f"Results have been written to '{csv_filename}'.")


# Example usage
#obj = Input_One(mly_req=250000, years=10)
#mly_req_func(obj.mly_req, obj.years, annual_inflation=5, csv_filename='monthly_requirements.csv')
