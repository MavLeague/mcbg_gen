from pynput.keyboard import Key, Controller
import PIL.Image
import io
import base64
import PySimpleGUI as gui
import shutil
import time
import webbrowser
import os


# --define Values--
target = ""
keyboard = Controller()
InfoText = "01. Set the Resolution of your Instance to a 1:1 Ratio (e.g. 512x512 or 1024x1024). \n02. Make sure your Instance is in Window Mode! \n03. Set your FOV to 82. \n04. Remove all Effects that influence the view! (e.g. Speed, Nausea, Slowness, etc.) \n05. (Open your World and) Go to a suitable place. This will be the Center of your Background! \n06. Press F1 to hide the Gui! (e.g. Hotbar) \n07. Press the \"Take Screenshots\"-Button and wait 7 Seconds! \n08. Open your Screenshots-Folder. Then Drag and Drop the taken Screenshots in order in the \"Source\"-Inputs so the Path appears in it. \n09. Choose the Background Folder in your Resourcepack and Drag and Drop it in the \"Target File\"-Input so the Path appears in it. \n10. Click \"Create Files\" and the files should appear in the chosen Folder."
TutorialVideo = "http://example.com"
tutorial_visibility = False

Font = "Segoe UI"
Font_size = 10
icon_path = "assets/icon.ico"

image_count = 6
image_visibility = False
image_size = (120, 120)
image_files = []

screenshot_delay = 0.5
commandlist = [
   "/execute align xyz run tp @s ~.5 ~.5 ~.5 0 0",
    "/execute align xyz run tp @s ~.5 ~.5 ~.5 90 0",
    "/execute align xyz run tp @s ~.5 ~.5 ~.5 180 0",
    "/execute align xyz run tp @s ~.5 ~.5 ~.5 -90 0",
    "/execute align xyz run tp @s ~.5 ~.5 ~.5 0 -90",
    "/execute align xyz run tp @s ~.5 ~.5 ~.5 0 90"
]

menu_image = ("&Images  ✓::SHOW_HIDE_IMAGE", "&Images::SHOW_HIDE_IMAGE")

x = image_count
while x > 0:
    image_files.append("Empty")
    x = x - 1


# --set GUI--
gui.ChangeLookAndFeel('Default')


# --define all Functions--
def menukey(string):
    # removes everything till the '::' of a string
    if "::" in string:
        string = string[string.find("::") + 2:]
    return string

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
        
def average(l):
    count = 0

    for x in l:
        count = count + x
        return count
    
    result = count/len(l)
    return result

def addtolist(x, list, imagekey, sourcekey):
    
    x = x - 1
    # create for every x a new image element
    while x >= 0:
        input = [
            gui.Image(size=image_size, visible= image_visibility, key= f"{imagekey}_{x}"),
            gui.Column(
                [
                    [gui.Text("Source:")],
                    [gui.InputText(enable_events= True, size= (15 , None),key= f"{sourcekey}_{x}"), 
                     gui.FileBrowse(enable_events= True, file_types= (("PNG-Images", "*.png"),))]
                ])]
        list.insert(0, input)
        x = x - 1



def takescreenshots(list, delay = 0.05):
    
    for command in list:
        time.sleep(delay)
        presskey("t")
        time.sleep(delay)
        typekey(command)
        presskey(Key.enter)
        time.sleep(delay)
        presskey(Key.f2)
        
        
def convert_to_list(string, seperator= ";"):
    print("")
    result = []
    for x in range(string.count(seperator)):
        sepos = string.find(seperator)
        result.append(string[0:sepos])
        string = string[sepos + len(seperator):]
        
    result.append(string)
    return result


def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()
    #source: https://www.pysimplegui.org/en/latest/cookbook/#recipe-convert_to_bytes-function-pil-image-viewer

#menu bar
menu_def= [
    ["&File", ["&Import Image::IMPORT_IMAGES"]],
    ["&Edit", ["!&Settings"]],
    ["&View", ["&Tutorial::SHOW_HIDE_TUTORIAL", menu_image[1]]]
]


#top column
tutorial_column= [
    [gui.Text("Tutorial:", font= (Font, 15, "bold"))],
    [gui.Text(InfoText, font= (Font, Font_size))],
    [gui.Text("Need Help? Here is a Tutorial Video!", text_color="#0000EE", font= (Font, Font_size, "underline"), tooltip = f"Open: {TutorialVideo}", enable_events= True, key= "TUTORIAL_LINK")]
]

#left column
image_column= [
#    [gui.Checkbox("show Images", key="SHOW_HIDE_IMAGE", default= image_visibility, enable_events= True)],
    [gui.FilesBrowse(key= "IMPORT_IMAGES",enable_events= True, file_types=(("PNG-Images", "*.png"),))]
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
        gui.Column([[gui.Button("Cancel", key= "STOP")]]),

        gui.Button("Take Screenshots (6s delay)", key="SCREENSHOTS", pad = (25, None)),
        gui.Column([[
            gui.Text("Starting in: -", key="TIMER", visible=False, size=(150, 30))
        ]])
    ]
]

#put everything together

addtolist(image_count, image_column, "IMAGE", "SOURCE")

layout= [
    [gui.Menu(menu_def, key= "MENUBAR"),
     gui.Column([        
        #[gui.Column(tutorial_column, key= "TOP_COLUMN", visible=tutorial_visibility)],
        [
            gui.Column(image_column),
            gui.VSeperator(),
            gui.Column(name_column)
        ],
        [
            gui.HSeparator()
        ],
        [
            gui.Column(feet_column)
        ]
    ], key= "MAIN_COLUMN")
    ]
]

#create the Window
main_window= gui.Window(
    "Set Background Images", 
    layout, 
    icon=resource_path(icon_path), 
    element_justification='c'
)

# --Event Loop--
while True:
    x = 0
    main_event, main_values= main_window.read()

    print(main_event)

    #close gui
    if main_event == gui.WIN_CLOSED or main_event == "STOP":
        break

    #Image Import
    while x < image_count:
        if main_event == f"SOURCE_{x}":
            source = main_values[f"SOURCE_{x}"]

            # update if path is valid
            if os.path.exists(source):
                bite_source = convert_to_bytes(source, image_size)
                main_window[f"IMAGE_{x}"].update(bite_source, size= image_size)
                main_window[f"SOURCE_{x}"].update(source)
                image_files[x] = source
                
                #debug
                print(f"Updated {x} with {source}")
                print(f"Updated List!:")
                for x in range(len(image_files)):
                    print(f"Image {x}: {image_files[x]}")
                print("")
                main_window[f"SOURCE_{x}"].update(text_color= "#000000")
                
            else:
                # lock typing
                if not image_files[x] == "Empty":
                    main_window[f"SOURCE_{x}"].update(image_files[x])
                elif image_files[x] == "Empty":
                    main_window[f"SOURCE_{x}"].update("")
                
                main_window[f"SOURCE_{x}"].update(text_color= "#660000")

            x = 0
            break

        x = x + 1
    #Insert target file
    if main_event == "TARGET_FILE":
        target = main_values["TARGET_FILE"]
        target = str(target.replace("file:///", ""))
        main_window["TARGET_FILE"].update(target)

    #Image Copying
    if main_event == "CREATE":
        x = 0
        if not target == "":
            while x < image_count:
                source = image_files[x]
                source = str(source.replace("file:///", ""))
                targetname = main_values[f"NAME_{x}"]
                targetfile = f"{target}/{targetname}"
                shutil.copyfile(source, targetfile)
                x = x + 1
            print("Created Files!")
            main_window["CREATE"].update("Done!")

        else:
            print("please insert target Folder!")

    
    if menukey(main_event) == "IMPORT_IMAGES":
        print("Values:", main_values["IMPORT_IMAGES"])
        
                
        list_return = convert_to_list(main_values["IMPORT_IMAGES"])
        if len(list_return) <= image_count:
            
            x = 0
            for x in range(len(list_return)):
                image_files[x] = list_return[x]
                
                
            
            x = 0
            print(f"Updated List!:")
            for x in range(len(image_files)):
                print(f"Image {x}: {image_files[x]}")
            print("")


    if menukey(main_event) == "SHOW_HIDE_IMAGE":
        state = not image_visibility
        x = 0
        print("Images", state)
        while x < image_count:
            main_window[f"IMAGE_{x}"].update(visible= state, size= image_size)
            x = x + 1
        
        if state:
            main_window[1].update(menu_image[0])
        elif not state:
            main_window[1].update(menu_image[1])
        
        
        image_visibility = state

    if not tutorial_visibility and menukey(main_event) == "SHOW_HIDE_TUTORIAL":
        tutorial_visibility = True
        # show Tutorial window
        Tutorial = gui.Window("Tutorial", tutorial_column)
        
        #state = not tutorial_visibility
        #main_window["TOP_COLUMN"].update(visible= state)
        
        #if state:
        #    main_window[1].update(menu_image[0])
        #elif not state:
        #    main_window[1].update(menu_image[1])
        #tutorial_visibility = state

    # events for Tutorial Window 
    if tutorial_visibility:
        tutorial_event, tutorial_values = Tutorial.read()
        if tutorial_event == gui.WIN_CLOSED or tutorial_event == 'Exit':
            tutorial_visibility  = False
            print("Visibility set to", tutorial_visibility)
            Tutorial.close() 

    if main_event == "SCREENSHOTS":
        time.sleep(6)
        takescreenshots(commandlist, screenshot_delay)
    if main_event == "TUTORIAL_LINK":
        webbrowser.open(TutorialVideo)


main_window.close()
