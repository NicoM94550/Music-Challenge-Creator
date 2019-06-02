import pytube
import moviepy
import sys
import csv
import os

def validate_clip_times(video_id, clip_start, clip_end):
    try:
        video_url = 'https://www.youtube.com/watch?v={0}'.format(video_id)
        video = pytube.YouTube(url=video_url)
    except:
        print('Could not validate range for target ({0}).'.format(video_id))
        return []
    if (clip_start < 0)\
        or (clip_start >= clip_end)\
        or (clip_end > int(video.length)):
            print('Range ({0}, {1}) invalid for target ({2}).'.format(
                video_id, clip_start, clip_end))
            return []
    print('Range for target ({0}) validated.'.format(video_id))
    return [(video, video_id)]

def get_video(video, filename_):
    print('Getting target ({0}).'.format(filename_))
    try:
        video_stream = video.streams.filter(
                progressive=True, file_extension='mp4').order_by(
                        'resolution').desc().first()
        video_file = video_stream.download(
                output_path='temp', filename=filename_)
    except:
        print('Could not get target ({0}).'.format(filename_))
    return None

def main(target):
    target_list = []
    try:
        with open(target) as target_file:
            target_reader = csv.reader(target_file)
            for (video_id, clip_start, clip_end) in target_reader:
                print('Found target ({0}).'.format(video_id))
                target_ = [video_id, int(clip_start), int(clip_end)]
                target_list.append(target_)
        print('Targets loaded.')
    except FileNotFoundError:
        print('Blueprint ({0}) not found.'
                .format(target))
        sys.exit(1)
    videos = []
    for (video_id, clip_start, clip_end) in target_list:
        if ('{0}.mp4'.format(video_id) in os.listdir('temp')):
            print('Target ({0}) loaded from temp.'.format(video_id))
        else:    
            print('Validating range for target ({0})'.format(video_id))
            video = validate_clip_times(video_id, clip_start, clip_end)
            videos.extend(video)
    print('Ranges validated.')
    print('Getting targets.')
    for (video, filename) in videos:
        get_video(video, filename)
    print('Got targets.')
    for target_ in target_list:
        video_file = '{0}.mp4'.format(*target_)
        if (video_file not in os.listdir('temp')):
            return main(target)
    return 0

if (__name__ == '__main__'):
    if not os.path.exists('blueprints'):
        os.mkdir('blueprints')
    if not os.path.exists('temp'):
        os.mkdir('temp')
    target_name = input('Blueprint: ')
    target = 'blueprints/{0}'.format(target_name)
    main(target)
