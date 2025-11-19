import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import requests
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'DISTRICT_RAINFALL_DISTRIBUTION_COUNTRY_INDIA_cd_(1)(1).csv')
df = pd.read_csv(csv_path)
new_df = df[df['NO'].astype(str).str.isdigit()]
rainfall_cities_mm = dict(zip(new_df['DIST'], new_df['(mm)']))

yield_path = os.path.join(BASE_DIR, 'yield_prediction.xlsx')
yield_model_path = os.path.join(BASE_DIR, 'yield_model.pkl')

def _train_yield_model():
    yield_df = pd.read_excel(yield_path)
    yield_df = yield_df.dropna(subset=['State_Name', 'District_Name', 'Season', 'Crop', 'Area', 'Production'])
    yield_df['Area'] = pd.to_numeric(yield_df['Area'], errors='coerce')
    yield_df = yield_df.dropna(subset=['Area'])

    YIELD_FEATURES = ['State_Name', 'District_Name', 'Season', 'Crop', 'Area']
    categorical_features = ['State_Name', 'District_Name', 'Season', 'Crop']
    numeric_features = ['Area']

    yield_preprocessor = ColumnTransformer(
        transformers=[
            ('categorical', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('numeric', 'passthrough', numeric_features),
        ]
    )

    yield_model = Pipeline(
        steps=[
            ('preprocess', yield_preprocessor),
            ('model', RandomForestRegressor(n_estimators=80, random_state=42, n_jobs=-1, max_depth=15)),
        ]
    )
    yield_model.fit(yield_df[YIELD_FEATURES], yield_df['Production'])
    with open(yield_model_path, 'wb') as model_file:
        pickle.dump(yield_model, model_file)
    return yield_model

if os.path.exists(yield_model_path):
    with open(yield_model_path, 'rb') as cached_model:
        yield_model = pickle.load(cached_model)
else:
    yield_model = _train_yield_model()


def get_weather(city):
    api_key = "3d1575a4abcc7b1a1a6e03a9a4f68a5f"
    unit = "metric"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={unit}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "main" not in data:
            raise ValueError("Weather response missing 'main'")
        return data
    except Exception as e:
        return {"error": str(e)}


def get_city_conditions(data, city):
    rainfall_in_mm = rainfall_cities_mm.get(city.upper())
    current_weather = get_weather(city)

    current_temp = current_weather.get('main', {}).get('temp')
    current_humidity = current_weather.get('main', {}).get('humidity')

    if data["temperature"] == "" and current_temp is not None:
        data["temperature"] = current_temp
    if data["humidity"] == "" and current_humidity is not None:
        data["humidity"] = current_humidity
    if data["rainfall"] == "" and rainfall_in_mm is not None:
        data["rainfall"] = rainfall_in_mm

    return data





app = Flask(__name__)
CORS(app, resources={r"/*": {"origin": "*"}})


def _require_fields(payload, required):
    missing = [field for field in required if field not in payload or payload[field] == ""]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")


def _to_float(value, field_name):
    if value == "" or value is None:
        raise ValueError(f"{field_name} is required")
    return float(value)


@app.route('/predict', methods=['POST'])
def predict():
    with open(os.path.join(BASE_DIR, 'DecisionTree.pkl'), 'rb') as file:
        model = pickle.load(file)

    data = request.get_json() or {}

    try:
        _require_fields(data, ['district', 'nitrogen', 'phosphorous', 'potassium', 'ph'])
        enriched = get_city_conditions(data.copy(), data["district"])
        values = [
            _to_float(enriched.get('temperature'), 'temperature'),
            _to_float(enriched.get('rainfall'), 'rainfall'),
            _to_float(enriched.get('nitrogen'), 'nitrogen'),
            _to_float(enriched.get('phosphorous'), 'phosphorous'),
            _to_float(enriched.get('potassium'), 'potassium'),
            _to_float(enriched.get('ph'), 'ph'),
            _to_float(enriched.get('humidity'), 'humidity'),
        ]
        features = np.array([[
            values[0],
            values[1],
            values[2],
            values[3],
            values[4],
            values[5],
            values[6],
        ]])
    except (ValueError, KeyError) as exc:
        return jsonify({'error': str(exc)}), 400

    prediction = model.predict(features)
    return jsonify({'prediction': prediction[0]})


@app.route('/predict-yield', methods=['POST'])
def predict_yield():
    payload = request.get_json() or {}
    try:
        _require_fields(payload, ['crop_name', 'season', 'state', 'district', 'area'])
        area = float(payload['area'])
    except ValueError as exc:
        return jsonify({'error': f'Invalid numeric value: {exc}'}), 400

    input_frame = pd.DataFrame([{
        'State_Name': payload['state'],
        'District_Name': payload['district'],
        'Season': payload['season'],
        'Crop': payload['crop_name'],
        'Area': area
    }])

    prediction = yield_model.predict(input_frame)[0]
    return jsonify({'prediction': float(prediction)})


if __name__ == '__main__':
    app.run(debug=True)
