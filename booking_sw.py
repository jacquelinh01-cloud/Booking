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
infants = st.number_input("Number of Infants (Ages 0-2)", min_value=0, max_value=guests)

if infants > guests:
    st.error("Infants cannot exceed total guests")
    st.stop()
lunch_count = guests - infants


payment_method = st.selectbox("Select a Payment Method", ["Pay Later", "Pay on Arrival", "Card (Coming soon)!"])


lunch_options = [
    "Smoked Salmon Wrap",
    "Grilled Chicken Wrap",
    "Vegan Hummus Wrap",
    "Peanut Butter and Jelly Sandwich",
    "Ham and Cheese Sandwich"
]

lunch_choices = []
for passenger in range(lunch_count):
    choice = st.selectbox(f'Lunch for passenger {passenger+1}', lunch_options, key=f"lunch_{passenger}")
    lunch_choices.append(choice)

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



def save_booking(name, email, date, time, service, guests, infants, lunches, payment_method):
    worksheet.append_row([
        name,
        email,
        str(date),
        time,
        service,
        guests,
        infants,
        ", ".join(lunches),
        payment_method
    ])

def check_avail(date, time, new_guests):
    total = 0
    records = worksheet.get_all_records()

    for row in records:
        row = {k.strip().lower(): v for k, v in row.items()}

        if str(row['date']) == str(date) and row['time'] == time:
            total += int(row['guests'])
    return total + new_guests <= 21


if st.button("Confirm Booking"):
    st.subheader("Confirm Your Booking")

    st.write(f"Name: {name}")
    st.write(f"Email: {email}")
    st.write(f"Date: {date}")
    st.write(f"Time: {time}")
    st.write(f"Service: {service}")
    st.write(f"Infants: {infants}")
    st.write(f"Payment: {payment_method}")
    st.write("Lunch/Lunches:")
    for passenger, lunch in enumerate(lunch_choices, 1):
        st.write(f"Passenger {passenger}: {lunch}")

    confirm = st.button("Confirm Booking")

    if confirm:
        if check_avail(date, time, guests):
            save_booking(name, email, date, time, service, guests, infants, lunch_choices, payment_method)
            st.success("Booking Saved! See you soon!")
        else:
            st.error("Slot full. Please try another date and time")



