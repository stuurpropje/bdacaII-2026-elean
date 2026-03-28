import json
import re
import time
from collections import Counter

import pandas as pd
import requests
from tqdm import tqdm

def api_get(title: str, 
            api_url: str="https://en.wikipedia.org/w/api.php", 
            user_agent: str = "Wingspan student project (13411438@uva.nl)", 
            request_delay: float=0.5, 
            timeout: int=30
            ) -> dict | None:
    """Make a safe request to the MediaWiki API with retries and rate limits"""
    
    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})

    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'revisions',
        'rvprop': 'content',
        'rvslots': 'main',
        'redirects': 1,  # follow redirects to get the content
    }

    try:
        response = session.get(api_url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except json.JSONDecodeError:
        print("Response was not valid JSON")
        return None
    finally:
        time.sleep(request_delay)

    return data

def get_article_links_wikitext(title: str) -> list[str]:
    """Extract internal Wikipedia links from the main body of the article"""
    data = api_get(title)
    if not data or 'query' not in data:
        return []

    pages = data['query']['pages']
    page_id = list(pages.keys())[0]
    if page_id == '-1' or 'revisions' not in pages[page_id]:
        return []

    wikitext = pages[page_id]['revisions'][0]['slots']['main']['*']

    parts = re.split(r'==\s*See also\s*==', wikitext, maxsplit=1)
    body = parts[0]

    # extract both the target AND the display text from links: 
    # [[Target|Display]]
    # group 1: target, group 2: display (if exists)
    raw_links = re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', body)

    extracted_terms = []
    for target, display in raw_links:
        # skip namespaces like Category: or File:
        if ':' in target: 
            continue
        extracted_terms.append(target.strip())
        if display:
            extracted_terms.append(display.strip())

    # extract tuples of target name, display name
    raw_links = re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', body)

    extracted_terms = []
    for target, display in raw_links:
        # skip file: category: etc
        if ':' in target: 
            continue
        
        # keep both link and display text
        extracted_terms.append(target.strip())
        if display:
            extracted_terms.append(display.strip())

    return extracted_terms

def find_edges(wingspan_birds):
    """Find linking edges between Wingspan birds based on Wikipedia links"""
    common_names = wingspan_birds['EnglishName'].tolist()
    common_names_lower = {name.lower() for name in common_names}
    scientific_names = wingspan_birds['ScientificName'].tolist()

    # tie scientific names to common names for easy lookup
    scientific_to_common_names = dict(zip(scientific_names, common_names))

    # only keep wingspan birds as list
    edges = []

    # only keep the link if the target is ALSO a Wingspan bird AND not itself
    # ensure case insensitive matching
    # preserve original for readability
    for scientific_name, common_name in tqdm(scientific_to_common_names.items()):
        linked_bird = get_article_links_wikitext(scientific_name) 

        linked_bird_counts = Counter(linked_bird)
        
        for linked_name, count in linked_bird_counts.items():
            linked_name_lower = linked_name.lower()
            if linked_name_lower in common_names_lower and linked_name_lower != common_name.lower():
                edges.append({
                    "source_bird": common_name,
                    "target_bird": linked_name,
                    "count": count
                })

        # rate limit to respect Wikipedia API guidelines
        time.sleep(0.1) 

    return edges

if __name__ == "__main__":
    df_birds = pd.read_excel("../data/raw/Wingspan Bird List ENG-NED-DEU.xlsx")

    edges = find_edges(df_birds)

    pd.DataFrame(edges).to_csv(
        "../data/processed/wikipedia_bird_links_with_counts.csv", 
        index=False
        )