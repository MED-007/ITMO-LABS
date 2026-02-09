# Variant 10 — open-notify.org
# open-notify.org provides public data about the International Space Station (ISS).
# i will use this endpoint: http://api.open-notify.org/iss-now.json

# it returns (JSON), Current latitude of the ISS, Current longitude of the ISS Timestamp (Unix time), Request status
# No API key required


#Example JSON response
# {
#   "message": "success",
#   "timestamp": 1700000000,
#   "iss_position": {
#     "latitude": "48.1234",
#     "longitude": "37.5678"
#   }
# }


import requests
import json
import time

def get_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching ISS data")
        return

    # Explicit JSON parsing using json library
    data = json.loads(response.text)

    status = data["message"]
    timestamp = data["timestamp"]
    latitude = data["iss_position"]["latitude"]
    longitude = data["iss_position"]["longitude"]

    readable_time = time.strftime(
        "%Y-%m-%d %H:%M:%S",
        time.localtime(timestamp)
    )

    print("===== ISS CURRENT LOCATION =====")
    print(f"Status: {status}")
    print(f"Timestamp (UNIX): {timestamp}")
    print(f"Readable time: {readable_time}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print("================================")

if __name__ == "__main__":
    get_iss_location()
