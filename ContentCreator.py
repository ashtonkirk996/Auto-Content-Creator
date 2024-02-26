from moviepy.editor import *
from moviepy.editor import VideoFileClip, concatenate_videoclips

#function to resize clips
def resize_clip(clip, target_height):
    width, height = clip.size
    target_width = int(width*target_height / height)
    return clip.resize((target_width,target_height))

#load the two video clips which are to be combined
clip1 = VideoFileClip('Videos/YourRage reacts to xQc reacting to him Pulling Gun out for Intruder (720p60).mp4').subclip(5,65)
clip2 = VideoFileClip('Videos/GTA 5 NO COPYRIGHT GAMEPLAY for TikTok & YouTube _ FREE TO USE _ 4K 60FPS _ 371 (720p60) - Trim.mp4', audio=False).subclip(5,65)


# resize the clip1 to have the same width and maintain aspect ratio
target_height = clip1.h/2
clip1_resized = resize_clip(clip1, target_height)



#calculate height
height = (int)(clip1_resized.w/9)*16
#calculate top and bottom gap
gap = (height- (2*clip1_resized.h))/2

# resize clip2
clip2_resized = resize_clip(clip2, height-( gap + clip1_resized.h))

#calculate the x position of clip2
offset = (clip2_resized.w - clip1_resized.w)/2

# set the position of the clips
clip1_position = (0, gap)
clip2_position = (-offset, clip1_resized.h + gap)



#stack the clips vertically
final_clip = CompositeVideoClip([clip1_resized.set_position(clip1_position), clip2_resized.set_position(clip2_position)], size = (clip1_resized.w, height))

#write the final clip to a file
final_clip.write_videofile("combined_video.mp4", codec='libx264', threads=4, preset='ultrafast', bitrate='5000k', fps=clip1.fps)