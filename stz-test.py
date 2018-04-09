#!/usr/bin/env python
import os
import pygame
import time
import math
import strazoloidwm as stz

#frame/desktop flag tester
def event_test(frameobj, data=None):
	#note: you should make sure all non if-statement code is behind if statements. see comments on frame/desktop flags below.
	if frameobj.statflg==1:
		print(frameobj.name + " stat 1: init call")
	elif frameobj.statflg==2:
		print(frameobj.name + " stat 2: post-resize call")
	elif frameobj.statflg==3:
		print(frameobj.name + " stat 3: frame terminate call. type:")
		if frameobj.runflg==0:
			print("   run 0: wm quit call")
			print(frameobj.pid)
			print(frameobj.wo)
		if frameobj.runflg==2:#the desktop class should never set runflg=2
			print("   run 2: frame (window) close call")
			print(frameobj.pid)
			print(frameobj.wo)
	elif frameobj.statflg==4:
		print(frameobj.name + " stat 4: clickdown")
	elif frameobj.statflg==5:
		print(frameobj.name + " stat 5: clickup")
	elif frameobj.statflg==6:
		print(frameobj.name + " stat 6: keydown")
	elif frameobj.statflg==7:
		print(frameobj.name + " stat 7: keyup")



desk=stz.desktop(800, 600, "Test desktop 1", pumpcall=event_test)
framesc=stz.framescape(desk)

def proccount(frameobj, data=None):
	if frameobj.statflg==0:
		frameobj.name="test3. proc count: "+ str(len(framesc.proclist))
	if frameobj.statflg==3:
		if frameobj.runflg==2:
			#persistance
			print("test3: frame has closed, restoring frame")
			framesc.add_frame(frameobj)

#the following flag values also apply to desktop class except where noted.

#statflg values:
#0=wm system pump call. (called every mainloop of framescape)
#1=startup. system should initalize
#2=frame resize. surface should be redrawn and positions recalibrated. (frames only)
#3=frame close/quit/halt check runflg value for condition.
#4=clickdown
#5=clickup
#6=keydown
#7=keyup


#runflg values:
#1=frame is running.
#0=frame has quit due to window manager shutting down.
#2=frame has been closed by user. (frames only)

		

	

testframe=stz.framex(200, 200, "test", resizable=1, pumpcall=event_test)
testframe2=stz.framex(200, 100, "test2", pumpcall=event_test)
testframe3=stz.framex(200, 60, "test3", pumpcall=proccount)
class doodlexq:
	def __init__(self):
		self.lineflg=0
		return
	def framecall(self, frameobj, data=None):
		if frameobj.statflg==0:
			if self.lineflg:
				#remove xy postition bias using mousehelper.
				self.curpos=stz.mousehelper(pygame.mouse.get_pos(), frameobj)
				pygame.draw.line(frameobj.surface, (255, 255, 255), self.prevpos, self.curpos, 1)
				self.prevpos=self.curpos
		elif frameobj.statflg==4:
			if data.button==1:
				self.prevpos=stz.mousehelper(data.pos, frameobj)
				self.lineflg=1
			elif data.button==3:
				frameobj.surface.fill((0, 0, 0))
		elif frameobj.statflg==5:
			self.lineflg=0
	
doodleinst=doodlexq()
doodleframe=stz.framex(300, 300, "doodle (left=draw, right=reset)", pumpcall=doodleinst.framecall)


framesc.add_frame(testframe)
framesc.add_frame(testframe2)
framesc.add_frame(testframe3)
framesc.add_frame(doodleframe)
framesc.process()
