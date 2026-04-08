<<<<<<< HEAD
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




=======
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("Booking System")

name = st.text_input("Name")
email = st.text_input("Email")
date = st.date_input("Select a date")
time = st.selectbox("Select time", ["9:00 AM", "1:00 PM", "5:00 PM"])
service = st.text_input("Service", ["Local", "Standard"])
guests = st.number_input("Guests", min_value=1)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_key("1d7Pc_Va8rMhfPBYzjPMeKPpuYPfpRCpc9vBB1_yP_64")

worksheet = sheet.worksheet("Bookings")

def save_booking(name, date, time, guests):
    worksheet.append_row([
        name,
        email,
        str(date),
        time,
        service,
        guests
    ])

def check_avail(date, time, new_guests):
    total = 0
    records = worksheet.get_all_records()

    for row in records:
        if str(row['date']) == str(date) and row['time'] == time:
            total += int(row['guests'])
    return total + new_guests <= 35



if st.button("Book Now"):
    if check_avail(date, time, guests):
        save_booking(name, email, date, time, service, guests)
        st.success("Booking saved!")
    else:
        st.error("Slot full")





>>>>>>> b2c804f (initial booking app update)
