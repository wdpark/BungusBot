from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array
import glob, os

def concat_files(dir):
    files = []
    for file in glob.glob(dir + "highlight*.mp4"):
        files.append(file)

    chats = []
    for file in glob.glob(dir + "chat*.mp4"):
        chats.append(file)

    clips = []
    for i in range(0,len(files)):
        file = files[i]
        chat = chats[i]
        highlightVid = VideoFileClip(file).resize(width=980).subclip(40,60)
        chatVid = VideoFileClip(chat).resize(width=300).subclip(40,60)

        highlightVid = highlightVid.set_fps(24)
        chatVid = chatVid.set_fps(24)

        clip = clips_array([[highlightVid, chatVid]])
        clip = clip.set_audio(highlightVid.audio)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("hello.mp4")

concat_files('')
