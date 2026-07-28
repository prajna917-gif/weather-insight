# Weather Insight 🌦️

A professional, real-time weather dashboard combining live weather data, 5-day forecasting, next-day rain prediction (machine learning), multi-city comparison, and weather-related news — built with Python and Streamlit.

## Live Demo
https://weather-insight-6fsyfcnppzj8qiucf5dcrf.streamlit.app

## Features
- **Live weather lookup** — current temperature, humidity, wind, "feels like," sunrise/sunset for any city worldwide (OpenWeatherMap API)
- **Rain prediction** — next-day rain forecast with confidence percentage, powered by a Logistic Regression model trained on the "Rain in Australia" dataset (Kaggle)
- **5-day forecast** — daily forecast cards with icons and temperatures
- **Temperature trend graph** — interactive, broadcast-style visualization built with Plotly
- **Compare cities** — view up to 3 cities side-by-side
- **Weather news** — latest weather-related headlines by country (NewsAPI)
- **°C / °F toggle**
- **Auto-rotating photo background** and weather-condition icons
- Fully responsive, dark-themed, professional UI

## Tech Stack
| Category | Tools |
|---|---|
| Language | Python |
| Web Framework | Streamlit |
| Machine Learning | Scikit-learn, Joblib |
| Data Handling | Pandas, NumPy |
| Visualization | Plotly |
| APIs | OpenWeatherMap, NewsAPI |
| Version Control | Git & GitHub |

## Project Structure
```
weather-insight/
├── data/
│   └── weatherAUS.csv
├── app.py
├── train_model.py
├── explore.py
├── rain_model.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

## How the Rain Prediction Works
1. Historical weather data (humidity, pressure, temperature, wind speed) is used to train a Logistic Regression classifier.
2. The model is evaluated on unseen test data, achieving ~84% accuracy — notably better than the ~78% baseline of always predicting "no rain."
3. The trained model is saved (`rain_model.pkl`) and loaded into the live app, where it makes predictions using real-time weather readings as input.

## How to Run Locally
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/weather-insight.git
   cd weather-insight
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Add your API keys in `app.py` (or set them as environment variables `WEATHER_API_KEY` and `NEWS_API_KEY`)
4. Run the app:
   ```
   streamlit run app.py
   ```

## Limitations
- The rain prediction model uses a single live weather reading as a stand-in for the separate 9am/3pm readings it was trained on — a reasonable simplification for a student project, noted here for transparency.
- The model was trained on Australian weather data, so prediction accuracy may vary for other regions.
- NewsAPI's free tier is intended for local development; a deployed public version may have request limitations.

## Future Improvements
- Retrain the rain model on region-specific data (e.g. coastal Karnataka)
- Extend rain prediction beyond next-day to a multi-day forecast
- Add historical weather trend analysis
- Add location auto-detect (geolocation)
