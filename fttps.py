import os, sys, urllib, time, datetime, curses, traceback, threading
from fttpsettings import Settings

#Thrown together for K.Mandla. http://kmandla.wordpress.com/2008/12/16/i-wish-i-had/

#This progress bar class was prewritten by someone else. I forget where I grabbed it- It was in a blog, and then people in the comments were improving it etc... All I did was incorporate it with a hook on urllib and put it in curses. That and make it so it grabs the settings for the filler and other stuff, you know.
class progressBar:
    """ Creates a text-based progress bar. Call the object with the `print'
        command to see the progress bar, which looks something like this:

        [=======>        22%                  ]

        You may specify the progress bar's width, min and max values on init.
    """

    def __init__(self, minValue = 0, maxValue = 100, totalWidth=80):
        self.progBar = "[]"   # This holds the progress bar string
        self.min = minValue
        self.max = maxValue
        self.span = maxValue - minValue
        self.width = totalWidth
        self.amount = 0       # When amount == max, we are 100% done
        self.updateAmount(0)  # Build progress bar string

    def updateAmount(self, newAmount = 0):
        """ Update the progress bar with the new amount (with min and max
            values set at initialization; if it is over or under, it takes the
            min or max value as a default. """
        if newAmount < self.min: newAmount = self.min
        if newAmount > self.max: newAmount = self.max
        self.amount = newAmount

        # Figure out the new percent done, round to an integer
        diffFromMin = float(self.amount - self.min)
	if float(self.span) != 0.0:
        	percentDone = (diffFromMin / float(self.span)) * 100.0
        	percentDone = int(round(percentDone))
	else: 
	        percentDone = (diffFromMin / 100.0) * 100.0
        	percentDone = int(round(percentDone))

        # Figure out how many hash bars the percentage should be
        allFull = self.width - 2
        numHashes = (percentDone / 100.0) * allFull
        numHashes = int(round(numHashes))

        # Build a progress bar with an arrow of equal signs; special cases for
        # empty and full
        if numHashes == 0:
            self.progBar = Settings.PROGLEFT + Settings.PROGPOINT + (' '*(allFull-1)) + Settings.PROGRIGHT
        elif numHashes == allFull:
            self.progBar = Settings.PROGLEFT + (str(Settings.FILLING)*allFull) + Settings.PROGRIGHT
        else:
            self.progBar = Settings.PROGLEFT + (str(Settings.FILLING)*(numHashes-1) + Settings.PROGPOINT + (' '*(allFull-numHashes))) + Settings.PROGRIGHT

        # figure out where to put the percentage, roughly centered
        percentPlace = (len(self.progBar) / 2) - len(str(percentDone))
        percentString = str(percentDone) + "%"

        # slice the percentage into the bar
        self.progBar = ''.join([self.progBar[0:percentPlace], percentString,
                                self.progBar[percentPlace+len(percentString):]
                                ])

    def __str__(self):
        return str(self.progBar)

    def __call__(self, value):
        """ Updates the amount, and writes to stdout. Prints a carriage return
            first, so it will overwrite the current line in stdout."""
        self.updateAmount(value)
        sys.stdout.write(str(self))

def seconds_to_dhms(secs):
    minutes, secs = divmod(secs, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return days,hours,minutes,secs

#WARNING: SLOPPY AMATURE CODE. I'M SORRY :[		

class Download(threading.Thread):
	def __init__(self, url):
		self.setName = url
		self.url = url
		threading.Thread.__init__(self)

	def run(self):
		global hookprog
		filename = self.url.split('/')[len(self.url.split('/')) - 1].replace('\r', '').replace('\n', '') + ' '
		start_time = ''
		def lolhook(bc, bs, fs):
			global screen
			global stdscr
			if self.url in hookprog:
				rate = ''
				x = time.localtime()
				current_time = datetime.datetime(int(time.strftime('%Y', x)), int(time.strftime('%m', x)), int(time.strftime('%d', x)), int(time.strftime('%H', x)), int(time.strftime('%M', x)), int(time.strftime('%S', x)))
				diff_time = current_time - start_time
			
				progress = str(bc*bs/1024) + '/' + str(fs/1024) + 'K '
				if bc*bs >= fs:
					progress = 'Complete\n'
				

				hookprog[self.url][1].updateAmount(bc*bs)
				rate = bc*bs
				if diff_time.seconds != 0:
					rate = rate/diff_time.seconds
				h = seconds_to_dhms(diff_time.seconds)
				remaining = ''
				try:
					left = (fs - (bc*bs))/rate
					left = seconds_to_dhms(left)
					remaining = str(left[0]) + ':' + str(left[1]) + ':' + str(left[2]) + ':' + str(left[3]) + 'R '
				except:
					remaining = ''
	
				
				elapsed = str(h[0]) + ':' + str(h[1]) + ':' + str(h[2]) + ':' + str(h[3]) + 'E '
				rate = str(rate/1024) + 'K/s '
				select = '[ ] '
				#I'm sure setting things and THEN checking if they exist or not and setting them to blank isn't the best way to go about things. I'm tired and not thinking, so this is the best way to do it in my mind right now. 
				if Settings.TIMESOFAR != 'True':
					elapsed = ''

				if Settings.TIMESOLONG != 'True' or progress == 'Complete\n':
					remaining = ''
			
				if Settings.SHOWPROG != 'True':
					progress = ''

				if Settings.PROGRATE != 'True':
					rate = ''
				if current_string == hookprog[self.url][0]:
					select = '[x] '
				bar = str(hookprog[self.url][1]) + ' '
				if Settings.PROGBAR != 'True':
					bar = ''

				hookprog[self.url][2] = select + filename + bar + rate + elapsed + remaining + progress
				screen.addstr(hookprog[self.url][0], 0, hookprog[self.url][2])
				screen.refresh()
				#This is for pausing/resuming. I think there's a better way to do this though, because when I asked what the best way to pause/resume a thread is the guys in #Python laughed at me and said if I didn't know then I shouldn't use threads. I dunno? :/
				if hookprog[self.url][3] == 1:
					while hookprog[self.url][3] == 1:
						time.sleep(1)
				#This is if the person has pressed "q".. Exits
				if hookprog[self.url][4] ==1:
					sys.exit()

	
			else:
				hookprog[self.url] = [len(hookprog), progressBar(0, fs, Settings.BARSIZE), '', 0, 0]
			


		if Settings.DISPLAY == 'True':
			x = time.localtime()
			start_time = datetime.datetime(int(time.strftime('%Y', x)), int(time.strftime('%m', x)), int(time.strftime('%d', x)), int(time.strftime('%H', x)), int(time.strftime('%M', x)), int(time.strftime('%S', x)))
			urllib.urlretrieve(self.url, Settings.DLOCATION + filename, reporthook=lolhook)
		else:
			urllib.urlretrieve(self.url, Settings.DLOCATION + filename)


class ReadQueue(threading.Thread):
	def __init__(self):
		self.setName = 'Getchin'
		threading.Thread.__init__(self)

	def run(self):
		global hookprog
		global quitt
		while 1:
			if quitt == 1:
				sys.exit()

			queuefile = open(Settings.QUEUEFILE, 'r')
			queue = queuefile.readlines()
			queuefile.close()
			for url in queue:
				dupe = 0
				if Settings.NOREPEAT == 'True':
					for lolurl in hookprog:
						if url.replace('\n', '') == lolurl.replace('\n', ''):
							dupe = 1
	
				if url != '' and dupe != 1 and url != '\n' and url != '\r' and url != ' ':
					queue.remove(url)
					#Start downloading the file on new things in the queue. (Starts a thread)
					Download(url.replace('\n', '')).start()
					newqueue = ''
					for uncomplete in queue:
						newqueue += uncomplete
	
					queuefile = open(Settings.QUEUEFILE, 'w')
					queuefile.write(newqueue)
					queuefile.close()
	
					logfile = open(Settings.LOGFILE, 'a')
					logfile.write(url)
					logfile.close()
			time.sleep(Settings.RTIME)


if __name__ == '__main__':
	global quitt
	quitt = 0
	global screen
	global hookprog
	hookprog = {}
	global current_string
	global stdscr
	#Here's where I add a / to the end of the home directory if the user didn't do that already, and then I also replace things like '~' and '$HOME' with their home dir..
	Settings.QUEUEFILE = str(Settings.QUEUEFILE).replace('~', os.path.expanduser('~')).replace('$HOME', os.path.expanduser('~'))
	Settings.LOGFILE = str(Settings.LOGFILE).replace('~', os.path.expanduser('~')).replace('$HOME', os.path.expanduser('~'))
	Settings.DLOCATION = str(Settings.DLOCATION).replace('~', os.path.expanduser('~')).replace('$HOME', os.path.expanduser('~'))
	if str(Settings.DLOCATION)[(len(Settings.DLOCATION) - 1):len(Settings.DLOCATION)] != '/':
		Settings.DLOCATION = Settings.DLOCATION + '/'

	ReadQueue().start()

	if Settings.DISPLAY == 'True':
		stdscr=curses.initscr()
		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)
		stdscr.keypad(1)

		rows, cols = stdscr.getmaxyx()
		screen = stdscr.subwin(rows, cols, 0, 0)
		current_string = 0
		
		while 1:
			c = screen.getch()
			#Pause
			if c == 112:
				for x in hookprog:
					if hookprog[x][0] == current_string:
						hookprog[x][3] = 1
			#Quit; I have to end all of the threads and stuff you know. I'm not sure how to catch "ctrl+c" to do the same thing, if someone knows, tell me.
			if c == 113:
				stdscr.keypad(0)
				curses.echo()
				curses.nocbreak()
				curses.endwin()
				for x in hookprog:
					hookprog[x][4] = 1
					print "Ending thread " + str(x)
					
				print "Calling system exit. Good bye!\n"
				quitt = 1
				sys.exit()
		
			#Resume	
			elif c == 114:
				for x in hookprog:
					if hookprog[x][0] == current_string:
						hookprog[x][3] = 0
			#Redownload
			elif c == 115:
				for x in hookprog:
					if hookprog[x][0] == current_string:
						Download(x).start()

			#For up and down arrows, it has multiple ascii values.
			elif c == 27:
				c = screen.getch()
				if c == 91:
					c = screen.getch()
					#Up
					if c == 65 and current_string != 0:
						current_string -= 1
						for x in hookprog:
							if hookprog[x][0] == current_string:
								hookprog[x][2] = hookprog[x][2].replace('[ ]', '[x]')
								screen.addstr(hookprog[x][0], 0, hookprog[x][2])
			
							else:
								hookprog[x][2] = hookprog[x][2].replace('[x]', '[ ]')
								screen.addstr(hookprog[x][0], 0, hookprog[x][2])
					#Down
					elif c == 66 and current_string != len(hookprog):
						current_string += 1
						for x in hookprog:
							if hookprog[x][0] == current_string:
								hookprog[x][2] = hookprog[x][2].replace('[ ]', '[x]')
								screen.addstr(hookprog[x][0], 0, hookprog[x][2])
		
							else:
								hookprog[x][2] = hookprog[x][2].replace('[x]', '[ ]')
								screen.addstr(hookprog[x][0], 0, hookprog[x][2])
			screen.refresh()


