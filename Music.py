#PLEASE RUN WITH PYTHON 3.5 OR ABOVE 

from pytube import YouTube
import os

Count = 0
DATA = [[x.split("@@@")[0],x.split("@@@")[1].split(":")] for x in input("...[").split("###")]
for x in DATA:
	print (x[0],"///", x[1])
for i,x in enumerate(DATA):
	toDownload = YouTube(x[0])
	toDownload.streams.filter(progressive = True, file_extension = 'mp4').order_by('resolution').desc().first().download()
	os.system("mv *.mp4 Video%s.mp4" % str(i + 1))
	minutes_start, seconds_start = divmod(int(x[1][0]), 60)
	hours_start, minutes_start = divmod(minutes_start, 60)
	minutes_end, seconds_end = divmod((int(x[1][1]) - int(x[1][0])), 60)
	hours_end, minutes_end = divmod(minutes_end, 60)
	hours_start, minutes_start, seconds_start, hours_end, minutes_end, seconds_end = str(hours_start), str(minutes_start), str(seconds_start), str(hours_end), str(minutes_end), str(seconds_end)
	if len(hours_start) != 2:
		hours_start = '0' + hours_start
	if len(minutes_start) != 2:
		minutes_start = '0' + minutes_start
	if len(seconds_start) != 2:
		seconds_start = '0' + seconds_start
	if len(hours_end) != 2:
		hours_end = '0' + hours_end
	if len(minutes_end) != 2:
		minutes_end = '0' + minutes_end
	if len(seconds_end) != 2:
		seconds_end = '0' + seconds_end
	start_time = "%02s:%02s:%02s"%(hours_start, minutes_start, seconds_start)
	duration = "%02s:%02s:%02s"%(hours_end, minutes_end, seconds_end)
	os.system("ffmpeg -y -ss %s -i Video%s.mp4 -c copy -t %s -avoid_negative_ts make_zero -fflags +genpts Video%s_C.mp4"%(start_time, str(i + 1), duration, str(i + 1)))
	os.system("mv *_C.mp4 Clipped/")
	os.system("rm -rf *.mp4")
	Count += 1
