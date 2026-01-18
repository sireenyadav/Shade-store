import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time
import random
import pandas as pd

# --- 1. APP CONFIGURATION & ASSETS ---
st.set_page_config(
    page_title="ShadeStore Pro | Secure Luggage Network",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Lottie Animations (Cached)
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Animation Assets
LOTTIE_LOADING = "https://lottie.host/95181165-f48d-4223-b68e-282672d5b610/9Y1j7X8l5h.json"  # Luggage loop
LOTTIE_SUCCESS = "https://lottie.host/8172945d-7984-474c-bd49-9f796213032b/gQe23c72q2.json"  # Success Check
LOTTIE_TRUST = "https://lottie.host/0200822e-13e5-4122-8610-d020d5854887/7b582b13-582b-458b-982b-582b13582b13.json" # Shield (Generic fallback)

# --- 2. ADVANCED CSS (SWIGGY/ZOMATO AESTHETIC) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Zomato-Red Gradient Button */
    .stButton>button {
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
        color: white;
        border: none;
        border-radius: 12px;
        height: 50px;
        font-weight: 600;
        letter-spacing: 1px;
        transition: transform 0.2s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(221, 36, 118, 0.4);
    }

    /* Glassmorphism Cards */
    .shop-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .shop-card:hover {
        border-color: #DD2476;
        background: rgba(255, 255, 255, 0.08);
    }

    /* Floating Tags */
    .tag-live {
        background-color: #00E676;
        color: #000;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 800;
        display: inline-block;
    }
    
    .price-tag {
        font-size: 1.2rem;
        font-weight: 700;
        color: #FF512F;
    }

    /* Footer Branding */
    .footer-brand {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'splash'
if 'selected_shop' not in st.session_state:
    st.session_state.selected_shop = None

# --- 4. REALISTIC MOCK DATA ---
SHOPS = [
    {"id": 1, "name": "Metro Heights Hotel", "loc": "New Delhi Station", "lat": 28.6415, "lon": 77.2205, "rating": 4.8, "price": 120, "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800", "tags": ["24/7", "CCTV"]},
    {"id": 2, "name": "CyberHub Travels", "loc": "Gurugram DLF", "lat": 28.4950, "lon": 77.0895, "rating": 4.5, "price": 150, "image": "https://images.unsplash.com/photo-1527786356703-4b100091cd2c?w=800", "tags": ["AC Storage", "Insurance"]},
    {"id": 3, "name": "Backpacker's Cafe", "loc": "Paharganj", "lat": 28.6356, "lon": 77.2173, "rating": 4.2, "price": 90, "image": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800", "tags": ["Cheap", "Open Late"]},
]

# --- 5. VIEWS ---

def splash_screen():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st_lottie(load_lottieurl(LOTTIE_LOADING), height=300, key="loading")
        st.markdown("<h2 style='text-align: center;'>Finding Secure Spots...</h2>", unsafe_allow_html=True)
    
    # Auto-redirect simulation
    time.sleep(3)
    st.session_state.page = 'home'
    st.rerun()

def home_page():
    # Header
    col1, col2 = st.columns([3,1])
    with col1:
        st.title("🎒 ShadeStore")
        st.caption("India's Most Trusted Luggage Network")
    with col2:
        st.markdown(f"<div style='text-align:right; padding-top:10px;'><b>📍 Gurugram</b></div>", unsafe_allow_html=True)

    # Search Simulation
    st.text_input("🔍 Search location (e.g. 'Railway Station')", placeholder="Try 'Connaught Place'")
    
    # Map Section (Interactive)
    st.subheader("🗺️ Near You")
    map_df = pd.DataFrame(SHOPS)
    st.map(map_df, latitude='lat', longitude='lon', size=20, color='#FF512F')

    # Listing Cards
    st.subheader("🔥 Top Rated Spots")
    
    for shop in SHOPS:
        with st.container():
            st.markdown(f"""
            <div class="shop-card">
                <div style="display:flex; justify-content:space-between;">
                    <h3>{shop['name']}</h3>
                    <span class="price-tag">₹{shop['price']}/hr</span>
                </div>
                <p>📍 {shop['loc']} &nbsp; | &nbsp; ⭐ {shop['rating']}</p>
                <div style="margin-top:10px;">
                    {' '.join([f'<span class="tag-live">{t}</span>' for t in shop['tags']])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action Button
            if st.button(f"Book Now - {shop['name']}", key=shop['id']):
                st.session_state.selected_shop = shop
                st.session_state.page = 'booking'
                st.rerun()

def booking_page():
    shop = st.session_state.selected_shop
    st.button("⬅ Back", on_click=lambda: st.session_state.update(page='home'))
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(shop['image'], use_container_width=True, caption=shop['name'])
    
    with col2:
        st.markdown(f"## {shop['name']}")
        st.markdown("🔒 **Security Protocol Active**")
        st.info("⚠️ Verified Partner. Tamper-Proof Seals Available.")
        
        bags = st.slider("🎒 Number of Bags", 1, 10, 2)
        hours = st.slider("🕐 Duration (Hours)", 1, 24, 3)
        
        total = (shop['price'] * hours) + (bags * 50) # Mock pricing logic
        
        st.markdown(f"### Total: ₹{total}")
        
        if st.button("Confirm & Pay"):
            st.session_state.page = 'success'
            st.rerun()

def success_page():
    st.balloons()
    st_lottie(load_lottieurl(LOTTIE_SUCCESS), height=200, key="success")
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: #1E1E1E; border-radius: 20px; border: 2px solid #00E676;">
        <h1>Booking Confirmed!</h1>
        <p>Show this QR Code at the counter</p>
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=ShadeStoreBooking123" style="border-radius:10px; margin: 10px;">
        <h3>OTP: 8821</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Return Home"):
        st.session_state.page = 'home'
        st.rerun()

# --- 6. MAIN ROUTER ---
if st.session_state.page == 'splash':
    splash_screen()
elif st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'booking':
    booking_page()
elif st.session_state.page == 'success':
    success_page()

# --- 7. FOOTER ---
st.markdown("---")
st.markdown("""
<div class="footer-brand">
    🚀 <b>Powered by Yash Bhati</b><br>
    <span style="font-size:0.8rem; opacity:0.7;">Vibecoded in Gurugram • © 2026 ShadeStore Inc.</span>
</div>
""", unsafe_allow_html=True)
