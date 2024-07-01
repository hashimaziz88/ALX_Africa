# weather.py
import os
import requests

def fetch_weather(api_key, city):
    try:
        # Construct API request
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'  # Specify Celsius for temperature
        }

        # Make API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (e.g., 404, 500)

        # Parse JSON response
        data = response.json()

        # Extract relevant weather information
        weather_info = {
            'city_name': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }

        return weather_info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    except (KeyError, IndexError) as e:
        print(f"Error processing data: {e}")
        return None
