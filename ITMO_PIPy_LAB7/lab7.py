import requests
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Function to get city weather

def get_weather(city_name):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Error: OPENWEATHER_API_KEY not set")
        return
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},MA&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        print(f"\n--- Weather in {city_name}, Morocco ---")
        print(f"Description: {weather_desc}")
        print(f"Temperature: {temp}°C, Humidity: {humidity}%, Pressure: {pressure} hPa")
    except Exception as e:
        print("Error fetching weather data:", e)



# Main program

def main():
    print("Welcome to Lab-7 Program!\n")

    
    # get_space_text()

    # Weather for Zagora
    get_weather("Zagora")


if __name__ == "__main__":
    main()
