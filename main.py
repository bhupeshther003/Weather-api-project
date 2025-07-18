import streamlit as st
import requests
import matplotlib.pyplot as plt

API_KEY = "e5850a382a5ed72e70e8d6b5a6401e02"  # Replace with your valid API key

# ----------------------
# Utility Functions
# ----------------------
def get_theme_icon(description, temp):
    desc = description.lower()
    if "rain" in desc:
        return "🌧️", "rainy"
    elif "snow" in desc:
        return "❄️", "snowy"
    elif "thunder" in desc:
        return "⛈️", "thunder"
    elif temp >= 35:
        return "🔥", "hot"
    elif 25 <= temp < 35:
        return "☀️", "warm"
    elif 15 <= temp < 25:
        return "🌤️", "cool"
    else:
        return "🌫️", "cold"

def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            icon, theme = get_theme_icon(data["weather"][0]["description"], data["main"]["temp"])
            return {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "description": data["weather"][0]["description"].title(),
                "icon": icon,
                "theme": theme
            }
        else:
            return None
    except:
        return None

def get_recommendation(desc, temp):
    desc = desc.lower()
    if "rain" in desc:
        return "🌧️ Carry an umbrella"
    elif "snow" in desc:
        return "❄️ Wear warm clothes"
    elif "thunder" in desc:
        return "⛈️ Stay indoors if possible"
    elif temp < 15:
        return "🧥 Wear a jacket"
    elif temp > 35:
        return "🧃 Stay hydrated and carry water"
    else:
        return "🌤️ Weather is pleasant"

def set_background(theme):
    background_urls = {
        "rainy": "https://wallpaperaccess.com/full/1358805.jpg",
        "snowy": "hhttps://images.unsplash.com/photo-1457269449834-928af64c684d?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "thunder": "https://wallpaperbat.com/img/8751213-lightning-wallpaper-thunder-sky-clouds.jpg",
        "hot": "https://wallpaperaccess.com/full/10584973.jpg",
        "warm": "https://wallpaperbat.com/img/133198341-warm-background.jpg",
        "cool": "https://wallpaperaccess.com/full/2942884.jpg",
        "cold": "https://png.pngtree.com/thumb_back/fw800/background/20240617/pngtree-drawn-on-the-snow-temperature-symbols-denoting-negative-very-cold-weather-image_15768757.jpg"
    }

    if theme in background_urls:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("{background_urls[theme]}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# ----------------------
# Streamlit UI
# ----------------------
st.set_page_config(page_title="Real-Time Weather", layout="centered")
st.title("☁️ Real-Time Weather Forecasting")

tab1, tab2 = st.tabs(["📍 Single City Weather", "📊 Compare Cities"])

# ----------------------
# Tab 1: Single City
# ----------------------
with tab1:
    city = st.text_input("Enter a city name", "")

    if st.button("Get Weather"):
        weather = get_weather(city)

        if weather:
            set_background(weather["theme"])  # change background

            st.success(f"{weather['icon']} Weather in {weather['city']}")
            col1, col2 = st.columns(2)
            col1.metric("🌡️ Temperature", f"{weather['temp']}°C")
            col1.metric("💧 Humidity", f"{weather['humidity']}%")
            col1.metric("🌬️ Wind Speed", f"{weather['wind']} m/s")
            col2.markdown(f"**🌈 Condition:** {weather['description']}")
            col2.markdown(f"**📝 Suggestion:** {get_recommendation(weather['description'], weather['temp'])}")
        else:
            st.error("City not found or error fetching data.")

# ----------------------
# Tab 2: Compare Cities
# ----------------------
with tab2:
    st.write("Enter up to 4 cities to compare:")
    col1, col2 = st.columns(2)
    city1 = col1.text_input("City 1", "Mumbai")
    city2 = col2.text_input("City 2", "Delhi")
    city3 = col1.text_input("City 3", "Chennai")
    city4 = col2.text_input("City 4", "Nagpur")

    if st.button("Compare"):
        cities = [city1, city2, city3, city4]
        names, temps, humidity, wind, descs = [], [], [], [], []

        for c in cities:
            if c.strip():
                data = get_weather(c.strip())
                if data:
                    names.append(data["city"])
                    temps.append(data["temp"])
                    humidity.append(data["humidity"])
                    wind.append(data["wind"])
                    descs.append(data["description"])

        if names:
            st.subheader("📊 Weather Comparison Chart")
            fig, ax = plt.subplots(figsize=(10, 5))
            x = range(len(names))
            ax.bar(x, temps, width=0.2, label="Temp (°C)", align='center')
            ax.bar([i + 0.2 for i in x], humidity, width=0.2, label="Humidity (%)", align='center')
            ax.bar([i + 0.4 for i in x], wind, width=0.2, label="Wind (m/s)", align='center')
            ax.set_xticks([i + 0.2 for i in x])
            ax.set_xticklabels(names)
            ax.set_ylabel("Values")
            ax.set_title("City Weather Comparison")
            ax.legend()
            st.pyplot(fig)

            st.subheader("🌦️ Descriptions")
            for n, d in zip(names, descs):
                st.write(f"**{n}**: {d}")
        else:
            st.warning("No valid data to compare.")
