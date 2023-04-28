import csv
import time
import datetime

from pydozer import ingest_pb2
from pydozer import types_pb2
from pydozer.ingest import IngestClient
from pydozer.api import ApiClient

DOZER_INGEST_URL = "0.0.0.0:7001"
DOZER_API_URL = "0.0.0.0:7003"

ingestion_client = IngestClient(url=DOZER_INGEST_URL)
api_client = ApiClient("events", url=DOZER_API_URL)


def send_message(seq, device, temp):
    user = ingest_pb2.IngestRequest(
        schema_name="events",
        typ=0,
        old=None,
        new=types_pb2.Record(values=[
            types_pb2.Value(string_value=device),
            types_pb2.Value(float_value=temp),
            types_pb2.Value(string_value=datetime.datetime.now().strftime("%H:%M:%S"))
        ]),
        seq_no=seq
    )
    res = ingestion_client.ingest_raw(user)
    assert res is not None

def run():
    seq = 1
    with open('config/iot_device_data.csv', newline='') as csvfile:
        data_reader = csv.DictReader(csvfile, delimiter=',')
        for row in data_reader:
            device = row['device']
            temp = float(row['temp'])
            print(f'{id}: {temp} ')
            send_message(seq, device, temp)
            seq += 1
            time.sleep(1)


if __name__ == '__main__':
    # ui.set_banner()
    run()
