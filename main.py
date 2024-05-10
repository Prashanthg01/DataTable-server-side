from flask import Flask
import pandas as pd
from flask_cors import CORS
import numpy as np
from flask import render_template
from functions.tables import customize_view, ViewDataHelper

app = Flask(__name__)
CORS(app)


# Define a route to serve the data
@app.route('/index')
def get_pincode_data():
    view_name = "realtime_pincode"
    options_list = customize_view.get(
            "Orient2", [])[view_name]
    return render_template('index.html', view_name='realtime_pincode', heading="Realtime Pincode", options_list=options_list)

@app.route('/json_data/<string:view_name>', methods=['POST', 'GET'])
def json_data(view_name):
    main_data = ViewDataHelper(
        view_name)
    try:
        row_data = main_data.get_data()
    except Exception as e:
        app.logger.error("An exception occurred", exc_info=True)

    row_data = row_data[row_data[row_data.columns[-1]] ==
                        "Currently Unavailable"] if view_name == 'pincode_stock_availability' else row_data
    row_data.replace({np.nan: None}, inplace=True)
    data_dict = row_data.to_dict(orient='records')
    response = {'data': data_dict}
    return response


if __name__ == '__main__':
    app.run(debug=True)
