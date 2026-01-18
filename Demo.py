import streamlit as st
import random
import time
from datetime import datetime, timedelta

# --- 1. APP CONFIGURATION & AESTHETICS ---
st.set_page_config(
    page_title="ShadeStore | Secure Luggage Network",
    page_icon="🎒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for "Heavy UI/UX" feel
st.markdown("""
<style>
    /* Global Font & Colors */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Custom Card Styling */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: #262730;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #363B47;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        height: 50px;
        background-color: #FF4B4B; 
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF2B2B;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
    }

    /* Trust Badges */
    .trust-badge {
        background-color: #00C853;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    .metric-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'booking_status' not in st.session_state:
    st.session_state.booking_status = None
if 'selected_shop' not in st.session_state:
    st.session_state.selected_shop = None

# --- 3. MOCK DATA (The "Fake" Reality) ---
SHOPS = [
    {
        "id": 1,
        "name": "Metro Heights Hotel",
        "area": "New Delhi Railway Station (500m)",
        "rating": 4.8,
        "reviews": 124,
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80",
        "verified": True,
        "cctv": True
    },
    {
        "id": 2,
        "name": "CyberHub Travels",
        "area": "Gurugram Cyber City",
        "rating": 4.5,
        "reviews": 89,
        "image": "https://images.unsplash.com/photo-1527786356703-4b100091cd2c?auto=format&fit=crop&w=800&q=80",
        "verified": True,
        "cctv": True
    },
    {
        "id": 3,
        "name": "Backpacker's Stop",
        "area": "Paharganj Main Bazar",
        "rating": 4.2,
        "reviews": 210,
        "image": "https://images.unsplash.com/photo-1555854785-985c9e318f30?auto=format&fit=crop&w=800&q=80",
        "verified": True,
        "cctv": False
    }
]

# --- 4. VIEW FUNCTIONS ---

def render_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎒 ShadeStore")
    with col2:
        # Toggle between User and Partner view
        mode = st.selectbox("View Mode", ["Tourist", "Shop Partner"], label_visibility="collapsed")
    return mode

def render_user_home():
    st.markdown("### 🔒 Store your bags. Free your hands.")
    st.markdown("Safe. Insured up to ₹5,000. Verified Partners.")
    
    # Search Bar Simulation
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_input("Where are you?", placeholder="e.g., New Delhi Railway Station")
    with col2:
        st.write("")
        st.write("")
        st.button("Search")

    st.markdown("---")
    st.subheader("📍 Nearby Trusted Spots")

    for shop in SHOPS:
        with st.container():
            col_img, col_info, col_action = st.columns([2, 3, 2])
            
            with col_img:
                st.image(shop["image"], use_container_width=True, clamp=True)
            
            with col_info:
                st.markdown(f"**{shop['name']}**")
                st.caption(f"📍 {shop['area']}")
                st.markdown(f"⭐ **{shop['rating']}** ({shop['reviews']} verified)")
                if shop['verified']:
                    st.markdown('<span class="trust-badge">🛡️ KYC Verified</span>', unsafe_allow_html=True)
                if shop['cctv']:
                    st.caption("📹 24/7 CCTV Monitoring")
            
            with col_action:
                st.write("")
                if st.button(f"Book ₹150", key=shop['id']):
                    st.session_state.selected_shop = shop
                    st.session_state.page = 'booking'
                    st.rerun()
            st.markdown("---")

def render_booking_flow():
    shop = st.session_state.selected_shop
    st.button("← Back", on_click=lambda: st.session_state.update(page='home'))
    
    st.success(f"Booking at: {shop['name']}")
    
    col1, col2 = st.columns(2)
    with col1:
        bags = st.slider("Number of Bags", 1, 5, 2)
    with col2:
        hours = st.slider("Duration (Hours)", 1, 24, 4)
    
    total_price = (100 * bags) + (10 * hours)
    
    st.markdown(f"""
    <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="text-align: center; color: #00E676;">Total: ₹{total_price}</h3>
        <p style="text-align: center; color: #888;">Includes Insurance & GST</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🛡️ Trust Protocols")
    st.checkbox("I agree NO ELECTRONICS are in the bag.", value=True)
    st.checkbox("I agree to tag my bag with ShadeStore Seal.", value=True)
    
    if st.button("Confirm & Pay (Demo)"):
        with st.spinner("Verifying Shop Availability..."):
            time.sleep(1.5)
        with st.spinner("Generating Secure OTP..."):
            time.sleep(1)
        st.session_state.booking_status = {
            "id": f"SHD-{random.randint(1000,9999)}",
            "otp": random.randint(1000, 9999),
            "shop": shop['name'],
            "bags": bags,
            "seal_code": "PENDING_SCAN"
        }
        st.session_state.page = 'success'
        st.rerun()

def render_success_page():
    booking = st.session_state.booking_status
    
    st.balloons()
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background-color: #262730; border-radius: 15px; border: 2px solid #00C853;">
        <h1>✅ Booked!</h1>
        <p>Show this to the shopkeeper</p>
        <h2 style="font-size: 3em; letter-spacing: 5px; color: #FAFAFA;">{booking['otp']}</h2>
        <p>Booking ID: {booking['id']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("⚠️ Hand over your bag and wait for the shopkeeper to apply the Security Seal.")
    
    if st.button("Go to Home"):
        st.session_state.page = 'home'
        st.rerun()

def render_partner_dashboard():
    st.markdown("## 🏪 Shop Partner Dashboard")
    st.markdown(f"**Status:** 🟢 Online | **Active Bags:** 4/10")
    
    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="metric-card"><h3>₹1,250</h3><p>Today\'s Earnings</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><h3>12</h3><p>Bags Stored</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="metric-card"><h3>4.9⭐</h3><p>Trust Score</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🔔 Incoming Drop-off")
    
    with st.container():
        st.warning("New Customer Arriving: **Rahul S.** (2 Bags)")
        st.markdown("**Booking ID:** SHD-8821")
        
        c_otp, c_verify = st.columns([2, 1])
        otp_input = c_otp.text_input("Enter Customer OTP")
        
        if c_verify.button("Verify OTP"):
            if otp_input:
                st.success("✅ OTP Verified!")
                st.markdown("### 📸 Step 2: Security Seal Evidence")
                st.file_uploader("Upload Photo of Sealed Bag", type=['jpg', 'png'])
                st.text_input("Enter Seal Serial Number (e.g., SEAL-992)")
                if st.button("Complete Check-In"):
                    st.success("Bag Secured. Liability Timer Started.")
            else:
                st.error("Enter OTP first")

# --- 5. MAIN APP LOGIC ---

mode = render_header()

if mode == "Tourist":
    if st.session_state.page == 'home':
        render_user_home()
    elif st.session_state.page == 'booking':
        render_booking_flow()
    elif st.session_state.page == 'success':
        render_success_page()
else:
    render_partner_dashboard()

# Footer
st.markdown("---")
st.caption("🔒 ShadeStore Mockup v1.0 | Built for Demo Purposes Only")
