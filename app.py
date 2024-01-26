from khaoyai import write_block, check_integrity
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Define the path to the 'blockchain' directory
BLOCKCHAIN_DIR = 'blockchain/'

# Ensure the 'blockchain' directory exists
if not os.path.exists(BLOCKCHAIN_DIR):
    os.makedirs(BLOCKCHAIN_DIR)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/khaoyai', methods=['POST','GET'])
def khaoyai():
    if request.method == 'POST':
        booking_name = request.form.get('booking_name')
        participants = request.form.get('participants')
        booking_date = request.form.get('booking_date')

        # Ensure the 'blockchain' directory exists again (in case it was created after the app started)
        if not os.path.exists(BLOCKCHAIN_DIR):
            os.makedirs(BLOCKCHAIN_DIR)

        # Call the write_block function
        write_block(booking_name=booking_name, participants=participants, booking_date=booking_date)

    return render_template("khaoyai.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/check')
def check():
    results = check_integrity()
    return render_template("check.html", check_results=results)

if __name__ == "__main__":
    app.run(debug=True)
