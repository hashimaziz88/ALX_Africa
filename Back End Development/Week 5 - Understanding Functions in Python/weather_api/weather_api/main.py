# main.py
import os
from dotenv import load_dotenv
from weather import fetch_weather

# Load environment variables from .env file
load_dotenv()

def main():
    # Fetch weather information
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    city = 'Haifa'  # Replace with the city you want to fetch weather for

    weather_info = fetch_weather(api_key, city)
    if weather_info:
        print(f"Weather in {weather_info['city_name']}:")
        print(f"Temperature: {weather_info['temperature']}°C")
        print(f"Description: {weather_info['description']}")
    else:
        print("Failed to fetch weather information.")

if __name__ == "__main__":
    main()
