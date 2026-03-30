import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.markdown("""
# 🌪️ Climate5GProp Pro - Live Demo
**SignalysTech | 5G Propagation Tool** | [Pro $199](buy.html)
""")

# Inputs
col1, col2, col3, col4 = st.columns(4)
wind = col1.slider("Wind Speed", 5, 35, 15)
ice = col2.slider("Ice mm", 0, 50, 10)
snr_test = col3.slider("Test SNR", 10, 30, 20)
dist_km = col4.slider("Distance km", 1, 10, 2)

# Live calculations
PL_base = 32.4 + 20*np.log10(dist_km) + 20*np.log10(3.5)  # 3.5GHz simplified
scint_wind = 0.2 * np.log10(wind + 1)
scint_ice = 0.1 * ice / 5
PL_climate = PL_base + scint_wind + scint_ice
PL_adapt = PL_climate - 5  # Beamforming gain
gain_db = PL_climate - PL_adapt

# Display
st.header("📊 Live Results")
col1, col2, col3 = st.columns(3)
col1.metric("📡 Base Loss", f"{PL_base:.1f} dB")
col2.metric("🌪️ Climate Loss", f"{PL_climate:.1f} dB") 
col3.metric("✅ Adaptive", f"{PL_adapt:.1f} dB")

st.metric("🎯 Total Gain", f"{gain_db:.1f} dB ({gain_db/PL_base*100:.0f}%)")

# CORRECT Plot - Simple exponential decay
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: SER vs SNR
snr = np.linspace(0, 30, 100)
ser_base = np.exp(-0.3 * snr * 10**(-PL_base/20))
ser_climate = np.exp(-0.3 * snr * 10**(-PL_climate/20))
ser_adapt = np.exp(-0.3 * snr * 10**(-PL_adapt/20))

ax1.semilogy(snr, ser_base, 'b-', linewidth=4, label='Baseline')
ax1.semilogy(snr, ser_climate, 'r--', linewidth=4, label='Climate Effect')
ax1.semilogy(snr, ser_adapt, 'g-', linewidth=4, label='Adaptive (Recommended)')
ax1.set_title(f'SER @ {snr_test} dB SNR\nAdaptive BEST', fontsize=12)
ax1.set_xlabel('SNR (dB)')
ax1.set_ylabel('Error Rate')
ax1.legend()
ax1.grid(True)
ax1.set_ylim(1e-4, 1)

# Plot 2: Gain breakdown
categories = ['Wind\nEffect', 'Ice\nEffect', 'Beam\nGain']
values = [scint_wind, scint_ice, gain_db]
colors = ['orange', 'cyan', 'green']
ax2.bar(categories, values, color=colors)
ax2.set_title('Gain Breakdown')
ax2.set_ylabel('dB')

plt.tight_layout()
st.pyplot(fig)

# SER @ test SNR
ser_test_base = np.exp(-0.3 * snr_test * 10**(-PL_base/20))
ser_test_adapt = np.exp(-0.3 * snr_test * 10**(-PL_adapt/20))
st.subheader(f"🎯 At {snr_test}dB SNR:")
col1.metric("Baseline SER", f"{ser_test_base:.2e}")
col2.metric("Adaptive SER", f"{ser_test_adapt:.2e}")
col3.metric("Improvement", f"{(1-ser_test_adapt/ser_test_base)*100:.0f}%")

st.markdown("---")
st.markdown("""
**🔒 PRO FEATURES ($199)**  
✅ 1000+ tower batch  
✅ Live NOAA API  
✅ KML/Google Earth export  
✅ Custom IEC profiles  
[Buy Pro License](buy.html)
""")
