from flask import Flask, jsonify, request

app = Flask(__name__)

def read_data_file():
    data = []
    try:
        with open('International_location.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = [part.strip() for part in line.split(',')]
                    if len(parts) >= 2:
                        # Handle different formats in the data
                        if len(parts) == 2:
                            # Format: "U.A.E,United Arab Emirates"
                            item = {
                                'name': parts[0],
                                'country': parts[1],
                                'region': '',
                                'type': 'Country'
                            }
                        elif len(parts) == 3:
                            # Format: "Burj Khalifa,U.A.E,United Arab Emirates"
                            item = {
                                'name': parts[0],
                                'country': parts[2],
                                'region': parts[1],
                                'type': 'Landmark'
                            }
                        elif len(parts) == 4:
                            # Format: "Malé Local Market,Maldives,Maldives,Malé"
                            # Or "Gardens by the Bay,Gardens by the Bay,Singapore,Nature/Landmark"
                            if parts[1] == parts[2]:
                                item = {
                                    'name': parts[0],
                                    'country': parts[1],
                                    'region': parts[3],
                                    'type': 'Attraction'
                                }
                            else:
                                item = {
                                    'name': parts[0],
                                    'country': parts[2],
                                    'region': parts[1],
                                    'type': parts[3] if '/' not in parts[3] else parts[3].split('/')[0]
                                }
                        else:
                            # Handle other formats if needed
                            item = {
                                'name': parts[0],
                                'country': parts[-1],
                                'region': parts[-2] if len(parts) > 2 else '',
                                'type': 'Place'
                            }
                        data.append(item)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
    return data

@app.route('/api/locations', methods=['GET'])
def get_all_locations():
    data = read_data_file()
    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data
    })

@app.route('/api/locations/<search_term>', methods=['GET'])
def search_locations(search_term):
    data = read_data_file()
    search_term = search_term.lower()
    results = [
        loc for loc in data 
        if (search_term in loc['name'].lower() or 
            search_term in loc['country'].lower() or 
            search_term in loc['region'].lower() or
            search_term in loc['type'].lower())
    ]
    return jsonify({
        'status': 'success',
        'search_term': search_term,
        'count': len(results),
        'data': results
    })

@app.route('/api/countries/<country_name>', methods=['GET'])
def get_by_country(country_name):
    data = read_data_file()
    country_name = country_name.lower()
    results = [
        loc for loc in data 
        if country_name in loc['country'].lower()
    ]
    return jsonify({
        'status': 'success',
        'country': country_name,
        'count': len(results),
        'data': results
    })

@app.route('/api/regions/<region_name>', methods=['GET'])
def get_by_region(region_name):
    data = read_data_file()
    region_name = region_name.lower()
    results = [
        loc for loc in data 
        if region_name in loc['region'].lower()
    ]
    return jsonify({
        'status': 'success',
        'region': region_name,
        'count': len(results),
        'data': results
    })

@app.route('/api/types/<location_type>', methods=['GET'])
def get_by_type(location_type):
    data = read_data_file()
    location_type = location_type.lower()
    results = [
        loc for loc in data 
        if location_type in loc['type'].lower()
    ]
    return jsonify({
        'status': 'success',
        'type': location_type,
        'count': len(results),
        'data': results
    })

@app.route('/')
def home():
    return """
    <h1>International Location API</h1>
    <p>Try these endpoints:</p>
    <ul>
        <li><a href="/api/locations">All locations</a></li>
        <li><a href="/api/locations/dubai">Search 'dubai'</a></li>
        <li><a href="/api/countries/thailand">Country 'thailand'</a></li>
        <li><a href="/api/regions/bangkok">Region 'bangkok'</a></li>
        <li><a href="/api/types/beach">Type 'beach'</a></li>
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=500)