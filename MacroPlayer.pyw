from tkinter import *
from recordingClass import *
import easygui

def loadMacro(filename,allRecordings):
	while len(allRecordings) > 0:
		allRecordings.pop()
	
	with open(filename,'r') as f:
		for line in f:
			cl = line.split(",")
			newRec(allRecordings,(cl[0],cl[1]),cl[2],cl[3],cl[4],cl[5])

def loadGui(allRecordings):
	selectedFile = easygui.fileopenbox(default="macros\\*.pmac")
	if selectedFile != '.':
		loadMacro(selectedFile,allRecordings)
	
def showGui(allRecordings,bgc,butfg,butbg,onTop):
	root = Tk()
	lineNo = 0
	bottomFrame = Frame(root,background=bgc) 
	bottomFrame.grid(row=0,column=0,padx=5,pady=2)
	freq = Entry(bottomFrame,width=5)
	freq.grid(row=0,column=1,padx=5)
	freq.insert(0,1)
	executeButton = Button(bottomFrame,text="Execute",command= lambda: executeAll(allRecordings, freq.get(),) ,bg=butbg,fg=butfg).grid(row=0,column=2)
	loadGuiButton = Button(bottomFrame,text="Load Macro", command= lambda: loadGui(allRecordings) ,bg=butbg,fg=butfg).grid(row=0,column=0)
	root.wm_title("Macro Player")
	root.geometry('{}x{}'.format(180, 30))
	root.wm_attributes("-topmost",int(onTop))
	root.configure(background=bgc)
	root.wm_attributes()
	root.mainloop()

def executeAll(allRecordings,frequency,):
	frequency = int(frequency)	
	while frequency != 0 :
		try:
			frequency -= 1
			print("Loops Left: {}".format(frequency),end='\r')
			for recording in allRecordings:
				recording.executeAction()
		except:
			break

def newRec(allRecordings,location=(0,0),action=0,predelay=0,postdelay=0,text="",relative=False):
	curr = Recording( location, action,predelay, postdelay,text)
	allRecordings.append(curr)

def main():
	allRecordings = []
	backgroundColour = "#CDFAE8"
	ButtonFore = '#000000'
	ButtonBack = '#a1dbcd'
	onTop = True
	showGui(allRecordings,backgroundColour,ButtonFore, ButtonBack,onTop)

if __name__ == "__main__":
	main()