import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Location Logger", layout="centered")
st.title("📍 Location Logger App")

location = streamlit_geolocation()

if location:
    st.success("Location access granted! ✅")
    st.write(f"**Latitude:** {location['latitude']}")
    st.write(f"**Longitude:** {location['longitude']}")
    st.write(f"**Accuracy:** {location['accuracy']} meters")

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

    # Save updated data
    df.to_csv(csv_file, index=False)
    st.success("📄 Location saved successfully!")

    with st.expander("📊 Show All Saved Locations"):
        st.dataframe(df)

else:
    st.warning("⚠️ Please allow location access in your browser.")
