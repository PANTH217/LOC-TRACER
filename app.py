import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="📍 Location Logger", layout="centered")
st.title("📍 Automatic Location Logger")

# 🔁 Automatically request location on page load
location = streamlit_geolocation()

if location:
    st.success("✅ Location access granted!")
    st.write(f"**Latitude:** {location['latitude']}")
    st.write(f"**Longitude:** {location['longitude']}")
    st.write(f"**Accuracy:** {location['accuracy']} meters")

    # Create a new record with timestamp
    record = {
        "timestamp": datetime.now().isoformat(),
        "latitude": location['latitude'],
        "longitude": location['longitude'],
        "accuracy": location['accuracy']
    }

    csv_file = "location_records.csv"

    # Check if file exists and is not empty
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        df = pd.read_csv(csv_file)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    # Save to CSV
    df.to_csv(csv_file, index=False)

    st.success("📄 Location saved!")

    with st.expander("📊 View All Saved Locations"):
        st.dataframe(df)

else:
    st.info("🔐 Waiting for location access. Please allow it in your browser.")
