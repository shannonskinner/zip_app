
# coding: utf-8

import pandas as pd
import numpy as np
from urllib.request import Request, urlopen
#from fake_useragent import UserAgent
import urllib.request
import json
import io


def downloadData(): 
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    #ua=UserAgent()
    
    zip_url = 'https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt'  
    zip_req = Request (url=zip_url, headers=header)
    zip_html = urlopen(zip_req).read()
    zips = pd.read_csv(io.StringIO(zip_html.decode('utf-8')),  dtype={'ZCTA5': str, 'STATE': str, 'COUNTY':str, 'GEOID':str}) #read census data for zipcodes & state / county
    
    count_url = 'https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt' 
    count_req = Request(url=count_url, headers=header)
    count_html = urlopen(count_req).read()
    counties = pd.read_csv(io.StringIO(count_html.decode('utf-8')), header=None, names=['STATE','STATEFP', 'COUNTYFP', 'COUNTYNAME', 'CLASSFP'], dtype={'STATEFP': str, 'COUNTYFP':str, 'GEOID':str}) #read list of counties
    counties['GEOID'] = counties.STATEFP.map(str)+counties.COUNTYFP.map(str)
    counties = counties[['STATE', 'GEOID', 'STATEFP', 'COUNTYFP', 'COUNTYNAME', 'CLASSFP']]
    
    place_url = 'https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_place_rel_10.txt'
    place_req = Request(url=place_url, headers=header)
    place_html = urlopen(place_req).read()
    place_zip = pd.read_csv(io.StringIO(place_html.decode('utf-8')), dtype={'ZCTA5': str, 'STATE': str, 'PLACE':str, 'GEOID':str})
    
    places_url = 'https://www2.census.gov/geo/docs/reference/codes/files/national_places.txt'
    places_req = Request(url=places_url, headers=header)
    places_html = urlopen(places_req).read()
    places = pd.read_csv(io.StringIO(places_html.decode('utf-8')),
                     encoding='latin-1', sep='|', 
                     header=0, names=['STATE','STATEFP', 'PLACEFP', 'PLACENAME', 'TYPE', 'FUNCSTAT', 'COUNTY'], 
                     dtype={'STATEFP': str, 'PLACEFP':str})#import places list
    places['PLACE_NAME'] = places['PLACENAME'].str.rsplit(' ', n=1, expand=True)[0]
    places['PLACE_TYPE'] = places['PLACENAME'].str.rsplit(' ', n=1, expand=True)[1]
    zips.to_csv('static/zips.csv', index=False)
    counties.to_csv('static/counties.csv', index=False)
    place_zip.to_csv('static/place_zip.csv', index=False)
    places.to_csv('static/places.csv', index=False)
    

# bring in data from Census sources
def main(zipcode):
    input_zip=zipcode
    
    zips = pd.read_csv('static/zips.csv',  dtype={'ZCTA5': str, 'STATE': str, 'COUNTY':str, 'GEOID':str})
    counties = pd.read_csv('static/counties.csv', dtype={'STATEFP': str, 'COUNTYFP':str, 'GEOID':str})
    place_zip = pd.read_csv('static/place_zip.csv', dtype={'ZCTA5': str, 'STATE': str, 'PLACE':str, 'GEOID':str})
    places = pd.read_csv('static/places.csv', dtype={'STATEFP': str, 'PLACEFP':str})

    input_geoid = str(zips[zips['ZCTA5']==input_zip]['GEOID'].values[0])
    county_output = counties.COUNTYNAME[counties.GEOID==str(zips[zips['ZCTA5']==input_zip]['GEOID'].values[0])].values[0]
    state_output = counties.STATE[counties.GEOID==str(zips[zips['ZCTA5']==input_zip]['GEOID'].values[0])].values[0]
    place_id = place_zip[place_zip['ZCTA5']==zipcode]['PLACE'].values[0]
    city_output = places[(places['PLACEFP']==place_id)& (places['STATE']==state_output)]['PLACE_NAME'].values[0]
    place_type = places[(places['PLACEFP']==place_id) & (places['STATE']==state_output)]['PLACE_TYPE'].values[0]
    
    output = [{'zipcode': zipcode, 'county_output': county_output, 'state_output': state_output, 'city_output': city_output, 'place_type': place_type}]
    with open('static/output.json', 'w') as f:
        json.dump(output, f)
    

    #print('Zip code ',input_zip, ' is in ',county_output,', ',state_output,'. Thank you!')

if __name__=="__main__":
    main()