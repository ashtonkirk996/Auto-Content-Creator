import assemblyai as aai
from moviepy.editor import *
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip
from pytube import YouTube
import customtkinter
import threading

#initialise some variables

videofile = 'default.mp4'





#function to create content from the video
def create_content():

  #function to resize clips
 def resize_clip(clip, target_height):
    width, height = clip.size
    target_width = int(width*target_height / height)
    return clip.resize((target_width,target_height))

  #load the two video clips which are to be combined
 clip1 = VideoFileClip('Videos/'+videofile).subclip(30,40)
 clip2 = VideoFileClip('Videos/GTA 5 NO COPYRIGHT GAMEPLAY for TikTok & YouTube _ FREE TO USE _ 4K 60FPS _ 371 (720p60) - Trim.mp4', audio=False).subclip(10,20)

#extract the audio from clip1
 clip1.audio.write_audiofile("combined_audio.wav")

# resize the clip1 to have the same width and maintain aspect ratio
 target_height = clip1.h/2
 clip1_resized = resize_clip(clip1, target_height)



#calculate height
 height = (int)(clip1_resized.w/9)*16
#calculate top and bottom gap
 gap = (height- (2*clip1_resized.h))/2 

# resize clip2
 clip2_resized = resize_clip(clip2, height-( gap + clip1_resized.h )+100)

#calculate the x position of clip2
 offset = (clip2_resized.w - clip1_resized.w)/2

# set the position of the clips
 clip1_position = (0, gap-100)
 clip2_position = (-offset, clip1_resized.h + gap -100)



#stack the clips vertically
 combined_clip = CompositeVideoClip([clip1_resized.set_position(clip1_position), clip2_resized.set_position(clip2_position)], size = (clip1_resized.w, height))

# thread for subtitle creation to prevent the ui from becoming unresponsive
 def subtitle_thread():
   #create the subtitles for the video
   aai.settings.api_key = "34a36dca14a2422793124482b209f654"

   transcript = aai.Transcriber().transcribe("combined_audio.wav")

   subtitles = transcript.export_subtitles_srt(chars_per_caption=25)
   subtitles = subtitles.strip()
   f= open('Auto-Content-Creator/subtitles.src', "w")
   f.write(subtitles)
   f.close()

 threading.Thread(target=subtitle_thread, daemon=True).start()

  #generate the subtitles to be shown on screen
 generator = lambda txt: TextClip(txt, font="Arial-Bold", fontsize=50, color = "white", method = 'caption', stroke_width=2, stroke_color='black', size=combined_clip.size)
 sub_clip = SubtitlesClip('Auto-Content-Creator/subtitles.src',generator)

 
  #combine the subtitles and the video
 final_clip = CompositeVideoClip((combined_clip, sub_clip), size = combined_clip.size)



 #thread for writing the clip without freezing the ui application
 def write_clip_thread():
  #write the final clip to a file
   final_clip.write_videofile("combined_video_final.mp4", codec='libx264', threads=4, preset='ultrafast', bitrate='5000k', fps=clip1.fps)
  #once complete display a message saying 'created sucessfully'
   sucess_message.place(x=256, y=250)

 threading.Thread(target=write_clip_thread, daemon=True).start()




#function to download youtube video
def downloadVideo():
  
  url = customtkinter.CTkEntry.get(videoURL)
  exit_dir = 'Videos'

  def download_thread():
    global videofile
    video = YouTube(url,on_progress_callback=on_progress)
    stream = video.streams.get_highest_resolution()
    videofile = stream.default_filename
    stream.download(output_path=exit_dir)

  threading.Thread(target=download_thread, daemon=True).start()

#function for the progress bar
def on_progress(stream, chunk, bytes_remaining ):
  total_size = stream.filesize
  bytes_download = total_size - bytes_remaining
  percentage_of_completion= bytes_download/total_size *100
  percent = str(int(percentage_of_completion))
  progress.configure(text=percent + "%")
  progress.update()
  
  #update progress bar
  progressbar.set(float(percentage_of_completion) )


#create and configure ui window
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("1024x768")
app.title("Content Generator")


#create widgets
videoURL = customtkinter.CTkEntry(
  master=app,
  placeholder_text='Enter video URL here',
  width = 512,
  height = 35
)
title = customtkinter.CTkLabel(master=app,text="Content Generator",width=256, height=40, font=customtkinter.CTkFont(size=40, weight="bold"))

sucess_message = customtkinter.CTkLabel(master=app,text="Created Sucessfully!",width=256, height=40, font=customtkinter.CTkFont(size=30))
#download progress percentage
progress = customtkinter.CTkLabel(app, text="0%")
progress.place(x=750,y=162)

#download progress bar
progressbar = customtkinter.CTkProgressBar(app, width=300)
progressbar.set(0)  
progressbar.place(x=600, y= 158)

download_button = customtkinter.CTkButton(master=app, command=downloadVideo, text='Download',text_color='white', hover=True, hover_color='black', height=35,width=120, border_width=2, corner_radius=4)
create_button =  customtkinter.CTkButton(master=app, command=create_content, text='Create Content',text_color='white', hover=True, hover_color='black', height=35,width=120, border_width=2, corner_radius=4)

#place widgets
videoURL.place(x=256, y=100)
title.place(x=256, y=20)
download_button.place(x=452, y=150)
create_button.place(x=452, y=200)





app.mainloop()