#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 10:29:01 2020

@author: max
"""
import os
import re
import sys
from shutil import copyfile
from shutil import move
import shutil 
import skimage.io
import numpy as np
from distutils.dir_util import copy_tree
from PIL import Image, ImageSequence
import imageio
from natsort import natsorted
import glob, os
import dask.array as da
from dask_image.imread import imread
#from dask import delayed
#from tqdm import tqdm

import argparse

#%%
import numpy as np
from PIL import Image

array = np.zeros([2, 6, 3], dtype=np.uint8)
array[:,:] = [0, 0, 255] #Orange left side
   #Blue right side

img = Image.fromarray(array)
img.save('/Users/max/Desktop/testrgb2.tif')


#%%

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
def parseArguments():
  # Define the parser and read arguments
  parser = argparse.ArgumentParser(description='collect segmentation files into one directory')
  parser.add_argument('-d', '--dir', type=str, help='The directory where the knockdown folders are', required=True)
  parser.add_argument('-ch', '--chan', type=str, help='specify the channel you want to make a movie from', required =False)
  parser.add_argument('-mic', '--mic', type=str, help='specify the microscope that generated the data. Either Jungfrau, Eiger, NIS or micromanager', required =False)
  parser.add_argument('-debug', '--debug', type=str, help='turn on debugging', required =False)

  args = parser.parse_args()
  return(args)
  
def simple_moviemaker(path):
    #comment the following out:

    
    if microscope=='Jungfrau':
        
        pattern=re.compile('^(?P<Timepoint>t[0-9]+)_.*_(?P<Movie_ID>XY[0-9]+)_.*.tif')
        
    if microscope=='Eiger':
        #pattern=re.compile('^(?P<Classifier>.*)(?P<FOV>_[0-9])_.*(?P<Site>_s[0-9]+)_(?P<Timepoint>t[0-9]+).TIF')
        pattern=re.compile('^(?P<Movie_ID>.*)_(?P<Timepoint>t[0-9]+).TIF')
    if microscope=='EigerNewFRET':
        pattern=re.compile('^(?P<Movie_ID>.*)_(?P<Timepoint>t[0-9]+)(?P<Channel>ratio).tiff')
    if microscope=='Eigertif':
        pattern=re.compile('^(?P<Classifier>.*)(?P<FOV>_[0-9])_.*(?P<Site>_s[0-9]+)_(?P<Timepoint>t[0-9]+).TIF')
        #pattern=re.compile('^(?P<Movie_ID>.*)_(?P<Timepoint>t[0-9]+).*.tif')
    if microscope=='NIS':
        pattern=re.compile('.*(?P<Timepoint>T[0-9]+)_(?P<Movie_ID>XY[0-9]+).*.tif')
    if microscope=='micromanager':
        pattern=re.compile('^raw_(?P<Movie_ID>[0-9]{2})_(?P<Timepoint>[0-9]{5}).tiff')
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
                if debugging=='True':
                    print(channel)
                if channel in item:
                    #create empty list to append later
                    current_Movie=[]
                    #extracts ID and timepoint
                    try:
                        if microscope=='Jungfrau' or microscope=='NIS' or microscope=='micromanager' or microscope=='Eigertif':
                            Movie_ID, Timepoint=re.search(pattern, item).group('Movie_ID', 'Timepoint')
                            current_ID=Movie_ID
                        if microscope=='Eiger':
                            Classifier, FOV, Site, Timepoint=re.search(pattern, item).group('Classifier', 'FOV', 'Site', 'Timepoint')
                            #Movie_ID, Timepoint=re.search(pattern, item).group('Movie_ID', 'Timepoint')
                            current_ID=Movie_ID
                            #current_ID=Classifier+FOV+Site
                            #Movie_ID=current_ID
                        if microscope=='EigerNewFRET':
                            #Classifier, FOV, Site, Timepoint=re.search(pattern, item).group('Classifier', 'FOV', 'Site', 'Timepoint')
                            Movie_ID, Timepoint, Channel=re.search(pattern, item).group('Movie_ID', 'Timepoint', 'Channel')
                            current_ID=Movie_ID+Channel
                        #go to next interation of loop if ID is in processed
                        if current_ID in processed:
                            continue
                            
                        print(current_ID)
                        #print(Timepoint)
                    #exception in case an item was found that cant be matched    
                    except:
                        print('{} does not match pattern'.format(item))
                        if debugging == 'True':
                            print (sys.exc_info())
                            print(pattern)
                        continue
                    #check if movie has been processed already
                    if current_ID!=None:
                    #get the files that belong to the current one 
                        for item in files:
                            try:
                                sanity_id, Timepoint=re.search(pattern, item).group('Movie_ID', 'Timepoint')
                            except:
                                continue

                            if current_ID ==sanity_id and channel in item:
        
                                current_Movie.append(item)
                    #append current id to the list of processed movies            
                    processed.append(current_ID)
                    #sorting current list
                    current_Movie=natsorted(current_Movie)
                    tifseries=[]
                    if microscope!='micromanager':
                        for i in current_Movie:
                            #print('oldfiles:', oldfiles)
    
                            if Movie_ID + 'movie' not in i :
                                img=Image.open(os.path.join(path, i))
                                
                                tifseries.append(img)
                                if debugging=='True':
                                    print(i)
                                    print(len(tifseries), ' open files')
                    if microscope=='micromanager':
                        tifseries=[imread(os.path.join(path, i)) for i in current_Movie]
# =============================================================================
#                         if debugging=='True':
#                             print(tifseries)
# =============================================================================
                        stack=da.stack(tifseries)
                        stack=np.squeeze(stack)
# =============================================================================
#                         for i in current_Movie:
#                             if debugging=='True':
#                                 print(i)
#                             if Movie_ID + 'movie' not in i :
#                                 img=imread(os.path.join(path, i))
#  
#                                 if debugging=='True':
#                                     print(len(tifseries), ' open files')
# =============================================================================
                         
                            
                            #print(tifseries)
                    createFolder(os.path.join(path, 'movies'))
                    Movie_ID=Movie_ID.replace(' ', '')
                    tifseriespath=os.path.join(path, 'movies', Movie_ID + 'movie.tiff')
                    if microscope == 'micromanager':
                        pathsplit=path.split(sep='/')
                        
                        #tifseriespath1=os.path.join(path, 'movies', pathsplit[len(pathsplit)-2] + '_'+  Movie_ID + 'C1_movie.tiff')
                        tifseriespath2=os.path.join(path, 'movies', pathsplit[len(pathsplit)-2] + '_'+  Movie_ID + 'C2_movie.tiff')

                        try:
                            print('trying to save image')
                            #tifseries[0].save(tifseriespath, save_all=True, append_images=tifseries[1:])
                            #activate for first channel to be safed.
                            #skimage.io.imsave(tifseriespath1, stack[:,1,:,:])
                            skimage.io.imsave(tifseriespath2, stack[:,0,:,:])
                            
                            print('Movie saved as', tifseriespath)
                        except (RuntimeError) as e:
                            print(e)
                            next        
                    else:
                        imageio.mimwrite(tifseriespath, tifseries)
                        print('Movie saved as', tifseriespath)
                else:
                    print('Channel cannot be found')
    return processed

def create_timelapse(path, length, prefix=''):
    length=list(range(length))
    length=[str(i) for i in length]
    length=[i.zfill(5) for i in length]
    files=os.listdir(path)
    print(files)
    pattern = re.compile('(?P<Channel>).*(?P<FOV>[0-9]{2})_(?P<Timepoint>[0-9]{5}).tiff')
    for item in files:
        print(item)
        Timepoint=re.search(pattern, item).group('Timepoint')
        #[shutil.copyfile(os.path.join(path, item), os.path.join(path, item.replace(Timepoint, t))) for t in length]
        for t in length:
            print(t)
            temp=os.path.join(path, prefix, item.replace(Timepoint, t))
            print(item)
            if Timepoint!=t:
                shutil.copyfile(os.path.join(path,item), temp)
            
        print('created timelapse of ', os.path.join(path, item))
        
        

 
        

#for filename in *.tiff; do mv "$filename" "lightmask_$filename"; done;
#for file in *.TIF; do mv "$file" "${file%.TIF}.tif"; done;            
#%%
if __name__ == '__main__':
    args=parseArguments()   
    path=args.dir
    channel=args.chan
    microscope=args.mic
    debugging=args.debug
    if args.mic == None:
        microscope='Jungfrau'
    if args.debug == None:
        debugging == 'True'
    simple_moviemaker(path)

    print(args)