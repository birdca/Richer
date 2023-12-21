import requests
import json
import time
from gmapdata.calculate_polygon import generate_points_within_polygon

def get_place_info(points, start, radius, api_key):
    print("start....")

    place_list = []  # List to store place details
    print("how many points:")
    print(len(points))
    try:
        for index, location in enumerate(points):
            print("point:" + str(index))
            nearbysearch_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&radius={}&type=restaurant&key={}".format(
                location, radius, api_key)
            start = index

            while True:
                # print("get response from nearbysearch_url: " + nearbysearch_url)
                response = requests.get(nearbysearch_url)
                res_json_payload = response.json()
                print("resutl:")
                print(res_json_payload)
                for result in res_json_payload['results']:
                    # print("each result:")
                    if 'price_level' in result and result['price_level'] in [2, 3, 4]:

                        place_id = result['place_id']
                        details_url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&key={}".format(
                            place_id, api_key)
                        details_response = requests.get(details_url)
                        details = details_response.json()
                        print(details)
                        place_list.append(details)  # Add details to list
                        place_list.append(result)  # Add details to list

                if 'next_page_token' not in res_json_payload:
                    break

                nearbysearch_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&pagetoken={}".format(
                    api_key, res_json_payload['next_page_token'])

                time.sleep(2)

    finally:
        # print("how many restaurants for this query: " + str(count) )
        print("start dump data to file...")
        # Write place details to a JSON file
        file_name = "restaurants_{}.json".format(start)
        with open(file_name, 'w') as f:
            json.dump(place_list, f, indent=4)


def filter_duplicates():
    # Open the JSON file
    with open('./restaurants_31186.json') as file:
        data = json.load(file)

    # Filter out duplicate JSON objects based on place_id
    filtered_data = []
    place_ids = set()
    for item in data:
        place_id = item.get('place_id')
        if place_id not in place_ids:
            filtered_data.append(item)
            place_ids.add(place_id)

    # Save the filtered data to a new JSON file
    with open('restaurant_candidates.json', 'w') as file:
        json.dump(filtered_data, file)

# Replace with your own values
api_key = "AIzaSyA0tQRy9A8ZY0RSMqHRXa7MbOqZH3b9N0E"
coordinates = ["25.066873, 121.592639", "25.086774, 121.555560", "25.078845, 121.509383", "25.020060, 121.497024", "25.023482, 121.567920"]
# location = "LATITUDE,LONGITUDE"  # Replace with your own values
radius = "40"  # RADIUS_IN_METERS

# get_place_info(location, radius, api_key)

if __name__ == "__main__":
    # points = generate_points_within_polygon(coordinates)
    # get_place_info(points=points, start=0, radius=radius, api_key=api_key)
    filter_duplicates()



