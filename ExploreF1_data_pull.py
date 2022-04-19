import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import fastf1 as ff1
from fastf1 import plotting
from time import sleep

# set cache directory

ff1.Cache.enable_cache('/Users/colinrenville/Documents/Projects/ExploreF1/cache')

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

# test_driver_lookup = get_driver_lookup('2021', 'Abu Dhabi', 'Q')

  

# parameterized function to return telemetry data
# car_data() and pos_data() are the truth, telemetry is imputed
## start with telemetry then correct where needed

def get_driver_data(season, circuit, session, driver, data_type, cached_flag='False'):
  """
  
  """
  
  # season = '2021'
  # # circuit = 'zandvoort'
  # circuit = 'Austrian Grand Prix'
  # session = 'Q'
  # data_type = 'laps'
  
  season = int(season)
  
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
  
  session_laps_car_data_copy['season'] = season
  session_laps_car_data_copy['raceName'] = circuit
  session_laps_car_data_copy['session'] = session
  
  # pause the function after each scrape to not spam
  
  if cached_flag == 'False' :
    
    sleep(7)
    
  return session_laps_car_data_copy

# python script works 

# test_brazil = get_driver_data(season = '2021', circuit = 'interlagos', session = 'Q', driver = 'ALL', data_type='laps')

# test_ndl = get_driver_data(season='2021', circuit='zandvoort', session='Q', driver='ALL', data_type='laps')

# test_ver_laps = get_driver_data(season = '2021',
#                                 circuit = 'Abu Dhabi',
#                                 session = 'Q',
#                                 driver = 'ALL',
#                                 data_type = 'laps')


def get_weekend_gp(season='2021') :
  """
  
  """
  
  list_sessions = []
  
  # defaulting as this for now.. can improve if needed
  
  for i in range(1,23,1):
  
    list_sessions.append(ff1.core.ergast.fetch_weekend(season, i))
    
  circuit_df = pd.DataFrame(list_sessions)
  
  # unlist circuit_df:Circuit and Circuit:Location columns
  
  circuits = pd.DataFrame(circuit_df['Circuit'].tolist())
  locations = pd.DataFrame(circuits['Location'].tolist())
  
  circuit_df = pd.concat([circuit_df, circuits, locations], axis = 1)
  circuit_df = circuit_df.drop(['Circuit', 'Location', 'url'], axis = 1)
  
  return circuit_df

# circuits_2021 = get_weekend_gp()

# test_weekend1 = ff1.core.ergast.fetch_weekend('2021', 3)
# test_weekend2 = ff1.core.ergast.fetch_weekend('2021', 6)
# test_weekend3 = ff1.core.ergast.fetch_weekend('2021', 13)


