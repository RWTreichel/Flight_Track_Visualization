# -*- coding: utf-8 -*-
"""
Import LT6 flight track data and format into a usable form

Created on Wed Aug 19 12:50:15 2015
@author: Justin
"""

filename = 'C:/Users/Justin/Documents/GitHub/Flight_Track_Visualization/Example_Tracks/LT6_Single_Flight_Track.txt'
#filename = 'C:/Users/Justin/Documents/GitHub/Flight_Track_Visualization/Example_Tracks/LT6_Multiple_Flight_Tracks.txt'

#%% Modules
###############################################################################
from datetime import datetime as dt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import csv
import json    

#%% Define Track Object
###############################################################################
class Track:
    def __init__(self, trk_data, trk_geo):
        self.externalid = int(trk_data[0])
        self.date = dt.strptime(trk_data[2], '%m/%d/%Y').date()
        self.starttime = dt.strptime(trk_data[3], '%H:%M:%S').time()
        self.endtime = dt.strptime(trk_data[4], '%H:%M:%S').time()
        self.duration = (dt.combine(dt.today(), self.endtime) - dt.combine(dt.today(), self.starttime)).total_seconds()
        self.mainapt = trk_data[5] #airport of interest
        self.recapt = trk_data[13] #reciprocal aiport
        self.flightnumber = trk_data[6]
        self.acft = trk_data[8]
        self.eng = trk_data[9]
        self.optype = trk_data[11]
        self.rwy = trk_data[14]
        self.x = []; self.y = []; self.z = []; self.s = []; self.t = []
        for line in trk_geo:
            self.x.append(int(line.group(1)))
            self.y.append(int(line.group(2)))
            self.z.append(int(line.group(3)))
            self.s.append(int(line.group(4)))
            self.t.append(int(line.group(5)))
    
    def plot_track(self, dim):
        fig = plt.figure()
        if dim == '2d':
            ax = plt.plot(self.x, self.y)
        elif dim == '3d':
            #ax = fig.gca(projection = '3d')
            #ax = fig.add_subplot(111, projection='3d')
            ax = Axes3D(fig)
            ax.plot(self.x, self.y, zs = self.z)
        elif dim == '3da':
            ax = fig.gca(projection = '3d')
            u = 1; v = 1; w = 1;
            ax.quiver(self.x, self.y, self.z, u, v, w, length = 100) #self.s)
        ax.set_aspect('equal')
        plt.show()

#%% Parsing functions
###############################################################################
def get_trk_data(data):
    trk_data = []
    for line in data:
        if line[:5] == 'TRACK':
            #trk_data[0] = (re.search('/d+', line))
            trk_data.append(line[7:].rstrip('\n'))#.group().rstrip('\n'))
            line_counter = 0
        elif re.search('\d+,\d+,\d+,\d+,\d+', line):
            break
        else:
            line_counter += 1
            #trk_data[counter] = line
            trk_data.append(line.rstrip('\n'))
    #data.close()            
    return(trk_data)
    
def get_trk_geo(data):
    trk_geo = []
    for line in data:
        if re.search('\d+,\d+,\d+,\d+,\d+', line):
                trk_geo.append(re.search('(\d+),(\d+),(\d+),(\d+),(\d+)', line))
    #data.close()
    return(trk_geo)  

def get_trk_count(data):
    trk_count = 0
    for line in open(filename):
        if line[:5] == 'TRACK':
            trk_count += 1
    return(trk_count)


#%% Create tracks dictionary
###############################################################################

def get_tracks(filename):
    data = []
    track_names = {}
    trk_counter = 0
    line_counter = 0
    for line in open(filename):
        if line[:5] == 'TRACK':
            track_names[trk_counter] = line_counter
            trk_counter += 1
        line_counter += 1
        data.append(line.rstrip('\n'))
    
    data_parts = []
    for i in sorted(track_names.keys()):
        if i == len(track_names.keys())-1:
            data_parts.append(data[track_names[i]:])
        else:
            data_parts.append(data[track_names[i]:track_names[i+1]])
    
    tracks = {}
    id = 0
    for t in data_parts:
        tracks[id] = Track(get_trk_data(t), get_trk_geo(t))
        id += 1
    return(tracks)
    
#%% Export
###############################################################################

def get_csv(tracks):
    with open('C:/Users/Justin/Documents/GitHub/Flight_Track_Visualization/Example_Tracks/csv_ouput.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',') #, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['TIME','X_COORD', 'Y_COORD','Z_COORD'])
        for i in range(len(tracks[0].x)):
            spamwriter.writerow([tracks[0].t[i], tracks[0].x[i], tracks[0].y[i], tracks[0].z[i]])
        
def get_json(tracks):    
    with open('C:/Users/Justin/Documents/GitHub/Flight_Track_Visualization/Example_Tracks/json_ouput.json', 'w') as outfile:
        #ls = ['TIME','X_COORD', 'Y_COORD','Z_COORD']
        ls = (list(zip(tracks[0].t, tracks[0].x, tracks[0].y, tracks[0].z)))
        ls.insert(0, ['TIME','X_COORD', 'Y_COORD','Z_COORD'])
        json.dump(ls, outfile, ensure_ascii=False)
    
    
    
# %% Test run area
    
tracks = get_tracks(filename)
get_csv(tracks)
get_json(tracks)