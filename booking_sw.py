import streamlit as st
import csv
import pandas as pd
import os

date = st.date_input("Select a date")

time = st.selectbox("Select time", ["9:00 am", "1:00 PM", "5:00 PM"])

name = st.text_input("Name")

people = st.number_input("Number of people", min_value=1)

if st.button("Book Now"):
    with open("bookings.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, date, time, people])

    st.success("Booking saved!")

def check_avail(date, time, new_people):
    total = 0

    with open("bookings.csv", "r")as file:
        reader = csv.reader(file)

        for row in reader:
            if row[1] == str(date) and row[2] == time:
                total += int(row[3])
    return total +new_people <= 35

CSV_FILE = "bookings.csv"

def save_booking(name, date, time, guests):
    new_data = pd.DataFrame([{
        "name": name,
        "date": date,
        "time": time,
        "guests": guests
    }])


    if os.path.exists(CSV_FILE):
        old_data = pd.read_csv(CSV_FILE)
        updated = pd.concat([old_data, new_data], ignore_index=True)
        updated.to_csv(CSV_FILE, index=False)
    else:
        new_data.to_csv(CSV_FILE, index=False)




