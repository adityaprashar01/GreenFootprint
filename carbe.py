import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Emission factors for different countries
EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,  # kgCO2/km
        "Electricity": 0.82,     # kgCO2/kWh
        "Diet": 2.5,             # kgCO2 per kg of food
        "Waste": 0.1,            # kgCO2/kg of waste
        "Flights": 0.09          # kgCO2 per km (domestic flights)
    },
    "USA": {
        "Transportation": 0.23,
        "Electricity": 0.45,
        "Diet": 3.2,
        "Waste": 0.12,
        "Flights": 0.13
    },
    "China": {
        "Transportation": 0.18,
        "Electricity": 0.7,
        "Diet": 2.8,
        "Waste": 0.15,
        "Flights": 0.1
    },
    "UK": {
        "Transportation": 0.2,
        "Electricity": 0.25,
        "Diet": 2.4,
        "Waste": 0.11,
        "Flights": 0.08
    },
    "Germany": {
        "Transportation": 0.22,
        "Electricity": 0.3,
        "Diet": 2.6,
        "Waste": 0.13,
        "Flights": 0.11
    }
}

# Page configuration
st.set_page_config(layout="wide", page_title="🌱 GreenFootprint")
st.title("🌱 **Personal Carbon Calculator App**")
st.subheader("Calculate your carbon footprint, visualize insights, and explore ways to reduce it! 🌱")

st.markdown("### 🌏 **Your Country**")
country = st.selectbox("Select your country", ["India", "USA", "China", "UK", "Germany"])

# User Inputs
st.markdown("### 📝 **Activity Details**")
col1, col2, col3 = st.columns(3)

# Transportation details
with col1:
    st.subheader("🚗 Transportation")
    daily_distance = st.slider("Daily commute distance (in km)", 0.0, 200.0, key="daily_distance_input")
    st.subheader("✈️ Flights")
    flights_distance = st.number_input("Annual flight distance (in km)", 0.0, 50000.0, key="flights_input")
    st.markdown("Top countries for air travel emissions:")
    st.info("1️⃣ China\n2️⃣ India\n3️⃣ USA\n4️⃣ UK\n5️⃣ Germany")

# Electricity usage
with col2:
    st.subheader("💡 Energy Usage")
    monthly_electricity = st.slider("Monthly electricity consumption (in kWh)", 0.0, 2000.0, key="electricity_input")

# Diet and waste
with col3:
    st.subheader("🍲 Diet & 🗑 Waste")
    daily_meals = st.slider("Number of meals per day", 0, 10, key="meals_input")
    weekly_waste = st.slider("Weekly waste generation (in kg)", 0.0, 50.0, key="waste_input")

# Normalize Inputs
annual_distance = daily_distance * 365 if daily_distance > 0 else 0
annual_electricity = monthly_electricity * 12 if monthly_electricity > 0 else 0
annual_meals = daily_meals * 365 if daily_meals > 0 else 0
annual_waste = weekly_waste * 52 if weekly_waste > 0 else 0

# Define categories and values globally (placeholders)
categories = ["Transportation", "Flights", "Electricity", "Diet", "Waste"]
values = [
    0,  # Transportation emissions (placeholder)
    0,  # Flights emissions (placeholder)
    0,  # Electricity emissions (placeholder)
    0,  # Diet emissions (placeholder)
    0   # Waste emissions (placeholder)
]

# Calculate Carbon Emissions based on the selected country
transportation_emissions = EMISSION_FACTORS[country]['Transportation'] * annual_distance
electricity_emissions = EMISSION_FACTORS[country]['Electricity'] * annual_electricity
diet_emissions = EMISSION_FACTORS[country]['Diet'] * annual_meals  # Assuming 1kg per meal
waste_emissions = EMISSION_FACTORS[country]['Waste'] * annual_waste
flights_emissions = EMISSION_FACTORS[country]['Flights'] * flights_distance

# Update values with calculated emissions
values = [
    round(transportation_emissions / 1000, 3),
    round(flights_emissions / 1000, 3),
    round(electricity_emissions / 1000, 3),
    round(diet_emissions / 1000, 3),
    round(waste_emissions / 1000, 3)
]

# Display Results
if st.button("Calculate CO2 Emissions"):
    st.header("🌟 Results")
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("🧮 **Carbon Emissions by Category**")
        st.info(f"🚗 **Transportation emissions**: {values[0]} tonnes CO2/year")
        st.info(f"✈️ **Flight emissions**: {values[1]} tonnes CO2/year")
        st.info(f"💡 **Electricity emissions**: {values[2]} tonnes CO2/year")
        st.info(f"🍲 **Diet emissions**: {values[3]} tonnes CO2/year")
        st.info(f"🗑 **Waste emissions**: {values[4]} tonnes CO2/year")

    with col5:
        total_emission = sum(values)
        st.subheader("🌏 **Total Carbon Footprint**")
        st.success(f"🌟 **Your Total Carbon Footprint**: {total_emission} tonnes CO2/year")
        st.warning(
            f"🌍 The average CO2 emissions per capita in {country} vary. Make sustainable lifestyle choices to reduce your emissions! 🌱"
        )

    # Visualization
    st.markdown("### 📊 **Carbon Footprint Breakdown**")
    st.bar_chart(pd.DataFrame({"Category": categories, "Emissions (tonnes)": values}).set_index("Category"))

    # Pie chart
    st.markdown("### 🍰 **Emissions Contribution by Category**")
    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig)

    # Additional Insights
    st.markdown("### 🔍 **Insights**")
    col6, col7 = st.columns(2)
    with col6:
        st.markdown("#### 🌟 **Top 3 Emitters in Your Data**")
        top_emitters = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)[:3]
        for i, (category, emission) in enumerate(top_emitters, start=1):
            st.info(f"{i}. **{category}**: {emission} tonnes CO2/year")

    with col7:
        st.markdown("#### 🌍 **Global Impact**")
        st.markdown(
            f"""
            - 🌏 **Average Emissions in {country}**: Data varies based on individual activity.
            - 🌎 **World's Average Emissions**: 4.47 tonnes CO2 per person.
            - 💡 **Action Tip**: Adopt sustainable practices to minimize your carbon footprint!
            """
        )
