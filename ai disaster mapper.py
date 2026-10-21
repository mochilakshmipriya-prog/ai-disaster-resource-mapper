
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AI Disaster Resource Mapper",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 AI Disaster Resource Mapper")
st.write(
    "An interactive dashboard for mapping disaster areas "
    "and displaying emergency resources."
)

# ---------------- SAMPLE DISASTER DATA ----------------
disasters = pd.DataFrame([
    {
        "Area": "Area A",
        "Disaster": "Flood",
        "Severity": 5,
        "Affected People": 900,
        "Latitude": 17.3850,
        "Longitude": 78.4867
    },
    {
        "Area": "Area B",
        "Disaster": "Cyclone",
        "Severity": 4,
        "Affected People": 600,
        "Latitude": 17.4500,
        "Longitude": 78.3800
    },
    {
        "Area": "Area C",
        "Disaster": "Earthquake",
        "Severity": 3,
        "Affected People": 250,
        "Latitude": 17.3300,
        "Longitude": 78.5500
    },
    {
        "Area": "Area D",
        "Disaster": "Flood",
        "Severity": 2,
        "Affected People": 150,
        "Latitude": 17.4100,
        "Longitude": 78.5200
    }
])

# ---------------- SAMPLE RESOURCE DATA ----------------
resources = pd.DataFrame([
    {
        "Resource": "City Hospital",
        "Type": "Hospital",
        "Status": "Available",
        "Latitude": 17.3900,
        "Longitude": 78.4800
    },
    {
        "Resource": "Community Shelter",
        "Type": "Shelter",
        "Status": "Available",
        "Latitude": 17.4400,
        "Longitude": 78.4000
    },
    {
        "Resource": "Food Distribution Center",
        "Type": "Food Center",
        "Status": "Limited",
        "Latitude": 17.3400,
        "Longitude": 78.5400
    },
    {
        "Resource": "Medical Aid Center",
        "Type": "Medical Aid",
        "Status": "Available",
        "Latitude": 17.3700,
        "Longitude": 78.5100
    },
    {
        "Resource": "Relief Camp",
        "Type": "Shelter",
        "Status": "Available",
        "Latitude": 17.4200,
        "Longitude": 78.4600
    }
])

# ---------------- PRIORITY CALCULATION ----------------
# Demonstration score, not a trained AI model.

disasters["Priority Score"] = (
    disasters["Severity"] * 15
    + disasters["Affected People"] / 30
).clip(upper=100).round(1)


def get_priority(score):
    if score >= 80:
        return "High"
    elif score >= 50:
        return "Medium"
    return "Low"


disasters["Priority"] = (
    disasters["Priority Score"].apply(get_priority)
)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("⚙️ Map Filters")

disaster_options = ["All"] + sorted(
    disasters["Disaster"].unique().tolist()
)

resource_options = ["All"] + sorted(
    resources["Type"].unique().tolist()
)

selected_disaster = st.sidebar.selectbox(
    "Select disaster type",
    disaster_options
)

selected_resource = st.sidebar.selectbox(
    "Select resource type",
    resource_options
)

# ---------------- FILTER DATA ----------------
filtered_disasters = disasters.copy()
filtered_resources = resources.copy()

if selected_disaster != "All":
    filtered_disasters = filtered_disasters[
        filtered_disasters["Disaster"] == selected_disaster
    ]

if selected_resource != "All":
    filtered_resources = filtered_resources[
        filtered_resources["Type"] == selected_resource
    ]

# ---------------- DASHBOARD METRICS ----------------
st.subheader("📊 Disaster Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Disaster Areas",
    len(filtered_disasters)
)

col2.metric(
    "Affected People",
    int(filtered_disasters["Affected People"].sum())
)

col3.metric(
    "High Priority Areas",
    int(
        (filtered_disasters["Priority"] == "High").sum()
    )
)

# ---------------- INTERACTIVE MAP ----------------
st.subheader("🗺️ Disaster and Emergency Resource Map")

disaster_map = folium.Map(
    location=[17.3850, 78.4867],
    zoom_start=11
)

# Add disaster markers
priority_colors = {
    "High": "red",
    "Medium": "orange",
    "Low": "green"
}

for _, row in filtered_disasters.iterrows():

    popup_text = (
        f"Area: {row['Area']}<br>"
        f"Disaster: {row['Disaster']}<br>"
        f"Severity: {row['Severity']}/5<br>"
        f"Affected people: {row['Affected People']}<br>"
        f"Priority: {row['Priority']}<br>"
        f"Score: {row['Priority Score']}"
    )

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=9,
        color=priority_colors[row["Priority"]],
        fill=True,
        fill_opacity=0.8,
        popup=folium.Popup(
            popup_text,
            max_width=300
        ),
        tooltip=f"{row['Area']} - {row['Priority']}"
    ).add_to(disaster_map)

# Add resource markers
resource_colors = {
    "Hospital": "blue",
    "Shelter": "purple",
    "Food Center": "green",
    "Medical Aid": "darkblue"
}

for _, row in filtered_resources.iterrows():

    popup_text = (
        f"Resource: {row['Resource']}<br>"
        f"Type: {row['Type']}<br>"
        f"Status: {row['Status']}"
    )

    folium.Marker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        popup=folium.Popup(
            popup_text,
            max_width=300
        ),
        tooltip=row["Resource"],
        icon=folium.Icon(
            color=resource_colors.get(
                row["Type"], "gray"
            ),
            icon="info-sign"
        )
    ).add_to(disaster_map)

st_folium(
    disaster_map,
    height=500,
    use_container_width=True,
    key="disaster_map"
)

st.caption(
    "Red = High priority, Orange = Medium priority, "
    "Green = Low priority. Map pins indicate resources."
)

# ---------------- DISASTER REPORT ----------------
st.subheader("🚨 Disaster Priority Report")

st.dataframe(
    filtered_disasters,
    use_container_width=True,
    hide_index=True
)

# ---------------- RESOURCE REPORT ----------------
st.subheader("🏥 Emergency Resources")

st.dataframe(
    filtered_resources,
    use_container_width=True,
    hide_index=True
)

# ---------------- DOWNLOAD REPORT ----------------
csv_data = filtered_disasters.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Disaster Report",
    data=csv_data,
    file_name="disaster_report.csv",
    mime="text/csv"
)

# ---------------- INFORMATION ----------------
st.info(
    "This is a demonstration project using sample data. "
    "The priority score uses a simple formula, not a trained "
    "machine-learning model. Locations and resource status "
    "are not verified or live."
)

st.warning(
    "Do not use this sample application to make real "
    "emergency response decisions."
)
