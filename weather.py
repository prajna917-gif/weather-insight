import requests

API_KEY = "db2c40ce39f3b033326671cb74c1da85"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

city_name = input("Enter city name: ")
weather_data = get_weather(city_name)
temperature = weather_data["main"]["temp"]
humidity = weather_data["main"]["humidity"]
wind_speed = weather_data["wind"]["speed"]
condition = weather_data["weather"][0]["description"]

print(f"Temperature: {temperature}°C")
print(f"Humidity: {humidity}%")
print(f"Wind Speed: {wind_speed} m/s")
print(f"Condition: {condition}")