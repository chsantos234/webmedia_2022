from email import header
import json
import requests
import re
import pandas as pd

ANALYSED_YEAR = 2020

# list of available species
species_array = ["O3", "NO2", "PM10", "PM2.5"]
# entrypoint for the API
url_entrypoint = 'http://api.erg.ic.ac.uk/AirQuality'
# gets data from the entire city of london on a single go
london_data_url = url_entrypoint + '/Annual/MonitoringObjective/GroupName=London/Year={year}/Json'
# get all url sites monitoring a certain type of poluent
sites_url = url_entrypoint + '/Annualiser/Sites/year={year}/species={species}/Json'
# get all polution related to a certain site
polution_url = url_entrypoint + '/Annual/MonitoringReport/SiteCode={code}/Year={year}/Json'
# get all current local authorities 
local_authorities_url = url_entrypoint + '/Information/MonitoringLocalAuthority/GroupName=London/Json'
# get data associated with an authority for a given year
local_authority_data_url = url_entrypoint + '/Annual/MonitoringObjective/LocalAuthorityId={id}/Year={year}/Json'
def get_authorities_information(url):
    data_dict = {"@LocalAuthorityCode": [], "@LocalAuthorityName": [], "@LaCentreLatitude": [],
        "@LaCentreLongitude": []}
    local_authorities_response = json.loads(requests.get(url).text)
    authority_data_array = local_authorities_response['LocalAuthorities']['LocalAuthority']
    # iterate over all objects in the array
    for authority_data in authority_data_array:
        # verifies whether the given field is important for the analysis or not
        for key in authority_data.keys():
            # if the key is not needed, then we can skip this iteration in the lasso
            if key not in data_dict.keys():
                continue 
            # else, append the data in the dictionary
            data_dict[key].append(authority_data[key])
    # returns the obtained data
    return data_dict
def get_authority_data(url):
    # specifies useful parameters for our analysis within the request
    data_dict = {"@SiteCode": [], "@Latitude": [], "@Longitude": []}
    # get the data from the specified route
    response = requests.get(url)
    # code the response as UTF-8
    response.encoding = 'utf-8-sig'
    # load the json response on a dictionary for posterior analysis
    local_authority_data_response = json.loads(response.text)
    local_authority_data_array = local_authority_data_response['SiteObjectives']['Site']
    for local_authority_data in local_authority_data_array:
        pass
def get_data_year(url):
    dict_data = {"@SiteCode": [], "@Latitude": [], "@Longitude": [], 
        "@SpeciesCode": [],"@annualMean": []}
    response = requests.get(url)
    response.encoding = "utf-8-sig"
    london_data = json.loads(response.text)
    london_data_array = london_data['SiteObjectives']['Site']
    for data in london_data_array:
        objective_array = data['Objective']
        for objective_item in objective_array:
                annual_mean_text = objective_item['@ObjectiveName']
                search_annual_measurement = re.search('annual', annual_mean_text)
                if search_annual_measurement != None:
                    dict_data['@annualMean'].append(objective_item['@Value'])
                    dict_data['@SpeciesCode'].append(objective_item['@SpeciesCode'])
                    for key in data.keys():
                        if key not in dict_data.keys():
                            continue
                        dict_data[key].append(data[key])
    return dict_data

data = get_data_year(london_data_url.format(year=ANALYSED_YEAR))

df = pd.DataFrame(data)

df.to_csv('datasets/sites_data_new.csv', index=None, header=True,sep=',')