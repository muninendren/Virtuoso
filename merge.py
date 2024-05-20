from moviepy.editor import VideoFileClip, AudioFileClip


def merge():
        
    # File paths
    video_path = "D:\projectfinal\Flaskproject\output.mp4"
    audio_path = "D:\projectfinal\Flaskproject\output.mp3"
    output_path = "D:\projectfinal\Flaskproject\static\\videos\outputt.mp4"

    # Load video and audio clips
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)



    video_clip=video_clip.set_duration(audio_clip.duration)
    # Set audio clip duration to match video duration
    # audio_clip = audio_clip.set_duration(video_clip.duration)

    # Merge video and audio
    final_clip = video_clip.set_audio(audio_clip)



    # Write final merged clip to file
    final_clip.write_videofile(output_path)
