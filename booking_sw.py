import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("Booking System")

name = st.text_input("Name")
email = st.text_input("Email")
date = st.date_input("Select a date")
time = st.selectbox("Select time", ["9:00 AM", "1:00 PM", "5:00 PM"])
service = st.selectbox("Service", ["Local", "Standard"])
guests = st.number_input("Guests", min_value=1)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

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
        row = {k.strip().lower(): v for k, v in row.items()}
        
        if str(row['date']) == str(date) and row['time'] == time:
            total += int(row['guests'])
    return total + new_guests <= 35



if st.button("Book Now"):
    if check_avail(date, time, guests):
        save_booking(name, email, date, time, service, guests)
        st.success("Booking saved!")
    else:
        st.error("Slot full")





