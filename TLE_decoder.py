#! python3

import re
import pyperclip
import math
from datetime import datetime

# Create regex for TLE
TLE = re.compile(r'[-]?\d*[.]?\d*[+]?[-]?\w*')

# Get the text off the clipboard
text = pyperclip.paste()

# Extract the groups from the text
extractedvalues = TLE.findall(text)
print('Extracted from clipboard:\n' + str(extractedvalues))

# Remove blank spaces from list
while('' in extractedvalues):
    extractedvalues.remove('')

print('\nCleaned up:\n' + str(extractedvalues) + '\n')

# Extract each orbital parameter from the TLE
sat_num = extractedvalues[1]
int_des = extractedvalues[2]
epoch = extractedvalues[3]
inclin_deg = extractedvalues[11]
right_asc_deg = extractedvalues[12]
eccent = '0.' + str(extractedvalues[13])
arg_of_perig_deg = extractedvalues[14]
mean_anom_deg = extractedvalues[15]
mean_mot_w_extra = extractedvalues[16]
mean_mot_rpd = mean_mot_w_extra[0:11]

# Determine time observation was taken
year_partial = int(epoch[0:2])
if year_partial < 57:
    year = 2000 + year_partial
else:
    year = 1900 + year_partial

DOY = int(epoch[2:5])
frac_time = float(epoch[5:14])
hour = math.floor((frac_time * 24))
minute = math.floor(((frac_time * 24) - hour) * 60)
seconds = math.floor(((((frac_time * 24) - hour) * 60) - minute) * 60)
u_seconds = (((((frac_time * 24) - hour) * 60) - minute) * 60) - seconds
u_seconds = int(round(u_seconds * 100000,0))

date_string = str(year) + ' ' + str(DOY).zfill(3) + ' ' + str(hour).zfill(2) + ':' + \
              str(minute).zfill(2) + ':' + str(seconds).zfill(2) + str(u_seconds).zfill(6)

formatted_date = datetime.strptime(date_string, "%Y %j %H:%M:%S%f")

# Convert mean motion into orbital period
# 1 day = 24hrs
# 1 period = 360 deg = 1 revolution
mean_mot_rpd_flt = float(mean_mot_rpd) # TLE is in revolutions per day
mean_mot_rad_sec = mean_mot_rpd_flt * 2 * math.pi / 24 / 3600 # converts to rad/sec
orb_period_sec = round(2 * math.pi / mean_mot_rad_sec,6)
orb_period_min = round(orb_period_sec / 60,6)   # 60 sec per min
orb_period_hrs = round(orb_period_sec / 3600,6) # 3600 sec per hr

# Convert orbital period into semimajor axis
mu_earth_km = 398600 # km^3/sec^2
rad_earth = 6378.14 # km, equatorial radius of earth
semi_maj_a = round((mu_earth_km / (mean_mot_rad_sec**2))**(1/3),3)
semi_min_b = round(semi_maj_a * math.sqrt(1 - float(eccent)**2),3)

# Radius of Perigee & Apogee
rad_perigee = round(semi_maj_a*(1-float(eccent)),3)
rad_apogee = round(semi_maj_a*(1+float(eccent)),3)

# Altitude of Perigee & Apogee
h_perigee = round(rad_perigee - rad_earth,3)
h_apogee = round(rad_apogee - rad_earth,3)

# Velocity @ Perigee & Apogee
vel_perigee = round(((2*mu_earth_km/rad_perigee)-(mu_earth_km/semi_maj_a))**(1/2),3)
vel_apogee = round(vel_perigee*rad_perigee/rad_apogee,3)

# Print results to terminal
print('Satellite Number: ' + sat_num)
print('International Designator: ' + int_des)
print('TLE Observation Year & DOY: ' + str(year) + ' DOY ' + str(DOY).zfill(3))
print('TLE Observation Date & Time: ' + str(formatted_date) + ' UTC')

print('\nSemimajor Axis a : ' + str(semi_maj_a) + ' km')
print('Semiminor Axis b : ' + str(semi_min_b) + ' km')
print('Eccentricity: ' + eccent)
print('Inclination: ' + inclin_deg + ' deg')
print('Right Ascension: ' + right_asc_deg + ' deg')
print('Argument of Perigee: ' + arg_of_perig_deg + ' deg')
print('Mean Anomaly: ' + mean_anom_deg + ' deg')
print('Mean Motion: '+ mean_mot_rpd + ' revolutions per day')
print('Orbital Period: ' + str(orb_period_hrs) + ' hrs')
print('Orbital Period: ' + str(orb_period_min) + ' min')
print('Orbital Period: ' + str(orb_period_sec) + ' sec')
print('\nRadius of Perigee: ' + str(rad_perigee) + ' km')
print('Altitude of Perigee: ' + str(h_perigee) + ' km')
print('Velocity at Perigee: ' + str(vel_perigee) + ' km/s')

print('\nRadius of Apogee: ' + str(rad_apogee) + ' km')
print('Altitude of Apogee: ' + str(h_apogee) + ' km')
print('Velocity at Apogee: ' + str(vel_apogee) + ' km/s')










