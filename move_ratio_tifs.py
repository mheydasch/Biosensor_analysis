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

import argparse
#path='/Users/max/Desktop/Office/Phd/Data/N1E_115/SiRNA/SiRNA_28/timelapse/analyzed/GC_ran/'

#%%

def parseArguments():
  # Define the parser and read arguments
  parser = argparse.ArgumentParser(description='collect segmentation files into one directory')
  parser.add_argument('-d', '--dir', type=str, help='The directory where the knockdown folders are', required=True)
  parser.add_argument('-e', '--errors', type=str, help='The file from which to read segmentation errors', required=False)
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
def get_move_paths(path):
    tifind=re.compile('.tif')
    findfile='movieData.mat'
    oldfiles=[]
    newfiles=[]
    newdir=path+'Collection'
    i_dirs=[]
    oldpath=[]
    newpath=[]
    one_up=go_one_up(path)
    for root, dirs, files in os.walk(path):
        if findfile in files:
            i_dirs.append(root)
            for item in i_dirs:
                folderpath=item.replace(path, '')
                folderlist=vars()['folderpath'].split('/')
                foldername=os.path.join(*folderlist)
                #pathlist=vars()['item'].split('/')
                identifier=folderpath.replace('/', '_')
                i_path=os.path.join(item, 'BiosensorsPackage', 'ratio_tiffs')
                #i_path=os.path.join(item, 'FRET')

                if os.path.isdir(i_path):
                    try:
                        oldfiles=[os.path.join(i_path, f) for f in os.listdir(i_path) if os.path.isfile(os.path.join(i_path, f))\
                                  if re.search(tifind, f) is not None ]
                        newfiles=[os.path.join(newdir, identifier+'_'+f) for f in os.listdir(i_path) if os.path.isfile(os.path.join(i_path, f))\
                                  if re.search(tifind, f) is not None ] 

                    except (NotADirectoryError, FileNotFoundError) as e :
                        print('Error in', i_path, '\n', 'no segmentation found')
                        #move_dirs(item, one_up, foldername)
                        next
                else:
                     print('Error in', i_path, '\n', 'no segmentation found')
                     #move_dirs(item, one_up, foldername)
                     next


                        
                [oldpath.append(f) for f in oldfiles]
                [newpath.append(f) for f in newfiles]  

                
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

        
# =============================================================================
# def get_move_paths(path):
#     createFolder(path+'/Collection')
#     onlydirs=[os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
#     oldpath=[]
#     newpath=[]
#     tifind=re.compile('.png')
#     newdir=path+'Collection'
#     oldfiles=[]
#     newfiles=[]
#     KD_pattern=re.compile('[A-Za-z0-9]+')
#     one_up=go_one_up(path)
#     #FOV_pattern=re.compile('[0-9]+')
#     for i in onlydirs:
#         #dont look in collection folder
#         foldername= vars()['i'].split('/')[-1]
#         if foldername != 'Collection' and foldername!= 'Flatfield' and foldername!= 'Not_segmented'  and foldername!= 'HierarchicalCluster' and foldername!= 'segmentation_errors':
#             matched_foldername=re.match(KD_pattern, foldername)
#             if matched_foldername is not None:                           
#                 #look in each folder and create a list of the paths, if it is a folder
#                 i_dirs=[os.path.join(i, folder) for folder in os.listdir(i) if os.path.isdir(os.path.join(i, folder))]
#                 for item in i_dirs:
#                     #get the identifier from the folder
#                     pathlist=vars()['item'].split('/')
#                     identifier=pathlist[-2]+'_'+pathlist[-1]
#                     i_path=item+'/GrowthConeAnalyzer/GCAMainVisualization/filoLength/ForMainMovie_Feature_Movie/Channel1Detect_OverlaidOnChannel1__/'
#                     
#                     #get the folder inside                                      
#                     try:
#                         oldfiles=[os.path.join(i_path, f) for f in os.listdir(i_path) if os.path.isfile(os.path.join(i_path, f))\
#                                   if re.search(tifind, f) is not None ]
#                         newfiles=[os.path.join(newdir, identifier+'_'+f) for f in os.listdir(i_path) if os.path.isfile(os.path.join(i_path, f))\
#                                   if re.search(tifind, f) is not None ]
#                         
#                         
#                     except (NotADirectoryError, FileNotFoundError) as e :
#                         print('Error in', i_path, '\n', 'no segmentation found')
#                         
#                         dump=os.path.join(one_up+'Not_segmented/')
#                         createFolder(dump)
#                         final_dump=os.path.join(dump+foldername+'/')
#                         print(item, 'moved to', final_dump, '\n')
#                         createFolder(final_dump)
#                         move(item, final_dump)            
#                         next
#                     [oldpath.append(f) for f in oldfiles]
#                     [newpath.append(f) for f in newfiles]
#     #print(oldpath, newpath)
#     return oldpath, newpath
# =============================================================================
#if vars()['i1'].split('/')[-7] in vars()['i2'].split('/')[-1]:
def copy_file(path):
    '''
    oldpath: list of paths+filename in which folders are seperated by '/'
            4th element from the back must be identifier of the file
    newpath: list of paths+filename. file must contain identifier
    '''
   
    oldpath, newpath, newdir=get_move_paths(path)
    createFolder(newdir)
    for i1, i2 in zip(oldpath, newpath):    
        shutil.copyfile(i1, i2)

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
    errors=args.errors
    
    if errors is None:
        copy_file(path)
    else:
        move_errors(errors)
    print(args)



#onlyfiles=[f for f in os.listdir(path) if isfile(join(path, f))]
#
 