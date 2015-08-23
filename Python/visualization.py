# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 18:58:10 2015

@author: Justin
"""

import importlib.machinery

#%% Get Track Data

#filename = 'C:/Users/Justin/Documents/GitHub/Flight_Track_Visualization/LT6_Single_Flight_Track.txt'
filename = 'C:/Users/Justin/Documents/GitHub/Flight_Track_Visualization/LT6_Multiple_Flight_Tracks.txt'

loader = importlib.machinery.SourceFileLoader('isd','import_and_structure_data.py')
isd = loader.load_module('isd')

tracks = isd.get_tracks(filename)

#%% Generate Animation

