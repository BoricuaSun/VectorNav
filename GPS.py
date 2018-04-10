# This program reads from Vector Nav 300 registers
# In order to run you must download the library from Vector Nav 
# and follow the instructions to install. First make the C library
# later the python library, in order to avoid problems.
# Configure sensor using the website Sensor Explorer program.
# Set up the sensor and when finish righ-click sensor icon, go to
# Commands> Save Settings to Sensor Memory.
# This will store your settings into a Non-Volatile memory in the sensor that
# will be read upon start.

from vnpy import *
import sys
import timeit

	
# This function gets GPS week and time and converts it to UTC format
def Week_Seconds_to_UTC(gpsweek,gpsseconds,leapseconds):
    import datetime, calendar
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
    elapsed = datetime.timedelta(days=(gpsweek*7),seconds=(gpsseconds+leapseconds))
    return datetime.datetime.strftime(epoch + elapsed,datetimeformat)
	
    
s = VnSensor()

## Setup ##

s.connect('/dev/ttyUSB0', 921600)  #connect to specified port and baudrate

#s.write_async_data_output_frequency(100) # Set Frequency to 100 Hz

gpslla = s.read_gps_solution_lla() 														# Reads the GPS Solution - LLA register.
file_name = Week_Seconds_to_UTC(gpslla.week,gpslla.time,0) +".csv" # Format 'YYYY-MM-DD HH:mm:ss'	

file = open(file_name , 'a')
header = "Timestamp,Latitude,Longitude,Altitude,VelocityX (m/s),VelocityY (m/s),VelocityZ (m/s),Yaw,Pitch,Roll,Yaw (rad/sec),Pitch (rad/sec),Roll (rad/sec)"
file.write(header+"\n")
file.close()


while(1):  
		
		start = timeit.default_timer() # gets start time
		
		ypr = s.read_yaw_pitch_roll()							 	# Reads the Yaw Pitch Roll register.
		angular = s.read_angular_rate_measurements()	# Reads the Angular Rate Measurements register.
		gpslla = s.read_gps_solution_lla() 						# Reads the GPS Solution - LLA register.
		gpsecef = s.read_gps_solution_ecef()					# Reads the GPS Solution - ECEF register.
		
		
		# Yaw,Pitch,Roll
		# Yes, the values don't make sense but the reference frame is all wrong
		
		psi= ypr.x 	#Yaw
		theta=ypr.y 	# Pitch
		phi=ypr.z 		# Roll
		
		
		# Angular rates in Yaw, Pitch, Roll
		# These values seem to be right
		
	
		r = angular.z 		# Velocity in Yaw (rad/sec)
		q = angular.y 	# Velocity in Pitch (rad/sec)
		p = angular.x 	# Velocity in Roll (rad/sec)
		
		
		# GPS Time, Position, Velocity
		
		date_time = Week_Seconds_to_UTC(gpslla.week,gpslla.time,16)  # Format 'YYYY-MM-DD HH:mm:ss'	
		latitude = gpslla.lla.x 					# Latitude in degrees.
		longitude = gpslla.lla.y 				# Longitude in degrees.
		altitude = gpslla.lla.z     				# Altitude above ellipsoid. (WGS84) in meters
		velocity_x = gpsecef.velocity.x 	# ECEF X velocity m/s
		velocity_y = gpsecef.velocity.y 	# ECEF Y velocity m/s
		velocity_z = gpsecef.velocity.z 	# ECEF Z velocity m/s
		
		file = open(file_name, 'a')
		result = date_time+ "," + str(latitude) +"," + str(longitude) + "," + str(altitude) + "," + str (velocity_x) +  ","  + str(velocity_y) + "," +str(velocity_z) + "," + str(psi) + "," + str(theta) + "," + str(phi) + "," + str(r) + "," + str(q) + ","+ str(p) 
		file.write( result +"\n")
		file.close() # always close a file when writing to SDcard
		
		stop = timeit.default_timer() # gets stop time
		time =  ' ' + str( stop - start ) + ' sec.' # calculates time elapse in seconds
		print (time)
		
		gps_vel = ' Vel X:' + str (velocity_x) +  ' m/s' +' Vel Y:' + str(velocity_y) + ' m/s' + ' Vel Z:' +str(velocity_z) + ' m/s' 
		print(gps_vel)
		
		gps_pos = ' Latitude:' + str(latitude) +'°'+ 'Longitude :' + str(longitude) + '°' + ' Altitude:' + str(altitude) + 'm'
		print(gps_pos)
			
		angular_rates = ' Yaw (rad/sec):' + str(r) + ' Pitch (rad/sec):' + str(q) + ' Roll (rad/sec):' + str(p) 
		print(angular_rates)
		
		ypr_data = ' Yaw:' + str(psi) + ' Pitch:' + str(theta) + ' Roll:' + str(phi) 
		print(ypr_data)
		
		print()
		
		

		
	
