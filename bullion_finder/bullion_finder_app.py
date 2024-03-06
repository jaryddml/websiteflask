import os
import json
from flask import Blueprint, Flask, render_template, request, redirect, url_for

from .scraper import JMBullionScraper, APMEXScraper

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

# Function to sort results based on price
def sort_results(data, sort_by):
    def get_price_value(item):
        price_str = item.get('price', '').replace('$', '').replace(',', '').strip()
        return float(price_str) if price_str else float('inf')  # Return infinity if price is empty

    if sort_by == "price_asc":
        return sorted(data, key=lambda x: get_price_value(x))
    elif sort_by == "price_desc":
        return sorted(data, key=lambda x: get_price_value(x), reverse=True)
    else:
        return data

# Function to sort results by price
def sort_results_by_price(data, sort_order):
    def get_price_value(item):
        price_str = item.get('price', '').replace('$', '').replace(',', '').strip()
        return float(price_str) if price_str else float('inf')  # Return infinity if price is empty

    sorted_data = sorted(data, key=lambda x: get_price_value(x))
    if sort_order == 'desc':
        sorted_data.reverse()
    return sorted_data

# Define routes for the bullion finder app
@bullion_finder_app.route('/')
def index():
    return render_template('bullion_finder.html')

@bullion_finder_app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']

    scraper_classes = {
        'jmbullion': JMBullionScraper,
        'apmex': APMEXScraper,
    }

    aggregated_results = []

    for website, scraper_class in scraper_classes.items():
        scraper = scraper_class(search_query)
        results = scraper.scrape()
        if results:
            aggregated_results.extend(results)

    # Filter out items with no prices
    aggregated_results = [item for item in aggregated_results if item.get('price')]

    save_to_json(aggregated_results)
    return redirect(url_for('bullion_finder_app.results', search_query=search_query))

@bullion_finder_app.route('/results')
def results():
    search_query = request.args.get('search_query')
    sort_by = request.args.get('sort_by')

    if search_query:
        scraper_classes = {
            'jmbullion': JMBullionScraper,
            'apmex': APMEXScraper,
        }

        aggregated_results = []

        for website, scraper_class in scraper_classes.items():
            scraper = scraper_class(search_query)
            results = scraper.scrape()
            if results:
                aggregated_results.extend(results)

        # Filter out items with no prices
        aggregated_results = [item for item in aggregated_results if item.get('price')]

        save_to_json(aggregated_results)
    else:
        aggregated_results = load_from_json()

    if sort_by:
        aggregated_results = sort_results(aggregated_results, sort_by)

    return render_template('search_results.html', results=aggregated_results)
