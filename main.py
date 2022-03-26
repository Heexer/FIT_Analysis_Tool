import fitparse
from tkinter import *
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import scipy.stats as stats
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import folium
import webbrowser
from IPython.display import display

# from decimal import Decimal

file_write = True
gps = False
show_map = True

# GUI - window init
root = Tk()
root.geometry('1200x720')
root.title('Fit app')

icon = PhotoImage(file='favicon.png')
root.iconphoto(True, icon)

# Scrollbar
scroll = Scrollbar(root)

# Load the FIT file
# fitFile = fitparse.FitFile(askopenfilename())
fitFile = fitparse.FitFile("run.fit")




# record, device_info, file_creator, event

for record in fitFile.get_messages():
    for message in record:
        tmp = str(message)
        if tmp[0:7] != 'unknown' and message.value is not None:
            # if type(message.value) == int or type(message.value) == float:
            #     print(message)

            # if message.units:
            #     print(message)

            # name: value, units
            # print(message.value)

            print(message)


# PRODUCT
# garmin_product, manufacturer, serial_number, time_created, software_version, mounting_side, dist_setting, elev_setting,
#
# LOCATION
# date_mode, time_mode, time_offset, time_zone_offset, utc_offset,
# USER
# activity_class, gender, height, weight, language, hr_setting, resting_heart_rate, sleep_time, wake_time, user_running_step_length,
#  user_walking_step_length
# ACTIVITY
# name, sport, sub_sport, max_heart_rate, duration, set_type, avg_cadence_position, avg_heart_rate, max_heart_rate, event, num_laps,
#  total_anaerobic_training_effect, total_calories, total_elapsed_time, total_timer_time, total_training_effect, num_sessions,
#  total_timer_time

# mes = list(fitFile.get_messages())
#
# print(mes[0].fields)
# print(mes[0].get_values())
# print(mes[1].get_values())
# print(mes[0].name)
# print(mes[1].name)

rec = list(fitFile.get_messages("record"))

# print(rec[0].as_dict())
initial_record = rec[0].as_dict()
print(initial_record['fields'])
# print(initial_record['fields'][0])

# -------------------------------------------------
# data = {'measurements': [], 'units': [], 'headers': [], 'type': []}
# data = []


# for value in initial_record['fields']:
#     if value['name'][0:7] != 'unknown':
#         if value['units'] != 'None':
#             headers.append('{} [{}]'.format(value['name'], value['units']))
#         else:
#             headers.append(value['name'])
#         # data['headers'].append(value['name'])
#         # data['units'].append(value['units'])
#         # data['type'].append(value['type'])
#
# # print(data['headers'])
# print(headers)


# Transform coordinate value from semicircles do degrees
def convert_to_degrees(value):
    return value * (180.0 / (2 ** 31))


data = []
coordinates = []
headers = []
headers_empty = True
counter = -1
for record in fitFile.get_messages("record"):

    measurements = []
    for message in record:

        # Creates list of measurement names
        if headers_empty:
            if message.name[0:7] != 'unknown':
                if message.name != 'position_lat' and message.name != 'position_long':
                    if message.units is not None:
                        headers.append('{} [{}]'.format(message.name, message.units))
                    else:
                        headers.append(message.name)
                    # headers.append(message.name)

        # Fills list with measurements
        if message.name[0:7] != 'unknown':
            if message.name == 'timestamp':
                # data['measurements'].append(measurement.raw_value)
                measurements.append(message.raw_value)
            elif message.name == 'position_lat':
                # measurements.append(convert_to_degrees(message.value))
                coordinates.append([convert_to_degrees(message.value)])
                counter += 1
            elif message.name == 'position_long':
                coordinates[counter].append(convert_to_degrees(message.value))
            else:
                # data['measurements'].append(measurement.value)
                measurements.append(message.value)

    data.append(measurements)
    headers_empty = False


# print(len(data['measurements']))
#
# for i in range(36):
#     if i % 9 == 0:
#         print("\n")
#     print("{} ".format(data['measurements'][i]))


# -------------------------------------------------


# names = []
#
# for name in mes:
#     if name not in names:
#         names.append(name)
#
# print('Names:\n')
# for name in names:
#     print('{}\n'.format(name))
#
# print(len(mes))


# for record in fitfile.get_messages():
#     print(record.fields)


# info1 = fitFile.get_messages("record")
# info2 = fitFile.get_messages("device_info")
# info3 = fitFile.get_messages("file_creator")
# info4 = fitFile.get_messages("event")

print('Garmin profile version: {}'.format(fitFile.profile_version))
print('CRC check: {}'.format(fitFile.check_crc))
# print(fitFile.parse())
print('Protocol version: {}'.format(fitFile.protocol_version))

if len(coordinates) > 0:
    # activity_map = folium.Map(zoom_start=2)
    print('GPS data available.')
    gps = True
else:
    print('GPS data not found in the file.')

# print(fitFile.messages)


# print(type(data['headers']))

# print(type(data))


# print(len(headers)
# print(len(tmpdata))
# print(len(tmpdata) / len(headers))ata=tmpdata, columns=headers)

df = pd.DataFrame(data=data, columns=headers)

print(df)
print(df.describe())
print(df.info())


# print(df.head(10))
# print(df.mean())
# print(df.T)

# display(activity_map)

# Graphs
# df['heart_rate [bpm]'].plot()
# df['cadence'].plot()

# plt.show()

# Plotting graphs

figure1 = plt.Figure(figsize=(6, 5), dpi=100)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side=LEFT, fill=BOTH)
# df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
df1 = df['heart_rate [bpm]']
df1.plot(kind='hist', legend=True, ax=ax1)
ax1.set_title('Heart rate')

figure2 = plt.Figure(figsize=(6, 5), dpi=100)
ax2 = figure2.add_subplot(111)
bar2 = FigureCanvasTkAgg(figure2, root)
bar2.get_tk_widget().pack(side=LEFT, fill=BOTH)
# df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
df2 = df['cadence [rpm]']
df2.plot(kind='line', legend=True, ax=ax2)
ax2.set_title('Cadence')

root.mainloop()


class Map:
    def __init__(self, positions, zoom_start):
        self.positions = positions
        self.zoom_start = zoom_start

    def showMap(self):
        # Create the map
        # my_map = folium.Map(location=self.coords, zoom_start=self.zoom_start)
        my_map = folium.Map(location=self.positions[0], zoom_start=self.zoom_start)
        folium.PolyLine(self.positions, color="red", weight=2.5, opacity=1).add_to(my_map)

        # Display the map
        print('Showing map...')
        my_map.save("map.html")
        webbrowser.open("map.html")


# Define coordinates of where we want to center our map
# coords = [51.5074, 0.1278]
#  hddd o   mm.mmm

#                                          48°08'36.7"N 17°04'37.4"E
#                                          48.143523, 17.077056
# coords1 = [57.4430013, 20.3626915]
# a = 574430013 * (180 / (2 ** 31))
# b = 203626915 * (180 / (2 ** 31))
# coords2 = [a, b]
# print(coords2)
# c = 609843842 * (180.0 / (2 ^ 31))
# print(c)

if gps and show_map:
    activity_map = Map(positions=coordinates, zoom_start=1)
    activity_map.showMap()

# outfile = open("output.txt", "w")

# for record in fitFile:
#     message = str()
#     typefile.write(fitFile.get_messages())

# message = str(fitFile.get_messages())
# typeFile.write(message)
# typeFile.write(fitFile.get_messages("device_info"))
# print("done")

# other types include "device_info", "file_creator", "event", etc

# for record in fitFile.get_messages("record"):
#
#     if file_write:
#         counter += 1
#         outfile.write("{}. record:\n".format(counter))
#
#     # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
#     for message in record:
#         write_to_file(message, counter)
#
#
#
#
#     # print("---")
#
#     outfile.write('')
#
# print('{} records written into the output.txt file'.format(counter))
# outfile.close()

# class FitFile(object):
#     def __init__(self, ):
#         self.df = pd.DataFrame()
#
#
#
#     @property
#     def messages(self):
#         return list(self.get_messages())
