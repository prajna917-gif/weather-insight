import streamlit as st
import requests
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
 
# ---- Page Setup ----
st.set_page_config(page_title="Weather Insight", page_icon="🌦️", layout="wide")
 
WEATHER_API_KEY = "db2c40ce39f3b033326671cb74c1da85"
NEWS_API_KEY = "163ed26700e14946802161eb85a08983"
model = joblib.load("rain_model.pkl")
 
# ---- Carousel Background Images ----
CAROUSEL_IMAGES = [
    "https://images.unsplash.com/photo-1601297183305-6df142704ea2?auto=format&fit=crop&w=1920&q=80",  # clear sky
    "https://images.unsplash.com/photo-1499956827185-0d63ee78a910?auto=format&fit=crop&w=1920&q=80",  # clouds
    "https://images.unsplash.com/photo-1519692933481-e162a57d6721?auto=format&fit=crop&w=1920&q=80",  # rain
    "https://images.unsplash.com/photo-1500674425229-f692875b0ab7?auto=format&fit=crop&w=1920&q=80",  # storm
    "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1920&q=80",  # night sky
]
 
N = len(CAROUSEL_IMAGES)
TOTAL_SECONDS = N * 6          # each photo gets a 6-second slot
SLOT_PERCENT = 100 / N
FADE_PERCENT = 3               # how much of the slot is used for the fade transition
 
# Build the slide divs, each staggered by its own delay
slide_divs = ""
for i, url in enumerate(CAROUSEL_IMAGES):
    delay = i * (TOTAL_SECONDS / N)
    slide_divs += f'<div class="bg-slide" style="background-image:url(\'{url}\'); animation-delay:{delay}s;"></div>\n'
 
carousel_css = f"""
.bg-carousel {{
    position: fixed; top:0; left:0; width:100%; height:100%; z-index:-2; overflow:hidden;
}}
.bg-slide {{
    position: absolute; top:0; left:0; width:100%; height:100%;
    background-size: cover; background-position: center;
    opacity: 0;
    animation-name: bgFade;
    animation-duration: {TOTAL_SECONDS}s;
    animation-iteration-count: infinite;
    animation-timing-function: ease-in-out;
}}
.bg-overlay {{
    position: fixed; top:0; left:0; width:100%; height:100%; z-index:-1;
    background: linear-gradient(rgba(8,12,18,0.82), rgba(8,12,18,0.82));
}}
@keyframes bgFade {{
    0% {{ opacity: 0; }}
    {FADE_PERCENT}% {{ opacity: 1; }}
    {SLOT_PERCENT - FADE_PERCENT}% {{ opacity: 1; }}
    {SLOT_PERCENT}% {{ opacity: 0; }}
    100% {{ opacity: 0; }}
}}
"""
 
st.markdown(f'<div class="bg-carousel">{slide_divs}</div><div class="bg-overlay"></div>', unsafe_allow_html=True)
 
def get_icon(code):
    if code < 300: return "⛈️"
    elif code < 400: return "🌦️"
    elif code < 600: return "🌧️"
    elif code < 700: return "❄️"
    elif code < 800: return "🌫️"
    elif code == 800: return "☀️"
    elif code < 803: return "🌤️"
    else: return "☁️"
 
# ---- Styling ----
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
 
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: 17px !important;
    }}
 
    .stApp {{
        background: transparent;
        color: white;
    }}
 
    {carousel_css}
 
    /* ---- Header ---- */
    .main-title {{
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }}
    .subtitle {{
        text-align: center;
        color: #cfd8dc;
        margin-bottom: 25px;
        font-size: 1.1rem !important;
        font-weight: 400;
    }}
 
    /* ---- Input Fields ---- */
    div[data-testid="stTextInput"] input {{
        background-color: rgba(255,255,255,0.08);
        color: white;
        border-radius: 14px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.25);
        font-size: 1rem !important;
    }}
    div[data-testid="stTextInput"] label {{
        font-size: 1 !important;
        font-weight: 600 !important;
    }}
 
    /* ---- Tabs ---- */
    button[data-baseweb="tab"] {{
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        padding: 10px 22px !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #4fc3f7 !important;
        border-bottom: 3px solid #4fc3f7 !important;
    }}
 
    /* ---- Cards ---- */
    .weather-card, .compare-card, .news-card, .forecast-card {{
        background: rgba(22, 28, 36, 0.6);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 28px;
        margin-top: 16px;
        text-align: center;
        backdrop-filter: blur(14px);
        box-shadow: 0 10px 40px rgba(0,0,0,0.45);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .weather-card:hover, .compare-card:hover, .forecast-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 14px 50px rgba(0,0,0,0.55);
    }}
 
    /* ---- Dashboard Metrics ---- */
    .metric-row {{ display: flex; justify-content: space-around; margin-top: 24px; flex-wrap: wrap; }}
    .metric-box {{ text-align: center; margin: 14px; }}
    .metric-value {{ font-size: 1.9rem !important; font-weight: 800; }}
    .metric-label {{ color: #cfd8dc; font-size: 0.9rem !important; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }}
 
    .prediction-card {{
        border-radius: 18px;
        padding: 24px;
        margin-top: 22px;
        text-align: center;
        font-size: 1.15rem !important;
        font-weight: 700;
    }}
    .rain-yes {{ background: rgba(255, 193, 7, 0.18); border: 1px solid rgba(255, 193, 7, 0.5); color: #ffca28; }}
    .rain-no {{ background: rgba(76, 175, 80, 0.18); border: 1px solid rgba(76, 175, 80, 0.5); color: #81c784; }}
 
    /* ---- News ---- */
    .news-card {{
        text-align: left !important;
        padding: 24px 28px;
        border-left: 4px solid #4fc3f7;
    }}
    .news-card:hover {{ background: rgba(35, 42, 52, 0.75); }}
    .news-title {{
        font-size: 1.1rem !important;
        font-weight: 700;
        line-height: 1.4;
        margin-bottom: 8px;
    }}
    .news-source {{
        font-size: 1.1rem !important;
        color: #4fc3f7;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
 
    h3 {{
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin-top: 30px !important;
        color: white !important;
    }}
    .broadcast-header {
    background: linear-gradient(90deg, #0c447c, #185fa5);
    padding: 12px 18px;
    border-radius: 12px 12px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}
.broadcast-title {
    color: white;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.5px;
}
.live-badge {
    color: #cfe4f7;
    font-size: 0.8rem;
    background: rgba(0,0,0,0.25);
    padding: 4px 12px;
    border-radius: 6px;
    font-weight: 600;
}
.chart-wrapper {
    background: rgba(10, 14, 20, 0.6);
    border-radius: 0 0 12px 12px;
    padding: 10px 10px 0px 10px;
    border: 1px solid rgba(255,255,255,0.08);
    border-top: none;
}
    </style>
""", unsafe_allow_html=True)
 
def convert_temp(temp_c, unit):
    return round(temp_c * 9/5 + 32, 1) if unit == "°F" else round(temp_c, 1)
 
def format_time(unix_ts, tz_offset):
    dt = datetime.utcfromtimestamp(unix_ts + tz_offset)
    return dt.strftime("%I:%M %p")
 
def fetch_current(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    return requests.get(url).json()
 
def fetch_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    return requests.get(url).json()
 
def predict_rain(humidity, pressure, temp, wind):
    input_data = np.array([[humidity, humidity, pressure, pressure, temp, temp, wind, wind]])
    pred = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]
    return pred, prob
 
def plot_google_style_temp(chart_rows, unit):
    """Broadcast-style temperature curve with a heat gradient (blue -> amber -> red)."""
    dates = [row["Date"] for row in chart_rows]
    temps = [row["Temperature"] for row in chart_rows]

    # ---- Header bar (mimics a weather-broadcast title strip) ----
    st.markdown(f"""
        <div class="broadcast-header">
            <span class="broadcast-title">5-DAY TEMPERATURE TREND</span>
            <span class="live-badge">LIVE</span>
        </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=temps,
        mode="lines+markers+text",
        line=dict(shape="spline", color="rgba(237,161,39,0.85)", width=4),
        marker=dict(
            size=14,
            color=temps,
            colorscale=[[0, "#378ADD"], [0.5, "#EDA127"], [1, "#E34948"]],
            line=dict(width=2, color="white"),
            showscale=False,
        ),
        fill="tozeroy",
        fillcolor="rgba(237,161,39,0.15)",
        text=[f"{t}{unit}" for t in temps],
        textposition="top center",
        textfont=dict(size=16, color="white"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=14),
        showlegend=False,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            tickfont=dict(size=13, color="#9fb0c3"),
            type="category",
            categoryorder="array",
            categoryarray=dates,
        ),
        yaxis=dict(showgrid=False, visible=False),
        height=300,
    )

    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
# ---- Header ----
st.markdown('<div class="main-title">Weather Insight 🌦️</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Live weather, forecasts, and news — powered by real-time data and machine learning</div>', unsafe_allow_html=True)
 
if "unit" not in st.session_state:
    st.session_state.unit = "°C"
col1, col2 = st.columns([5, 1])
with col2:
    st.session_state.unit = st.radio("Unit", ["°C", "°F"], horizontal=True, label_visibility="collapsed")
unit = st.session_state.unit
 
tab1, tab2, tab3 = st.tabs(["🏠 Dashboard", "🌍 Compare Cities", "📰 Weather News"])
 
# ===================== TAB 1: DASHBOARD =====================
with tab1:
    city = st.text_input("", placeholder="Search a city... e.g. Mangaluru", key="main_city")
 
    if city:
        data = fetch_current(city)
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            pressure = data["main"]["pressure"]
            condition = data["weather"][0]["description"]
            code = data["weather"][0]["id"]
            city_display = data["name"]
            tz_offset = data["timezone"]
            sunrise = format_time(data["sys"]["sunrise"], tz_offset)
            sunset = format_time(data["sys"]["sunset"], tz_offset)
            icon = get_icon(code)
 
            st.markdown(f"""
                <div class="weather-card">
                    <div style="font-size: 3.5rem;">{icon}</div>
                    <div style="font-size: 1.6rem; font-weight: 700;">{city_display}</div>
                    <div style="text-transform: capitalize; font-size: 1.3rem;">{condition}</div>
                    <div class="metric-row">
                        <div class="metric-box"><div class="metric-value">{convert_temp(temp, unit)}{unit}</div><div class="metric-label">Temperature</div></div>
                        <div class="metric-box"><div class="metric-value">{convert_temp(feels_like, unit)}{unit}</div><div class="metric-label">Feels Like</div></div>
                        <div class="metric-box"><div class="metric-value">{humidity}%</div><div class="metric-label">Humidity</div></div>
                        <div class="metric-box"><div class="metric-value">{wind} m/s</div><div class="metric-label">Wind</div></div>
                        <div class="metric-box"><div class="metric-value">{sunrise}</div><div class="metric-label">Sunrise</div></div>
                        <div class="metric-box"><div class="metric-value">{sunset}</div><div class="metric-label">Sunset</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
 
            pred, prob = predict_rain(humidity, pressure, temp, wind)
            if pred == 1:
                st.markdown(f'<div class="prediction-card rain-yes">☔ Likely to rain tomorrow — {prob*100:.1f}% chance</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="prediction-card rain-no">☀️ Unlikely to rain tomorrow — {(1-prob)*100:.1f}% confidence</div>', unsafe_allow_html=True)
 
            forecast_data = fetch_forecast(city)
            if forecast_data.get("cod") == "200":
                st.markdown("### 5-Day Forecast")
                daily = [item for item in forecast_data["list"] if "12:00:00" in item["dt_txt"]]
 
                cols = st.columns(len(daily))
                chart_rows = []
                for i, day in enumerate(daily):
                    day_temp = day["main"]["temp"]
                    day_code = day["weather"][0]["id"]
                    day_icon = get_icon(day_code)
                    day_date = datetime.strptime(day["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%a %d")
                    with cols[i]:
                        st.markdown(f"""
                            <div class="forecast-card">
                                <div>{day_date}</div>
                                <div style="font-size:2rem;">{day_icon}</div>
                                <div>{convert_temp(day_temp, unit)}{unit}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    chart_rows.append({"Date": day_date, "Temperature": convert_temp(day_temp, unit)})
 
                st.markdown("### Temperature Trend")
                plot_google_style_temp(chart_rows, unit)
        else:
            st.error("City not found. Please check the spelling.")
 
# ===================== TAB 2: COMPARE CITIES =====================
with tab2:
    st.write("Enter up to 3 cities to compare side-by-side")
 
    c1, c2, c3 = st.columns(3)
    with c1:
        city_a = st.text_input("City 1", placeholder="e.g. Mangaluru", key="city_a")
    with c2:
        city_b = st.text_input("City 2", placeholder="e.g. Bengaluru", key="city_b")
    with c3:
        city_c = st.text_input("City 3", placeholder="e.g. Mumbai", key="city_c")
 
    entered_cities = [c for c in [city_a, city_b, city_c] if c.strip()]
 
    if entered_cities:
        result_cols = st.columns(len(entered_cities))
        for i, c in enumerate(entered_cities):
            data = fetch_current(c)
            with result_cols[i]:
                if data.get("cod") == 200:
                    temp = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    condition = data["weather"][0]["description"]
                    code = data["weather"][0]["id"]
                    icon = get_icon(code)
                    st.markdown(f"""
                        <div class="compare-card">
                            <div style="font-size:2.5rem;">{icon}</div>
                            <div style="font-weight:700;">{data['name']}</div>
                            <div style="text-transform: capitalize;">{condition}</div>
                            <div class="metric-value">{convert_temp(temp, unit)}{unit}</div>
                            <div class="metric-label">Humidity: {humidity}%</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"'{c}' not found")
 
# ===================== TAB 3: WEATHER NEWS =====================
with tab3:
    country_options = {
        "India": "India", "United States": "United States", "United Kingdom": "United Kingdom",
        "Australia": "Australia", "Canada": "Canada", "Germany": "Germany"
    }
    country_name = st.selectbox("Select a country", list(country_options.keys()))
 
    news_url = (
        f"https://newsapi.org/v2/everything?"
        f"q=weather {country_options[country_name]}&language=en&sortBy=publishedAt&pageSize=6&apiKey={NEWS_API_KEY}"
    )
    news_data = requests.get(news_url).json()
 
    if news_data.get("status") == "ok" and news_data.get("articles"):
        for article in news_data["articles"][:6]:
            st.markdown(f"""
                <div class="news-card">
                    <div class="news-title">{article['title']}</div>
                    <div class="news-source">{article['source']['name']}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No weather-related news found right now. Try a different country.")
        if news_data.get("message"):
            st.caption(f"Debug info: {news_data['message']}")
 
