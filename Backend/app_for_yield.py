from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('DISTRICT_RAINFALL_DISTRIBUTION_COUNTRY_INDIA_cd_(1)(1).csv')
new_df = df[df['NO'].astype(str).str.isdigit()]
rainfall_cities_mm = new_df['(mm)']

@app.route('/predict', methods=['POST'])
def predict():
    with open('RandomForest_YieldPre.pkl', 'rb') as file:
        model = pickle.load(file)

    data = request.get_json()
    dist = data['District']

    # Fetch rainfall data for the district from the DataFrame
    rainfall = rainfall_cities_mm[dist]

    prediction = model.predict(np.array([[
        data['Crop'],
        data['Season'],
        data['State'],
        rainfall,
        data['Area'],
    ]]))

    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)