import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time
import random
import pandas as pd

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="ShadeStore | Secure Luggage Network",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ROBUST ASSET LOADER (Crash-Proof) ---
@st.cache_data
def load_lottieurl(url: str):
    """
    Safely loads Lottie animations. 
    If it fails (network error), returns None without crashing the app.
    """
    try:
        r = requests.get(url, timeout=5) # 5s timeout to prevent hanging
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        return None

# Reliable Animation URLs
LOTTIE_LOADING = "https://assets9.lottiefiles.com/packages/lf20_s72855.json" # Reliable luggage loop
LOTTIE_SUCCESS = "https://assets5.lottiefiles.com/packages/lf20_jbrw3hcz.json" # Green Check
LOTTIE_MAP = "https://assets3.lottiefiles.com/packages/lf20_fw09tn.json" # Map pin location

# --- 3. ADVANCED AESTHETICS (Dark Mode + Glassmorphism) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    /* Global Font */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #0E1117; 
        color: #FFFFFF;
    }

    /* Primary Button (Gradient) */
    .stButton>button {
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
        color: white;
        border: none;
        border-radius: 12px;
        height: 55px;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(221, 36, 118, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(221, 36, 118, 0.5);
    }

    /* Glassmorphism Shop Cards */
    .shop-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
        transition: border-color 0.3s ease;
    }
    .shop-card:hover {
        border-color: #DD2476;
        background: rgba(255, 255, 255, 0.08);
    }

    /* Trust Tags */
    .tag-trust {
        background-color: #00E676;
        color: #000;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 800;
        display: inline-block;
        margin-right: 5px;
    }
    
    .price-display {
        color: #FF512F;
        font-weight: 800;
        font-size: 1.4rem;
    }

    /* Footer Branding */
    .footer-brand {
        text-align: center;
        margin-top: 60px;
        padding: 30px;
        border-top: 1px solid rgba(255,255,255,0.1);
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SESSION STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = 'splash'
if 'selected_shop' not in st.session_state:
    st.session_state.selected_shop = None
if 'booking_data' not in st.session_state:
    st.session_state.booking_data = {}

# --- 5. MOCK DATA ---
SHOPS = [
    {
        "id": 1, 
        "name": "Metro Heights Hotel", 
        "area": "New Delhi Railway Stn.", 
        "lat": 28.6415, 
        "lon": 77.2205, 
        "rating": 4.9, 
        "price": 100, 
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
        "features": ["24/7 CCTV", "Verified"]
    },
    {
        "id": 2, 
        "name": "CyberHub Travels", 
        "area": "Gurugram Cyber City", 
        "lat": 28.4950, 
        "lon": 77.0895, 
        "rating": 4.7, 
        "price": 150, 
        "image": "https://images.unsplash.com/photo-1527786356703-4b100091cd2c?w=800&q=80",
        "features": ["Insurance", "AC Storage"]
    },
    {
        "id": 3, 
        "name": "Backpacker's Cafe", 
        "area": "Paharganj Main Bazar", 
        "lat": 28.6356, 
        "lon": 77.2173, 
        "rating": 4.3, 
        "price": 80, 
        "image": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800&q=80",
        "features": ["Low Cost", "Open Late"]
    },
]

# --- 6. PAGE FUNCTIONS ---

def render_splash():
    """Intro animation screen"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.write("")
        # Try loading animation, if fail, show text only
        lottie_json = load_lottieurl(LOTTIE_LOADING)
        if lottie_json:
            st_lottie(lottie_json, height=250, key="loading_anim")
        else:
            st.info("Loading ShadeStore Secure Network...")
            
        st.markdown("<h1 style='text-align: center;'>ShadeStore</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Secure Luggage Network</p>", unsafe_allow_html=True)
    
    # Simulate loading time then redirect
    time.sleep(3)
    st.session_state.page = 'home'
    st.rerun()

def render_home():
    # Navbar area
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("🎒 ShadeStore")
        st.caption("Drop your bags. Explore the city.")
    with c2:
        st.write("")
        st.markdown("📍 **Gurugram**")

    # Search Simulation
    st.text_input("🔍 Search Location", placeholder="Try 'Connaught Place' or 'Sector 29'")

    # Map Visualization
    st.subheader("🗺️ Nearby Secure Spots")
    map_data = pd.DataFrame(SHOPS)
    st.map(map_data, latitude='lat', longitude='lon', size=25, color='#FF512F')

    # Shop Listings
    st.subheader("🔥 Top Rated Partners")
    
    for shop in SHOPS:
        # Create a container for the card
        with st.container():
            # Inject HTML for the card layout
            st.markdown(f"""
            <div class="shop-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0;">{shop['name']}</h3>
                    <span class="price-display">₹{shop['price']}<small style="font-size:0.8rem; color:#888;">/hr</small></span>
                </div>
                <p style="color:#AAA; margin-top:5px;">📍 {shop['area']} &nbsp; | &nbsp; ⭐ {shop['rating']}</p>
                <div style="margin-top:10px;">
                    {' '.join([f'<span class="tag-trust">🛡️ {f}</span>' for f in shop['features']])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Streamlit button to handle the click logic (HTML buttons can't trigger Python easily)
            col_act1, col_act2 = st.columns([3, 1])
            with col_act2:
                if st.button("Book Now", key=f"btn_{shop['id']}"):
                    st.session_state.selected_shop = shop
                    st.session_state.page = 'booking'
                    st.rerun()

def render_booking():
    shop = st.session_state.selected_shop
    
    # Back button
    if st.button("⬅ Back to Search"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown("---")
    
    # Two column layout
    c_img, c_details = st.columns([1, 1])
    
    with c_img:
        st.image(shop['image'], use_container_width=True, caption=shop['name'])
        st.success("✅ **Verified Partner:** This location has passed our 3-step KYC process.")
        
    with c_details:
        st.markdown(f"## Booking at {shop['name']}")
        st.markdown(f"📍 {shop['area']}")
        
        st.markdown("### ⚙️ Booking Details")
        bags = st.slider("Number of Bags", 1, 10, 2)
        hours = st.slider("Duration (Hours)", 1, 24, 3)
        
        # Calculation
        total = (shop['price'] * hours) + (bags * 50) # Mock base fee + bag fee
        
        st.markdown(f"""
        <div style="background:#1E1E1E; padding:15px; border-radius:15px; border:1px solid #333; margin:20px 0;">
            <div style="display:flex; justify-content:space-between;">
                <span>Storage Fee ({hours} hrs)</span>
                <span>₹{shop['price'] * hours}</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span>Service & Insurance Fee</span>
                <span>₹{bags * 50}</span>
            </div>
            <hr style="border-color:#333;">
            <div style="display:flex; justify-content:space-between; font-size:1.5rem; font-weight:bold; color:#00E676;">
                <span>Total</span>
                <span>₹{total}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Confirm Button
        if st.button(f"Pay ₹{total} & Secure Spot"):
            with st.spinner("Encrypting Booking Details..."):
                time.sleep(2) # Fake loading
                st.session_state.booking_data = {
                    "otp": random.randint(1000, 9999),
                    "id": f"SHD-{random.randint(10000, 99999)}",
                    "total": total
                }
                st.session_state.page = 'success'
                st.rerun()

def render_success():
    data = st.session_state.booking_data
    
    st.balloons()
    
    # Lottie Success Animation
    lottie_success = load_lottieurl(LOTTIE_SUCCESS)
    if lottie_success:
        st_lottie(lottie_success, height=150, key="success_anim")
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background: rgba(0, 230, 118, 0.1); border-radius: 20px; border: 2px solid #00E676;">
        <h1 style="color: #00E676; margin:0;">Booking Confirmed!</h1>
        <p style="color: #AAA;">Show this QR Code to the shopkeeper</p>
        
        <div style="background: white; padding: 10px; display: inline-block; border-radius: 10px; margin: 20px 0;">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={data['id']}" width="150" height="150">
        </div>
        
        <h2 style="font-size: 3em; letter-spacing: 5px; margin: 0; color: #FFF;">{data['otp']}</h2>
        <p>Secret PIN</p>
        
        <p style="margin-top: 20px; font-family: monospace;">Booking ID: {data['id']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("⚠️ **Reminder:** Ensure the shopkeeper applies the Green Security Seal before you leave.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Go to Home"):
        st.session_state.page = 'home'
        st.rerun()

# --- 7. MAIN ROUTER ---

if st.session_state.page == 'splash':
    render_splash()
elif st.session_state.page == 'home':
    render_home()
elif st.session_state.page == 'booking':
    render_booking()
elif st.session_state.page == 'success':
    render_success()

# --- 8. FOOTER ---
st.markdown("""
<div class="footer-brand">
    🚀 <b>Powered by Yash Bhati</b><br>
    <span style="font-size:0.8rem; opacity:0.7;">Vibecoded in Gurugram • © 2026 ShadeStore Inc.</span>
</div>
""", unsafe_allow_html=True)
    
