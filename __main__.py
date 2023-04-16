# Python 3 server example
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer, HTTPServer
import time
import requests
import json
import threading
from pyngrok import ngrok
import os

print(os.environ.get('PORT', 8080))

hostName = "localhost"
serverPort = int(os.environ.get('PORT', 8080))

decanter_api_key = os.environ.get('DECANTER_API_KEY')
decanter_project_id = os.environ.get('DECANTER_PROJECT_ID')
decanter_model_id = os.environ.get('DECANTER_MODEL_ID')

ragic_api_key = os.environ.get('RAGIC_API_KEY')
ragic_host = os.environ.get('RAGIC_HOST')
ragic_ap_id = os.environ.get('RAGIC_AP_ID')
ragic_sheet_id = os.environ.get('RAGIC_SHEET_ID')
ragic_table_id = os.environ.get('RAGIC_TABLE_ID')
ragic_field_id = os.environ.get('RAGIC_FIELD_ID')

processed = {}
processed_lock = threading.Lock()

class MyServer(BaseHTTPRequestHandler):
    # def __init__(self, request, client_address, server):
    #     super().__init__(request, client_address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("ok", "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("ok", "utf-8"))
        # log the message
        thread = threading.Thread(target=self.process)
        thread.start()
        
    def process(self):
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        print(post_data)
        # show Headers
        print(self.headers)
        # if Content-Type contains application/json
        if 'application/json' in self.headers['Content-Type']:
            # decode json data, example '[902]'
            data = json.loads(post_data.decode('utf-8'))
            print(data)
            # get record_id
            record_id = data[0]
            print(record_id)
            if self.is_processed(record_id=record_id) is True:
                print('Already processed')
                return
            print('Not processed')
            self.write_processed(record_id=record_id)

            # get data from Ragic
            user_input = self.request_ragic_data(record_id=record_id)
            # get predict result from Decanter
            predict = self.request_decanter_predict(
                project_id=decanter_project_id, 
                model_id=decanter_model_id, 
                experiment_id='', 
                data=user_input
                )
            
            # write predict result to Ragic
            self.write_ragic_data(record_id=record_id, field_id=ragic_field_id, data=predict)


    def request_ragic_data(self, record_id):
        # if record_id is not str, convert to str
        if not isinstance(record_id, str):
            record_id = str(record_id)
        
        url = 'https://{ap_host}/{ap_id}/{table_id}/{sheet_id}/{record_id}?v=3&api'.format(
            ap_host=ragic_host, ap_id=ragic_ap_id, table_id=ragic_table_id, sheet_id=ragic_sheet_id, record_id=record_id)

        r = requests.get(url, headers={'Authorization': 'Basic {}'.format(ragic_api_key)}, allow_redirects=True)
        print(r.text)
        # get data
        data = r.json()
        print(data)
        # get feature
        feature = data[record_id]
        print(feature)
        return feature

    def write_ragic_data(self, record_id, field_id, data):  
        # if record_id is not str, convert to str
        if not isinstance(record_id, str):
            record_id = str(record_id)
        url = 'https://{ap_host}/{ap_id}/{table_id}/{sheet_id}/{record_id}?v=3&api'.format(
            ap_host=ragic_host, ap_id=ragic_ap_id, table_id=ragic_table_id, sheet_id=ragic_sheet_id, record_id=record_id)

        form_data = {
            field_id: data
        }

        r = requests.post(url, 
            headers={'Authorization': 'Basic {}'.format(ragic_api_key)},
            data=form_data
            )
        print(r.text)

    def request_decanter_predict(self, project_id, model_id, experiment_id, data):
        url = 'https://decanter.ai/v1/prediction/single_predict'

        data_payload = {
            "project_id": project_id,
            "model_id": model_id,
            "experiment_id": experiment_id,
            "features": [
                data
            ]
        }
        data_json = json.dumps(data_payload)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + decanter_api_key
        }
        r = requests.post(url, data=data_json, headers=headers)
        print(r.text)

        # sample response: {"message":"Prediction successful","single_predict_result":[{"index":0,"predict_status":"success","result":{"0.0":0.8522941041282368,"1.0":0.14770589587176317,"prediction":"0.0"}}],"status":"OK","status_code":201}
        # get predict result
        predict_result = r.json()
        print(predict_result)
        # get predict result
        result = predict_result['single_predict_result'][0]['result']
        print(result)
        # get prediction
        prediction = result['prediction']
        print(prediction)
        return prediction

    

    ##　Echo cancel
    def is_processed(self, record_id):
        ## check if record_id is processed
        processed_lock.acquire()
        if record_id in processed:
            if time.time() - processed[record_id] < 30:
                processed_lock.release()
                return True
        processed_lock.release()
        return False

    def write_processed(self, record_id):
        processed_lock.acquire()
        processed[record_id] = time.time()
        processed_lock.release()

def register_webhook(public_url):
    table_id = 'train'
    url = 'https://{ap_host}/sims/webhookSubscribe.jsp'.format(ap_host=ragic_host)

    form_data = {
        'ap': ragic_ap_id,
        'path': '/{table_id}'.format(table_id=ragic_table_id),
        'si': ragic_sheet_id,
        'url': public_url
    }

    r = requests.post(url, headers={'Authorization': 'Basic {}'.format(ragic_api_key)}, data=form_data)
    print(r.text)




if __name__ == "__main__":        
    webServer = ThreadingHTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    public_url = ngrok.connect(serverPort).public_url
    print("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, serverPort))

    registed_url = register_webhook(public_url)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
