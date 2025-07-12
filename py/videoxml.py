import requests
from bs4 import BeautifulSoup
import pytz
from datetime import datetime, timedelta
import time
import sys

channel_names = {
    "ae-canada/4311": "A&E",
    "acc-network/130609": "ACC Network",
    "amc-canada/4313": "AMC",
    "american-heroes-channel/12388": "American Heroes Channel",
    "animal-planet-canada/4315": "Animal Planet",
    "bbc-america/12436": "BBC America",
    "bbc-world-news-hd/89666": "BBC World News HD",
    "bet/4331": "BET",
    # ... (all other channels from your original file)
}

def convert_to_xmltv_time(dt):
    return dt.strftime('%Y%m%d%H%M%S %z')

def fetch_page(url, retries=3, backoff=2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"# Error fetching {url}: {e}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(backoff * (2 ** attempt))
            else:
                return None
    return None

def get_program_data(channel_id, date):
    url = f"https://www.tvpassport.com/tv-listings/stations/{channel_id}/{date.strftime('%Y%m%d')}"
    html_content = fetch_page(url)
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    programs = []
    listings = soup.find_all('div', class_='row listing')
    
    for listing in listings:
        time_elem = listing.find('div', class_='col-time')
        title_elem = listing.find('div', class_='col-title')
        desc_elem = listing.find('div', class_='col-description')
        
        if time_elem and title_elem:
            time_str = time_elem.text.strip()
            try:
                start_time = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {time_str}", '%Y-%m-%d %I:%M %p')
                start_time = pytz.timezone('America/New_York').localize(start_time)
            except ValueError:
                continue
            
            title = title_elem.text.strip()
            desc = desc_elem.text.strip() if desc_elem else ""
            
            duration_elem = listing.find('div', class_='col-duration')
            duration = 30
            if duration_elem:
                duration_text = duration_elem.text.strip()
                try:
                    duration = int(duration_text.split()[0])
                except (ValueError, IndexError):
                    pass
            
            end_time = start_time + timedelta(minutes=duration)
            
            programs.append({
                'start': start_time,
                'end': end_time,
                'title': title,
                'desc': desc
            })
    
    return programs

def create_xml(channels, date):
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<!DOCTYPE tv SYSTEM "xmltv.dtd">')
    print('<tv generator-info-name="TVPassport Scraper">')
    
    for channel_id, channel_name in channels.items():
        print(f'  <channel id="{channel_name}">')
        print(f'    <display-name>{channel_name}</display-name>')
        print('  </channel>')
    
    for channel_id, channel_name in channels.items():
        programs = get_program_data(channel_id, date)
        for program in programs:
            start_time = convert_to_xmltv_time(program['start'])
            end_time = convert_to_xmltv_time(program['end'])
            print(f'  <programme start="{start_time}" stop="{end_time}" channel="{channel_name}">')
            print(f'    <title lang="en">{program["title"]}</title>')
            if program['desc']:
                print(f'    <desc lang="en">{program["desc"]}</desc>')
            print('  </programme>')
    
    print('</tv>')

if __name__ == "__main__":
    today = datetime.now(pytz.timezone('America/New_York')).replace(hour=0, minute=0, second=0, microsecond=0)
    create_xml(channel_names, today)
