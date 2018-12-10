
# coding: utf-8

import pandas as pd
import numpy as np
import json


# bring in data from Census sources
def main(zipcode):
    input_zip=zipcode
    zips = pd.read_csv('https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt', dtype={'ZCTA5': str, 'STATE': str, 'COUNTY':str, 'GEOID':str}) #read census data for zipcodes & state / county
    
    counties = pd.read_csv('https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt', header=None, names=['STATE','STATEFP', 'COUNTYFP', 'COUNTYNAME', 'CLASSFP'], dtype={'STATEFP': str, 'COUNTYFP':str, 'GEOID':str}) #read list of counties
    
    place_zip = pd.read_csv('https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_place_rel_10.txt', dtype={'ZCTA5': str, 'STATE': str, 'PLACE':str, 'GEOID':str})
    places = pd.read_csv('https://www2.census.gov/geo/docs/reference/codes/files/national_places.txt', 
                     encoding='latin-1', sep='|', 
                     header=0, names=['STATE','STATEFP', 'PLACEFP', 'PLACENAME', 'TYPE', 'FUNCSTAT', 'COUNTY'], 
                     dtype={'STATEFP': str, 'PLACEFP':str})#import places list
    
    
    counties['GEOID'] = counties.STATEFP.map(str)+counties.COUNTYFP.map(str)
    counties = counties[['STATE', 'GEOID', 'STATEFP', 'COUNTYFP', 'COUNTYNAME', 'CLASSFP']]
    
    input_geoid = str(zips[zips['ZCTA5']==input_zip]['GEOID'].values[0])
    county_output = counties.COUNTYNAME[counties.GEOID==str(zips[zips['ZCTA5']==input_zip]['GEOID'].values[0])].values[0]
    state_output = counties.STATE[counties.GEOID==str(zips[zips['ZCTA5']==input_zip]['GEOID'].values[0])].values[0]
    place_id = place_zip[place_zip['ZCTA5']==zipcode]['PLACE'].values[0]
    city_output = places[(places['PLACEFP']==place_id)& (places['STATE']==state_output)]['PLACENAME'].values[0]
    
    output = [{'zipcode': zipcode, 'county_output': county_output, 'state_output': state_output, 'city_output': city_output}]
    with open('static/output.json', 'w') as f:
        json.dump(output, f)
    

    #print('Zip code ',input_zip, ' is in ',county_output,', ',state_output,'. Thank you!')

if __name__=="__main__":
    main()