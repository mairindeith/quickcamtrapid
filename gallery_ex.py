#!/usr/bin/env python3
### Example of script with scrollable column
### import PySimpleGUI as pSG
### 
### layout = [
###     [pSG.Column([[pSG.Text(f"Testing{i}", font=("Courier New", -20))] for i in range(10)],
###                 scrollable=True)]
### ]
### window = pSG.Window("test", layout, margins=(0, 0))
### 
### while True:
###     event, values = window.Read()
###     if event is None or event == 'Exit':
###         break
### 
### window.Close()
### 
### 
### 
### ### 
### 
### test_dir = "/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/tmpPhotos/TEAMRIR/1/2014.01/CT-CAX-1/CT-CAX-1-21/"
### 
### files = os.listdir(test_dir)
### 
### for f in files:
### 	print(f)
### 

# ### Example of a script viewer that can convert jpgs to png:
# image_browser.py

import glob
import PySimpleGUI as sg
from PIL import Image, ImageTk

def parse_folder(path):
    images = glob.glob(f'{path}/*.jpg') + glob.glob(f'{path}/*.png')
    return images

def load_image(path, window, imageID):
    try:
        imageIn = Image.open(path)
        imageIn.thumbnail((640, 640))
        photo_img = ImageTk.PhotoImage(image=imageIn)
        window[imageID].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")
        
def main():
    # Helps to "keep track" of which image is which
    theme_picker = [
        "DarkTeal3","LightBrown9","DarkPurple3"
    ]
    fll = [
        [
        '/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/tmpPhotos/TEAMRIR/1/2014.01/CT-CAX-1/CT-CAX-1-21/100-IMG_0041.JPG', 
        '/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/tmpPhotos/TEAMRIR/1/2014.01/CT-CAX-1/CT-CAX-1-21/100-IMG_0043.JPG', 
        '/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/tmpPhotos/TEAMRIR/1/2014.01/CT-CAX-1/CT-CAX-1-21/100-IMG_0044.JPG'
        ],
        [
        '/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/tmpPhotos/TEAMRIR/1/2014.01/CT-CAX-1/CT-CAX-1-21/100-IMG_0040.JPG', 
        '/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/tmpPhotos/TEAMRIR/1/2014.01/CT-CAX-1/CT-CAX-1-21/100-IMG_0042.JPG', 
        '/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/TEAMData/tmpPhotos/TEAMRIR/1/2014.01/CT-CAX-1/CT-CAX-1-21/100-IMG_0045.JPG'
        ]
    ]
    set_counter = 0
    images = fll[set_counter]
    sg.theme(theme_picker[set_counter % len(theme_picker)])
    layout = [
#        [sg.InputText("", readonly=True, key="-CURRENT-")],
        [sg.Button("Prev (pg up)"),sg.Button("Next (pg down)")],
        [sg.InputText("", font=("Roboto", 16), key="-ERROR-")],
        [sg.Image("/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/gsutil_images/yeshunter.png", size=(640,200))],
        [sg.Image(key=f"current_img", size=(640,640))],
        [sg.Image("/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/gsutil_images/nohunter.png", size=(640,200))]
    ]
    location = (10,10)
    window = sg.Window("Image Viewer", location=location, size=(800, 1000), return_keyboard_events=True).Layout(layout)
    error_box = window['-ERROR-']
    # for i in range(len(fll[0])):
    #     print(images[i])
    load_image(images[0], window, f'current_img')
    img_counter = 0
    while True:
        event, values = window.read()
        window.BringToFront()
        error_box = window['-ERROR-']
        print(event)
        print(set_counter)
        # Replace with ID of df
        # current_box.update(value=f"Set: {set_counter}")
        # current_box.Widget.xview("end")
        images = fll[set_counter]
        # print(images)
        # for i in range(len(images)):
        #     print(images[i])
        load_image(images[img_counter], window, f'current_img')
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # On assignment:
        if event == "Right:114":
            if (img_counter + 1) == len(images):
                error_box.update(value="Final image in set")
                error_box.Widget.xview("end")
            else:
                img_counter += 1
                error_box.update(value="")
                error_box.Widget.xview("end")
                load_image(images[img_counter], window, f'current_img')
        if event == "Left:113":
            if (img_counter - 1) < 0:
                error_box.update(value="First image in set")
                error_box.Widget.xview("end")
            else:
                img_counter -= 1
                error_box.update(value="")
                error_box.Widget.xview("end")
                load_image(images[img_counter], window, f'current_img')
        # If press "Next" or "Enter" (Return:36)"
        # if event == "Up:111":
        #     print("RESPONSE:"+str(event))
        # if event == "Down:116":
        #     print("RESPONSE:"+str(event))
        if event == "Next" or event=="Next:117" or event in ["Up:111", "Down:117"]:
            if event == "Up:111":
                # write CSV row
                print("UP")
            if event == "Down:117":
                # write CSV row
                print("DOWN")
            if set_counter == len(fll):
                break
            img_counter = 0
            set_counter += 1
            print("NEXT")
            # images = fll[set_counter]
            # print(images)
            sg.theme(theme_picker[set_counter % len(theme_picker)])
            layout = [
                [sg.Button("Prev (pg up)"),sg.Button("Next (pg down)")],
                [sg.InputText("", font=("Roboto", 16), key="-ERROR-")],
                [sg.Image("/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/gsutil_images/yeshunter.png", size=(640,200))],
                [sg.Image(key=f"current_img", size=(640,640))],
                [sg.Image("/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/gsutil_images/nohunter.png", size=(640,200))]
            ]
            window1 = sg.Window("Image Viewer", location=location, size=(800, 1000), return_keyboard_events=True).Layout(layout)
            window.Close()
            window = window1
            event, values = window.read()
            window.BringToFront()
        if event == "Previous" or event=="Prior:112":
            print("PREVIOUS")
            if set_counter == 0:
                bleh = window['-ERROR-'].get()
                teh = f'ERROR: First set.'
                error_box.update(value=teh)
                error_box.Widget.xview("end")
            else:
                error_box.update(value="-")
                error_box.Widget.xview("end")
                set_counter -= 1
                img_counter = 0
                # images = fll[set_counter]
                sg.theme(theme_picker[set_counter % len(theme_picker)])
                layout = [
                    [sg.Button("Prev (pg up)"),sg.Button("Next (pg down)")],
                    [sg.InputText("", font=("Roboto", 16), key="-ERROR-")],
                    [sg.Image("/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/gsutil_images/yeshunter.png", size=(640,200))],
                    [sg.Image(key=f"current_img", size=(640,640))],
                    [sg.Image("/home/mairin/Documents/GradSchool/PhD/Research/CircuitTheory_TEAM/gsutil_images/nohunter.png", size=(640,200))]
                ]
                window1 = sg.Window("Image Viewer", location=location, size=(800, 1000), return_keyboard_events=True).Layout(layout)
                window.Close()
                window = window1
                event, values = window.read()
                window.BringToFront()
#!#                for i in range(len(images)):
#!#                    print(images[i])
#!#                    load_image(images[i], window, f'image{i}')
            # if df_counter == 0:
            #     pass
            # else:
            #     df_counter -= 1
            #     pass
            # print(df_counter)
    window.close()

if __name__ == "__main__":
    main()