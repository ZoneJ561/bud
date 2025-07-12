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
import urllib.parse

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
    "BET Her": "https://cdn.tvpassport.com/image/station/240x135/v2/s10052_h15_aa.png",
    "Big Ten Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s111906_h15_aa.png",
    "Bloomberg TV": "https://cdn.tvpassport.com/image/station/240x135/v2/s10053_h15_aa.png",
    "Boomerang": "https://cdn.tvpassport.com/image/station/240x135/v2/s18333_h15_aa.png",
    "Bravo": "https://cdn.tvpassport.com/image/station/240x135/v2/s10054_h15_aa.png",
    "Cartoon Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s10055_h15_aa.png",
    "CBS Sports Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s111907_h15_aa.png",
    "Cinemax": "https://cdn.tvpassport.com/image/station/240x135/v2/s10056_h15_aa.png",
    "CMT": "https://cdn.tvpassport.com/image/station/240x135/v2/s10057_h15_aa.png",
    "CNBC": "https://cdn.tvpassport.com/image/station/240x135/v2/s10058_h15_aa.png",
    "CNN": "https://cdn.tvpassport.com/image/station/240x135/v2/s10059_h15_aa.png",
    "Comedy Central": "https://cdn.tvpassport.com/image/station/240x135/v2/s10060_h15_aa.png",
    "Cooking Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s18285_h15_aa.png",
    "CSPAN": "https://cdn.tvpassport.com/image/station/240x135/v2/s10061_h15_aa.png",
    "CSPAN 2": "https://cdn.tvpassport.com/image/station/240x135/v2/s10062_h15_aa.png",
    "Destination America": "https://cdn.tvpassport.com/image/station/240x135/v2/s18286_h15_aa.png",
    "Discovery": "https://cdn.tvpassport.com/image/station/240x135/v2/s10063_h15_aa.png",
    "Discovery Family Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s18287_h15_aa.png",
    "Discovery Life": "https://cdn.tvpassport.com/image/station/240x135/v2/s18288_h15_aa.png",
    "Disney Channel (East)": "https://cdn.tvpassport.com/image/station/240x135/v2/s10064_h15_aa.png",
    "Disney Junior": "https://cdn.tvpassport.com/image/station/240x135/v2/s10065_h15_aa.png",
    "Disney XD": "https://cdn.tvpassport.com/image/station/240x135/v2/s10066_h15_aa.png",
    "E!": "https://cdn.tvpassport.com/image/station/240x135/v2/s10067_h15_aa.png",
    "ESPN": "https://cdn.tvpassport.com/image/station/240x135/v2/s10068_h15_aa.png",
    "ESPN2": "https://cdn.tvpassport.com/image/station/240x135/v2/s10069_h15_aa.png",
    "ESPNews": "https://cdn.tvpassport.com/image/station/240x135/v2/s111908_h15_aa.png",
    "ESPNU": "https://cdn.tvpassport.com/image/station/240x135/v2/s111909_h15_aa.png",
    "Food Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s10070_h15_aa.png",
    "Fox Business Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s10071_h15_aa.png",
    "FOX News Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s10072_h15_aa.png",
    "FOX Sports 1": "https://cdn.tvpassport.com/image/station/240x135/v2/s111910_h15_aa.png",
    "FOX Sports 2": "https://cdn.tvpassport.com/image/station/240x135/v2/s111911_h15_aa.png",
    "Freeform": "https://cdn.tvpassport.com/image/station/240x135/v2/s10073_h15_aa.png",
    "Fuse HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s89543_h15_aa.png",
    "FX": "https://cdn.tvpassport.com/image/station/240x135/v2/s10074_h15_aa.png",
    "FX Movie": "https://cdn.tvpassport.com/image/station/240x135/v2/s10075_h15_aa.png",
    "FXX": "https://cdn.tvpassport.com/image/station/240x135/v2/s10076_h15_aa.png",
    "FYI": "https://cdn.tvpassport.com/image/station/240x135/v2/s18289_h15_aa.png",
    "Golf Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s10077_h15_aa.png",
    "Hallmark": "https://cdn.tvpassport.com/image/station/240x135/v2/s10078_h15_aa.png",
    "Hallmark Drama HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s89544_h15_aa.png",
    "Hallmark Movies & Mysteries HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s89545_h15_aa.png",
    "HBO 2 East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10079_h15_aa.png",
    "HBO Comedy HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s89546_h15_aa.png",
    "HBO East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10080_h15_aa.png",
    "HBO Family East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10081_h15_aa.png",
    "HBO Signature": "https://cdn.tvpassport.com/image/station/240x135/v2/s10082_h15_aa.png",
    "HBO Zone HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s89547_h15_aa.png",
    "HGTV": "https://cdn.tvpassport.com/image/station/240x135/v2/s10083_h15_aa.png",
    "History": "https://cdn.tvpassport.com/image/station/240x135/v2/s10084_h15_aa.png",
    "HLN": "https://cdn.tvpassport.com/image/station/240x135/v2/s10085_h15_aa.png",
    "IFC": "https://cdn.tvpassport.com/image/station/240x135/v2/s10086_h15_aa.png",
    "Investigation Discovery": "https://cdn.tvpassport.com/image/station/240x135/v2/s10087_h15_aa.png",
    "ION Television East HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s10088_h15_aa.png",
    "Lifetime": "https://cdn.tvpassport.com/image/station/240x135/v2/s10089_h15_aa.png",
    "LMN": "https://cdn.tvpassport.com/image/station/240x135/v2/s10090_h15_aa.png",
    "Logo": "https://cdn.tvpassport.com/image/station/240x135/v2/s10091_h15_aa.png",
    "MeTV Toons": "https://cdn.tvpassport.com/image/station/240x135/v2/s89548_h15_aa.png",
    "MLB Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s111912_h15_aa.png",
    "MoreMAX": "https://cdn.tvpassport.com/image/station/240x135/v2/s10092_h15_aa.png",
    "MotorTrend HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s10093_h15_aa.png",
    "MovieMAX": "https://cdn.tvpassport.com/image/station/240x135/v2/s10094_h15_aa.png",
    "MSNBC": "https://cdn.tvpassport.com/image/station/240x135/v2/s10095_h15_aa.png",
    "MTV": "https://cdn.tvpassport.com/image/station/240x135/v2/s10096_h15_aa.png",
    "Nat Geo WILD": "https://cdn.tvpassport.com/image/station/240x135/v2/s10097_h15_aa.png",
    "National Geographic": "https://cdn.tvpassport.com/image/station/240x135/v2/s10098_h15_aa.png",
    "NBA TV": "https://cdn.tvpassport.com/image/station/240x135/v2/s111913_h15_aa.png",
    "Newsmax TV": "https://cdn.tvpassport.com/image/station/240x135/v2/s10099_h15_aa.png",
    "NFL Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s111914_h15_aa.png",
    "NFL Red Zone": "https://cdn.tvpassport.com/image/station/240x135/v2/s111915_h15_aa.png",
    "NHL Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s111916_h15_aa.png",
    "Nick Jr.": "https://cdn.tvpassport.com/image/station/240x135/v2/s10100_h15_aa.png",
    "Nickelodeon East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10101_h15_aa.png",
    "Nicktoons": "https://cdn.tvpassport.com/image/station/240x135/v2/s10102_h15_aa.png",
    "Outdoor Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s10103_h15_aa.png",
    "OWN": "https://cdn.tvpassport.com/image/station/240x135/v2/s10104_h15_aa.png",
    "Oxygen True Crime": "https://cdn.tvpassport.com/image/station/240x135/v2/s10105_h15_aa.png",
    "PBS 13 (WNET) New York": "https://cdn.tvpassport.com/image/station/240x135/v2/s10106_h15_aa.png",
    "ReelzChannel": "https://cdn.tvpassport.com/image/station/240x135/v2/s10107_h15_aa.png",
    "Science": "https://cdn.tvpassport.com/image/station/240x135/v2/s10108_h15_aa.png",
    "SEC Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s111917_h15_aa.png",
    "Showtime (E)": "https://cdn.tvpassport.com/image/station/240x135/v2/s10109_h15_aa.png",
    "SHOWTIME 2": "https://cdn.tvpassport.com/image/station/240x135/v2/s10110_h15_aa.png",
    "STARZ East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10111_h15_aa.png",
    "SundanceTV HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s10112_h15_aa.png",
    "SYFY": "https://cdn.tvpassport.com/image/station/240x135/v2/s10113_h15_aa.png",
    "TBS": "https://cdn.tvpassport.com/image/station/240x135/v2/s10114_h15_aa.png",
    "TCM": "https://cdn.tvpassport.com/image/station/240x135/v2/s10115_h15_aa.png",
    "TeenNick": "https://cdn.tvpassport.com/image/station/240x135/v2/s10116_h15_aa.png",
    "Telemundo East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10117_h15_aa.png",
    "Tennis Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s111918_h15_aa.png",
    "The CW (WPIX New York)": "https://cdn.tvpassport.com/image/station/240x135/v2/s10118_h15_aa.png",
    "The Movie Channel East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10119_h15_aa.png",
    "The Weather Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s10120_h15_aa.png",
    "TLC": "https://cdn.tvpassport.com/image/station/240x135/v2/s10121_h15_aa.png",
    "TNT": "https://cdn.tvpassport.com/image/station/240x135/v2/s10122_h15_aa.png",
    "Travel Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s10123_h15_aa.png",
    "truTV": "https://cdn.tvpassport.com/image/station/240x135/v2/s10124_h15_aa.png",
    "TV One HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s89549_h15_aa.png",
    "Universal Kids": "https://cdn.tvpassport.com/image/station/240x135/v2/s10125_h15_aa.png",
    "Univision East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10126_h15_aa.png",
    "USA Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s10127_h15_aa.png",
    "VH1": "https://cdn.tvpassport.com/image/station/240x135/v2/s10128_h15_aa.png",
    "VICE": "https://cdn.tvpassport.com/image/station/240x135/v2/s10129_h15_aa.png",
    "WABC (New York) ABC East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10130_h15_aa.png",
    "WCBS (New York) CBS East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10131_h15_aa.png",
    "WE tv": "https://cdn.tvpassport.com/image/station/240x135/v2/s10132_h15_aa.png",
    "WNBC (New York) NBC East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10133_h15_aa.png",
    "WNYW (New York) FOX East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10134_h15_aa.png",
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

    # Filter links to only those in channel_logos
    live_tv_links = []
    for link in links:
        channel_name = link.text.strip()
        link_url = link.get_attribute("href")
        if channel_name in channel_logos and link_url and link_url.startswith("https://thetvapp.to/"):
            live_tv_links.append((channel_name, link_url))
        else:
            print(f"# Skipping link: name={channel_name}, url={link_url}", file=sys.stderr)

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
            time.sleep(random.uniform(2, 5))  # Increased random delay to avoid bot detection

            try:
                # Wait for video button to be clickable
                wait = WebDriverWait(driver, 30)
                video_button = None
                for button_selector in [
                    (By.ID, 'loadVideoBtn'),
                    (By.ID, 'loadVideoBtnTwo'),
                    (By.ID, 'video-play-button'),
                    (By.ID, 'play-button'),
                    (By.CSS_SELECTOR, 'button.play, button.video-play, .play-btn, button.btn-play'),
                ]:
                    try:
                        video_button = wait.until(EC.element_to_be_clickable(button_selector))
                        break
                    except:
                        continue
                if not video_button:
                    print(f"# No playable button found for {name}", file=sys.stderr)
                    continue
                
                # Scroll and click the button using JavaScript
                driver.execute_script("arguments[0].scrollIntoView(true);", video_button)
                driver.execute_script("arguments[0].click();", video_button)

                # Wait for network requests to load
                time.sleep(20)  # Increased to ensure requests are captured

                # Clear performance entries to avoid old requests
                driver.execute_script("performance.clearResourceTimings();")
                time.sleep(1)

                # Get network requests
                network_requests = driver.execute_script("return JSON.stringify(performance.getEntriesByType('resource'));")
                network_requests = json.loads(network_requests)

                # Filter for .m3u8 URLs
                m3u8_urls = [req["name"] for req in network_requests if ".m3u8" in req.get("name", "").lower()]
                
                # Prefer direct .m3u8 URLs from thetvapp.to
                filtered_urls = [url for url in m3u8_urls if 'thetvapp.to' in url and 'tracks-v2a1/mono.m3u8' in url]
                if filtered_urls:
                    m3u8_url = filtered_urls[0]
                
                # Fallback: Check ping.gif URLs for .m3u8 in mu parameter
                if not m3u8_url:
                    for req in network_requests:
                        url = req.get("name", "")
                        if 'thetvapp.to/v1/error/ping.gif' in url:
                            parsed = urllib.parse.urlparse(url)
                            query_params = urllib.parse.parse_qs(parsed.query)
                            mu_url = query_params.get('mu', [None])[0]
                            if mu_url and '.m3u8' in mu_url:
                                m3u8_url = mu_url
                                break
                
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
