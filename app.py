from flask import Flask, render_template, redirect, url_for
from bullion_finder.bullion_finder_app import bullion_finder_app  # Import the blueprint object from bullion_finder

app = Flask(__name__)

# Register the blueprint with the app
app.register_blueprint(bullion_finder_app, url_prefix='/app')

# Define your other routes
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for /app, which will redirect to the bullion finder blueprint
@app.route('/app')
def bullion_finder():
    return redirect(url_for('bullion_finder_app.index'))

# Ensure to run the app if executed directly
if __name__ == '__main__':
    app.run(debug=True)