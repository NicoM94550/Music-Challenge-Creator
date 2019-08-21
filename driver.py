###############################################################################


from csv import reader
from os import listdir
from os import makedirs
from os import remove
from os import rmdir
from sys import exit

from moviepy.editor import concatenate_videoclips
from moviepy.editor import TextClip
from moviepy.editor import VideoFileClip
from moviepy.video.io import ffmpeg_tools
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from pytube import YouTube

import os.path


###############################################################################


def clip_videos(video_sets):
	clip_files = []
	for video_file, clip_start, clip_end in video_sets:
		clip_file = video_file.replace('temp/', 'temp/c_')
		ffmpeg_tools.ffmpeg_extract_subclip(
			video_file, clip_start, clip_end, targetname=clip_file)
		remove(video_file)
		clip_files.append(clip_file)
	return clip_file


def main():
	makedirs('blueprints', exist_ok=True)
	makedirs('challenges', exist_ok=True)
	makedirs('temp')
	nodes = listdir('blueprints')
	blueprint_names = [node for node in nodes if os.path.isfile(
		'blueprints/{0}'.format(node))]
	blueprint_name = input('Blueprint: ')
	while blueprint_name not in blueprint_names:
		blueprint_name = input('Please Enter a Valid Blueprint: ')
	blueprint_file = 'blueprints/{0}'.format(blueprint_name)
	video_sets = procure_videos(blueprint_file)
	clip_files = clip_videos(video_sets)
	merged_clips = merge_clips(clip_files)
	challenge_file = 'challenges/{0}.mp4'.format(blueprint_name)
	merged_clips.write_videofile(
		challenge_file, temp_audiofile='temp_audio.m4a',
        remove_temp=True, codec='libx264', audio_codec='aac')
	print('Generated Music Challenge: {0}'.format(blueprint_name))
	rmdir('temp')
	return 0


def merge_clips(clip_files):
	clip_titles = list(range(1, 1 + len(clip_files)))
	clip_titles[-1] = 'Bonus Clip'
	final_clips = []
	for clip_title, clip_file in zip(clip_titles, clip_files):
		title_clip = TextClip(clip_title).set_duration(5)
		title_clip = fadein(title_clip, 2)
		title_clip = fadeout(title_clip, 2)
		final_clips.append(title_clip)
		clip = VideoFileClip(clip_file)
		remove(clip)
		clip = fadein(clip, 2)
		clip = fadeout(clip, 2)
		final_clips.append(clip)
	merged_clips = concatenate_videoclips(final_clips)
	return merged_clips


def procure_videos(blueprint_file):
	video_sets = []
	with open(blueprint_file, 'r') as blueprint:
		blueprint_reader = reader(blueprint)
		for video_id, clip_start, clip_end in blueprint_reader:
			clip_start = int(clip_start)
			clip_end = int(clip_end)
			if ((clip_start < 0)
					or (clip_start >= clip_end)):
				print('Invalid Clip Times for Video {0}'.format(video_id))
				exit(1)
			video_name = '{0}.mp4'.format(video_id)
			video_file = 'temp/{0}'.format(video_name)
			try:
				if not os.path.isfile(video_file):
					youtube_url = 'https://www.youtube.com/watch?v={0}'
					video_url = youtube_url.format(video_id)
					video = YouTube(url=video_url)
			except:
				print('Invalid Video ID: {0}'.format(video_id))
				exit(1)
			if clip_end > int(video.length):
				print('Invalid Clip Times for Video {0}'.format(video_id))
				exit(1)
			video_stream = video.streams.filter(
				progressive=True, file_extension='mp4').order_by(
				'resolution').desc().first()
			video_file = video_stream.download(output_path='temp')
			video_sets.append([video_file, clip_start, clip_end])
	return video_sets


###############################################################################


if __name__ == '__main__':
	main()


###############################################################################
