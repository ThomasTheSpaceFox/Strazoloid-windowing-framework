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
	elif frameobj.statflg==8:
		print(frameobj.name + " stat 8: desktop window resize")
	elif frameobj.statflg==9:
		print(frameobj.name + " stat 9: frame shade")
	elif frameobj.statflg==10:
		print(frameobj.name + " stat 10: frame unshade")


stz.framestyle=2

#if you want the multi-window enviornment to be resizable, set the resizable flag to 1 in the desktop instance.
desk=stz.desktop(800, 600, "Test desktop 1", pumpcall=event_test, resizable=1)
framesc=stz.framescape(desk)

def proccount(frameobj, data=None):
	if frameobj.statflg==0:
		frameobj.name="frames: " + str(len(framesc.proclist)) + " | ghosts: " +  str(len(framesc.ghostproc))
	if frameobj.statflg==3:
		if frameobj.runflg==2:
			#persistence
			print("frames/ghosts counter: frame has closed, restoring frame")
			#restore frame
			framesc.add_frame(frameobj)
			#make active frame.
			#framesc.raise_frame(frameobj)

#the following flag values also apply to desktop class except where noted.

#statflg values:
#0=wm system pump call. (called every mainloop of framescape)
#1=startup. system should initialize
#2=frame resize. surface should be redrawn and positions recalibrated. (frames only)
#3=frame close/quit/halt check runflg value for condition.
#4=clickdown
#5=clickup
#6=keydown
#7=keyup
#8=desktop window resize (desktop only) (desktop must have realizability enabled)
#9=window has been shaded. (aka, shrunk to just a title bar. surface is HIDDEN.) (frames only)
#10=window has been unshaded. (aka returned to normal) (frames only)

#runflg values:
#1=frame is running.
#0=frame has quit due to window manager shutting down.
#2=frame has been closed by user. (frames only)


#ghost tasks can't display anything, hence the name 'ghost'.
#they are useful for things like getting all keyboard events,
#getting all mouse events, etc.
#Also, they are 'pumped' every frame as well, and can be closed 
#via their PID, or via passing the ghost instance to framescape.close_ghost(ghost)

#both frame and ghost tasks can be terminated via their unique PID:
#framescape.close_pid(pid)
#in addition frames can be closed via passing the framex instance to:
#ramescape.close_frame(framex)

testghost=stz.ghost("GHOST TASK 1", pumpcall=event_test)

testframe=stz.framex(200, 200, "test --REALLYLONGNAME--  -- -----------", resizable=1, pumpcall=event_test, xpos=10, ypos=0)
testframe2=stz.framex(200, 100, "test2", pumpcall=event_test, xpos=560, ypos=200)

tstfrm3_icon=pygame.image.load("testicon1_20px.png")
testframe3=stz.framex(235, 60, "frames: 0 | ghosts: 0", pumpcall=proccount, xpos=550, ypos=100, icon=tstfrm3_icon)

#### SIMPLE DOODLE APP EXAMPLE ####

class drawxq:
	def __init__(self):
		self.lineflg=0
		return
	def framecall(self, frameobj, data=None):
		if frameobj.statflg==0:
			if self.lineflg:
				#remove xy position bias using mousehelper.
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
drawicon=pygame.image.load("doodle.png")	
drawinst=drawxq()
drawframe=stz.framex(300, 300, "draw (left=draw, right=reset)", pumpcall=drawinst.framecall, xpos=235, ypos=0, icon=drawicon)

########


#### 'colored' example from docs/events.md  (EXAMPLE 2) ####

colorsicon=pygame.image.load("colors1.png")

class colored:
	def __init__(self, color=(255, 0, 255)):
		self.color=color
	def drawdisp(self, frameobj):
		frameobj.surface.fill(self.color)
	def pumpcall1(self, frameobj, data=None):
		if frameobj.statflg==1:
			self.drawdisp(frameobj)
			
		if frameobj.statflg==2:
			self.drawdisp(frameobj)

#purple
colorpurple=colored()
purpleframe=stz.framex(400, 50, "colored (purple) (from docs/events.md)", pumpcall=colorpurple.pumpcall1, xpos=150, ypos=400, resizable=1, sizeminx=250, sizeminy=50, icon=colorsicon)
framesc.add_frame(purpleframe)

#orange
colororange=colored(color=(255, 127, 0))
orangeframe=stz.framex(400, 50, "colored (orange) (from docs/events.md)", pumpcall=colororange.pumpcall1, xpos=150, ypos=500, resizable=1, sizeminx=250, sizeminy=50, icon=colorsicon)
framesc.add_frame(orangeframe)

########

#once we create our framex task objects, we can start them like so:
framesc.add_frame(testframe)
framesc.add_frame(testframe2)
framesc.add_frame(testframe3)
framesc.add_frame(drawframe)
#and for ghost task objects, we do:
framesc.add_ghost(testghost)
#begin wm mainloop.
framesc.process()
