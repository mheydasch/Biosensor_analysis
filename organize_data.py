#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 13:40:44 2019

@author: max
"""
import os
import re
import functools
import pandas as pd
import numpy as np

#%%
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
#%%  



#%%
def get_groups(path):
    tif_search=re.compile('.TIF$')
    #name_search=re.compile('.+?(?=_w[0-9]+)')
    name_search('.+?(?=_w[0-9]+)')
    for file in os.listdir(path):    
        if re.search(tif_search, file)!=None:
            print(file)
            groupFolder=os.path.join(path, re.search(name_search, file).group())
            createFolder(groupFolder)
            print(groupFolder)
            os.rename(os.path.join(path, file), os.path.join(groupFolder, file))