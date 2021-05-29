#!/usr/bin/env python3

# title             : GUIImageID.py
# description       : Open "grouped" images (grouped by proximity in time)
# author            : Mairin Deith (mdeith@zoology.ubc.ca)
# date              : May 26 2021
# version           : 0.1
# usage             : python3 GUIImagesID.py
# notes             : Assumes that images have already been downloaded (from .csv URL column)
# python_version    : 3.8.5

# Modules
import PySimpleGUI as sg
from PIL import Image
import sys,os
import csv
import pandas as pd

# def translate_url(url){
#     # Translate the URL column into a relative path
# }

# Identify images and return a list of files

# Iterate through the list, grouping by data frame



# Path to images to show 
imgs = ['/home/mairin/Pictures/gato.png', '/home/mairin/Pictures/nomozo.png']
sg.theme('DarkTeal3')

# def loadImage(path, window):
#     try:
#         # gsutil lookup
#         image = Image.open(path)
#         image.thumbnail(500,500)
#         photo.img = ImageTk.PhotoImage(image)
#         window["-IMAGE-"].update(data=photo_img)
#     except:
#         print(f"Unable to open {path}!")

def main():
    ### GLOBAL 
    # Path to "tracking" csv (images filtered to humans), created with the associated Python3 script 'TEAMDataPrep_Download.py'
datafile = '/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/genusHomoFilter_team_tv_data_MDAnnotated.csv'
# In case downloads are needed, identify the google storage root URL
gs_root = 'gs://cameratraprepo-vcm/TEAMRIR_final_bu/'
# Root folder for all photo files (these are saved in subdirs)
photo_loc = '/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/tmpPhotos/'
# Read the file, force the type of the 'photoDT' column as date
df = pd.read_csv(datafile, parse_dates=['photoDT'])
# Every time you run, subset to only those rows with 'NA/None' in the hunter01N column, the column for IDing hunters
df_sub = df.loc[pd.isna(df['hunter01N'])]
# Then, group this by combination of "Sampling Unit Name" and time, assuming 5 minute intervals are good enough
df_group = df_sub.groupby(['Sampling Unit Name',pd.Grouper(key='photoDT', freq='5min')])
# Now, set up the GUI
elements = [[
    sg.Column([[sg.Image(key=f"image{i}")] for i in range(len(fll))], scrollable=True, expand_y=True, expand_x=True),
        sg.Text("Identification (h, n, or u"),
        sg.Button("Prev"),sg.Button("Next"), 
        sg.Input(size=(25, 1), enable_events=True, key="imgid")
    ]
]
    df_counter = 0
    for df, d in df_group:
        print(f"Assessing {df}")
        print(f"...number of images: {len(d)}")
        # Iterate over rows
        file_list = []
        for i, r in d.iterrows():
            # Check if the images are already downloaded; if not, download
            # (try/except:)may need to rename some - return an error at least?
            file = r['Photo ID URL']
            url = gs_root+file
            # print(f"......url: {url}")
            if not os.path.isfile(f'{photo_loc}/{file}'):
                print("...file not found, downloading...")
                # Download using gsutil from a "command line"
                out = subprocess.run(['gsutil','-m','cp',f'{url}',f'{photo_loc}/{file}'])
                # If there was an error, go to the next row 
                if out.returncode==1:
                    print("ERROR")
                    continue
            file_list += [f'{photo_loc}/{file}']
    
    # SET ACTIVE ROWS IN CSV