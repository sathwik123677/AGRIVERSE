import pandas as pd
import requests

df = pd.read_csv('DISTRICT_RAINFALL_DISTRIBUTION_COUNTRY_INDIA_cd_(1)(1).csv')
new_df=df[df['NO'].astype(str).str.isdigit()]
rainfall_cities_mm= dict(zip(new_df['DIST'], new_df['(mm)']))
print(dist_mm_dict)


def get_weather(city):
    api_key = "3d1575a4abcc7b1a1a6e03a9a4f68a5f"
    unit = "metric"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={unit}"

    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

def get_city_conditions(city):
    rainfall_in_mm= rainfall_cities_mm[city.upper()]
    current_weather = get_weather(city)
    # print(current_weather)
    current_temp = current_weather['main']['temp']
    current_humdiity = current_weather['main']['humidity']
    print(current_temp,current_humdiity ,rainfall_in_mm)



get_city_conditions("patna")
