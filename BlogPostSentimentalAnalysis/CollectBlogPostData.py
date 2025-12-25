from bs4 import BeautifulSoup
import requests



BaseURL = "https://oldschool.runescape.wiki/w/"


def get_bs_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the URL: {url}")
    return BeautifulSoup(response.text, 'html.parser')

def get_updates():
    soup = get_bs_html("https://oldschool.runescape.wiki/w/Game_updates")
    updates_links = []
    
    for update in soup.find_all('a', attrs={'title': lambda x: x and x.startswith("Update:")}):
        print(update)
        update_url = BaseURL + update['title'].replace(" ", "_")
        updates_links.append(update_url)
    return updates_links

def get_update_details(update_url):
    soup = get_bs_html(update_url)

    update_details = {}

    section = soup.find('h1', attrs={'class': 'mw-header'})
    update_details['main_header'] = section.text.strip()
    
    for section in soup.find_all(['h2', 'h3'], attrs={'class': 'mw-header'}):
        section_title = section.text.strip()
        
        section_content = section.find_next_sibling('p').text.strip()
        update_details[section_title] = section_content

    return update_details