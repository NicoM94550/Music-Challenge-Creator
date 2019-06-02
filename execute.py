import pytube
import moviepy
import sys
import csv

def validate_clip_times(video_id, clip_start, clip_end):
    video_url = 'https://www.youtube.com/watch?v={0}'.format(video_id)
    video = pytube.YouTube(url=video_url)
    if (clip_start < 0)\
        or (clip_start >= clip_end)\
        or (clip_end > int(video.length)):
            print('Range ({0}, {1}) invalid for target ({2}).'.format(
                video_id, clip_start, clip_end))
            sys.exit(1)
    print('Range for target ({0}) validated.'.format(video_id))
    return video

def get_video(video, filename_):
    video_stream = video.streams.filter(
            progressive=True, file_extension='mp4').order_by(
                    'resolution').desc().first()
    video_file = video_stream.download(
            output_path='temp', filename=filename_)
    return video_file

def main(target):
    target_list = []
    try:
        with open(target) as target_file:
            target_reader = csv.reader(target_file)
            for (video_id, clip_start, clip_end) in target_reader:
                print('Found target ({0}).'.format(video_id))
                target = [video_id, int(clip_start), int(clip_end)]
                target_list.append(target)
        print('Targets loaded.')
    except FileNotFoundError:
        print('Blueprint ({0}) not found.'
                .format(target))
    videos = []
    for (video_id, clip_start, clip_end) in target_list:
        print('Validating range for target ({0})'.format(video_id))
        video = validate_clip_times(video_id, clip_start, clip_end)
        videos.append(video)
    print('Ranges validated.')

if (__name__ == '__main__'):
    target_name = input('Blueprint: ')
    target = 'blueprints/{0}'.format(target_name)
    main(target)
