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
        update_url = BaseURL + update['title'].replace(" ", "_")
        updates_links.append(update_url)
    return updates_links

def get_update_details(update_url):
    soup = get_bs_html(update_url)
    content = soup.find('div', attrs={'id': 'content'})

    update_details = {}
    update_details["date"] = "No Date Found"

    changelog_date = soup.find('span', class_='mw-headline', id=re.compile(r'^Changelog_'))
    if changelog_date:
        changelog_date_text = changelog_date.text.strip()
        m = re.search(r'Changelog\s*[-–]\s*(.+)', changelog_date_text, re.I)
        if m:
            update_details["date"] = m.group(1).strip()
        else:
            idval = changelog_date.get('id', '')
            if idval.startswith('Changelog_'):
                update_details["date"] = idval[len('Changelog_'):].replace('_', ' ').strip()
            else:
                update_details["date"] = changelog_date_text

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
    """
    Sanitizes a string to make it a safe filename.
    Replaces invalid characters with underscores.
    """
    invalid_chars_pattern = r'[\\:*?"<>|/]'
    sanitized_name = re.sub(invalid_chars_pattern, '_', name)
    sanitized_name = ''.join(char for char in sanitized_name if char.isprintable())
    return sanitized_name.strip()

if __name__ == "__main__":
    load_dotenv()
    main_file_path = os.getenv("FILE_PATH") + "BlogPostSentimentalAnalysis/BlogPosts/"
    
    for update_link in get_updates():
        path = Path(main_file_path) / f"{sanitize_filename(update_link.split('/')[-1])}.txt"
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        details = get_update_details(update_link)
        with open(path, "w", encoding="utf-8") as file:
            for key, value in details.items():
                file.write(f"{key}\n{value}\n\n")
        with open("AllBlogPosts.txt", "a", encoding="utf-8") as file:
            file.write(f"--- {update_link.split('/')[-1]} ---\n")
            for key, value in details.items():
                file.write(f"{key}\n{value}\n\n")

    