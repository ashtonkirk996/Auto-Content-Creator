import assemblyai as aai
from moviepy.editor import *
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip

#function to resize clips
def resize_clip(clip, target_height):
    width, height = clip.size
    target_width = int(width*target_height / height)
    return clip.resize((target_width,target_height))

#load the two video clips which are to be combined
clip1 = VideoFileClip('Videos/YourRage reacts to xQc reacting to him Pulling Gun out for Intruder (720p60).mp4').subclip(10,25)
clip2 = VideoFileClip('Videos/GTA 5 NO COPYRIGHT GAMEPLAY for TikTok & YouTube _ FREE TO USE _ 4K 60FPS _ 371 (720p60) - Trim.mp4', audio=False).subclip(10,25)

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

#create the subtitles for the video
aai.settings.api_key = "34a36dca14a2422793124482b209f654"

transcript = aai.Transcriber().transcribe("combined_audio.wav")

subtitles = transcript.export_subtitles_srt(chars_per_caption=25)
subtitles = subtitles.strip()
f= open('Auto-Content-Creator/subtitles.src', "w")
f.write(subtitles)
f.close()

#generate the subtitles to be shown on screen
generator = lambda txt: TextClip(txt, font="Arial-Bold", fontsize=50, color = "white", method = 'caption', stroke_width=25, size=combined_clip.size)
sub_clip = SubtitlesClip('Auto-Content-Creator/subtitles.src',generator)




#combine the subtitles and the video
final_clip = CompositeVideoClip((combined_clip, sub_clip), size = combined_clip.size)


#write the final clip to a file
final_clip.write_videofile("combined_video_final.mp4", codec='libx264', threads=4, preset='ultrafast', bitrate='5000k', fps=clip1.fps)