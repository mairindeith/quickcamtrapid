#!/usr/bin/env python3

# title             : TEAMDataPrep_Download.py
# description       : A script to manipulate a CSV of images with associated download URLs
# author            : Mairin Deith (mdeith@zoology.ubc.ca)
# date              : May 26 2021
# version           : 0.1
# usage             : python3 TEAMDataPrep_Download.py
# notes             : 
# python_version    : 3.8.5

# Import necessary modules
from google.cloud import storage
import PySimpleGUI as pSG
from PIL import Image
import sys,os
import csv
import pandas as pd
import subprocess

# Link to API key
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/GCloud/double-approach-307117-0fb89015d6a3.json"

### Previous processing
# Import the csv file of images
# df = pandas.read_csv('/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/TV_team_data_new_07312018.csv/TV_team_data_new_07312018.csv') # 3,512,805 rows

# df = pandas.read_csv('/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/TEAM_Data_GClinks/team_tv_data.csv')
# site_key = pandas.read_csv('/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/TEAM_Data_GClinks/partner_datasets_TEAM_metadata_sites_team.csv')

# df = df[df['Genus']=="Homo"] # 17,775
# df.to_csv('/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMCamTrapData/genusHomoFilter_team_tv_data.csv')
def data_processing(infile):
    df = pd.read_csv(
        infile,
        parse_dates=[['Photo Date','Photo Time']]
        )
    df.rename(columns={'Photo Date_Photo Time':'photoDT'}, inplace=True)
    df['hunter01N'] = None
    nonhunterlist = [
        'SMART TEAM Patrol','BCI Employee','BCI Employees',
        'Scientist, Meg Crofoot','scientist','Norwegian research!',
        'Norwegian Researcher!','Worker that was walking towards the uplands',
        'Rangers','rangers','tourists, rangers, and porters','porter','Tourists'
        ]
    hunterlist = [
        'Poacher/encroacher','Illegal','Possibly hunter',
        'Possibly hornbill hunter','Do not seem like forest guards but more like poachers',
        'hunter','Male - Holding 2 axes..','Actually 2: Canis lupus also in photo',
        '2 actually: Canis lupus','2 species: H. sapiens and Canis lupus',
        'also with a dog (Canis lupus)','also Canis lupus','Poacher'
        ]
    nonhunteridx = []
    hunteridx = []
    for e in nonhunterlist:
        hits = df.index[df['Photo Notes'].str.contains(e, na=False, regex=False)].tolist()
        for h in hits:
            nonhunteridx.append(h)
    for e in hunterlist:
        hits = df.index[df['Photo Notes'].str.contains(e, na=False, regex=False)].tolist()
        for h in hits:
            hunteridx.append(h)
    nonhunteridx = list(set(nonhunteridx))
    hunteridx = list(set(hunteridx))
    df.loc[nonhunteridx, 'hunter01N'] = 0
    df.loc[hunteridx, 'hunter01N'] = 1
    return(df)

def loadImage(path, window):
    try:
        # gsutil lookup
        # Image loading
        image = Image.open(path)
        image.thumbnail(500,500)
        photo.img = ImageTk.PhotoImage(image)
        window["-IMAGE-"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")

def main():
    gs_root = 'gs://cameratraprepo-vcm/TEAMRIR_final_bu/'
    photo_loc = '/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/tmpPhotos/'
    try:
        os.mkdir(photo_loc)
    except:
        pass

infile = '/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/genusHomoFilter_team_tv_data_MDAnnotated.csv'
    # Load data - in this case, processing has already been completed (see function, does not need to be re-run)
    # df = data_processing('/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/genusHomoFilter_team_tv_data.csv')
    # df.to_csv('/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/genusHomoFilter_team_tv_data_MDAnnotated.csv')
df = pd.read_csv(infile, parse_dates=['photoDT'])
# Every time you run, subset to only those rows with 'NA/None' in the hunter01N column, the column for IDing hunters
df_sub = df.loc[pd.isna(df['hunter01N'])]
# Then, group this by combination of "Sampling Unit Name" and time, assuming 5 minute intervals are good enough
df_group = df_sub.groupby(['Sampling Unit Name',pd.Grouper(key='photoDT', freq='10min')])
# For each group, first download. Then, once they are all downloaded, go through the window-based processing (offline processing vs. active time...)
for df, d in df_group:
    print(f"Assessing {df}")
    print(f"...number of images: {len(d)}")
#    urls='("'+'" "'.join(gs_root+d['Photo ID URL'])+'")'
    # Download images if less than 10:
    if len(d) >= 10:
        print("...downloading images")
        # Iterate over rows
        for i, r in d.iterrows():
            file = r['Photo ID URL']
            url = gs_root+file
            # print(f"......url: {url}")
            subprocess.call(['gsutil','-m','cp',f'{url}',f'{photo_loc}/{file}'])
        # equivalent to e.g.:

    ### Need to do a re-download for incomplete suffixes, iterate over rows
    # e.g. gs://cameratraprepo-vcm/TEAMRIR_final_bu/TEAMRIR/5/2014.01/CT-VB-/CT-VB-1-7/IMG_0018.JPG
    # Rules: 
    #   CT-VB-X/CT-VB-X-Y/ - X must match
    # for i,r in df_sub.iterrows():
    #     urltmp = r['Photo ID URL']
    #     urlchunk = urltmp.split("/")
    #     ymatch = "-".join((urlchunk[4].split("-"))[0:3])
    #     if urlchunk[3] != ymatch:
    #         urlchunk[3] = ymatch
    #         url = gs_root+"/".join(urlchunk)
    #         subprocess.call(['gsutil','-m','cp',f'{url}',f'{photo_loc}/{file}'])
    # 
    # for df, d in df_group:
    #     print(f"Assessing {df}")
    #     print(f"...number of images: {len(d)}")
    # #    urls='("'+'" "'.join(gs_root+d['Photo ID URL'])+'")'
    #     # Download images if less than 10:
    #     if len(d) >= 10:
    #         print("...downloading images")
    #         # Iterate over rows
    #         for i, r in d.iterrows():
    #             file = r['Photo ID URL']
    #             url = gs_root+file
    #             # print(f"......url: {url}")
    #             subprocess.call(['gsutil','-m','cp',f'{url}',f'{photo_loc}/{file}'])
