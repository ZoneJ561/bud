from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import random
import time
import json
import sys

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.58 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
]

channel_logos = {
    "A&E": "https://cdn.tvpassport.com/image/station/960x540/v2/s10036_h15_aa.png",
    "ACC Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s111905_h15_ac.png",
    "AMC": "https://cdn.tvpassport.com/image/station/240x135/v2/s52247_h15_aa.png",
    "American Heroes Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s18284_h15_aa.png",
    "Animal Planet": "https://cdn.tvpassport.com/image/station/240x135/v2/s16331_h9_ad.png",
    "BBC America": "https://cdn.tvpassport.com/image/station/240x135/v2/s18332_h15_aa.png",
    "BBC World News HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s89542_h15_ab.png",
    "BET": "https://cdn.tvpassport.com/image/station/240x135/v2/s10051_h15_ad.png",
    # Add more channels to match mikekaprielian’s .m3u
}

# Initialize Chrome WebDriver
chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--crash-dumps-dir=/tmp")
chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

try:
    # Open the webpage
    url = "https://thetvapp.to/"
    driver.get(url)
    print("# Navigating to https://thetvapp.to/", file=sys.stderr)

    # Wait for the page to load
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "row")))

    # Find the Live TV Channels row
    try:
        live_tv_row = driver.find_element(By.XPATH, "//h3[contains(text(), 'Live TV Channels')]/..")
    except Exception as e:
        print(f"# Error finding Live TV Channels row: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Find all links in the Live TV Channels row
    links = live_tv_row.find_elements(By.TAG_NAME, "a")

    # Initialize a list to store the links
    live_tv_links = []

    # Iterate over each link
    for link in links:
        channel_name = link.text.strip()
        link_url = link.get_attribute("href")
        if channel_name and link_url and link_url.startswith("https://thetvapp.to/"):
            live_tv_links.append((channel_name, link_url))
        else:
            print(f"# Skipping invalid link: name={channel_name}, url={link_url}", file=sys.stderr)

    # Print the M3U header
    print('#EXTM3U url-tvg="https://raw.githubusercontent.com/BuddyChewChew/buddylive/main/en/videoall.xml"')

    # Iterate over each live TV channel link
    for name, link in live_tv_links:
        logo_url = channel_logos.get(name, "")
        m3u8_url = None

        try:
            # Navigate to the channel page
            driver.get(link)
            print(f"# Processing {name}: {link}", file=sys.stderr)
            time.sleep(random.uniform(1, 3))  # Random delay to avoid bot detection

            try:
                # Wait for video button to be clickable
                wait = WebDriverWait(driver, 30)
                video_button = None
                for button_id in ['loadVideoBtn', 'loadVideoBtnTwo', 'video-play-button', 'play-button']:
                    try:
                        video_button = wait.until(EC.element_to_be_clickable((By.ID, button_id)))
                        break
                    except:
                        continue
                if not video_button:
                    try:
                        video_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.play, button.video-play, .play-btn')))
                    except:
                        print(f"# No playable button found for {name}", file=sys.stderr)
                        continue
                
                # Scroll and click the button
                driver.execute_script("arguments[0].scrollIntoView(true);", video_button)
                driver.execute_script("arguments[0].click();", video_button)

                # Wait for network requests to load
                time.sleep(15)

                # Get network requests
                network_requests = driver.execute_script("return JSON.stringify(performance.getEntries());")
                network_requests = json.loads(network_requests)

                # Filter for .m3u8 URLs
                m3u8_urls = [req["name"] for req in network_requests if ".m3u8" in req.get("name", "").lower()]
                
                # Prefer URLs from thetvapp.to
                filtered_urls = [url for url in m3u8_urls if 'thetvapp.to' in url]
                m3u8_url = filtered_urls[0] if filtered_urls else (m3u8_urls[0] if m3u8_urls else None)
                
                if not m3u8_url:
                    print(f"# No valid .m3u8 URL found for {name}. Network requests: {m3u8_urls}", file=sys.stderr)
                    continue

                # Print channel info and URL
                print(f'#EXTINF:-1 group-title="USA TV" tvg-ID="{name}" tvg-name="{name}" tvg-logo="{logo_url}",{name}')
                print(m3u8_url)
                print(f"# Successfully added {name} with URL: {m3u8_url}", file=sys.stderr)

            except Exception as e:
                print(f"# Error processing video button for {name}: {str(e)}", file=sys.stderr)
                continue
        
        except Exception as e:
            print(f"# Error loading page for {name}: {str(e)}", file=sys.stderr)
            continue

finally:
    driver.quit()
