from tkinter import filedialog
from tkinter.ttk import *
from tkinter import *
import cv2
import os
import time
file_path = ""
clicked = ""
progress = ""
l1 = ""

# Remove a widget from the grid
def remove(obj):
    obj.grid_remove()

# Receives video input from user
def selectVideo():
    global file_path
    file_path = filedialog.askopenfilename(initialdir="C:\\",
                                           title="Select input-file",
                                           filetypes=(("input-file", "*.mkv *.mov *.mp4 *.avi *.wmv"),
                                                      ("all files", "*.*")))
    video = cv2.VideoCapture(file_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    print("\nSelected Video: \t" + file_path + " [FPS: " + str(fps) + ", Rounded FPS: " + str(round(fps)) + "]")

# Converts video to timelapse
def convertVideoToImages():
    global file_path, l1, clicked, progress
    if file_path == "":
        l1 = Label(text="Pending", width=20)
        l1.grid(row=3,column=1)
    #remove(l1)
    l1 = Label(text="Extracting Frames", width=20)
    l1.grid(row=3, column=1)
    video = cv2.VideoCapture(file_path)
    rounded_fps = round(video.get(cv2.CAP_PROP_FPS));
    number_of_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Path data
    local_date = time.strftime("%d-%m-%Y")
    local_time = time.strftime("%H-%M-%S")
    frame_path = os.getcwd() + "/frames/" + local_date + "_" + local_time + "_Selected-Frames"
    video_path = os.getcwd() + '/video/' + local_date + "_" + local_time + ".mkv"
    if not os.path.exists(frame_path): os.makedirs(frame_path)
    if not os.path.exists('video'): os.makedirs('video')

    frame_frequency = clicked.get();
    frame_freq = ""
    if frame_frequency == "3 Per Second":
        frame_freq = 3
    if frame_frequency == "2 Per Second":
        frame_freq = 2
    if frame_frequency == "1 Per Second":
        frame_freq = 1
    if frame_frequency == "1 Per 5 Seconds":
        frame_freq = 0.2

    print("Extracting Frequency: \t" + frame_frequency + " [Timelapse FPS: " + str(frame_freq) + "]")
    frame_select_rate = rounded_fps / frame_freq;
    print("Selecting one frame per " + str(frame_select_rate))

    # Extract frames from video
    success, image = video.read()
    i = 0
    frame_count = 0
    while success:
        success, image = video.read()
        if success:
            if i % frame_select_rate == 0:
                cv2.imwrite(frame_path + "/" + "a%d.jpg" % frame_count, image)
                frame_count += 1
                progress['value'] = int((i / number_of_frames) * 100)
                progress.update_idletasks()
            if cv2.waitKey(10) == 27:
                break
            i += 1

    # Assemble frames into timelapse
    images = [img for img in os.listdir(frame_path) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(frame_path, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_path, 0, 24, (width, height))

    for i in range(len(images)):
        video.write(cv2.imread(os.path.join(frame_path, 'a' + str(i) + '.jpg')))

    cv2.destroyAllWindows()
    video.release()
    Label(text="All done!", width=20).grid(row=6,column=0)

# Assemble UI
def assemble_UI():
    global l1, clicked, progress
    root = Tk()
    root.title('Video2Timelapse')
    root.geometry("450x300")
    Label(text="Video:", width=20).grid(row=0,column=0)
    Button(text="Select", command=selectVideo, width=10).grid(row=0, column=1)
    Label(text="Frames Frequency", width=20).grid(row=1,column=0)
    options = [
        "3 Per Second",
        "2 Per Second",
        "1 Per Second",
        "1 Per 5 Seconds"
    ]
    clicked = StringVar()
    clicked.set("2 Per Second") #default
    drop = OptionMenu(root, clicked, *options).grid(row=1,column=1)
    update_label_on_grid("Current Status", 20, 3, 0)
    update_label_on_grid("Pending", 20, 3, 1)
    update_label_on_grid("Progress", 20, 4, 0)
    progress = Progressbar(orient=HORIZONTAL, length=130, mode='determinate')
    progress.grid(row=4, column=1)
    Button(text="Start", command=convertVideoToImages, width=10).grid(row=5, column=0, pady=30)

def update_label_on_grid(label_text, width, row, col):
    g = Label(text=label_text, width=width)
    g.grid(row=row, column=col)

assemble_UI()
mainloop()

