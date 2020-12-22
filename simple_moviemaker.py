#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 10:29:01 2020

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

def parseArguments():
  # Define the parser and read arguments
  parser = argparse.ArgumentParser(description='collect segmentation files into one directory')
  parser.add_argument('-d', '--dir', type=str, help='The directory where the knockdown folders are', required=True)
  parser.add_argument('-ch', '--chan', type=str, help='specify the channel you want to make a movie from', required =False)
  parser.add_argument('-mic', '--mic', type=str, help='specify the microscope that generated the data. Either Jungfrau or Eiger', required =False)

  args = parser.parse_args()
  return(args)
  
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
def simple_moviemaker(path):
    
    if microscope=='Jungfrau':
        
        pattern=re.compile('.*(?P<Timepoint>_T[0-9]+)_(?P<Movie_ID>XY[0-9]+_.*).tif')
    if microscope=='Eiger':
        pattern=re.compile('^(?P<Classifier>.*)(?P<FOV>_[0-9])_.*(?P<Site>_s[0-9]+)_(?P<Timepoint>t[0-9]+).TIF')
    #pattern=re.compile('(?P<Movie_ID>.*)(?P<Timepoint>_t[0-9]+)')
    processed=[]
    

        
    #generating file list
    files=os.listdir(path)
        #checking individual files
    for item in files:
        current_ID=None
        #selecting only tifs
        if '.tif' in item or '.TIF' in item or '.tiff' in item:
            #in case a channel was specified, select only files with that channel
            if channel != None:
                if channel in item:
                    #create empty list to append later
                    current_Movie=[]
                    #extracts ID and timepoint
                    try:
                        if microscope=='Jungfrau':
                            Movie_ID, Timepoint=re.search(pattern, item).group('Movie_ID', 'Timepoint')
                            current_ID=Movie_ID
                        if microscope=='Eiger':
                            Classifier, FOV, Site, Timepoint=re.search(pattern, item).group('Classifier', 'FOV', 'Site', 'Timepoint')
                            current_ID=Classifier+FOV+Site
                        #go to next interation of loop if ID is in processed
                        if current_ID in processed:
                            continue
                            
                        print(current_ID)
                        #print(Timepoint)
                    #exception in case an item was found that cant be matched    
                    except:
                        print('{} does not match pattern'.format(item))
                    #check if movie has been processed already
                    if current_ID!=None:
                    #get the files that belong to the current one 
                        for item in files:
                            if current_ID in item:
        
                                current_Movie.append(item)
                    #append current id to the list of processed movies            
                    processed.append(current_ID)
                    #sorting current list
                    current_Movie=natsorted(current_Movie)
                
                    tifseries=[]
                    for i in current_Movie:
                        #print('oldfiles:', oldfiles)
                        if Movie_ID + 'movie' not in i:
                            img=Image.open(os.path.join(path, i))
                            tifseries.append(img)
                            #print(tifseries)
                    tifseriespath=os.path.join(path, Movie_ID + 'movie.tiff')
                    try:
                        imageio.mimwrite(tifseriespath, tifseries)
                        print('Movie saved as', tifseriespath)
                    except (RuntimeError) as e:
                        print(e)
                        next        
                else:
                    print('Channel cannot be found')
    return processed

if __name__ == '__main__':
    args=parseArguments()
    path=args.dir
    channel=args.chan
    microscope=args.mic
    if args.mic == None:
        microscope='Jungfrau'
    simple_moviemaker(path)

    print(args)