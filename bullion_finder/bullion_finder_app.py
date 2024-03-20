import os
import json
from flask import Blueprint, Flask, render_template, request, redirect, url_for
from .scraper import JMBullionScraper, APMEXScraper
from flask import jsonify
from flask import render_template_string

# Create a blueprint for the bullion finder app
bullion_finder_app = Blueprint('bullion_finder_app', __name__, template_folder="../templates", static_folder="../static")

# Define the path to the JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, "scraped_results.json")

# Function to save data to JSON file
def save_to_json(data):
    with open(json_file_path, "w") as f:
        json.dump(data, f)

# Function to load data from JSON file
def load_from_json():
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            # Filter out items with no price
            filtered_data = [item for item in data if item.get('price')]
            return filtered_data
    except FileNotFoundError:
        return []


# Define routes for the bullion finder app
@bullion_finder_app.route('/')
def index():
    return render_template('bullion_finder.html')


@bullion_finder_app.route('/search', methods=['POST', 'GET'])
def search():
    # Check if it's a POST request (initial search) or a GET request (pagination)
    if request.method == 'POST':
        search_query = request.form['search_query'].lower()
    else:
        search_query = request.args.get('search_query', '').lower()
    
    page = request.args.get('page', 1, type=int)
    items_per_page = 21
    
    # Load data from JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "scraped_results.json")
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    
    # Filter data based on search query
    filtered_data = [item for item in data if search_query in item['title'].lower()]
    
    # Pagination logic
    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_data = filtered_data[start:end]
    
    # For AJAX requests, return JSON with paginated data
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(results=paginated_data, has_more=(end < len(filtered_data)))
    
    # For initial load or non-AJAX pagination, render template with paginated data
    return render_template('search_results.html', results=paginated_data, search_query=search_query, next_page=page + 1, has_more=(end < len(filtered_data)))

@bullion_finder_app.route('/results')
def results():
    page = int(request.args.get('page', 1))
    items_per_page = 21
    start = (page - 1) * items_per_page
    end = start + items_per_page

    # Load your JSON data as before
    try:
        with open(json_file_path, "r") as f:
            all_data = json.load(f)
    except FileNotFoundError:
        all_data = []

    paginated_data = all_data[start:end]

    # Check if the request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return only the HTML for the products
        products_html = render_template_string('''
        {% for result in paginated_data %}
            <li class="result-item">
                <img src="{{ result.image }}" alt="{{ result.title }}">
                <div class="item-info">
                    <a href="{{ result.link }}">{{ result.title }}</a>
                    <div class="price">{{ result.price }}</div>
                </div>
            </li>
        {% endfor %}
        ''', paginated_data=paginated_data)
        return jsonify(html=products_html, next_page=page+1)
    else:
        # Initial page load
        return render_template('search_results.html', results=paginated_data, next_page=page+1)
