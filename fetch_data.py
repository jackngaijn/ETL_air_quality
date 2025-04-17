import requests 
import pandas as pd 
import re 

def requests_url(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'
    data = response.text
    return data

def transform_data(data):
    # Extract the data from the XML response by PollutantConcentration
    pattern = r'<PollutantConcentration>(.*?)</PollutantConcentration>'
    pollutant_data = re.findall(pattern, data, re.DOTALL)

    # Extract the element from PollutantConcentration
    station_pattern = r'<StationName>(.*?)</StationName>'
    datetime_pattern = r'<DateTime>(.*?)</DateTime>'
    no2_pattern = r'<NO2>(.*?)</NO2>'
    o3_pattern = r'<O3>(.*?)</O3>'
    so2_pattern = r'<SO2>(.*?)</SO2>'
    co_pattern = r'<CO>(.*?)</CO>'
    pm10_pattern = r'<PM10>(.*?)</PM10>'
    pm25_pattern = r'<PM2.5>(.*?)</PM2.5>'

    data_dict = {
        'Station': [],
        'DateTime': [],
        'NO2': [],
        'O3': [],
        'SO2': [],
        'CO': [],
        'PM10': [],
        'PM2.5': []
    }
    for measurement in pollutant_data:
        data_dict['Station'].append(re.findall(station_pattern, measurement)[0])
        data_dict['DateTime'].append(re.findall(datetime_pattern, measurement)[0])
        data_dict['NO2'].append(re.findall(no2_pattern, measurement)[0])
        data_dict['O3'].append(re.findall(o3_pattern, measurement)[0])
        data_dict['SO2'].append(re.findall(so2_pattern, measurement)[0])
        data_dict['CO'].append(re.findall(co_pattern, measurement)[0])
        data_dict['PM10'].append(re.findall(pm10_pattern, measurement)[0])
        data_dict['PM2.5'].append(re.findall(pm25_pattern, measurement)[0])

    # Create DataFrame
    df = pd.DataFrame(data_dict)

    # Convert DateTime to datetime type
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Convert numeric columns to float, replacing '-' with NaN
    numeric_columns = ['NO2', 'O3', 'SO2', 'CO', 'PM10', 'PM2.5']
    for col in numeric_columns:
        df[col] = df[col].replace('-', pd.NA)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df.groupby('Station')[col].fillna(method='ffill')
    
    df.to_csv('cleaned_data.csv', index=False)
    return df


