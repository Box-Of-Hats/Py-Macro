import pyautogui, time
from tkinter import *
from recordingClass import *
import glob
import winsound
import threading
import subprocess
import easygui

actionTypes = {
		0: "Move",
		1: "Left Click",
		2: "Right Click",
		3: "Text",
		4: "KeyPress",
		5: "Drag",
	}

try:
	cfg = open('resources\\config.txt', 'r')
except:
	print('Error: Missing Config File!')


allRecordings = []

cmdKeys = [str(line) for line in open('resources\\cmdKeys.txt')]

def loadGui(allRecordings,listbox,root):

	def loadMacro(filename,listbox,allRecordings):
		while len(allRecordings) > 0:
			try:
				allRecordings.pop()
			except IndexError:
				pass
			listbox.delete(len(allRecordings),END)
		with open(filename,'r') as f:
			for line in f:
				cl = line.split(",")
				newRec(allRecordings,(cl[0],cl[1]),cl[2],cl[3],cl[4],cl[5])
				listbox.insert(END,'{}: ({},{}) - {} - [{}~{}]'.format(len(allRecordings),cl[0],cl[1],actionTypes[int(cl[2])],cl[3],cl[4]))
	selectedFile = easygui.fileopenbox(default="macros\\*.pmac")
	if selectedFile != '.':
		loadMacro(selectedFile,listbox,allRecordings)
	

def saveGui(allRecordings):
	fileToSaveAs = easygui.filesavebox(default='macros\\*.pmac')
	if fileToSaveAs != '.':
		saveHandle = SaveHandler()
		saveHandle.saveToFile(allRecordings, '{}'.format(fileToSaveAs))

def keysGui(cmdKeys,changeVar):

	def loadKey(lb,changeVar):
		keyToLoad = int(lb.curselection()[0])
		keyStr = cmdKeys[keyToLoad]
		changeVar.delete(0,'end')
		changeVar.insert(0,keyStr)
		rootC.destroy()

	rootC = Tk()
	scrollbar2 = Scrollbar(rootC)
	scrollbar2.pack(side=RIGHT,fill=BOTH)
	listbox2 = Listbox(rootC, yscrollcommand=scrollbar2.set,width=40)
	scrollbar2.config(command=listbox2.yview)

	for keyK in cmdKeys:
		listbox2.insert(END,str(keyK))

	def clickEvent(event):
		try:
			loadKey(listbox2,changeVar)
		except IndexError:
			pass

	currentMousePos = pyautogui.position()

	listbox2.pack(fill=BOTH,expand=1,side=LEFT)
	rootC.geometry('{}x{}+{}+{}'.format(320, 430,(currentMousePos[0]-155),currentMousePos[1]-185))
	rootC.bind("<Button-1>", clickEvent)
	rootC.wm_attributes("-topmost",int(True))
	rootC.wm_title("List Of Keys")
	rootC.mainloop()

def showGui(allRecordings,cfg):

	root = Tk()
	def keyPress(event):
		if event.char == " ":
			x, y = pyautogui.position()
			locX.delete(0,END)
			locY.delete(0,END)
			locX.insert(0,x)
			locY.insert(0,y)
			submitEntry(action.get())
		elif event.char == "\r":
			executeAll(allRecordings, freq.get(),delayBetween,echoOn,loopDelay.get(),beep.get())
	root.bind("<Key>", keyPress)

	def editEvent(listBox):

		def overwriteRecording(index):
			listBox.delete(index)
			allRecordings.remove(allRecordings[index])

			alocX= int(PosXEntry.get())
			alocY= int(PosYEntry.get())
			aPre= float(PreEntry.get())
			aPost= float(PostEntry.get())
			aText= str(TextEntry.get())
			aAction= int(ActionEntry.get())

			allRecordings.insert(index,Recording( (alocX,alocY), aAction, aPre, aPost,aText) )
			listbox.insert(index,"{}: ({},{}) - {} - [{}~{}]".format(index+1,alocX,alocY, actionTypes[aAction], aPre, aPost,aText))
			editGui.destroy()

		def removeRecording(index):
			listBox.delete(index)
			allRecordings.remove(allRecordings[index])
			editGui.destroy()

		try:
			recordingToEdit = allRecordings[int(listBox.curselection()[0])]
		except IndexError:
			print("You need to select a recording to edit")
			return False

		editGui = Tk()

		thisIndex = listBox.curselection()[0]
		PosXLabel = Label(editGui,text="X Pos:").grid(row=5,column=5)
		PosXEntry = Entry(editGui)
		PosXEntry.grid(row=5,column=6)
		PosXEntry.insert(0,allRecordings[thisIndex].location[0])

		PosYLabel = Label(editGui,text="X Pos:").grid(row=6,column=5)
		PosYEntry = Entry(editGui)
		PosYEntry.grid(row=6,column=6)
		PosYEntry.insert(0,allRecordings[thisIndex].location[1])

		PreLabel = Label(editGui,text="PreSleep:").grid(row=7,column=5)
		PreEntry = Entry(editGui)
		PreEntry.grid(row=7,column=6)
		PreEntry.insert(0,allRecordings[thisIndex].predelay)

		PostLabel = Label(editGui,text="PostSleep:").grid(row=8,column=5)
		PostEntry = Entry(editGui)
		PostEntry.grid(row=8,column=6)
		PostEntry.insert(0,allRecordings[thisIndex].postdelay)

		TextLabel = Label(editGui,text="Text:").grid(row=9,column=5)
		TextEntry = Entry(editGui)
		TextEntry.grid(row=9,column=6)
		TextEntry.insert(0,allRecordings[thisIndex].text)

		ActionLabel = Label(editGui,text="Action:").grid(row=10,column=5)
		ActionEntry = Entry(editGui)
		ActionEntry.grid(row=10,column=6)
		ActionEntry.insert(0,allRecordings[thisIndex].action)

		overWriteBut = Button(editGui,text='Save',command= lambda: overwriteRecording(thisIndex))
		overWriteBut.grid(row=15,column=6)

		deleteBut = Button(editGui,text='Delete',bg='#DE2E21',command= lambda: removeRecording(thisIndex))
		deleteBut.grid(row=15,column=5)

		editGui.wm_attributes('-topmost',int(True))
		editGui.wm_title("Edit Recording")
		editGui.geometry("{}x{}+{}+{}".format(200,160,pyautogui.position()[0]-200,pyautogui.position()[1]-150))
		editGui.mainloop()
		
	#########################################################################


	def openConfig():
		def toggleTop(top):
			root.wm_attributes("-topmost",top)
		def openConfigFile():
			this = threading.Thread(target=subprocess.call,args=(['C:\\Program Files\\Sublime Text 2\\sublime_text.exe',"resources\\config.txt"],) )
			this.start()
		conwin = Tk()
		conwin.geometry('{}x{}+{}+{}'.format(200,100,500,150))
		conwin.wm_attributes("-topmost",True)
		Label(conwin,text='On Top').grid(row=6,column=4)
		Button(conwin,text='True',width=10,command=lambda:toggleTop(True)).grid(row=6,column=5)
		Button(conwin,text='False',width=10,command=lambda:toggleTop(False)).grid(row=6,column=6)
		Button(conwin,text='Open Config File',width=22,command=lambda:openConfigFile()).grid(row=8,column=5,columnspan=2)
		conwin.mainloop()

	lineNo = 0
	for line in cfg:
		lineNo +=1
		#Window Stays On Top
		if lineNo == 2:
			root.wm_attributes("-topmost",int(line))
		#Delay Between Actions
		elif lineNo == 4:
			delayBetween = float(line)
		#Echo
		elif lineNo == 6:
			echoOn = bool(line)
			print("EchoOn:",echoOn)
		#BG Colour
		elif lineNo == 8:
			bgc = str(line)
		#Button Fore Colour
		elif lineNo == 10:
			butfg = str(line)
		#Button Back Colour
		elif lineNo == 12:
			butbg = str(line)

	bottomFrame = Frame(root,background=bgc ) 
	bottomFrame.grid(row=11,column=0,columnspan=8)

	labelX = Label(text="X-CoOrd:",bg=bgc).grid(row=0,column=0)
	locX = Entry(root)
	locX.grid(row=0,column=1)

	#Settings Button can Display a cog instead if desired.
	cogImage = PhotoImage(file="resources\\MacroRecorderApplicationGUI\\settings.png")
	cog = Button(image=cogImage,width=60,command= lambda: openConfig())

	cog.grid(row=0,column=2,rowspan=2)

	labelY = Label(text="Y-CoOrd:",bg=bgc).grid(row=1,column=0)
	locY = Entry(root)
	locY.grid(row=1,column=1)

	labelPre = Label(text="Pre-Sleep:",bg=bgc).grid(row=5,column=0)

	pre = Entry(root)
	pre.grid(row=5,column=1)

	labelPost = Label(text="Post-Sleep:",bg=bgc).grid(row=6,column=0)

	post = Entry(root)
	post.grid(row=6,column=1)

	action = IntVar()
	action.set(0)

	curX = IntVar()
	curX.set(0)

	curY = IntVar()
	curY.set(0)

	Radiobutton(root, text="Move", variable=action, value=0,bg=bgc).grid(row=3,column=0)
	Radiobutton(root, text="Left Click", variable=action, value=1,bg=bgc).grid(row=3,column=1)
	Radiobutton(root, text="Right Click", variable=action, value=2,bg=bgc).grid(row=3,column=2)
	Radiobutton(root, text="Text", variable=action, value=3,bg=bgc).grid(row=4,column=0)
	Radiobutton(root, text="KeyPress", variable=action, value=4,bg=bgc).grid(row=4,column=2)
	Radiobutton(root, text="Drag",variable=action, value=5, bg=bgc).grid(row=5,column=2)
	textToType = Entry(root)
	textToType.grid(row=4,column=1)

	labelfreq = Label(bottomFrame,text="Loops:",bg=bgc).grid(row=10,column=0)
	freq = Entry(bottomFrame)
	freq.grid(row=10,column=1)

	Label(bottomFrame,text="Delay:",bg=bgc).grid(row=11,column=0)
	loopDelay = Entry(bottomFrame)
	loopDelay.grid(row=11,column=1)

	#Sets default values of entry fields:
	pre.insert(0,0)
	post.insert(0,0)
	freq.insert(0,1)
	locY.insert(0,0)
	locX.insert(0,0)
	textToType.insert(0,1)
	loopDelay.insert(0,0)

	#Scroll Box
	scrollbar = Scrollbar(bottomFrame)
	scrollbar.grid(row=0,column=5,sticky='n'+'s')

	listbox = Listbox(bottomFrame, yscrollcommand=scrollbar.set,width=40)
	listbox.grid(row=0,column=0,columnspan=4,rowspan=2)

	scrollbar.config(command=listbox.yview)

	submitButton = Button(root,text="Record",command= lambda: submitEntry(action.get()) ,bg=butbg,fg=butfg).grid(row=10,column=0)
	executeButton = Button(bottomFrame,text="Execute",command= lambda: executeAll(allRecordings, freq.get(),delayBetween,echoOn,loopDelay.get(),beep.get()) ,bg=butbg,fg=butfg).grid(row=10,column=2)

	beep = IntVar()
	beepButton = Checkbutton(bottomFrame,text="Beep",bg=bgc,variable=beep)
	beepButton.grid(row=11,column=2)

	editButton = Button(bottomFrame,bg=butbg,fg=butfg,text="Edit",command= lambda: editEvent(listbox))
	editButton.grid(row=1,column=5,columnspan=2)

	keysButton = Button(root,text="Key list", command= lambda: keysGui(cmdKeys,textToType) ,bg=butbg,fg=butfg).grid(row=10,column=1)

	locationButton = Button(root,text="Get Location",command= lambda: showLocation() ,bg=butbg,fg=butfg).grid(row=10,column=2)
	deleteButton = Button(bottomFrame,text="Delete Last",command= lambda: deleteLastEntry() ,bg=butbg,fg=butfg).grid(row=9,column=0)
	saveGuiButton = Button(bottomFrame,text="Save Macro", command= lambda: saveGui(allRecordings) ,bg=butbg,fg=butfg).grid(row=9,column=1)
	loadGuiButton = Button(bottomFrame,text="Load Macro", command= lambda: loadGui(allRecordings,listbox,root) ,bg=butbg,fg=butfg).grid(row=9,column=2)

	def deleteLastEntry():
		try:
			allRecordings.pop()
		except IndexError:
			pass
		listbox.delete(len(allRecordings),END)

	def submitEntry(action):
		newRec(allRecordings,(locX.get(),locY.get()), action, pre.get(), post.get(),textToType.get() )
		print("New Recording made.")
		print("\tLoc: (" + str(locX.get()) + "," + str(locY.get()) + ")" )
		print("\tAction: " + str(actionTypes[action]) )

		listbox.insert(END, ("{}: ({},{}) - {} - [{}~{}]".format(len(allRecordings),locX.get(),locY.get(),actionTypes[action],pre.get(),post.get() )))

	def showLocation():
		lastLoc = (0,0)
		newLoc = (1,0)
		while lastLoc !=  newLoc:
			x, y = pyautogui.position()
			time.sleep(0.25)
			locX.delete(0,END)
			locY.delete(0,END)
			locX.insert(0,x)
			locY.insert(0,y)
			lastLoc = newLoc
			newLoc = pyautogui.position()

	root.wm_title("Macro Creator")
	root.geometry('{}x{}'.format(300, 410))
	root.configure(background=bgc)
	root.mainloop()

def executeAll(allRecordings,frequency,execDelay,echoOn,loopDelay,beep):
	frequency = int(frequency)
	time.sleep(execDelay)
	while frequency != 0 :
		print("\nLoops Left: " + str(frequency) )
		for recording in allRecordings:
			recording.executeAction(echoOn)
		frequency -= 1
		loopDelayCounter = float(loopDelay)*10
		while loopDelayCounter > 0:
			time.sleep(0.10)
			loopDelayCounter -= 1

	thisC = 10
	while thisC > 0:
		if beep:
			winsound.Beep(600, 100)
		thisC-= 1


def newRec(allRecordings,location=(0,0),action=0,predelay=0,postdelay=0,text="",relative=False):
	curr = Recording( location, action,predelay, postdelay,text)
	allRecordings.append(curr)

def main():
	showGui(allRecordings,cfg)

if __name__ == "__main__":
	main()