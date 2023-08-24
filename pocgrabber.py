import requests
import json
import argparse
import time
import sqlite3
from datetime import datetime

def get_github_pocs(cve_id):
    url = f"https://api.github.com/search/repositories?q={cve_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data['items']
    else:
        print(f"Failed to get data for CVE ID: {cve_id}")
        return None

def save_to_db(cve_id, pocs):
    conn = sqlite3.connect('pocs.db')
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS pocs
                 (cve_id text, name text, url text, description text, fetched_at text)''')

    for poc in pocs:
        # Insert a row of data
        c.execute("INSERT INTO pocs VALUES (?, ?, ?, ?, ?)",
                  (cve_id, poc['name'], poc['html_url'], poc['description'], datetime.now()))

    # Save (commit) the changes
    conn.commit()

    # Close the connection
    conn.close()

def main(cve_id, sleep_time):
    while True:
        pocs = get_github_pocs(cve_id)

        if pocs is not None:
            print(f"Found {len(pocs)} PoCs for {cve_id} on GitHub:")
            for poc in pocs:
                print(f"Name: {poc['name']}, URL: {poc['html_url']}, Description: {poc['description']}")

            save_to_db(cve_id, pocs)

        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find GitHub PoCs for a specific CVE ID.')
    parser.add_argument('cve_id', type=str, help='The CVE ID to find PoCs for.')
    parser.add_argument('-s', '--sleep_time', type=int, default=43200, help='The sleep time between checks, in seconds (default is 12 hours).')
    args = parser.parse_args()

    main(args.cve_id, args.sleep_time)
