#Some important Notes at the beginning of the code:
#To #constants, there is a program with opening the files. In path_2d and path_3d give a path to your files with r in the beginning. Just do not delete this r!
#At constants there are some constants that we will use (like R of the air)
#At calculated constants there are constants from our files (like Mach number etc.)

import pandas as pd
import numpy as np
import scipy as sp

path_2d = r"C:\Users\Jango\Desktop\DELFT\Y2 bachelor\S1\wind tunnel\uno\windtunnel-group11-2025-main\raw_Group11_2D.txt"
path_3d = r"C:\Users\Jango\Desktop\DELFT\Y2 bachelor\S1\wind tunnel\uno\windtunnel-group11-2025-main\raw_Group11_3D.txt"

df_2d = pd.read_csv(path_2d, sep=r"\s+", engine="python", skiprows=1)
df_no_time_2d = df_2d.drop(df_2d.columns[1], axis=1)
data_2d = df_no_time_2d.to_numpy(dtype=float)
number_of_columns_2d = sum(1 for _ in open(path_2d)) - 3

df_3d = pd.read_csv(path_3d, sep=r"\s+", engine="python", skiprows=1)
df_no_time_3d = df_3d.drop(df_3d.columns[1], axis=1)
data_3d = df_no_time_3d.to_numpy(dtype=float)
number_of_columns_3d = sum(1 for _ in open(path_3d)) - 3

#data_2d and data_3d are formatted in the same way, which is:
#they are arrays in numpy. First position (data_2d[0][0]) is a run number, the next one (data_2d[0][1]) is an angle of attack. The time is not included, because it gave me errors
#To get some number, take data_2d[number_of_row][number_of_column]
#If you want to use the enite row, take just data_2d[number_of_row]
#Use those prints, if you are uncertain:

#print(data_2d[0][0])
#print(data_3d[0][0])

#Constants
gas_constant = 8.31446 #R [J/(kg*K)
velocity = 25 #m/s
adiabatic_constant = 1.4 #gamma
molecular_weight = 0.02896 #kg/mol

#Constants - Sutherland's Law
viscosity_0 = 1.716 * 10**(-5)
temperature_0 = 273.15
sutherlands_temp = 110.4

#functions definitions

def atmospheric_conditions(nb,file,k):
    sum_pressure = 0
    sum_temperature = 0
    sum_density = 0
    sum_delta_pressure = 0
    for i in range(nb):
        sum_pressure += file[i][3] * 100
        sum_temperature += file[i][4] + 273.15
        sum_density += file[i][k]
        sum_delta_pressure += file[i][2]
    atmospheric_pressure = sum_pressure / nb
    atmospheric_temperature = sum_temperature / nb
    atmospheric_density = sum_density / nb
    atmospheric_delta_pb = sum_delta_pressure / nb
    return atmospheric_pressure, atmospheric_temperature, atmospheric_density, atmospheric_delta_pb

def ambient_cond_and_ref_speed(mw, pres, temp, dp):
    dens = ((mw * pres) / (gas_constant * temp))

    dyn_visc = viscosity_0*(temp/temperature_0)**1.5*((temperature_0+sutherlands_temp)/(temp+sutherlands_temp))

    dyn_pres = 0.211804+1.928442*dp+0.0001879374*dp**2

    static_pres = pres - dyn_pres

    free_stream_vel = np.sqrt((2*(pres - static_pres)/dens))
    return dens, dyn_visc, dyn_pres,static_pres, free_stream_vel

#Calculated constants
atmospheric_pressure_2d, atmospheric_temperature_2d, atmospheric_density_2d, atmospheric_delta_pressure_2d = atmospheric_conditions(number_of_columns_2d,data_2d,6)
atmospheric_pressure_3d, atmospheric_temperature_3d, atmospheric_density_3d, atmospheric_delta_pressure_3d = atmospheric_conditions(number_of_columns_3d,data_3d,9)

pressure = (number_of_columns_2d*atmospheric_pressure_2d+number_of_columns_3d*atmospheric_pressure_3d)/(number_of_columns_3d+number_of_columns_2d)
temperature = (number_of_columns_2d * atmospheric_temperature_2d + number_of_columns_3d * atmospheric_temperature_3d) / (number_of_columns_3d + number_of_columns_2d)
#density_from_data = (number_of_columns_2d * atmospheric_density_2d + number_of_columns_3d * atmospheric_density_3d) / (number_of_columns_3d + number_of_columns_2d)
delta_pressure = (number_of_columns_2d * atmospheric_delta_pressure_2d + number_of_columns_3d * atmospheric_delta_pressure_3d) / (number_of_columns_3d + number_of_columns_2d)

velocity_of_sound = np.sqrt(adiabatic_constant * gas_constant * temperature)
mach_number = velocity / velocity_of_sound

#END OF CONSTANTS
#Section 3.1 - Conditions and reference speeds
denisty, dynamic_viscosity, dynamic_pressure, static_pressure, free_stream_velocity = ambient_cond_and_ref_speed(molecular_weight, pressure, temperature, delta_pressure)
#print(molecular_weight, pressure, temperature, delta_pressure)
#print(denisty, dynamic_viscosity, dynamic_pressure, static_pressure, free_stream_velocity)



print('chuj')
