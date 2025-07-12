import requests
from bs4 import BeautifulSoup
import pytz
from datetime import datetime, timedelta
import time
import sys

# Updated channel IDs based on tvpassport.com (verified manually where possible)
channel_names = {
    "ae/10036": "A&E",
    "acc-network/111905": "ACC Network",
    "amc/52247": "AMC",
    "american-heroes-channel/18284": "American Heroes Channel",
    "animal-planet/16331": "Animal Planet",
    "bbc-america/18332": "BBC America",
    "bbc-world-news/89542": "BBC World News HD",
    "bet/10051": "BET",
    # Add more channels to match videolivetv.py’s channel_logos
    "bet-her/10052": "BET Her",
    "big-ten-network/111906": "Big Ten Network",
    "bloomberg-television/10053": "Bloomberg TV",
    "boomerang/18333": "Boomerang",
    "bravo/10054": "Bravo",
    "cartoon-network/10055": "Cartoon Network",
    "cbs-sports-network/111907": "CBS Sports Network",
    "cinemax/10056": "Cinemax",
    "cmt/10057": "CMT",
    "cnbc/10058": "CNBC",
    "cnn/10059": "CNN",
    "comedy-central/10060": "Comedy Central",
    "cooking-channel/18285": "Cooking Channel",
    "cspan/10061": "CSPAN",
    "cspan-2/10062": "CSPAN 2",
    "destination-america/18286": "Destination America",
    "discovery-channel/10063": "Discovery",
    "discovery-family/18287": "Discovery Family Channel",
    "discovery-life/18288": "Discovery Life",
    "disney-channel/10064": "Disney Channel (East)",
    "disney-junior/10065": "Disney Junior",
    "disney-xd/10066": "Disney XD",
    "e/10067": "E!",
    "espn/10068": "ESPN",
    "espn2/10069": "ESPN2",
    "espnews/111908": "ESPNews",
    "espnu/111909": "ESPNU",
    "food-network/10070": "Food Network",
    "fox-business/10071": "Fox Business Network",
    "fox-news-channel/10072": "FOX News Channel",
    "fs1/111910": "FOX Sports 1",
    "fs2/111911": "FOX Sports 2",
    "freeform/10073": "Freeform",
    "fuse/89543": "Fuse HD",
    "fx/10074": "FX",
    "fxm/10075": "FX Movie",
    "fxx/10076": "FXX",
    "fyi/18289": "FYI",
    "golf-channel/10077": "Golf Channel",
    "hallmark-channel/10078": "Hallmark",
    "hallmark-drama/89544": "Hallmark Drama HD",
    "hallmark-movies-mysteries/89545": "Hallmark Movies & Mysteries HD",
    "hbo-2/10079": "HBO 2 East",
    "hbo-comedy/89546": "HBO Comedy HD",
    "hbo/10080": "HBO East",
    "hbo-family/10081": "HBO Family East",
    "hbo-signature/10082": "HBO Signature",
    "hbo-zone/89547": "HBO Zone HD",
    "hgtv/10083": "HGTV",
    "history/10084": "History",
    "hln/10085": "HLN",
    "ifc/10086": "IFC",
    "investigation-discovery/10087": "Investigation Discovery",
    "ion/10088": "ION Television East HD",
    "lifetime/10089": "Lifetime",
    "lmn/10090": "LMN",
    "logo/10091": "Logo",
    "metv-toons/89548": "MeTV Toons",
    "mlb-network/111912": "MLB Network",
    "moremax/10092": "MoreMAX",
    "motortrend/10093": "MotorTrend HD",
    "moviemax/10094": "MovieMAX",
    "msnbc/10095": "MSNBC",
    "mtv/10096": "MTV",
    "nat-geo-wild/10097": "Nat Geo WILD",
    "national-geographic-channel/10098": "National Geographic",
    "nba-tv/111913": "NBA TV",
    "newsmax/10099": "Newsmax TV",
    "nfl-network/111914": "NFL Network",
    "nfl-redzone/111915": "NFL Red Zone",
    "nhl-network/111916": "NHL Network",
    "nick-jr/10100": "Nick Jr.",
    "nickelodeon/10101": "Nickelodeon East",
    "nicktoons/10102": "Nicktoons",
    "outdoor-channel/10103": "Outdoor Channel",
    "own/10104": "OWN",
    "oxygen/10105": "Oxygen True Crime",
    "pbs-wnet/10106": "PBS 13 (WNET) New York",
    "reelz/10107": "ReelzChannel",
    "science-channel/10108": "Science",
    "sec-network/111917": "SEC Network",
    "showtime/10109": "Showtime (E)",
    "showtime-2/10110": "SHOWTIME 2",
    "starz/10111": "STARZ East",
    "sundance-tv/10112": "SundanceTV HD",
    "syfy/10113": "SYFY",
    "tbs/10114": "TBS",
    "tcm/10115": "TCM",
    "teennick/10116": "TeenNick",
    "telemundo/10117": "Telemundo East",
    "tennis-channel/111918": "Tennis Channel",
    "the-cw-wpix/10118": "The CW (WPIX New York)",
    "the-movie-channel/10119": "The Movie Channel East",
    "weather-channel/10120": "The Weather Channel",
    "tlc/10121": "TLC",
    "tnt/10122": "TNT",
    "travel-channel/10123": "Travel Channel",
    "tru-tv/10124": "truTV",
    "tv-one/89549": "TV One HD",
    "universal-kids/10125": "Universal Kids",
    "univision/10126": "Univision East",
    "usa-network/10127": "USA Network",
    "vh1/10128": "VH1",
    "vice/10129": "VICE",
    "abc/10130": "WABC (New York) ABC East",
    "cbs/10131": "WCBS (New York) CBS East",
    "we-tv/10132": "WE tv",
    "nbc/10133": "WNBC (New York) NBC East",
    "fox/10134": "WNYW (New York) FOX East",
}

def convert_to_xmltv_time(dt):
    return dt.strftime('%Y%m%d%H%M%S %z')

def fetch_page(url, retries=3, backoff=2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
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
        # Fallback: Try scraping channel page for listings
        channel_page = f"https://www.tvpassport.com/tv-listings/stations/{channel_id}"
        html_content = fetch_page(channel_page)
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
