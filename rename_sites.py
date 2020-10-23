#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:22:27 2019

@author: max
"""

import re
import pandas
import os

#%%

#filename=(?P<Site_ID>W[A-Z][0-9]+_S[0-9]{4})(?P<TrackID>_E[0-9]+)(?P<Timepoint>_T[0-9]+)
#        Site_ID, track_ID, Timepoint =re.search(pattern, ID_or).group(
#                 'Site_ID', 'TrackID', 'Timepoint')
filename=re.compile('(?P<Experiment>.*Ctrl|Dlc|CTRL|DLC_[0-9]*)(?P<Channel>_w[0-9]+.*)(?P<Site>_s[0-9])(?P<Timepoint>_t[0-9]+)')