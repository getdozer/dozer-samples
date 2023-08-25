import argparse

from pydozer.api import ApiClient

DOZER_CLOUD_HOST = "data.dev.getdozer.io:443"


def get_api_client(app_id=None):
    return ApiClient("trips", url=DOZER_CLOUD_HOST, app_id=app_id,
                     secure=True) if app_id else ApiClient("trips", url="localhost:80")


def main(app_id=None):
    api = get_api_client(app_id)
    trips = api.query()
    if trips and trips.records:
        print(trips.records[0])
    else:
        print("No records found")


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-a", "--app", help="The Application id")

    args = argParser.parse_args()

    main(args.app)
