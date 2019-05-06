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
TEMPERATURE_4 = NumericStreamParser(DEVICE.stream('Name4_t'))
TEMPERATURE_5 = NumericStreamParser(DEVICE.stream('Name5_t'))
TEMPERATURE_6 = NumericStreamParser(DEVICE.stream('Name6_t'))
TEMPERATURE_7 = NumericStreamParser(DEVICE.stream('Name7_t'))
TEMPERATURE_8 = NumericStreamParser(DEVICE.stream('Name8_t'))
TEMPERATURE_9 = NumericStreamParser(DEVICE.stream('Name9_t'))

@app.route("/", methods=['GET'])
def main():
    start = request.args.get('start')
    end = request.args.get('end')

    temp1, update_time = TEMPERATURE_1.current_value()

    temp1 = TEMPERATURE_1.current_value()[0]
    temp2 = TEMPERATURE_2.current_value()[0]
    temp3 = TEMPERATURE_3.current_value()[0]
    temp4 = TEMPERATURE_4.current_value()[0]
    temp5 = TEMPERATURE_5.current_value()[0]
    temp6 = TEMPERATURE_6.current_value()[0]
    temp7 = TEMPERATURE_7.current_value()[0]
    temp8 = TEMPERATURE_8.current_value()[0]
    temp9 = TEMPERATURE_9.current_value()[0]

    if start:
        limit = 10000
        latest = False
    else:
        limit = 300
        latest = True

    temp1_stream = TEMPERATURE_1.stream.values(start=start, end=end, limit=limit)
    temp2_stream = TEMPERATURE_2.stream.values(start=start, end=end, limit=limit)
    temp3_stream = TEMPERATURE_3.stream.values(start=start, end=end, limit=limit)
    temp4_stream = TEMPERATURE_4.stream.values(start=start, end=end, limit=limit)
    temp5_stream = TEMPERATURE_5.stream.values(start=start, end=end, limit=limit)
    temp6_stream = TEMPERATURE_6.stream.values(start=start, end=end, limit=limit)
    temp7_stream = TEMPERATURE_7.stream.values(start=start, end=end, limit=limit)
    temp8_stream = TEMPERATURE_8.stream.values(start=start, end=end, limit=limit)
    temp9_stream = TEMPERATURE_9.stream.values(start=start, end=end, limit=limit)

    return render_template('body.html', 
                           temp1=int(temp1), 
                           temp2=int(temp2),
                           temp3=int(temp3),
                           temp4=int(temp4),
                           temp5=int(temp5),
                           temp6=int(temp6),
                           temp7=int(temp7),
                           temp8=int(temp8),
                           temp9=int(temp9),
                           temp1_stream=json.dumps(temp1_stream),
                           temp2_stream=json.dumps(temp2_stream),
                           temp3_stream=json.dumps(temp3_stream),
                           temp4_stream=json.dumps(temp4_stream),
                           temp5_stream=json.dumps(temp5_stream),
                           temp6_stream=json.dumps(temp6_stream),
                           temp7_stream=json.dumps(temp7_stream),
                           temp8_stream=json.dumps(temp8_stream),
                           temp9_stream=json.dumps(temp9_stream),
                           latest=latest, startdate=start, enddate=end,
                           time=update_time)

if __name__ == "__main__":
    app.run()


