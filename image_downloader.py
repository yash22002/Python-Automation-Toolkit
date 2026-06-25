import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# Setup
url = 'https://flatdeal.codewraps.com'
output_folder = r'C:\Users\prath\Desktop\MyImages'
#create folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Browser setup
options = webdriver.ChromeOptions()
# options.add_argument('--headless') # Debugging ke liye ise comment out karein taaki browser dikhe
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)

# Page ko scroll karna
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(30) # 30 second wait for loading the images 

soup = BeautifulSoup(driver.page_source, 'html.parser')
images = soup.find_all('img')

print(f"Total images tags found: {len(images)}")

# Download logic
for i, img in enumerate(images):
    # 'src' or 'data-src' searching the link
    img_url = img.get('src') or img.get('data-src') or img.get('data-original')
    
    if img_url:
        # convertRelative link to full link
        img_url = urljoin(url, img_url)
        
        # downloading only valid http/https links 
        if img_url.startswith('http'):
            try:
                # headers are important for 99acres 
                headers = {'User-Agent': 'Mozilla/5.0'}
                img_data = requests.get(img_url, headers=headers).content
                
                # downloading only large images, to avoid icons
                if len(img_data) > 500:  # 1KB threshold for image size
                    file_name = os.path.join(output_folder, f'image_{i}.jpg')
                    with open(file_name, 'wb') as f:
                        f.write(img_data)
                    print(f'Downloaded: {file_name}')
            except Exception as e:
                print(f'Failed to download {img_url}: {e}')

driver.quit()
print("Process completed!")