# 🛰️ Sentinel Hub Satellite Image Downloader (Python)

Sentinel Hub API Integration
This repository demonstrates how to fetch satellite images from Sentinel Hub based on a specific area and date range using their API. It covers the steps for obtaining an access token, searching for satellite images, and downloading them as PNG images.

### 📁Project File Structure
Here’s a clean way to structure your project:

```bash
satellite-fetch/
├── .env                 # Store secrets
├── get_token.py         # Get access token
├── search_images.py     # Search image metadata
├── download_image.py    # Download satellite images in PNG format
 ```

⚙️ Setup Instructions
1. Create a Sentinel Hub Account
   Go to Sentinel Hub and create an account.
   Once logged in, create an OAuth client to obtain your client_id and client_secret.

2. Install Dependencies
To get started, clone this repository and install the necessary dependencies using pip:
```bash
  git clone https://github.com/Chandan785/Setallite-image-API.git
```
🔐 Step 1: Create .env File
Create a file named .env and add your credentials:
```bash
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
```
Step 2: Install Required Libraries
```bash
pip install requests python-dotenv
```
Step 3: get_token.py – Fetch Access Token
```bash
python get_token.py
```
Step 4: search_images.py – Search Image Metadata

```bash
python search_images.py
```
You’ll get:

• Dates of satellite captures

• Cloud cover percentage

• Scene ID (useful for fetching images)

Step 5:  
```bash
python download_image.py
```
You’ll get:

• An actual PNG satellite image

• It will also open in your image viewer

• Image saved as satellite_image.png

 
