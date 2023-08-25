
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import urllib.request
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pocs.db'
db = SQLAlchemy(app)

class PoC(db.Model):
    __tablename__ = 'PoC'
    id = db.Column(db.Integer, primary_key=True)
    cve_id = db.Column(db.String(15), nullable=False)
    repo_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1000), nullable=True)

@app.route('/cve/<cve>', methods=['GET'])
def get_poc(cve):
    url = f"https://api.github.com/search/repositories?q={cve}&sort=stars&order=desc"
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req).read()
    data = json.loads(r.decode('utf-8'))
    
    # Check for the total count and items
    total_count = data.get('total_count', 0)
    items_added = 0

    for item in data['items']:
        try:
            poc = PoC(cve_id=cve, repo_url=item['html_url'], description=item['description'])
            db.session.add(poc)
            items_added += 1
        except Exception as e:
            # Log the error (for the sake of this example, we'll just print it)
            print(f"Error adding repo {item['html_url']}: {e}")

    db.session.commit()

    # Check if items added is less than total_count to detect possible pagination
    if items_added < total_count:
        message = f"{items_added} out of {total_count} repos added. There might be pagination or some repos failed to add."
    else:
        message = f"{items_added} repos added."

    return jsonify({'status': message}), 200

@app.route('/fetch_cve/<cve_id>', methods=['GET'])
def fetch_cve(cve_id):
    poc_data = PoC.query.filter_by(cve_id=cve_id).all()
    if poc_data:
        result = []
        for poc in poc_data:
            result.append({
                'id': poc.id,
                'cve_id': poc.cve_id,
                'repo_url': poc.repo_url,
                'description': poc.description
            })
        return jsonify(result), 200
    else:
        return jsonify({'message': f"No PoC found for {cve_id}"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
