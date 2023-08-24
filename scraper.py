import requests
import json
from bs4 import BeautifulSoup

def get_pocs(cve_id):
    url = f"https://poc-in-github.motikan2010.net/api/v1/?cve_id={cve_id}"
    response = requests.get(url)

    # If the request was successful, 'status_code' will be 200
    if response.status_code == 200:
        data = json.loads(response.text)
        return data['pocs']
    else:
        print(f"Failed to get data for CVE ID: {cve_id}")
        return None

def main():
    # Fetch the RSS feed and parse it
    url = "https://poc-in-github.motikan2010.net/rss/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')

    # Extract the CVE IDs from the feed entries
    cve_ids = [item.category.text for item in soup.find_all('item')]

    for cve_id in cve_ids:
        pocs = get_pocs(cve_id)
        if pocs is not None:
            print(f"Found {len(pocs)} PoCs for {cve_id}:")
            for poc in pocs:
                print(f"ID: {poc['id']}, Name: {poc['name']}, URL: {poc['html_url']}")

if __name__ == "__main__":
    main()
