"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
import math


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.

# create dictionarys for the specified time and location values

# controls between 0-200 km
control_0_2 = {'start_dist': 0, 'end_dist': 200, 'min_speed': 15, 'max_speed': 34}

# controls between 200-400 km
control_2_4 = {'start_dist': 200, 'end_dist': 400, 'min_speed': 15, 'max_speed': 32}

# controls between 400-600 km
control_4_6 = {'start_dist': 400, 'end_dist': 600, 'min_speed': 15, 'max_speed': 30}

# controls between 600-1000 km
control_6_10 = {'start_dist': 600, 'end_dist': 1000, 'min_speed': 11.428, 'max_speed': 28}


def control_st_calc(control, brevet_start_time, max_speed):
   raw_time = control / max_speed
   hour = math.floor(raw_time)
   frac_minutes = raw_time - hour
   minute = round(frac_minutes * 60)
   return brevet_start_time.shift(hours=hour, minutes=minute)

def control_cl_calc(control, brevet_start_time, min_speed):
   raw_time = control / min_speed
   hour = math.floor(raw_time)
   frac_minutes = raw_time - hour
   minute = round(frac_minutes * 60)
   return brevet_start_time.shift(hours=hour, minutes=minute)

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    start_time = brevet_start_time

   #if the control is longer than the brevet the calulation should be with brevet instead
    if control_dist_km > brevet_dist_km:
       control = brevet_dist_km
    else:
       control = control_dist_km
        
    if control <= 200:
       start_time = control_st_calc(control, brevet_start_time, control_0_2['max_speed'])
    elif control <= 400:
       #calcalute when distance is <=200
       new_start_time = control_st_calc(200, brevet_start_time, control_0_2['max_speed'])

       #calculate when distance is >200 with new start time
       remain_control_dist = control - 200
       start_time = control_st_calc(remain_control_dist, new_start_time, control_2_4['max_speed'])
    elif control <= 600:
       #calcalute when distance is <=200
       new_start_time = control_st_calc(200, brevet_start_time, control_0_2['max_speed'])

       #calculate when distance is <=400 with new start time
       new_start_time = control_st_calc(200, new_start_time, control_2_4['max_speed'])

       #calulate remaining distance with new start time
       remain_control_dist = control - 400
       start_time = control_st_calc(remain_control_dist, new_start_time, control_4_6['max_speed'])
    elif control <= 1000:
       #calcalute when distance is <=200
       new_start_time = control_st_calc(200, brevet_start_time, control_0_2['max_speed'])

       #calculate when distance is <=400
       new_start_time = control_st_calc(200, new_start_time, control_2_4['max_speed'])

       #calulate when distance is <=600
       new_start_time = control_st_calc(200, new_start_time, control_4_6['max_speed'])
       
       #calulate remaing distance
       remain_control_dist = control - 600
       start_time = control_st_calc(remain_control_dist, new_start_time, control_6_10['max_speed'])

    return start_time


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    close_time = brevet_start_time
     #if the control is longer than the brevet the calulation should be with brevet instead
    if control_dist_km > brevet_dist_km:
       control = brevet_dist_km
    else:
       control = control_dist_km

    #if the control is 0 close time should be 1hr
    if control == 0:
       close_time = brevet_start_time.shift(hours=1)
    elif control <= 60:
       close_time = control_st_calc(control, brevet_start_time, 20)
       close_time = close_time.shift(hours=1)
    elif control == 200:
       close_time = brevet_start_time.shift(hours=13, minutes=30)
    elif control <= 600:
       close_time = control_st_calc(control, brevet_start_time, control_0_2['min_speed'])
    elif control <= 1000:
       #calcalute when distance is <=600
       new_start_time = control_st_calc(600, brevet_start_time, control_4_6['min_speed'])
       #calulate remaining distance with new start time
       remain_control_dist = control - 600
       close_time = control_st_calc(remain_control_dist, new_start_time, control_6_10['min_speed'])

    return close_time
