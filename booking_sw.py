import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #0f172a, #1e3a8a);
        color: white;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    </style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "booking"

def booking_page():
    st.title("Whales and Lunch Tours")
    st.subheader("Book your unforgettable ocean experience")

    st.markdown("## 👤 Your Information")
    name = st.text_input("Name")
    email = st.text_input("Email")

    st.markdown("## 📅 Booking Details")
    date = st.date_input("Select a date")
    time = st.selectbox("Select time", ["9:00 AM", "1:00 PM", "5:00 PM"])
    service = st.selectbox("Service", ["Local", "Standard"])
    guests = st.number_input("Guests", min_value=1)
    infants = st.number_input("Number of Infants (Ages 0-2)", min_value=0, max_value=guests)

    if infants > guests:
        st.error("Infants cannot exceed total guests")
        st.stop()
    lunch_count = guests - infants

    lunch_options = [
        "Smoked Salmon Wrap",
        "Grilled Chicken Wrap",
        "Vegan Hummus Wrap",
        "Peanut Butter and Jelly Sandwich",
        "Ham and Cheese Sandwich"
    ]

    st.markdown("## 🍽️ Lunch Selection")
    lunch_choices = []
    for passenger in range(lunch_count):
        choice = st.selectbox(f'Lunch for passenger {passenger+1}', lunch_options, key=f"lunch_{passenger}")
        lunch_choices.append(choice)

    st.markdown("## 💳 Payment")
    payment_method = st.selectbox("Select a Payment Method", ["Pay Later", "Pay on Arrival", "Card (Coming soon)!"])
    
    if st.button("Review Booking"):
        st.session_state.booking_data = {
            "name": name,
            "email": email,
            "date": date,
            "time": time,
            "service": service,
            "guests": guests,
            "infants": infants,
            "lunches": lunch_choices,
            "payment": payment_method
        }
        st.session_state.page = "confirm"

def confirm_page():
    data = st.session_state.booking_data

    st.title("Confirm Your Booking")

    st.write(f"Name: {data['name']}")
    st.write(f"Email: {data['email']}")
    st.write(f"Date: {data['date']}")
    st.write(f"Time: {data['time']}")
    st.write(f"Service: {data['service']}")
    st.write(f"Guests: {data['guests']}")
    st.write(f"Infants: {data['infants']}")
    st.write(f"Payment: {data['payment']}")

    st.write("Lunches:")
    for i, lunch in enumerate(data["lunches"], 1):
        st.write(f"Passenger {i}: {lunch}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.page = "booking"

    with col2:
        if st.button("Confirm Booking"):
            if check_avail(data["date"], data["time"], data["guests"]):
                save_booking(
                    data["name"],
                    data["email"],
                    data["date"],
                    data["time"],
                    data["service"],
                    data["guests"],
                    data["infants"],
                    data["lunches"],
                    data["payment"]
                )
                st.success("Booking saved! We look forward to seeing you!")
                st.session_state.page = "booking"
            else:
                st.error("Slot full. Please try another date and time")

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

if st.session_state.page == "booking":
    booking_page()
else:
    confirm_page()


