from pytube import YouTube
from pytube.cli import on_progress 
from  tkinter import *
from tkinter import filedialog
import os.path
import ffmpeg

#getting the user input 
url = input("Enter the url of the video\t :")

#creating the object
yt = YouTube(url,on_progress_callback=on_progress)

#filtering available streams
fps = [24,25,30,60]                         #available fps 
quality = ["360p","480p","720p","1080p"]    #available qualities

#finding the streams available
options = []
for i in range(4):
    for j in range(4):
        videos = yt.streams.filter(adaptive=True,only_video=True,fps=fps[i],file_extension="mp4",res=quality[j])
        if len(videos)>0:
            option = quality[j]+" "+str(fps[i])+"fps"
            options.append(option)

for option in options:
    print(option)

#getting the video quality and the fps from the user
print()
download_quality = input("Enter the quality\t:")
download_fps = int(input("Enter the fps\t\t:"))

#filter available streams according to the user input
video = yt.streams.filter(adaptive=True,only_video=True,fps=download_fps,file_extension="mp4",res=download_quality).first()
print(video)
video_file_name = video.default_filename

#getting the directory to save the file 
root = Tk()
root.withdraw()
root.directory = filedialog.askdirectory()

#downloading the video
video.download(output_path=root.directory,filename="video")

#downloading the highest quality audio file 
audio = yt.streams.get_audio_only()
audio_file_name = audio.default_filename
audio_file_extension = os.path.splitext(audio_file_name)[1]
audio.download(output_path=root.directory,filename="audio")

#adding audio to the video
video_stream = ffmpeg.input(root.directory+'/video.mp4')
audio_stream = ffmpeg.input(root.directory+'/audio'+audio_file_extension)
ffmpeg.output(audio_stream, video_stream, root.directory+'/'+video_file_name ,vcodec="copy").run()

#deleting the video and audio file after encoding
os.remove(root.directory+'/video.mp4')
os.remove(root.directory+'/audio'+audio_file_extension)

root.destroy()
root.mainloop()

