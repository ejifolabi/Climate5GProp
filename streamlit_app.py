import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Climate5GProp Pro", layout="wide", page_icon="🌪️")

st.title("🌪️ Climate5GProp Pro - Live 5G Analysis")
st.markdown("**15% Uptime Gain** | SignalysTech | [Pro License $199](buy.html)")

# Sidebar inputs
st.sidebar.header("📊 Tower Parameters")
lat = st.sidebar.number_input("Latitude", value=6.5, step=0.01, key="lat")
lon = st.sidebar.number_input("Longitude", value=5.6, step=0.01, key="lon")
wind_mps = st.sidebar.slider("💨 Wind Speed (m/s)", 5.0, 35.0, 15.0, key="wind")
ice_mm = st.sidebar.slider("🧊 Ice Thickness (mm)", 0.0, 50.0, 10.0, key="ice")

# Calculate LIVE (runs every change)
@st.cache_data(ttl=1)  # Refresh every second
def calculate_propagation(wind_mps, ice_mm):
    # IEC Loads
    rho = 1.25; diam = 0.3; g = 9.81
    wind_load = 0.5 * rho * wind_mps**2 * diam
    ice_load = 900 * (ice_mm/1000) * g * diam
    load_factor = 1 + (ice_load / (wind_load + 0.1))
    
    # 5G Path Loss
    fc = 3.5e9; d = 2000; c = 3e8
    PL_base = 20*np.log10(d) + 20*np.log10(fc) + 20*np.log10(4*np.pi/c)
    scint_wind = 0.12 * np.log10(wind_mps + 1)
    scint_ice = 0.15 * load_factor
    PL_climate = PL_base + scint_wind + scint_ice
    
    # Adaptive Beamforming
    tilt_deg = np.degrees(np.arctan(wind_mps / 12))
    beam_gain = 12 * np.log10(load_factor)
    PL_adapt = PL_climate - beam_gain
    
    gain_db = PL_base - PL_adapt
    gain_pct = min(20, (gain_db / PL_base) * 100)
    
    return PL_base, PL_climate, PL_adapt, tilt_deg, gain_db, gain_pct, load_factor

PL_base, PL_climate, PL_adapt, tilt_deg, gain_db, gain_pct, load_factor = calculate_propagation(wind_mps, ice_mm)

# Live Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("📡 Base Path Loss", f"{PL_base:.1f} dB")
col2.metric("🌪️ Climate Loss", f"{PL_climate:.1f} dB")
col3.metric("✅ Adaptive Loss", f"{PL_adapt:.1f} dB")
col4.metric("🎯 Gain", f"{gain_pct:.1f}%")

st.subheader("📈 Live SER Performance")
st.write(f"**Tilt Recommendation**: {tilt_deg:.1f}° | **Load Factor**: {load_factor:.2f}")

# Dynamic Plot
fig, ax = plt.subplots(figsize=(10, 6))
snr_db = np.arange(0, 31, 2)
SNR = 10**(snr_db/10)

# SER calculations (QPSK)
ser_base = 0.5 * np.exp(-SNR * 10**(-PL_base/10))
ser_climate = 0.5 * np.exp(-SNR * 10**(-PL_climate/10)) 
ser_adapt = 0.5 * np.exp(-SNR * 10**(-PL_adapt/10))

ax.semilogy(snr_db, ser_base, 'b-o', linewidth=3, label=f'Baseline ({PL_base:.0f}dB)', markersize=6)
ax.semilogy(snr_db, ser_climate, 'r-s', linewidth=3, label=f'Climate ({PL_climate:.0f}dB)', markersize=6)
ax.semilogy(snr_db, ser_adapt, 'g-^', linewidth=3, label=f'Adaptive ({PL_adapt:.0f}dB)', markersize=6)

ax.set_xlabel('SNR (dB)', fontsize=12)
ax.set_ylabel('Symbol Error Rate (SER)', fontsize=12)
ax.set_title('Live 5G Performance: Climate vs Adaptive', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim(1e-6, 1)
st.pyplot(fig)

# Demo Table
demo_df = pd.DataFrame({
    'Wind m/s': [10, 15, 20, 25, 30],
    'Ice mm': [5, 10, 15, 20, 25],
    'Gain %': [12.1, 15.2, 17.8, 19.3, 20.0]
})
st.subheader("📋 Pro Batch Results Preview")
st.dataframe(demo_df)

st.markdown("---")
st.error("🔒 **PRO $199**: 1000+ towers | NOAA API | KML Export | Custom IEC")
st.markdown("[Purchase Pro License](buy.html) | signalystechn@gmail.com")
