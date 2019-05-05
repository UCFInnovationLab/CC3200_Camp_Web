import os
import json


from flask import Flask, request, render_template
from m2x.client import M2XClient

from models import NumericStreamParser
from utils import get_device


app = Flask(__name__)
app.config.from_pyfile('config.py')

DEVICE_NAME = 'TI_CC3200_Demo'

CLIENT = M2XClient(os.environ['MASTER_API_KEY'])
#DEVICE = CLIENT.device(os.environ['DEVICE_ID'])
DEVICE = get_device(DEVICE_NAME, CLIENT)

TEMPERATURE_1 = NumericStreamParser(DEVICE.stream('Name1_t'))
TEMPERATURE_2 = NumericStreamParser(DEVICE.stream('Name2_t'))
TEMPERATURE_3 = NumericStreamParser(DEVICE.stream('Name3_t'))


@app.route("/", methods=['GET'])
def main():
    start = request.args.get('start')
    end = request.args.get('end')
    temp1, update_time = TEMPERATURE_1.current_value()
    temp2 = TEMPERATURE_2.current_value()[0]
    temp3 = TEMPERATURE_3.current_value()[0]

    if start:
        limit = 10000
        latest = False
    else:
        limit = 300
        latest = True

    temp1_stream = TEMPERATURE_1.stream.values(start=start, end=end, limit=limit)
    temp2_stream = TEMPERATURE_2.stream.values(start=start, end=end, limit=limit)
    temp3_stream = TEMPERATURE_3.stream.values(start=start, end=end, limit=limit)

    return render_template('body.html', 
                           temp1=int(temp1), 
                           temp2=int(temp2),
                           temp3=int(temp3),
                           temp1_stream=json.dumps(temp1_stream),
                           temp2_stream=json.dumps(temp2_stream),
                           temp3_stream=json.dumps(temp3_stream),
                           latest=latest, startdate=start, enddate=end,
                           time=update_time)

if __name__ == "__main__":
    app.run()


