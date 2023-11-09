import requests
from datetime import date, timedelta
import pandas as pd

### Deze file zorgt ervoor dat er data uit de API gehaald kan worden van het KNMI.
### Deze file kan lang duren in uitvoering(+/- 2 minuten) omdat die 500.000+ gegevens moet ophalen

locations = ['06260','06240','06225','06209','06257','06248','06249','06258','06267','06235','06242']

token = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjcxZGFmYmI1NGZkYTQ4NjI5ZGU0Mjk5OTM1ZDlmMzdmIiwiaCI6Im11cm11cjEyOCJ9"
headers = {"Authorization": token}

request = requests.get(url='https://api.dataplatform.knmi.nl/edr/collections/observations/instances/unvalidated/locations', headers=headers)
jsonre = request.json()   

df = pd.DataFrame(columns=['Naam', 'id'])
length = len(jsonre['features'])

count = 0 
while count != length:
    df.loc[len(df)] = [jsonre['features'][count]['properties']['name'], jsonre['features'][count]['id']]
    count += 1
    
df['Naam'] = df['Naam'].str.lower()
df

def month(month):
    """
    Een functie die één variabele krijgt namelijk een integer.
    Deze integer staat voor de maand die aangemaakt wordt.
    De functie zet door middel van een API het juiste ID bij het station en voegt
    bij elke rij de eerste dag van de maand toe.
    """
    weerstat = pd.read_csv('weerstations_noordholland.csv', sep=';')
    weerstat['station_id'] = '0'
    weerstat['date'] = date(year=2021, month=month, day=1)
    weerstat['NAME'] = weerstat['NAME'].str.lower()
    for i in weerstat.index:
        for j in df.index:
            if weerstat.loc[i, 'NAME'] in df.loc[j, 'Naam']:
                weerstat.loc[i, 'station_id'] = df.loc[j, 'id']
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

    weerstat = weerstat[weerstat['station_id'].isin(locations)]
    weerstat = weerstat.reset_index(drop=True) 
    return weerstat.copy()

def api_prepper(station_id, start_date, end_date):
    """
    Een simpele functie die de URL klaarmaakt voor de API.
    Neemt het id van het staion, de start_datum en de eind_datum.
    Deze worden daarna in het juiste format gezet voor de API.
    """
    api = 'https://api.dataplatform.knmi.nl/edr/collections/observations/instances/unvalidated/locations/'+station_id+'?datetime='+start_date+'T00%3A00%3A00Z%2F'+end_date+'T00%3A00%3A00Z&parameter-name=ff_10m_10%2Cdd_10%2Cp_nap_msl_10%2Cmor_10%2Cri_pws_10%2Ct_dryb_10%2Cww_cor_10'
    return api

def date_adderv2(df: pd.DataFrame, num_days: int):
    """
    Een functie die een dataframe neemt (gemaakt met month functie) en een aantal dagen.
    De functie kopieert de dataframe(df) num_days aantal keer met iedere keer een dag verder
    en voegt deze telkens samen.
    """
    count = 0
    copy = df.copy()
    while num_days != count:
        copy['date'] = copy['date'] + timedelta(days=1)
        df = pd.concat([df, copy], ignore_index=True)
        count += 1
    return df

def api_frame_maker(weather_stats: pd.DataFrame):
    """
    Een functie die een dataframe neemt als argument.
    Hiervan doet die een API voor het hele jaar voor de eerste
    drie stations. 
    """
    month_var = 1
    count = 0
    end_frame = pd.DataFrame(columns=['datetime','Windsnelheid (km/h)','Windrichting (Graden)', 'Luchtdruk (ps)','Zichtbaarheid (Decimeter ver kunnen kijken)',	'Regenval (mm/h)', 'Temperatuur (C)	Weercode', 'station_id'])
    while count != 11:

        while month_var != 13:
            if month_var == 1 or month_var == 3 or month_var == 5 or month_var == 7 or month_var == 8 or month_var == 10 or month_var == 12:
                weather_stats = month(month_var)
                weather_stats = weather_stats[weather_stats['station_id'].isin(locations)]
                weather_stats = date_adderv2(weather_stats, 30)
                api = api_prepper(weather_stats['station_id'][count], str(weather_stats['date'].min()), str(weather_stats['date'].max()))
                print(api)
                request = requests.get(url=api, headers=headers)
                jsonre = request.json()
                d = {'datetime': jsonre['domain']['axes']['t']['values'], 'Windsnelheid (km/h)': jsonre['ranges']['ff_10m_10']['values'],
                    'Windrichting (Graden)': jsonre['ranges']['dd_10']['values'], 'Luchtdruk (ps)': jsonre['ranges']['p_nap_msl_10']['values'],
                    'Zichtbaarheid (Decimeter ver kunnen kijken)': jsonre['ranges']['mor_10']['values'], 'Regenval (mm/h)': jsonre['ranges']['ri_pws_10']['values'],
                    'Temperatuur (C)': jsonre['ranges']['t_dryb_10']['values'], 'Weercode': jsonre['ranges']['ww_cor_10']['values']}

                api_data = pd.DataFrame(data=d)
                api_data['station_id'] = weather_stats['station_id'][count]
                end_frame = pd.concat([end_frame, api_data])
                month_var += 1

            elif month_var == 4 or month_var == 6 or month_var == 9 or month_var == 11:
                weather_stats = month(month_var)
                weather_stats = weather_stats[weather_stats['station_id'].isin(locations)]
                weather_stats = date_adderv2(weather_stats, 29)
                api = api_prepper(weather_stats['station_id'][count], str(weather_stats['date'].min()), str(weather_stats['date'].max()))
                print(api)
                request = requests.get(url=api, headers=headers)
                jsonre = request.json()
                d = {'datetime': jsonre['domain']['axes']['t']['values'], 'Windsnelheid (km/h)': jsonre['ranges']['ff_10m_10']['values'],
                    'Windrichting (Graden)': jsonre['ranges']['dd_10']['values'], 'Luchtdruk (ps)': jsonre['ranges']['p_nap_msl_10']['values'],
                    'Zichtbaarheid (Decimeter ver kunnen kijken)': jsonre['ranges']['mor_10']['values'], 'Regenval (mm/h)': jsonre['ranges']['ri_pws_10']['values'],
                    'Temperatuur (C)': jsonre['ranges']['t_dryb_10']['values'], 'Weercode': jsonre['ranges']['ww_cor_10']['values']}

                api_data = pd.DataFrame(data=d)
                api_data['station_id'] = weather_stats['station_id'][count]
                end_frame = pd.concat([end_frame, api_data])
                month_var += 1

            elif month_var == 2:
                weather_stats = month(month_var)
                weather_stats = weather_stats[weather_stats['station_id'].isin(locations)]
                weather_stats = date_adderv2(weather_stats, 27)
                api = api_prepper(weather_stats['station_id'][count], str(weather_stats['date'].min()), str(weather_stats['date'].max()))
                print(api)
                request = requests.get(url=api, headers=headers)
                jsonre = request.json()
                d = {'datetime': jsonre['domain']['axes']['t']['values'], 'Windsnelheid (km/h)': jsonre['ranges']['ff_10m_10']['values'],
                    'Windrichting (Graden)': jsonre['ranges']['dd_10']['values'], 'Luchtdruk (ps)': jsonre['ranges']['p_nap_msl_10']['values'],
                    'Zichtbaarheid (Decimeter ver kunnen kijken)': jsonre['ranges']['mor_10']['values'], 'Regenval (mm/h)': jsonre['ranges']['ri_pws_10']['values'],
                    'Temperatuur (C)': jsonre['ranges']['t_dryb_10']['values'], 'Weercode': jsonre['ranges']['ww_cor_10']['values']}

                api_data = pd.DataFrame(data=d)
                api_data['station_id'] = weather_stats['station_id'][count]
                end_frame = pd.concat([end_frame, api_data])
                month_var += 1
        count += 1
        month_var = 1

    end_frame['datetime'] = pd.to_datetime(end_frame['datetime'])
    end = end_frame.drop(columns=['Temperatuur (C)\tWeercode'])
    end = end.fillna(0)
    # return end.groupby([end['datetime'].dt.date,'station_id'])[['Windsnelheid (km/h)', 'Windrichting (Graden)', 'Luchtdruk (ps)', 'Zichtbaarheid (Decimeter ver kunnen kijken)','Regenval (mm/h)', 'station_id', 'Temperatuur (C)', 'Weercode']].mean()
    return end.reset_index(drop=True)

weather_stats = month(1)
end_frame = api_frame_maker(weather_stats)
end_frame.to_csv('apidata_2021.csv')



