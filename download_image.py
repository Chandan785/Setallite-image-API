import requests
from get_token import get_access_token
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta


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
        "limit": 2,
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
    content_type = response.headers.get("Content-Type", "")
    if "image" in content_type:
        image = Image.open(BytesIO(response.content))
        image.show()
        image.save(save_name)
        print(f"✅ Saved: {save_name}")
    else:
        print("⚠️ Could not retrieve image:", response.text)


if __name__ == "__main__":
    # Get user inputs for bounding box and target date
    print("Enter bounding box coordinates as minLon,minLat,maxLon,maxLat (e.g., 77.5946,12.9716,77.7046,13.0216):")
    bbox_input = input().strip().split(",")
    bbox = [float(c) for c in bbox_input]

    date_str = input("Enter target date (YYYY-MM-DD): ").strip()
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        exit(1)

    # Compute range: two days before to fifteen days after
    start_date = target_date - timedelta(days=2)
    end_date = target_date + timedelta(days=15)

    # Format as ISO strings
    start_iso = start_date.strftime("%Y-%m-%dT00:00:00Z")
    end_iso = end_date.strftime("%Y-%m-%dT23:59:59Z")
    date_range = f"{start_iso}/{end_iso}"

    print(f"🔍 Searching images from {start_iso} to {end_iso} for area {bbox}")
    images = search_images(bbox, date_range)

    if not images:
        print("❌ No images found in the specified range.")
    else:
        for i, feature in enumerate(images):
            timestamp = feature["properties"]["datetime"]
            cloud_cover = feature["properties"].get("eo:cloud_cover", "N/A")
            print(f"{i+1}. 🕒 {timestamp}, ☁️ Cloud: {cloud_cover}")

            # Save each image with descriptive filename
            filename = (
                f"image_{timestamp.replace(':', '-').replace('T', '_').replace('Z', '')}_"
                f"cloud{cloud_cover}.png"
            )
            download_image(bbox, timestamp, filename)
