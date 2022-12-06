from pynput.keyboard import Key, Controller
#from PIL import Image, ImageTk
import PySimpleGUIQt as gui
import shutil
import time
import webbrowser
import os


# --define Values--
target = ""
imageFiles = ["Empty","Empty","Empty","Empty","Empty","Empty"]
keyboard = Controller()
InfoText = "01. Set the Resolution of your Instance to a 1:1 Ratio (e.g. 512x512 or 1024x1024). \n02. Make sure your Instance is in Window Mode! \n03. Set your FOV to 82. \n04. Remove all Effects that influence the view! (e.g. Speed, Nausea, Slowness, etc.) \n05. (Open your World and) Go to a suitable place. This will be the Center of your Background! \n06. Press F1 to hide the Gui! (e.g. Hotbar) \n07. Press the \"Take Screenshots\"-Button and wait 7 Seconds! \n08. Open your Screenshots-Folder. Then Drag and Drop the taken Screenshots in order in the \"Source\"-Inputs so the Path appears in it. \n09. Choose the Background Folder in your Resourcepack and Drag and Drop it in the \"Target File\"-Input so the Path appears in it. \n10. Click \"Create Files\" and the files should appear in the chosen Folder."
TutorialVideo = "http://example.com"
Font = "Segoe UI"
Font_size = 10
icon_path = "assets/icon.ico"


# --set GUI--
gui.ChangeLookAndFeel('Default')

#top column
top_column= [
    [gui.Text("Tutorial:", font= (Font, 15, "bold"))],
    [gui.Text(InfoText, font= (Font, Font_size))],
    [gui.Text("Need Help? Here is a Tutorial Video!", text_color="#0000EE", font= (Font, Font_size, "underline"), tooltip = f"Open: {TutorialVideo}", enable_events= True, key= "TUTORIAL_LINK")],
    [
    gui.Checkbox("show Images", key="SHOW_HIDE_IMAGE", default= True, enable_events= True),
    gui.Button("Take Screenshots\n(6 Second delay)", key="SCREENSHOTS", size=(None, None)),
    gui.Column([[
        gui.Text("Starting in: -", key="TIMER", visible=False, size=(150, 30))
    ]])
    ]
]

#left column
image_column= [
    [
        gui.Image(key= "IMAGE_0"),
        gui.Column(
        [
            [gui.Text("Source:")],
            [gui.InputText(size=(10, 1), enable_events= True, key= "SOURCE_0")]
        ]
    )
    ],
    [
    gui.Image(size=(20, 20), key= "IMAGE_1"),
    gui.Column(
        [
            [gui.Text("Source:")],
            [gui.InputText(size=(10, 1), enable_events= True, key= "SOURCE_1")]
        ]
    )
    ],
    [
    gui.Image(size=(20, 20), key= "IMAGE_2"),
    gui.Column(
        [
            [gui.Text("Source:")],
            [gui.InputText(size=(10, 1), enable_events= True, key= "SOURCE_2")]
        ]
    )
    ],
    [
    gui.Image(size=(20, 20), key= "IMAGE_3"),
    gui.Column(
        [
            [gui.Text("Source:")],
            [gui.InputText(size=(10, 1), enable_events= True, key= "SOURCE_3")]
        ]
    )
    ],
    [
    gui.Image(size=(20, 20), key= "IMAGE_4"),
    gui.Column(
        [
            [gui.Text("Source:")],
            [gui.InputText(size=(10, 1), enable_events= True, key= "SOURCE_4")]
        ]
    )
    ],
    [
    gui.Image(size=(20, 20), key= "IMAGE_5"),
    gui.Column(
        [
            [gui.Text("Source:")],
            [gui.InputText(size=(10, 1), enable_events= True, key= "SOURCE_5")]
        ]
    )
    ]

]

#right column
name_column= [
    [
        gui.Column([[gui.Text("North:")],
        [gui.InputText("panorama_0.png", key= "NAME_0")]])
    ],
    [
        gui.Column([[gui.Text("East:")],
        [gui.InputText("panorama_1.png", key= "NAME_1")]])
    ],
    [
        gui.Column([[gui.Text("South:")],
        [gui.InputText("panorama_2.png", key= "NAME_2")]])
    ],
    [
        gui.Column([[gui.Text("West:")],
        [gui.InputText("panorama_3.png", key= "NAME_3")]])
    ],
    [
        gui.Column([[gui.Text("Up:")],
        [gui.InputText("panorama_4.png", key= "NAME_4")]])
    ],
    [
        gui.Column([[gui.Text("Down:")],
        [gui.InputText("panorama_5.png", key= "NAME_5")]])
    ]

]

#lower column
feet_column=[
    [
    gui.Text("Target File: "),
    gui.InputText(key= "TARGET_FILE", enable_events= True)
    ],
    [
    gui.Column([[gui.Button("Create Files", key= "CREATE")]]),
    gui.Column([[gui.Button("Cancel", key= "STOP")]])
    ]
]

#put everything together
layout= [
    #top column
    [
    gui.Column(top_column)
    ],
    [
        gui.Column(image_column),
        gui.VSeperator(),
        gui.Column(name_column)
    ],
    [
        gui.HSeperator()
    ],
    [
        gui.Column(feet_column)
    ]
]

# --define all Functions--

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def presskey(key):
    keyboard.press(key)
    keyboard.release(key)

def typekey(text):
    text = list(text)
    for x in text:
        presskey(x)

def takescreenshots():
    presskey("t")
    time.sleep(0.05)
    typekey("/execute align xyz run tp @s ~.5 ~.5 ~.5 0 0")
    presskey(Key.enter)
    time.sleep(0.05)
    presskey(Key.f2)
    presskey("t")
    time.sleep(0.05)
    typekey("/execute align xyz run tp @s ~.5 ~.5 ~.5 90 0")
    presskey(Key.enter)
    time.sleep(0.05)
    presskey(Key.f2)
    presskey("t")
    time.sleep(0.05)
    typekey("/execute align xyz run tp @s ~.5 ~.5 ~.5 180 0")
    presskey(Key.enter)
    time.sleep(0.05)
    presskey(Key.f2)
    presskey("t")
    time.sleep(0.05)
    typekey("/execute align xyz run tp @s ~.5 ~.5 ~.5 -90 0")
    presskey(Key.enter)
    time.sleep(0.05)
    presskey(Key.f2)
    presskey("t")
    time.sleep(0.05)
    typekey("/execute align xyz run tp @s ~.5 ~.5 ~.5 0 -90")
    presskey(Key.enter)
    time.sleep(0.05)
    presskey(Key.f2)
    presskey("t")
    time.sleep(0.05)
    typekey("/execute align xyz run tp @s ~.5 ~.5 ~.5 0 90")
    presskey(Key.enter)
    time.sleep(0.05)
    presskey(Key.f2)

#create the Window
window= gui.Window("Set Background Images", layout,size=(600, 600), icon=resource_path(icon_path))

# --Event Loop--
while True:
    x = 0
    event, values= window.read()

    #close gui
    if event == gui.WIN_CLOSED or event == "STOP":
        break

    #Image Import
    while x < 6:
        if event == f"SOURCE_{x}":
            source = values[f"SOURCE_{x}"]
            source = str(source.replace("file:///", ""))

            window[f"IMAGE_{x}"].update(filename=source)
            window[f"SOURCE_{x}"].update(source)
            imageFiles[x] = source

            #debug
            print(f"Updated {x} with {source}")
            print(f"Updated List!:")
            for x in range(len(imageFiles)):
                print(f"Image {x}: {imageFiles[x]}")
            print("")

            x = 0
            break

        x = x + 1
    #Insert target file
    if event == "TARGET_FILE":
        target = values["TARGET_FILE"]
        target = str(target.replace("file:///", ""))
        window["TARGET_FILE"].update(target)

    #Image Copying
    if event == "CREATE":
        x = 0
        if not target == "":
            while x < 6:
                source = imageFiles[x]
                source = str(source.replace("file:///", ""))
                targetname = values[f"NAME_{x}"]
                targetfile = f"{target}/{targetname}"
                shutil.copyfile(source, targetfile)
                x = x + 1
            print("Created Files!")
            window["CREATE"].update("Done!")

        else:
            print("please insert target Folder!")



    if event == "SHOW_HIDE_IMAGE":
        state = values["SHOW_HIDE_IMAGE"]
        x = 0
        while x < 6:
            window[f"IMAGE_{x}"].update(visible=state)
            x = x + 1

    if event == "SCREENSHOTS":
        time.sleep(6)
        takescreenshots()
    if event == "TUTORIAL_LINK":
        webbrowser.open(TutorialVideo)


window.close()
