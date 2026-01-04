from bs4 import BeautifulSoup
import json
import requests

ItemID_URL = "https://oldschool.runescape.wiki/w/Item_IDs"

def get_bs_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the URL: {url}")
    return BeautifulSoup(response.text, 'html.parser')

def scrape_item_ids():
    soup = get_bs_html(ItemID_URL)
    item_table = soup.find('tbody')
    
    item_ids = {}
    
    if item_table:
        rows = item_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 2: 
                continue
            item_name = cols[0].text.strip()
            item_id = cols[1].text.strip()
            item_ids[item_name] = item_id
    
    return item_ids

def save_item_ids(item_ids, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(item_ids, indent=4))

# Main execution
item_ids = scrape_item_ids()
save_item_ids(item_ids, "ItemIDs.json")
