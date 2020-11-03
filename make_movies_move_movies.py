#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 17:56:26 2020

@author: max
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 09:52:03 2019

@author: max
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 15:17:42 2018

@author: max
"""

'''
takes all segmentation representations burried deep in the folder of the GC output
and copies all of them to a single folder
moves all directories for which no segmentation could be found to a 'Not_segmented'
directory
with the -e option it accepts a text file as second input and moves all folders 
annotated in that file to a segmentation error directory.

'''
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
#path='/Users/max/Desktop/Office/Phd/Data/N1E_115/SiRNA/SiRNA_28/timelapse/analyzed/GC_ran/'

#%%

def parseArguments():
  # Define the parser and read arguments
  parser = argparse.ArgumentParser(description='collect segmentation files into one directory')
  parser.add_argument('-d', '--dir', type=str, help='The directory where the knockdown folders are', required=True)
  parser.add_argument('-e', '--errors', type=str, help='The file from which to read segmentation errors', required=False)
  parser.add_argument('-m', '--mode', type=str, help='The movie type that should be moved Either \'ratio\', or the channel name.', required=True)
  args = parser.parse_args()
  return(args)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)
#%%
#for filepath in glob.glob(path + '*{}'.format(identifier))
def go_one_up(path):
    '''
    takes one folder upwards of the given input folder
    '''
  
    split_path=vars()['path'].split('/')
    one_up='/'+split_path[0]
    for n, i in enumerate(split_path[:-3]):
        one_up=one_up=os.path.join(one_up, split_path[n+1])
    one_up=one_up+'/'
    return one_up

#%%
def get_move_paths(path, mode):
    '''
    mode is either ratio for raito movies, or the channel name
    '''
    tifind=re.compile('.tif')
    findfile='movieData.mat'
    oldfiles=[]
    newfiles=[]
    newdir=path+'Collection'
    i_dirs=[]
    oldpath=[]
    newpath=[]
    one_up=go_one_up(path)
    end_dirs=[]
    moviename=mode
    
    for root, dirs, files in os.walk(path):
        if findfile in files:
            i_dirs.append(root)
            for item in i_dirs:
                if moviename !='ratio':
                    i_path=os.path.join(item, moviename)
                if moviename=='ratio':
                    i_path=os.path.join(item, 'BiosensorsPackage', 'ratio_tiffs')
                #print(i_path)
                end_dirs.append(i_path)
                end_dirs=set(end_dirs)
                end_dirs=list(end_dirs)
                
    for i_path in end_dirs:      
                
                folderpath=i_path.replace(path, '')
                folderlist=vars()['folderpath'].split('/')
                #foldername=os.path.join(*folderlist)
                #pathlist=vars()['item'].split('/')
                identifier=folderpath.replace('/', '_')    
                #i_path=os.path.join(item, 'FRET')

                if os.path.isdir(i_path):
                    try:
                        oldfiles=[os.path.join(i_path, f) for f in os.listdir(i_path) if os.path.isfile(os.path.join(i_path, f))\
                                  if re.search(tifind, f) is not None ]
                        #print(oldfiles)
                        oldfiles=natsorted(oldfiles)
                        tifseries=[]    
                        print('ipath_:',i_path)
                        
                        for i in oldfiles:
                            #print('oldfiles:', oldfiles)
                            if moviename + 'movie' not in i:
                                img=Image.open(i)
                                tifseries.append(img)
                                #print(tifseries)
                        tifseriespath=os.path.join(i_path, moviename + 'movie.tiff')
                        try:
                            imageio.mimwrite(tifseriespath, tifseries)
                            newfiles=os.path.join(newdir,identifier + moviename + 'movie.tiff') 
                            oldpath.append(tifseriespath)
                            newpath.append(newfiles)
                        except (RuntimeError) as e:
                            print(e)
                            next
  
                    except (NotADirectoryError, FileNotFoundError) as e :
                        print('Error in', i_path, '\n', 'no segmentation found')
                        #move_dirs(item, one_up, foldername)
                        next
                else:
                     print('Error in', i_path, '\n', 'no segmentation found')
                     #move_dirs(item, one_up, foldername)
                     next


                        
                 

                
    return oldpath, newpath, newdir

def move_dirs(item, one_up, foldername):
    dump=os.path.join(one_up,'Not_segmented/')
    createFolder(dump)
    final_dump=os.path.join(dump, foldername)   
    createFolder(final_dump)
    if os.path.isdir(item):
        #new_location=os.path.join(final_dump, foldername)
        try:
            copy_tree(item, final_dump) 
            print(item, 'moved to', final_dump, '\n')
            #shutil.rmtree(item)
        except FileExistsError as e:
            print(e)
            next        

#simple function to make movies out of individual tif files, without running hte whole script.
        
def simple_moviemaker(path):
    pattern=re.compile('(?P<Movie_ID>.*)(?P<Timepoint>_t[0-9]+)')
    processed=[]
    #generating file list
    files=os.listdir(path)
        #checking individual files
    for item in files:
        current_ID=None
        if '.tif' in item or '.TIF' in item or '.tiff' in item:
            current_Movie=[]
            #extracts ID and timepoint
            try:
                Movie_ID, Timepoint=re.search(pattern, item).group('Movie_ID', 'Timepoint')
                current_ID=Movie_ID
                if current_ID in processed:
                    next
                    
                print(current_ID)
                #print(Timepoint)
            except:
                print('{} does not match pattern'.format(item))
            #check if movie has been processed already
            if current_ID!=None:
            #get the files that belong to the current one 
                for item in files:
                    if current_ID in item:
# =============================================================================
#                     if '.tif' in item or '.TIF' in item or '.tiff' in item:
#                         Movie_ID, Timepoint=re.search(pattern, item).group('Movie_ID', 'Timepoint') 
#                         if Movie_ID==current_ID:
# =============================================================================
                        current_Movie.append(item)
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
    return processed

# =============================================================================
#if vars()['i1'].split('/')[-7] in vars()['i2'].split('/')[-1]:
def copy_file(path, mode):
    '''
    oldpath: list of paths+filename in which folders are seperated by '/'
            4th element from the back must be identifier of the file
    newpath: list of paths+filename. file must contain identifier
    '''
   
    oldpath, newpath, newdir=get_move_paths(path, mode)
    createFolder(newdir)
    for i1, i2 in zip(oldpath, newpath):    
        #print('oldfile, newfile:', i1, i2)
        shutil.copyfile(i1, i2)
        print(i1, 'copied to', i2)

def read_text(errors):
    '''
    reads in a textfile with the names of folders that have segmentation errors.
    '''
    file= open(errors, 'r')
    #creates a list of lines from the file
    lines=file.readlines()
    for n, i in enumerate(lines):        
        lines[n]=i.replace('\n', '')    
    return lines

def move_errors(errors):
    lines=read_text(errors)
    one_up=go_one_up(path)
    if len(lines)>0:
        seg_dump=os.path.join(one_up, 'segmentation_errors')
        createFolder(seg_dump)
        for i in lines:
            try:
                item=os.path.join(path, i)
                kd = vars()['i'].split('/')[-2]        
                kd_dump=os.path.join(seg_dump, kd)
                createFolder(kd_dump)            
                move(item, kd_dump)
                print(item, 'was moved to', kd_dump, '\n')
            except Exception as e:
                print(e)

    
#%%%
if __name__ == '__main__':
    args=parseArguments()
    path=args.dir
    mode=args.mode
    errors=args.errors
    
    if errors is None:
        copy_file(path, mode)
    else:
        move_errors(errors)
    print(args)
#%%
pattern=re.compile('(?P<Movie_ID>.*)(?P<Timepoint>_t[0-9]+)')
processed=[]
#generating file list
files=os.listdir(path)
    #checking individual files
for item in files:
    current_ID=None
    if '.tif' in item or '.TIF' in item or '.tiff' in item:
        current_Movie=[]
        #extracts ID and timepoint
        try:
            Movie_ID, Timepoint=re.search(pattern, item).group('Movie_ID', 'Timepoint')
        except:
            pass

#onlyfiles=[f for f in os.listdir(path) if isfile(join(path, f))]
#