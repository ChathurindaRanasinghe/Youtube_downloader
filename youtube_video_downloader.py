from pytube import YouTube
from pytube.cli import on_progress #use tdqm for progress bar
from  tkinter import *
from tkinter import filedialog
import os.path

import ffmpeg



yt = YouTube('https://www.youtube.com/watch?v=FLrWfrFIMMU',on_progress_callback=on_progress)



#filtering fps and qualities
fps = [24,25,30,60]
quality = ["360p","480p","720p","1080p"]
options = []

for i in range(4):
    for j in range(4):
        videos = yt.streams.filter(adaptive=True,only_video=True,fps=fps[i],file_extension="mp4",res=quality[j])
        if len(videos)>0:
            option = quality[j]+" "+str(fps[i])+"fps"
            options.append(option)

for option in options:
    print(option)

print()
download_quality = input("Enter the quality\t:")
download_fps = int(input("Enter the fps\t\t:"))

video = yt.streams.filter(adaptive=True,only_video=True,fps=download_fps,file_extension="mp4",res=download_quality).first()
print(video)

video_file_name = video.default_filename

root = Tk()
root.withdraw()
root.directory = filedialog.askdirectory()



video.download(output_path=root.directory,filename="video")

#audio file 
audio = yt.streams.get_audio_only()
audio_file_name = audio.default_filename
audio_file_extension = os.path.splitext(audio_file_name)[1]
audio.download(output_path=root.directory,filename="audio")


#encoding adaptive videos

video_stream = ffmpeg.input(root.directory+'/video.mp4')
audio_stream = ffmpeg.input(root.directory+'/audio'+audio_file_extension)
ffmpeg.output(audio_stream, video_stream, root.directory+'/'+video_file_name ,vcodec="copy").run()

print("done")
root.destroy()
root.mainloop()

