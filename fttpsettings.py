class Settings(object):
	#How often you want it to check for new things in the file.
	RTIME = 2
	#NOTE: For locations, you can use ~/ and $HOME if you'd like.
	#Log file for it to note down things it takes out of the queue when it's done downloading them..
	LOGFILE = '/home/blice/fttps/fttps.log'
	#Queue file.. This is where you paste in URLs for it to download.
	QUEUEFILE = '/home/blice/fttps/fttps.queue'
	#The location you want the downloaded files placed.
	DLOCATION = '~'
	#Check if a url has already been downloaded, and if so, don't download it again.. This is useful for if you want to keep a file open and keep adding to it, rather than add to the file, close it, open it again later, etc. since FTTPS will delete each thing out of the queue as it finishes them.
	NOREPEAT = 'False'


	#LOOK AND FEEL
	#Show the display or not. If you don't care to see the progress of files and just know they'll be downloaded eventually or want to run this script in the background, you should disable this.
	DISPLAY = 'True'
	#Show the progress bar.
	PROGBAR = 'True'
	#Show download rate. I.E, '339KB/s'
	PROGRATE = 'True'
	#Show how much of the file has transferred so far (Keep in mind there's also a percentage on the bar.) I.E, "70948/453145KB"
	SHOWPROG = 'False'
	#Show time elapsed.
	TIMESOFAR = 'False'
	#Show time remaining
	TIMESOLONG = 'True'
	#Size of the progress bar. When I implement ncurses this setting won't be here anymore..
	BARSIZE = 25
	#This is the character that's used to fill the bar.
	FILLING = '='
	#And this is the character at the very end of the bar that moves down..
	PROGPOINT = '>'
	#This is the closing brackets for the progress bar. Left and right.
	PROGLEFT = '['
	PROGRIGHT = ']'
	

