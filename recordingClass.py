import pyautogui
import time

class Recording():
	def __init__(self,location=(0,0),action=0,predelay=0,postdelay=2,text=""):
		actionTypes = {
		0: "Move",
		1: "Left Click",
		2: "Right Click",
		3: "Text",
		4: "KeyPress",
		5: "Drag",
		}
		self.location = location
		self.action = int(action)
		self.actionName = actionTypes[self.action]
		self.predelay = predelay
		self.postdelay = postdelay
		self.text = text

	def executeAction(self,echo=False):
		def action_leftClick():
			try:
				clickcount = int(self.text)
			except ValueError:
				clickcount = 1

			if echo: print("Left Click at:\t{} x{}".format(self.location, clickcount))
			action_movePointer()
			pyautogui.click(clicks=clickcount)

		def action_rightClick():
			if echo: print("Right Click at:\t{}".format(self.location))
			action_movePointer()
			pyautogui.click(button='right')

		def action_typeString():
			if echo: print("Typing:\t{}".format(self.text))
			pyautogui.typewrite(str(self.text), interval=(float(self.predelay)) )

		def action_keyPress():
			if echo: print("KeyPress:\t['{}']".format(self.text))
			pyautogui.typewrite( [ str(self.text) ])

		def action_movePointer():
			if echo: print("Move To:\t{}".format(self.location))
			if ('+' in str(self.location)) or ('-' in str(self.location)): #Relative
				pyautogui.moveRel(int(self.location[0]),int(self.location[1]))
			else: #Absolute
				pyautogui.moveTo(self.location)

		def action_dragPointer():
			if echo: print("Drag To:\t{}".format(self.location))
			try:
				tween = float(self.text)
			except:
				tween = 1
			pyautogui.dragTo(self.location[0],self.location[1], tween)

		action_functions = {
			'1': action_leftClick,
			'2': action_rightClick,
			'3': action_typeString,
			'4': action_keyPress,
			'0': action_movePointer,
			'5': action_dragPointer,
		}

		if (echo and (float(self.predelay) > 0)):
			print("Sleeping: " + str(self.predelay) )

		time.sleep(float(self.predelay))

		try: action_functions[str(self.action)]()
		except KeyError: print('KeyError: \'{}\' not found in action_functions as a valid key'.format(self.action))

		
		if (echo and (float(self.predelay) > 0)):
			print("Sleeping: " + str(self.postdelay) )
		time.sleep(float(self.postdelay))

class SaveHandler():
	def __init__(self):
		pass

	def loadFromFile(self,filepath,outList=[]):
		"""Return a list of recording objects from a given .pmac file"""
		with open(filepath,'r') as f:
			for line in f:
				cl = line.split(",")
				outList.append(Recording((int(cl[0]),int(cl[1])),cl[2],cl[3],cl[4],cl[5]))
		return outList

	def saveToFile(self,listOfRecordings,filepath):
		"""Save a list of recordings to a .pmac file"""
		file = open(filepath, "w")
		for rec in listOfRecordings:
			file.write('{},{},{},{},{},{}'.format(rec.location[0],rec.location[1],rec.action,rec.predelay,rec.postdelay,rec.text,).strip())
			file.write('\n')
		file.close()