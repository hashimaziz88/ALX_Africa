# weather_advice.py

# Prompt the user for the current weather
todays_weather = input("What's the weather like today? (sunny/rainy/cold): ").strip().lower()

# Provide clothing recommendations based on the weather
if todays_weather == "sunny":
    print("Wear a t-shirt and sunglasses.")
elif todays_weather == "rainy":
    print("Don't forget your umbrella and a raincoat.")
elif todays_weather == "cold":
    print("Make sure to wear a warm coat and a scarf.")
else:
    print("Sorry, I don't have recommendations for this weather.")
