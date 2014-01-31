#!/usr/bin/python
import time, parallel, threading, Tkinter
from optparse import OptionParser
class parallelBuffer(threading.Thread):
	def __init__(self, pwmHertz = 60.0):
		"""
			Initilization.
			@param pwmHertz Optional parameter to set PWM frequency.
		"""
		threading.Thread.__init__(self, name='ParallelBufferThread')
		self.pwmTotalCycleTime = 1.0 / pwmHertz
		self.daemon = True
		self.running = False
		self.onTime = self.pwmTotalCycleTime
		self.offTime = 0
	def run(self):
		"""
			Starts the buffer.
		"""
		self.running = True
		while(self.running):
			p.setData(self.dataOn)
			time.sleep(self.onTime)
			p.setData(self.dataOff)
			time.sleep(self.offTime)
	def setDataOn(self, data):
		"""
			Sets the data to be set when PMW is cycled on.
		"""
		self.dataOn = data
	def setDataOff(self, data):
		"""
			Sets the data to be set when PMW is cycled off.
		"""
		self.dataOff = data
	def setPWMLevel(self, data):
		"""
			Takes % to set PWM at.
		"""
		self.onTime = self.pwmTotalCycleTime * float(data)/100.0
		self.offTime = self.pwmTotalCycleTime - self.onTime
	def stop(self):
		"""
			Stops the buffer.
		"""
		self.running = False
class newLightTimer(threading.Thread):
    def __init__(self, Slider, portCode=1):
        threading.Thread.__init__(self, name='LightingThread')
        self.portCode=portCode
        self.slider=Slider
        self.daemon = True
    def internalRunLights(self):
        level=self.slider.getLevel()
        totalCycleTime=1.0/80.0
        onTime=totalCycleTime*(float(level)/100.0)
        offTime=totalCycleTime-onTime
        while(self.running):
            if(level!=self.slider.getLevel()):
                level=self.slider.getLevel()
                onTime=totalCycleTime*(float(level)/100.0)
                offTime=totalCycleTime-onTime
            p.setData(self.portCode)
            time.sleep(onTime)
            p.setData(0)
            time.sleep(offTime)
    def run(self):
        self.running=True
        self.internalRunLights()
    def stop(self):
        self.running=False
class newLightSlider(object):
    def __init__(self, TkWindow, callback, startValue=0, title=None):
        self.levelVar=Tkinter.IntVar(value=startValue)
        scale=Tkinter.Scale(TkWindow, command = callback, variable = self.levelVar, label=title, from_=100, to=0)
        scale.pack(side=Tkinter.RIGHT)
    def getLevel(self):
        try:
            return self.levelVar.get()
        except:
            return 0
def GUItest():
	# Init.
	p.setData(000)
	pB = parallelBuffer(80.0)
	# Start with relay off.
	pB.setDataOn(002)
	pB.setDataOff(000)
	# GUI Init.
	window = Tkinter.Tk()
	window.title("LED")
	relayStatus = Tkinter.IntVar()
	def checkRelayStatus():
		if not relayStatus.get():
			pB.setDataOn(002)
			pB.setDataOff(000)
		elif relayStatus.get():
			pB.setDataOn(003)
			pB.setDataOff(001)
	radio = Tkinter.Checkbutton(window, variable = relayStatus, command = checkRelayStatus, text = "Relay")
	radio.pack(side = Tkinter.TOP)
	slide1 = Tkinter.Scale(window, command = pB.setPWMLevel, label = "Lights", from_ = 100, to = 0)
	slide1.pack(side = Tkinter.TOP)
	headColor = '#3C3B37'
	window.configure(background=headColor)
	radio.configure(background=headColor, highlightbackground=headColor)
	slide1.configure(background=headColor, highlightbackground=headColor)
	#timer1 = newLightTimer(slide1, 2)
	#slide2 = newLightSlider(window, 100, 'Light 2')
	#timer2 = newLightTimer(slide1, 2)
	#timer1.start()
	#timer2.start()
	# Start buffer then GUI.
	pB.start()
	window.mainloop()
	window.quit()
	return
def verbtoseTest():
    print('10%')
    runLights(5, 10, 001)
    print('20%')
    runLights(5, 20, 001)
    print('30%')
    runLights(5, 30, 001)
    print('40%')
    runLights(5, 40, 001)
    print('50%')
    runLights(5, 50, 001)
    print('60%')
    runLights(5, 60, 001)
    print('70%')
    runLights(5, 70, 001)
    print('80%')
    runLights(5, 80, 001)
    print('90%')
    runLights(5, 90, 001)
    print('100%')
    runLights(5, 100, 001)
    print('Finished')
    return
def quickTest(var):
    print('Started')
    l=1
    while(l<=var):
        runLights(0.1, l, 001)
        l+=1
    print('Finshed')
    return
def runLights(runningTime, powerPercent, portCode):
	"""
		Runs lights at specified power (%) for about specified time (seconds). Requires parallel module and time module.
	"""
	totalCycleTime = 1.0 / 80.0
	onTime = totalCycleTime * (float(powerPercent) / 100.0)
	offTime = totalCycleTime - onTime
	iterations = int(runningTime * 80)
	i=0
	while(i < iterations):
		p.setData(portCode)
		time.sleep(onTime)
		i += 1
		p.setData(0)
		time.sleep(offTime)
	return
def userInterface():
	choice = raw_input("[V]erbtose test, [Q]uick test, G[U]I, or [E]xit: ")
	if choice == 'V' or choice == 'v':
		verbtoseTest()
		return 'continue'
	elif choice == 'Q' or choice == 'q':
		quickTest(100)
		return 'continue'
	elif choice == 'U' or choice == 'u':
		GUItest()
		return 'continue'
	else:
		return 'exit'
print('Welcome to parallel control tester!')
p = parallel.Parallel()
# Setup the command line arguments.
optp = OptionParser()

# Output verbosity options.
optp.add_option('-u', '--gui', help='Open GUI',
                action='store_const', dest='gui',
                const=True, default=False)

options, args = optp.parse_args()
if (options.gui):
	GUItest();
else:
	while(True):
		if(userInterface() == 'exit'):
			p.setData(000)
			break
exit()
