""" module containing an api endpoint that responds only to a get request,
it utilizes the `requests` library for making requests to other third party
api endpoints 
"""

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/hello', methods=['GET'])
def visitor_info():
	"""View for handling the request including a querry parameter
	"""

	client_ip = request.headers.get('X-Requested-For')
	if client_ip:
		client_ip = client_ip.split(',')[0]

	if not client_ip:
		client_ip = request.headers.get('X-Forwarded-For')
		if client_ip:
			client_ip = client_ip.split(',')[0]

	if not client_ip:
		client_ip = request.remote_addr

	visitor_name = request.args.get('visitor_name')

	location_api_url = 'http://ip-api.com/json/' + str(client_ip)
	location_response =  requests.get(location_api_url)
	if location_response.status_code == 200:
		location_data = location_response.json()
	else:
		return jsonify({"error": "your city was not loaded successfully"}), 400

	location = location_data.get('city') 
	

	weather_api_url = f'http://api.weatherapi.com/v1/current.json?key=31d8e3e2f00a4cd1be0135729240107&q={location}'
	weather_response = requests.get(weather_api_url) 
	if weather_response.status_code == 200:
		weather_data = weather_response.json()
		temperature = weather_data.get('current')
		temperature = temperature.get('temp_c')
		
	
	

	return jsonify({'client_ip': client_ip,
			'location': location,
			'greeting': f'Hello, {visitor_name}!, the temperature is
			{temperature} degrees celcius in {location}'
	}), 200

if __name__ == '__main__':
	app.run() 


