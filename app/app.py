from flask import Flask, render_template, jsonify, request
from hashlib import sha256

import uuid
import json
import requests
import os

app = Flask(__name__)

BASE_ADDR = 'http://notary-promedicus.itsbeta.com'

API_KEY = 'F24CDF1a6fED79b3f48eD559244a5c6b'
API_URL = BASE_ADDR + '/api/v1/uploadData?apikey={}'.format(API_KEY)


def get_full_cert_addr(cert):
		return BASE_ADDR + '/certificate/' + cert

def check_result(hash_fio, hash_dogovor, guid, cert_id):
		addr = BASE_ADDR + '/api/v1/files/{}?apikey={}'.format(cert_id, API_KEY)
		data = json.loads(requests.get(addr).text)[0]['object']
		metadata = data['metadata']

		assert metadata['hash_fio'] == hash_fio
		assert metadata['hash_dogovor'] == hash_dogovor

		file_content=''.join(['{"key":"', guid 
				, '","eTag":"' , data['eTag']
				,'","size":207,"metadata":{"GUID":"' , guid
				,'","hash_dogovor":"' ,hash_dogovor
				,'","hash_fio":"', hash_fio
				,'"},"sequencer":"',data['sequencer'],'"}'])
		assert cert_id == sha256(file_content.encode('utf-8')).hexdigest()

def upload_data(fio, dogovor):
		json_data = dict()
		json_data['hash_fio'] = sha256(fio.encode('utf-8')).hexdigest()
		json_data['hash_dogovor'] = sha256(dogovor.encode('utf-8')).hexdigest()
		json_data['GUID'] = uuid.uuid4().__str__()
		try:
				cert = requests.post(API_URL, json=json_data).json()['cert']
		except Exception as e:
				return None
		check_result(json_data['hash_fio'], json_data['hash_dogovor'], json_data['GUID'], cert)
		return get_full_cert_addr(cert)

@app.route('/_ajax', methods=['POST'])
def handle_ajax():
		field_fio = request.form.get('field_fio')
		field_dogovor = request.form.get('field_dogovor')
		if not field_fio or not field_dogovor:
				return jsonify(success=False, error="Please fill all fields")
		cert_addr = upload_data(field_fio, field_dogovor)
		if not cert_addr:
				return jsonify(success=False, error="Error on server")
		return jsonify(success=True, cert_addr=cert_addr)

@app.route('/')
def home():
		return render_template('index.html')

if __name__ == '__main__':
		if API_KEY == '':
				print('plz add API_KEY to {}'.format(os.path.abspath(__file__)))
				os._exit(1)
		app.run()
