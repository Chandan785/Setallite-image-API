import requests
from get_token import get_access_token
from PIL import Image
from io import BytesIO

def search_images(bbox, date_range):
    url = "https://services.sentinel-hub.com/api/v1/catalog/search"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

    payload = {
        "bbox": bbox,
        "datetime": date_range,
        "collections": ["sentinel-2-l2a"],
        "limit": 1,
        "query": {
            "eo:cloud_cover": {
                "lt": 20
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json().get("features", [])

def download_image(bbox, datetime_str, save_name):
    url = "https://services.sentinel-hub.com/api/v1/process"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "bounds": {"bbox": bbox},
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": datetime_str,
                        "to": datetime_str
                    }
                }
            }]
        },
        "output": {
            "width": 512,
            "height": 512,
            "responses": [{
                "identifier": "default",
                "format": {"type": "image/png"}
            }]
        },
        "evalscript": """
        //VERSION=3
        function setup() {
          return {
            input: ["B04", "B03", "B02"],
            output: { bands: 3 }
          };
        }
        function evaluatePixel(sample) {
          return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
        }
        """
    }

    response = requests.post(url, headers=headers, json=payload)
    if "image" in response.headers.get("Content-Type", ""):
        image = Image.open(BytesIO(response.content))
        image.show()
        image.save(save_name)
        print(f"✅ Saved: {save_name}")
    else:
        print("⚠️ Could not retrieve image:", response.text)

if __name__ == "__main__":
    bbox = [77.5946, 12.9716, 77.7046, 13.0216]
    date_range = "2024-03-01T00:00:00Z/2024-04-01T23:59:59Z"

    images = search_images(bbox, date_range)

    for i, feature in enumerate(images):
        timestamp = feature["properties"]["datetime"]
        cloud_cover = feature["properties"].get("eo:cloud_cover", "N/A")
        print(f"{i+1}. 🕒 {timestamp}, ☁️ Cloud: {cloud_cover}")

        filename = f"image_{timestamp.replace(':', '-').replace('T', '_').replace('Z', '')}.png"
        download_image(bbox, timestamp, filename)
