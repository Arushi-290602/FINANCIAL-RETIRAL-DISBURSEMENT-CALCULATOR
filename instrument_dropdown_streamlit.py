import streamlit as st
import csv
from future_value import mly_fv_calc  # Assuming these imports are available
from assumptions import my_assumptions_names, my_assumptions_rate_card
from find_key_from_dict import find_key


st.title("FINANCIAL INSTRUMENTS")
holders_data = {}
total_sum = 0


def select_instruments(holder):
    options = st.multiselect(
        f"SELECT FINANCIAL INSTRUMENTS FOR {holder}",
        ["EPF", "PPF", "SUPERANNUATION FUND", "NPS INVESTMENT", "MF INVESTMENT", "ALTERNATE INVESTMENTS",
         "ULP INSURANCE PROCEEDS", "TRADITIONAL INSURANCE PROCEEDS", "FIXED INCOME INVESTMENT",
         "ESOP/RSU FOREIGN INVESTMENTS", "PROPERTIES"])
    return options

def write_inputs_to_csv(dict, filename):
    fieldnames = [
        "INSTRUMENT",
        "VALUE"
    ]

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for key,value in dict.items():
         writer.writerow({
            "INSTRUMENT":key,
             "VALUE":value

         })

def loop_for_instruments(holder, options):
    global total_sum
    total_sum=0
    holder_data = {}
    global holders_data
    holders_data={}

    with st.form(key=f'financial_instruments_form_{holder}'):
        for opt in options:
            st.write(f"You selected: {opt} for {holder}")
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                cv = st.number_input(f"ENTER CURRENT VALUE for {opt}", key=f'cv_st_{holder}_{opt}')
                st.write(cv)

            with col2:
                new_add = st.number_input(f"ENTER NEW ADDITION (0 FOR NIL) for {opt}", key=f'new_add_st_{holder}_{opt}')
                st.write(new_add)

            with col3:
                tenure = st.slider(f"NO.OF YEARS for {opt}", 0, 30, 10, key=f'tenure_st_{holder}_{opt}')
                st.write(tenure)

            with col4:
                time_period = st.selectbox(f"SELECT TIME PERIOD OF INVESTMENTS for {opt}", ["MLY", "ANNUAL", "NIL"],
                                           key=f'time_period_st_{holder}_{opt}')
                st.write(time_period)

            with col5:
                r = find_key(opt, my_assumptions_names, my_assumptions_rate_card)
                amt = mly_fv_calc(cv, new_add, r, tenure, time_period)
                total_sum += amt
                st.write(amt)
                holder_data[opt] = amt



        if st.form_submit_button(label='Submit'):
            holders_data[holder] = holder_data
            st.write(f"Form Submitted for {holder}!")
            st.write(holder_data)
            print(holder_data)
            write_inputs_to_csv(holder_data,"financial_instruments_data.csv")


# Main section

def write_val(total_sum, holders_data):
    st.write(f"Total Sum: {total_sum}")
    # st.write(f"holder : {holders_data}")

# if st.button("Submit All"):
# write_val(total_sum,holders_data)
# st.write("All Holders Data:")
# st.write(holders_data)

# total_sum = 0
# for holder, instruments in holders_data.items():
# for key, value in instruments.items():
# total_sum += int(value)

# st.write(f"Total Sum: {total_sum}")
