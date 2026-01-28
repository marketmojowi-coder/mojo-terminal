import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# CONFIGURATION (Pulls from Render Env Variables)
# If Env Variables aren't set, it defaults to the placeholder titles below
MANAGER_TITLE = os.getenv('MANAGER_ROLE', 'Lead Artificer')
ENTITY_ID = os.getenv('ENTITY_ID', 'M131228')

@app.route('/')
def home():
    return render_template('index.html', 
                           entity_id=ENTITY_ID, 
                           manager_title=MANAGER_TITLE)

@app.route('/index_search')
def historical_search():
    query = request.args.get('artificer', 'all')
    return jsonify({
        "status": "Success",
        "results": f"Filtering records for: {query}",
        "authorized_by": MANAGER_TITLE,
        "record_groups": ["RG 42", "RG 217"]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
