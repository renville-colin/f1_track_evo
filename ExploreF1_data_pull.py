import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import fastf1 as ff1
from fastf1 import plotting

# set cache directory

ff1.Cache.enable_cache('/Users/colinrenville/Documents/Projects/ExploreF1/cache')


# will need function to convert all timedelta datatypes to seconds

def tdelt_to_sec(df):
  
  for col in df.columns[df.dtypes == 'timedelta64[ns]']:
    df[col].dt.total_seconds()

  return df

def tdelt_to_sec2(x):
  
  x = x.dt.total_seconds()
      
  return x


# test scrape

def get_lec_data():
  
  monza_quali = ff1.get_session(2019, 'Monza', 'Q')
  
  laps = monza_quali.load_laps(with_telemetry=True)
  fast_leclerc = laps.pick_driver('LEC').pick_fastest()
  lec_car_data = fast_leclerc.get_car_data()
  
  # convert timedeltas to seconds
  
  for col in lec_car_data.columns[lec_car_data.dtypes == 'timedelta64[ns]']:
    
    lec_car_data[col] = tdelt_to_sec2(lec_car_data[col])
  
  return lec_car_data

# lec_car_data = get_lec_data()
# lec_car_data['Time'] = tdelt_to_sec2(lec_car_data['Time'])

# test ad hoc pull: Did Checo's tow make a difference?

def get_max_ad_quali_2021():

  ad_quali_2021 = ff1.get_session(2021, 'Abu Dhabi', 'Q')
  ad_quali_2021_laps = ad_quali_2021.load_laps(with_telemetry=True)
  
  ad_quali_2021_laps_car33 = ad_quali_2021_laps.pick_driver('VER').get_telemetry()
  
  for col in ad_quali_2021_laps_car33.columns[ad_quali_2021_laps_car33.dtypes == 'timedelta64[ns]']:
    
    ad_quali_2021_laps_car33[col] = tdelt_to_sec2(ad_quali_2021_laps_car33[col])
  
  return ad_quali_2021_laps_car33


# function that loads driver lookup
# this will be needed for telemetry data

def get_driver_lookup(season, circuit, session):
  """
  
  """

  session_data = ff1.get_session(season, circuit, session)
  session_laps_data = session_data.load_laps(with_telemetry=True)
  
  session_laps_car_data = session_laps_data
  
  # cant figure out any other way to remedy slice warning
  session_laps_car_data_copy = session_laps_car_data.copy()
  col_delta_time = list(session_laps_car_data_copy.loc[:,session_laps_car_data_copy.dtypes == 'timedelta64[ns]'])  
    
  # clean this up
    
  for col in col_delta_time:
    
    session_laps_car_data_copy.loc[:,col] = session_laps_car_data_copy.loc[:,col].dt.total_seconds()
    
  session_laps_driver_list = pd.unique(session_laps_car_data_copy['Driver'])
  
  return session_laps_driver_list

test_driver_lookup = get_driver_lookup('2021', 'Abu Dhabi', 'Q')

  

# parameterized function to return telemetry data
# car_data() and pos_data() are the truth, telemetry is imputed
## start with telemetry then correct where needed

def get_driver_data(season, circuit, session, driver, data_type):
  """
  
  """
  
  # season = 2021
  # circuit = 'Abu Dhabi'
  # session = 'Q'
  
  session_data = ff1.get_session(season, circuit, session)
  session_laps_data = session_data.load_laps(with_telemetry=True)
  
  if data_type.lower() == 'telemetry':
    
    session_laps_car_data = session_laps_data.pick_driver(driver).get_telemetry()
    
  elif data_type.lower() == 'laps':
    
    if driver.upper() != 'ALL':
    
      session_laps_car_data = session_laps_data.pick_driver(driver)
      
    else:
      
      session_laps_car_data = session_laps_data
    
  # cant figure out any other way to remedy slice warning
  session_laps_car_data_copy = session_laps_car_data.copy()
  col_delta_time = list(session_laps_car_data_copy.loc[:,session_laps_car_data_copy.dtypes == 'timedelta64[ns]'])
  
  # clean this up / consolidate code from other functions
    
  for col in col_delta_time:
    
    session_laps_car_data_copy.loc[:,col] = session_laps_car_data_copy.loc[:,col].dt.total_seconds()
    
  # source this script then test this line
  
  # session_laps_car_data_copy = session_laps_car_data_copy.reset_index()
    
  return session_laps_car_data_copy


# test_ver_laps = get_driver_data(season = '2021',
#                                 circuit = 'Abu Dhabi',
#                                 session = 'Q',
#                                 driver = 'ALL',
#                                 data_type = 'laps')


def make_path(wname, wdate, sname, sdate):
  """Create the api path base string to append on livetiming.formula1.com for api
    requests.
    The api path base string changes for every session only.
    Args:
        wname: Weekend name (e.g. 'Italian Grand Prix')
        wdate: Weekend date (e.g. '2019-09-08')
        sname: Session name 'Qualifying' or 'Race'
        sdate: Session date (formatted as wdate)
    Returns:
        relative url path
    """

  smooth_operator = f'{wdate[:4]}/{wdate} {wname}/{sdate} {sname}/'
  return '/static/' + smooth_operator.replace(' ', '_')

make_path(wname='Italian Grand Prix', wdate='2019-09-08', sname='Qualifying',sdate='2019-09-08')

