from flask import Flask, render_template, Response, session, redirect, url_for, escape, request, send_from_directory, jsonify, make_response
from flask_bootstrap import Bootstrap
import json
import zip_code_lookup


app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def upload():
    '''try: 
        zipcode = request.args['zipcode']
    except KeyError:
        zipcode = "No zipcode set"
    try: 
        county_output = request.args['county_output']
    except KeyError:
        county_output = "No zipcode set"
    try: 
        state_output = request.args['state_output']
    except KeyError:
        state_output = "No zipcode set"'''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'zipcode' not in request.form:
            flash('No zipcode requested')
            return redirect(request.url)
        zipcode = request.form['zipcode']
        # if user does not select file, browser also
        # submit an empty part without filename
        if zipcode:
            response=zip_code_lookup.main(zipcode)
            return redirect(url_for('script', zipcode=zipcode))
    else: 
        with open('static/output.json') as f: 
            data = json.load(f)
        zipcode=data[0]['zipcode']
        county_output = data[0]['county_output']
        state_output = data[0]['state_output']
        city_output = data[0]['city_output']
        output = [{'zipcode': 'ENTER ZIPCODE', 'county_output': 'ENTER ZIPCODE', 'state_output': 'ENTER ZIPCODE', 'city_output': 'ENTER ZIPCODE'}]
        with open('static/output.json', 'w') as f:
            json.dump(output, f)
    return render_template('zip_app.html', zipcode=zipcode, county_output=county_output, state_output=state_output, city_output=city_output)

@app.route('/run_script')
def script(): 
    zipcode = request.args['zipcode']
    response=zip_code_lookup.main(zipcode)
    return redirect(url_for('upload'))
