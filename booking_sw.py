import streamlit as st

date = st.date_input("Select a date")

time = st.selectbox("Select time", ["9:00 am", "1:00 PM", "5:00 PM"])

name = st.text_input("Name")

people = st.number_input("Number of people", min_value=1)

def check_avail(date, time, new_people):
    total = 0

    with open("bookings.csv", "r")as file:
        reader = csv.reader(file)

        for row in reader:
            if row[1] == str(date) and row[2] == time:
                total += int(row[3])
    return total +new_people <= 35



