import os
import json


from flask import Flask, request, render_template
from m2x.client import M2XClient

from models import NumericStreamParser, MacStreamParser
from utils import get_device


app = Flask(__name__)
app.config.from_pyfile('config.py')

DEVICE_NAME = 'rpi-network-monitor'

CLIENT = M2XClient(os.environ['MASTER_API_KEY'])
DEVICE = get_device(DEVICE_NAME, CLIENT)

MACS = MacStreamParser(DEVICE.stream('mac_addresses'))

TOTAL_CONNECTIONS = NumericStreamParser(DEVICE.stream('total_connections'))
KNOWN_CONNECTIONS = NumericStreamParser(DEVICE.stream('number_mac_addresses'))
UNKNOWN_CONNECTIONS = NumericStreamParser(
    DEVICE.stream('number_unknown_connections'))


@app.route("/", methods=['GET'])
def main():
    start = request.args.get('start')
    end = request.args.get('end')
    total, update_time = TOTAL_CONNECTIONS.current_value()
    known = KNOWN_CONNECTIONS.current_value()[0]
    unknown = UNKNOWN_CONNECTIONS.current_value()[0]

    if start:
        limit = 10000
        latest = False
    else:
        limit = 300
        latest = True

    total_connections = TOTAL_CONNECTIONS.stream.values(start=start,
                                                        end=end,
                                                        limit=limit
                                                        )
    known_connections = KNOWN_CONNECTIONS.stream.values(start=start,
                                                        end=end,
                                                        limit=limit
                                                        )
    unknown_connections = UNKNOWN_CONNECTIONS.stream.values(start=start,
                                                            end=end,
                                                            limit=limit
                                                            )
    MACS.set_stream_values(start=start,
                           end=end,
                           limit=limit)
    number_of_uniques, startdate, enddate = MACS.unique_macs(start=start,
                                                             end=end
                                                             )
    macs_vendors = MACS.macs_vendors(start=start)

    return render_template('body.html', total=int(total), known=int(known),
                           unknown=int(unknown), time=update_time,
                           uniques=number_of_uniques,
                           macs_vendors=macs_vendors,
                           latest=latest, startdate=startdate, enddate=enddate,
                           total_connections=json.dumps(total_connections),
                           known_connections=json.dumps(known_connections),
                           unknown_connections=json.dumps(unknown_connections))

if __name__ == "__main__":
    app.run()
