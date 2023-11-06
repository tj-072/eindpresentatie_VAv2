from datetime import date, timedelta
import pandas as pd
import requests

def api_prepper(station_id, start_date, end_date):
    api = f'https://api.dataplatform.knmi.nl/edr/collections/observations/instances/unvalidated/locations/{station_id}?datetime={start_date}T04%3A10%3A00Z%2F{end_date}T04%3A10%3A00Z&parameter-name=t_dryb_10'
    return api

def date_adderv2(df, num_days):
    count = 0
    copy = df.copy()
    while num_days != count:
        copy['date'] = copy['date'] + timedelta(days=1)
        df = pd.concat([df, copy], ignore_index=True)
        count += 1
    return df

token = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjcxZGFmYmI1NGZkYTQ4NjI5ZGU0Mjk5OTM1ZDlmMzdmIiwiaCI6Im11cm11cjEyOCJ9"
headers = {"Authorization": token}

request = requests.get(url='https://api.dataplatform.knmi.nl/edr/collections/observations/instances/unvalidated/locations', headers=headers)
jsonre = request.json() 

api_locations = pd.DataFrame(columns=['Naam', 'id'])
length = len(jsonre['features'])

# Request om alle mogelijk data uit de api te halen.
# r = requests.get(f"https://api.dataplatform.knmi.nl/edr/collections/observations", headers=headers)
# r.raise_for_status()
# r.json()

count = 0 
while count != length - 1:
    api_locations.loc[len(api_locations)] = [jsonre['features'][count]['properties']['name'], jsonre['features'][count]['id']]
    count += 1

api_locations['Naam'] = api_locations['Naam'].str.lower()

weerstat = pd.read_csv('weerstations6.csv',sep=',')
weerstat['station_id'] = '0'
weerstat['date'] = date(year=2023, month=10, day=1)
weerstat['NAME'] = weerstat['NAME'].str.lower()

for i in weerstat.index:
    for j in api_locations.index:
        if weerstat.loc[i, 'NAME'] in api_locations.loc[j, 'Naam']:
            weerstat.loc[i, 'station_id'] = api_locations.loc[j, 'id']
        if weerstat['NAME'][i] == 'gilze-rijen':
            weerstat.loc[i, 'station_id'] = '06350'
        if weerstat['NAME'][i] == 'cabauw mast':
            weerstat.loc[i, 'station_id'] = '06348'
        if weerstat['NAME'][i] == 'valkenburg zh':
            weerstat.loc[i, 'station_id'] = '06210'
        if weerstat['NAME'][i] == 'hoorn terschelling':
            weerstat.loc[i, 'station_id'] = '06251'
        if weerstat['NAME'][i] == 'tholen':
            weerstat.loc[i, 'station_id'] = '06310'
        if weerstat['NAME'][i] == 'hoofdplaat':
            weerstat.loc[i, 'station_id'] = '06310'
        if weerstat['NAME'][i] == 'schaar':
            weerstat.loc[i, 'station_id'] = '06310'  





