# gsutil python tutorial


# Login with your Google Cloud Platform account in the browser, once you are logged in, you can browse the bucket through
# the project's bucket url: https://console.cloud.google.com/storage/browser/{ PROJECT } where { PROJECT } is the bucket
# name of the project, you can find it in images.csv file under location column, for example, given the following value:
# gs://camera_trap_project__main/deployment/2019497/37f3aa87-a36e-4ca4-8fe6-ceca57977bf6.JPG
# the name of the the bucket is the string contained between 'gs://' and '/deployment/': camera_trap_project__main so, for this example,
# the full bucket url is: https://console.cloud.google.com/storage/browser/camera_trap_project__main
# 
# 
# 
# Using gsutil software
# ---------------------
# 
# gsutil is a Python application that lets you access Cloud Storage from the command line. Is the best option for batch downloads.
# 
# gsutil is easy to install, follow the Google Cloud Platform instructions: https://cloud.google.com/storage/docs/gsutil_install
# 
# Below some examples, replace the values between the brackets with your project values:
# 
#     - Download all images of the project to the current directory: gsutil -m cp -r  gs://{ PROJECT } .
#     - Download all images of one specific deployment to the current directory: gsutil -m cp -r  gs://{ PROJECT }/deployment/{ DEPLOYMENT_ID } .
#     - Download a single image, you can find image url in images.csv file under the column location:  gsutil -m cp -r  gs://{ PROJECT }/deployment/{ DEPLOYMENT_ID }/{ IMAGE } .

# central_suriname_nature_reserve__thumbnails/deployment/2013391/2722d8ce-e697-4014-9f4a-bf0572e9223f.jpg

# import gsutil
from google.cloud import storage
import PySimpleGUI as sg
from PIL import Image
import sys,os
import csv
import pandas

# Import the csv file of images
df = pandas.read_csv('/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/TV_team_data_new_07312018.csv/TV_team_data_new_07312018.csv') # 3,512,805 rows
# top = df.head() # Examine the 'Species' column

df = df[df['Genus']=="Homo"] # 17,775
df.to_csv('/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMCamTrapData/genusHomoFilter_TV_team_data_new_07312018.csv')

# Should also filter out "scientists", for example

for c in df.columns:
    print(c)

# 'Photo ID URL; - the column with URLs 

print(df['Photo ID URL'][1:5])

# image_csv_file = os.path("              ")
# 
# for r in 1:len(image_csv_file):

    # Open image, set up in a gui element

    # GUI element (sg)

imgs = ['/home/mairin/Pictures/gato.png', '/home/mairin/Pictures/nomozo.png']
sg.theme('DarkTeal8')

def loadImage(path, window):
    try:
        # gsutil lookup
        image = Image.open(path)
        image.thumbnail(500,500)
        photo.img = ImageTk.PhotoImage(image)
        window["-IMAGE-"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")

def main():
    # Setup layout of the window app
    layout = [
        [sg.Image(key='-IMAGE-')],
        [sg.Text('Hunter (1)? Or not (leave blank)?'), sg.InputText('')], 
        # [sg.Submit(), sg.Cancel()],
        [sg.Button("Prev"),sg.Button("Next")]
    ]
    window = sg.Window('Image viewer', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            print('Closed normally')
            break
        elif event == 'Submit':
            newval = values[(1)]
            print(newval)
            break
    window1.close()
