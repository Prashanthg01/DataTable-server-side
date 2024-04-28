from flask import Flask
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Read the CSV file
csv_file_path = r'E:\Projects\Python_Projects\API_filter_with_Datatable\Realtime_pincode.csv'
data = pd.read_csv(csv_file_path)

# Define a route to serve the data
@app.route('/api/pincode')
def get_pincode_data():
    # Convert the DataFrame to a list of dictionaries
    data_dict = data.to_dict(orient='records')
    # Wrap the data within a dictionary with the key 'data'
    response = {'data': data_dict}
    return response

if __name__ == '__main__':
    app.run(debug=True)
