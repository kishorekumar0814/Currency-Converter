from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{{}}"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    from_currency = data['from']
    to_currency = data['to']
    amount = float(data['amount'])

    try:
        response = requests.get(API_URL.format(from_currency))
        response.raise_for_status()
        rates = response.json()['conversion_rates']
        converted = round(amount * rates[to_currency], 2)
        return jsonify({'converted_amount': converted})
    except Exception as e:
        return jsonify({'error': 'Conversion failed. Please try again later.'}), 500

@app.route('/currencies', methods=['GET'])
def get_currencies():
    try:
        response = requests.get(API_URL.format("USD"))
        response.raise_for_status()
        currencies = list(response.json()['conversion_rates'].keys())
        return jsonify({'currencies': currencies})
    except Exception as e:
        return jsonify({'error': 'Failed to fetch currencies'}), 500

if __name__ == '__main__':
    app.run(debug=True)