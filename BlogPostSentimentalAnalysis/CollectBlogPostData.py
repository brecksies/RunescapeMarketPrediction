from bs4 import BeautifulSoup
from pathlib import Path
from dotenv import load_dotenv
import re
import os
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
        update_url = BaseURL + update['title']
        updates_links.append(update_url)
    return updates_links

def get_update_details(update_url):
    update_url = sanitize_URL(update_url)
    soup = get_bs_html(update_url)
    content = soup.find('div', attrs={'id': 'content'})

    update_details = {}

    update_date_information = soup.find('div', attrs={'class': 'update'})
    date_text = "Not found"
    if update_date_information:
        date_text = ""
        date_information = update_date_information.find_all('a', attrs={'title': re.compile("^\\d+.*")})
        if date_information and len(date_information) >= 2: 
            for date_div in date_information[0:2]: # Get first two since any further date parts include revisions 
                date_text += date_div['title'].strip() + " "
    update_details["Date:"] = date_text.strip()

    for section in content.find_all(['h1', 'h2', 'h3']):
        section_title = section.text.strip()
        section_content = extract_contents_under_header(section)
        update_details[section_title] = section_content

    return update_details

def extract_contents_under_header(header_section):
    contents = ""
    if header_section is None:
        return contents
        
    nextSection = header_section.find_next_sibling()
    while nextSection and nextSection.name not in ['h1', 'h2', 'h3']:
        if nextSection.has_attr('class') and 'mw-footer' in nextSection['class']:
            break
        match (nextSection.name):
            case 'p':
                contents += nextSection.text.strip() + "\n"
                break
            case 'ul':
                for li in nextSection.find_all('li'):
                    contents += "- " + li.text.strip() + "\n"
                break
            case 'ol':
                for idx, li in enumerate(nextSection.find_all('li'), start=1):
                    contents += f"{idx}. " + li.text.strip() + "\n"
                break
        nextSection = nextSection.find_next_sibling()
    return contents

def sanitize_filename(name):
    invalid_chars_pattern = r'[\\:*?"<>|/]'
    sanitized_name = re.sub(invalid_chars_pattern, '_', name)
    sanitized_name = ''.join(char for char in sanitized_name if char.isprintable())
    return sanitized_name.strip()

def sanitize_URL(url):
    url = url.replace("?", "%3F").replace("&", "%26").replace("=", "%3D").replace("'", "%27").replace("#", "%23").replace("+", "%2B").replace(" ", "_")
    return url

if __name__ == "__main__":
    load_dotenv()
    main_file_path = os.getenv("FILE_PATH") + "BlogPostSentimentalAnalysis/BlogPosts/"
    
    for update_link in get_updates():
        path = Path(main_file_path) / f"{sanitize_filename(update_link.split('/')[-1])}.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        details = get_update_details(update_link)
        with open(path, "w", encoding="utf-8") as file:
            for key, value in details.items():
                file.write(f"{key}\n{value}\n\n")
        with open("AllBlogPosts.txt", "a", encoding="utf-8") as file:
            file.write(f"--- {update_link.split('/')[-1]} ---\n")
            for key, value in details.items():
                file.write(f"{key}\n{value}\n\n")

    