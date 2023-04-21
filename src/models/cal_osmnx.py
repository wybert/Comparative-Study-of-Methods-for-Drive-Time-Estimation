import geopandas as gpd
from tqdm import tqdm
from georouting.routers.osmnx import OSMNXRouter
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)
import datetime
import pandas as pd
import time

us_adm = gpd.read_file("../data/raw/cb_2018_us_state_500k.zip")
# name_1 is state name, name_2 is county name, COUNTRY is USA
us_adm = us_adm.to_crs(crs="EPSG:4326")

# read od pairs
od_pairs = pd.read_parquet("../data/processed/sample_and_results.csv")


# get o and d Geodataframe
o = gpd.GeoDataFrame(od_pairs, geometry=gpd.points_from_xy(od_pairs['AHA_ID_X'], od_pairs['AHA_ID_Y']),crs="EPSG:4326")
d = gpd.GeoDataFrame(od_pairs, geometry=gpd.points_from_xy(od_pairs['ZIP_X'], od_pairs['ZIP_Y']),crs="EPSG:4326")
# sjoin o, d with states
o = gpd.sjoin(o, us_adm, how="left", op='within')
d = gpd.sjoin(d, us_adm, how="left", op='within')
# merge o and d use GIS_ID
od_pairs_ = pd.merge(o,d,on="SAMPLE_ID")


od_pairs_not_in_the_same_state = od_pairs_[od_pairs_["NAME_x"]!=od_pairs_["NAME_y"]]
od_pairs_not_in_the_same_state.rename(columns={"NAME_x":"AHA_STATE","NAME_y":"ZIP_STATE","AHA_ID_X_x":"AHA_ID_lon",
                        "AHA_ID_Y_x":"AHA_ID_lat","ZIP_X_x":"ZIP_lon","ZIP_Y_x":"ZIP_lat"},inplace=True)

od_pairs_not_in_the_same_state.drop(columns=['geometry_x', 'geometry_y'],inplace=True)
# od_pairs_not_in_the_same_state_ = od_pairs_not_in_the_same_state[['AHA_ID_lon', 'AHA_ID_lat', 'ZIP_lon', 'ZIP_lat', 'AHA_STATE', 'ZIP_STATE']]
# visualize the trips not in the same state
od_pairs_not_in_the_same_state_ = od_pairs_not_in_the_same_state[['AHA_ID_lon', 'AHA_ID_lat', 'ZIP_lon', 'ZIP_lat', 'AHA_STATE', 'ZIP_STATE']]
# od_pairs_not_in_the_same_state_.to_csv("/Users/kang/Downloads/od_pairs_not_in_the_same_state.csv",index=False)
od_pairs_not_in_the_same_state_.head()

od_pairs_in_the_same_state = od_pairs_[od_pairs_["NAME_x"]==od_pairs_["NAME_y"]]
od_pairs_in_the_same_state.rename(columns={"NAME_x":"AHA_STATE","NAME_y":"ZIP_STATE","AHA_ID_X_x":"AHA_ID_lon",
                        "AHA_ID_Y_x":"AHA_ID_lat","ZIP_X_x":"ZIP_lon","ZIP_Y_x":"ZIP_lat"},inplace=True)
od_pairs_in_the_same_state = od_pairs_in_the_same_state[['AHA_ID_lon', 'AHA_ID_lat',
 'ZIP_lon', 'ZIP_lat', 'AHA_STATE', 'ZIP_STATE']]
od_pairs_in_the_same_state

us_state_names = od_pairs_in_the_same_state["AHA_STATE"].unique()



def get_drive_time(row,router):
      # (lat,lon)
    origins = (row["ZIP_lat"],row["ZIP_lon"])
    destinations = (row["AHA_ID_lat"],row["AHA_ID_lon"])
    # try 3 times
    try:
        for i in range(3):
            try:
                route = router.get_route(origins, destinations)
                duration = route.get_duration()
                time.sleep(1)
                return duration
            except Exception as e:
                # print(e)
                time.sleep(1)
                continue
    except Exception as e:
        print(e)
        return None
# results = []
already_list = []
import os
os.makedirs("../data/processed_2/",exist_ok=True)
for file_name in os.listdir("../data/processed_2/"):
    if file_name.endswith(".pa"):
        already_list.append(file_name.split(".")[0])
time_stas = []
for state_name in tqdm(us_state_names):
    if state_name in already_list:
        continue
#     if state_name in ["Texas","North Carolina","Florida","Illinois","New Mexico"]:
# #         this one crashed the python kernel 
#         continue
    print(state_name)
    t1 = datetime.datetime.now()
    one_state_pairs = od_pairs_in_the_same_state[od_pairs_in_the_same_state["AHA_STATE"]==state_name]
    print("downloading road network data...")
    router = OSMNXRouter(mode='drive', area = '%s, USA'%state_name)
    t2 = datetime.datetime.now()
    print("download network data done use",t2-t1)
    print("now calculating the drive time distance...")
    one_state_pairs=one_state_pairs[["AHA_ID_lon", "AHA_ID_lat", "ZIP_lon", "ZIP_lat"]]
    one_state_pairs["osmnx_drive_time_in_seconds"] = one_state_pairs.parallel_apply(
        lambda x:get_drive_time(x,router=router),axis=1)
    t3 = datetime.datetime.now()
    print("calculated the drive time distance use ",t3-t2)
    # writing the time consuming  to csv
    time_used = pd.DataFrame({"state":[state_name],"download_network_data_time":[t2-t1],"calculate_drive_time_distance_time":[t3-t2]})
    time_stas.append(time_used)

    # break
    one_state_pairs.to_parquet("data/processed_2/%s.pa"%state_name)
    # results.append(one_state_pairs)
    # pass
time_stas = pd.concat(time_stas)
time_stas.to_csv("../data/interim/time_stas.csv",index=False)