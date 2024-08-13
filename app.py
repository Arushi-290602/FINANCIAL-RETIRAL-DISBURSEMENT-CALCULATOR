import os

import streamlit as st
import pickle
import csv
import pandas as pd
from results01 import disp_results
from mly_requirement import mly_req_func
from phase_wise01 import phase_wise, write_phases_to_csv
from bucket_wise import bucket_wise_calc, write_bucket_wise_calc_results_to_csv
from instrument_dropdown_streamlit import select_instruments, loop_for_instruments, write_val, total_sum, holders_data
from future_value import fv_calc, pv_calc, equivalent_monthly_rate, pmt
from single_val_to_csv import write_single_value_to_csv
from dict_to_csv import write_dict_to_csv

# Default initial session state
initial_session_state = {
    'no_of_yrs_left_st': 0,
    'retiral_period_st': 0,
    'monthly_requirement_st': 0,
    'medical_corpus_st': 0,
    'medical_corpus_rate_st': 0,
    'travel_corpus_st': 0,
    'travel_corpus_rate_st': 0,
    'liquidity_corpus_st': 0,
    'liquidity_corpus_rate_st': 0,
    'legacy_amt_st': 0,
    'general_inflation_st': 0,
    'b1_rate_st': 0,
    'bucket_two_growth_rate_st': 0,
    'number_of_phases_st': 0,
    'phase_duration_st': 0,
    'reset': False,
    'total_sum': 0,
    'other_corpus_st': 0,
    'other_corpus_rate_st': 0

}

flag = False


# Function to load session state from file
def load_session_state():
    try:
        with open("session_state.pkl", "rb") as f:
            session_state = pickle.load(f)
            if session_state.get('reset', False):
                return initial_session_state.copy()
            return session_state
    except FileNotFoundError:
        return initial_session_state.copy()


# Function to save session state to file
def save_session_state(session_state):
    with open("session_state.pkl", "wb") as f:
        pickle.dump(session_state, f)


# Function to write specific inputs to a CSV file
def write_inputs_to_csv(session_state, filename="input_values.csv"):
    data = {
        "No of Years for Fin. Independence from Now to Start Mly Income": session_state['no_of_yrs_left_st'],
        "Retiral Period": session_state['retiral_period_st'],
        "Monthly Requirement (as on Date Valuation)": session_state['monthly_requirement_st'],
        "Required Medical Corpus (as on Date Valuation)": session_state['medical_corpus_st'],
        "Required Liquidity Corpus (as on Date Valuation)": session_state['liquidity_corpus_st'],
        "Required Travel Corpus (as on Date Valuation)": session_state['travel_corpus_st'],
        "Current Value of Residual Amt at the end (Legacy Amount)": session_state['legacy_amt_st']
    }

    # Write data to CSV file row-wise
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["INPUT", "VALUE"])
        for fieldname, value in data.items():
            writer.writerow([fieldname, value])


# Load session state initially
session_state = load_session_state()

# Main title of the app
st.title("FINANCIAL INDEPENDENCE")


def client(session_state):
    st.subheader("NO.OF YEARS LEFT FOR RETIREMENT")
    session_state['no_of_yrs_left_st'] = st.number_input("Years left for retirement",
                                                         min_value=0, max_value=20,
                                                         key='no_of_yrs_left_st',
                                                         value=session_state['no_of_yrs_left_st'])

    st.subheader("ENTER THE DURATION OF RETIREMENT (RETIRAL PERIOD)")
    session_state['retiral_period_st'] = st.number_input("Duration of retirement",
                                                         min_value=0, max_value=53,
                                                         key='retiral_period_st',
                                                         value=session_state['retiral_period_st'])

    st.subheader("ENTER MONTHLY REQUIREMENT (AS ON DATE VALUATION)")
    session_state['monthly_requirement_st'] = st.number_input("Monthly requirement",
                                                              key='monthly_requirement_st',
                                                              value=session_state['monthly_requirement_st'])

    st.subheader("ENTER MEDICAL CORPUS (AS ON DATE VALUATION)")
    session_state['medical_corpus_st'] = st.number_input("Medical corpus",
                                                         key='medical_corpus_st',
                                                         value=session_state['medical_corpus_st'])
    session_state['medical_corpus_rate_st'] = st.number_input("Medical corpus rate",
                                                              key='medical_corpus_rate_st',
                                                              value=float(session_state['medical_corpus_rate_st']),
                                                              step=0.01)

    st.subheader("ENTER TRAVEL CORPUS (AS ON DATE VALUATION)")
    session_state['travel_corpus_st'] = st.number_input("Travel corpus",
                                                        key='travel_corpus_st',
                                                        value=session_state['travel_corpus_st'])
    session_state['travel_corpus_rate_st'] = st.number_input("Travel corpus rate",
                                                             key='travel_corpus_rate_st',
                                                             value=float(session_state['travel_corpus_rate_st']),
                                                             step=0.01)

    st.subheader("ENTER LIQUIDITY CORPUS (AS ON DATE VALUATION)")
    session_state['liquidity_corpus_st'] = st.number_input("Liquidity corpus",
                                                           key='liquidity_corpus_st',
                                                           value=session_state['liquidity_corpus_st'])
    session_state['liquidity_corpus_rate_st'] = st.number_input(
        "Liquidity corpus rate",
        key='liquidity_corpus_rate_st',
        value=float(session_state['liquidity_corpus_rate_st']),  # Ensure value is a float
        step=0.01  # Optional: step size for the float input
    )
    st.subheader("OTHER CORPUS (AS ON DATE VALUATION)")
    session_state['other_corpus_st'] = st.number_input("other corpus",
                                                       key='other_corpus_st',
                                                       value=session_state.get('other_corpus_st', 0))  # Default value
    session_state['other_corpus_rate_st'] = st.number_input("Other corpus rate",
                                                            key='other_corpus_rate_st',
                                                            value=float(session_state.get('other_corpus_rate_st',
                                                                                          0.00)),
                                                            step=0.01)  # Default value

    st.subheader("ENTER LEGACY AMOUNT (AS ON DATE VALUATION)")
    session_state['legacy_amt_st'] = st.number_input("Legacy amount",
                                                     key='legacy_amt_st',
                                                     value=session_state['legacy_amt_st'])

    # Save session state to file after updating values
    save_session_state(session_state)
    write_inputs_to_csv(session_state)


def user1(session_state):
    st.subheader("GENERAL INFLATION (IN %)")
    session_state['general_inflation_st'] = st.number_input("General inflation",
                                                            min_value=0.00, max_value=20.00,
                                                            key='general_inflation_st',
                                                            value=float(session_state['general_inflation_st']),
                                                            step=0.01)

    st.subheader("BUCKET 1 GROWTH RATE (IN %)")
    session_state['b1_rate_st'] = st.number_input("Bucket 1 growth rate",
                                                  min_value=0.00, max_value=20.00,
                                                  key='b1_rate_st',
                                                  value=float(session_state.get('b1_rate_st', 0.00)), step=0.01)
    st.subheader("BUCKET 2 GROWTH RATE (IN %)")
    session_state['bucket_two_growth_rate_st'] = st.number_input("Bucket 2 growth rate",
                                                                 min_value=0.00, max_value=20.00,
                                                                 key='bucket_two_growth_rate_st',
                                                                 value=float(
                                                                     session_state['bucket_two_growth_rate_st']),
                                                                 step=0.01)

    st.subheader("NO.OF PHASES")
    session_state['number_of_phases_st'] = st.number_input("Number of phases",
                                                           min_value=0, max_value=20,
                                                           key='number_of_phases_st',
                                                           value=session_state['number_of_phases_st'])

    st.subheader("PHASE DURATION (IN YRS)")
    session_state['phase_duration_st'] = st.number_input("Phase duration",
                                                         min_value=0, max_value=20,
                                                         key='phase_duration_st',
                                                         value=session_state['phase_duration_st'])

    # Save session state to file after updating values
    save_session_state(session_state)
    write_inputs_to_csv(session_state)


def financial_instruments():
    num_holders = st.number_input("Enter number of holders:", min_value=1, step=1, value=1)
    holders = [f"Holder {i + 1}" for i in range(num_holders)]

    for holder in holders:
        st.header(f"Financial Instruments for {holder}")
        options = select_instruments(holder)
        if options:
            loop_for_instruments(holder, options)
    if st.button("Submit All"):
        write_val(total_sum, holders_data)
        save_session_state(session_state)


def display_stored_values(session_state):
    st.write("### Stored Values:")
    st.write(f"No. of years left for retirement: {session_state['no_of_yrs_left_st']}")
    st.write(f"Retiral period: {session_state['retiral_period_st']}")
    st.write(f"Monthly requirement: {session_state['monthly_requirement_st']}")
    st.write(f"Medical corpus: {session_state['medical_corpus_st']}")
    st.write(f"Travel corpus: {session_state['travel_corpus_st']}")
    st.write(f"Liquidity corpus: {session_state['liquidity_corpus_st']}")
    st.write(f"Legacy amount: {session_state['legacy_amt_st']}")
    st.write(f"General inflation: {session_state['general_inflation_st']}")
    st.write(f"Bucket 1 growth rate: {session_state['b1_rate_st']}")
    st.write(f"Bucket 2 growth rate: {session_state['bucket_two_growth_rate_st']}")
    st.write(f"No. of phases: {session_state['number_of_phases_st']}")
    st.write(f"Phase duration: {session_state['phase_duration_st']}")


# Main menu selection
choice = st.sidebar.selectbox('MENU', ['CLIENT', 'USER 1', 'FINANCIAL INSTRUMENTS', 'RESULT', 'RESET'])

# Routing based on menu choice
if choice == 'CLIENT':
    client(session_state)
elif choice == 'USER 1':
    user1(session_state)
elif choice == 'FINANCIAL INSTRUMENTS':
    financial_instruments()
elif choice == 'RESET':
    session_state = initial_session_state.copy()
    session_state['reset'] = True
    total_sum = 0
    surp_def = 0
    save_session_state(session_state)
    st.write("Session state has been reset.")
elif choice == 'RESULT':
    disp_results("input_values.csv")
    if os.path.exists("output.csv"):
        disp_results("output.csv")
    if os.path.exists("financial_instruments_data.csv"):
     disp_results("financial_instruments_data.csv")
    # disp_results("projected_required_corpus.csv")
    # disp_results("surp_def.csv")
    # disp_results("legacy_fv_corpus.csv")

    if os.path.exists("lumpsum.csv"):
        disp_results("lumpsum.csv")
        #disp_results("pmt_required.csv")

# Submission button and logic
if st.button("Submit"):
    total_yrs = session_state['no_of_yrs_left_st'] + session_state['retiral_period_st']
    bucket_wise_final_val = 0
    travel_corp_fv = fv_calc(
        session_state['travel_corpus_st'], session_state['travel_corpus_rate_st'],
        session_state['no_of_yrs_left_st'])
    medical_corp_fv = fv_calc(session_state['medical_corpus_st'],
                              session_state['medical_corpus_rate_st'],
                              session_state['no_of_yrs_left_st'])
    liquidity_corp_fv = fv_calc(session_state['liquidity_corpus_st'],
                                session_state['liquidity_corpus_rate_st'],
                                session_state['no_of_yrs_left_st'])
    other_corp_fv = fv_calc(session_state['other_corpus_st'], session_state['other_corpus_rate_st'],
                            session_state['no_of_yrs_left_st'])
    legacy_corp_fv = fv_calc(session_state['legacy_amt_st'], session_state['general_inflation_st'], total_yrs)

    # Example calculations and file writes
    mly_req_func(session_state['monthly_requirement_st'], session_state['no_of_yrs_left_st'],
                 session_state['general_inflation_st'], "streamlit_mly_req.csv")
    all_phases = phase_wise(session_state['no_of_yrs_left_st'], session_state['phase_duration_st'],
                            session_state['number_of_phases_st'], session_state['b1_rate_st'])
    write_phases_to_csv(all_phases, "phase_wise_streamlit.csv")
    total_yrs = session_state['no_of_yrs_left_st'] + session_state['retiral_period_st']
    results = bucket_wise_calc(session_state['general_inflation_st'], total_yrs, session_state['legacy_amt_st'],
                               session_state['number_of_phases_st'], session_state['phase_duration_st'],
                               session_state['bucket_two_growth_rate_st'])
    write_bucket_wise_calc_results_to_csv(results, "bucket_wise_calc_results_streamlit.csv")
    bucket_wise_val = bucket_wise_final_val
    corpus = fv_calc(session_state['medical_corpus_st'],
                     session_state['medical_corpus_rate_st'],
                     session_state['no_of_yrs_left_st']) + fv_calc(
        session_state['travel_corpus_st'], session_state['travel_corpus_rate_st'],
        session_state['no_of_yrs_left_st']) + fv_calc(session_state['liquidity_corpus_st'],
                                                      session_state['liquidity_corpus_rate_st'],

                                                    session_state['no_of_yrs_left_st'])
    corpus_add=0
    if results and results[0] and results[0][0] is not None:
        corpus_add = round(results[0][0]) + corpus

    # st.write("bucket: ", round(results[0][0]))
    # # required corpus
    #
    # st.write("bucket(medical/travel/liquididty): ", corpus)
    # st.write("Total required corpus: ", corpus_add)
    write_single_value_to_csv("PROJECTED REQUIRED CORPUS", corpus_add, "projected_required_corpus.csv")
    #st.write("Instrument wise total amount: ", total_sum)
    surp_def = total_sum - corpus_add
    #st.write("Surplus/deficit: ", surp_def)
    write_single_value_to_csv("SURPLUS/DEFICIT", surp_def, "surp_def.csv")

    if surp_def < 0:
        flag = True
        lumpsum_amt = pv_calc(abs(surp_def), session_state['bucket_two_growth_rate_st'],
                              session_state['no_of_yrs_left_st'])
        mly_rate = equivalent_monthly_rate(session_state['bucket_two_growth_rate_st'])
        pmt_amt = pmt(lumpsum_amt, mly_rate, session_state['no_of_yrs_left_st'])
        lp = {
            "PARTICULARS":"VALUE",
            "SURPLUS/DEFICIT": f"{surp_def:,.2f}",
            "ANNUAL RATE":  f"{session_state['bucket_two_growth_rate_st']:.2f}%",
            "INVESTMENT REQUIRED (Lumpsum)": f"{lumpsum_amt:,.2f}",
            "EQUIVALENT MONTHLY RATE": f"{mly_rate:.2f}%",
            "INVESTMENT REQUIRED (Monthly)": f"{pmt_amt:,.2f}"

        }
        write_dict_to_csv(lp, "lumpsum.csv")
        monthly_pmt = {
            "SURPLUS/DEFICIT": surp_def,
            "EQUIVALENT MONTHLY RATE": mly_rate,
            "INVESTMENT REQUIRED": pmt_amt

        }
        write_dict_to_csv(monthly_pmt, "pmt_required.csv")
    #st.write("lumpsum: ", lumpsum_amt)

    # write_single_value_to_csv("LUMPSUM AMOUNT", surp_def, "surp_def.csv")
    #st.write("pmt: ", pmt_amt)

    # Save session state to file after processing
    write_single_value_to_csv("PROJECTED REQUIRED CORPUS", corpus_add, "projected_required_corpus.csv")
    write_single_value_to_csv("ESTIMATED LEGACY AMOUNT (FUTURE VALUE)",
                              fv_calc(session_state['legacy_amt_st'], session_state['general_inflation_st'], total_yrs),
                              "legacy_fv_corpus.csv")
    op_dict = {
        "PARTICULARS": "VALUE",
        'Monthly Income Corpus': round(results[0][0]) if results and results[0] and results[0][0] is not None else 0,
        'Travel Corpus': round(travel_corp_fv),
        'Medical Corpus': round(medical_corp_fv),
        'Liquidity Corpus': round(liquidity_corp_fv),
        'Other Corpus': round(other_corp_fv),
        "Projected Required Corpus ": round(corpus_add),
        'Estimated Legacy Amount':round(other_corp_fv)
    }

    write_dict_to_csv(op_dict, "output.csv")
    save_session_state(session_state)
    write_inputs_to_csv(session_state)

# Display stored values
# display_stored_values(session_state)
