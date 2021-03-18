#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 12:34:28 2021

@author: max
"""

import os
import re
from shutil import copyfile
from shutil import move
import shutil 
from distutils.dir_util import copy_tree
from PIL import Image
import imageio
from natsort import natsorted
import glob, os

import argparse

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
        
        
def namedFolder(path):
        #generating file list
    files=os.listdir(path)
        #checking individual files
    for item in files:
        #selecting only tifs
        if '.tif' in item or '.TIF' in item or '.tiff' in item:
            item=item.replace(path, '')
            namepat=re.compile('[^.]*')
            filename=re.search(namepat, item).group()
            createFolder(os.path.join(path, filename))
        print(filename)
        