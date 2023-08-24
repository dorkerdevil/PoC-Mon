### Description
This repository contains two primary scripts focused on managing and retrieving Proof of Concepts (PoCs) associated with specific CVE IDs:

1. pocgrabber.py: A script dedicated to grabbing PoCs from GitHub based on the provided CVE ID.

2. cve.py: Houses the Flask application setup, routes, and SQLite database models for storing and managing PoCs.

### Dependencies
Install These Dependencies using pip3:
```
requests json argparse sqlite3 flask flask_sqlalchemy
```

### Usage
PoC Grabber (pocgrabber.py):
Fetch PoCs from GitHub for a specific CVE ID using cli:
```
python pocgrabber.py <cve-id> -s <set sleep timing , Default to 12 hours>
```
CVE Application (cve.py):
This will start the flask api you can use it and saves the info in db file .
```
FLASK_APP=cve.py flask run
```
```
http://127.0.0.1:5000/cve/<CVE-ID>  (This will fetch the repos related to CVE-ID) and saves them to the database
http://127.0.0.1:5000/fetch_cve/<CVE-ID> (You can fetch the CVE-ID from the database)
```

### Feedback & Contributions:
For suggestions, bugs, or feature requests, please open an issue. If you'd like to contribute, create a branch for each feature or fix, and submit a pull request for review.


