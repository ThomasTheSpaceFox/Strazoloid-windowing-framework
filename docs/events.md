# Status Flag Events:

[Index](index.md)

### Overview

All task types require a pumpcall function with 2 arguments. the first
contains a reference to the task object instance, the other any data
relevant to the current status code.

Using classes is HIGHLY reccomended. this lets you spin up multiple instances easily. 
For example, a help viewer.

EVERY STATUS CODE GETS RUN THROUGH THESE PUMPCALL FUNCTIONS. YOU MUST ALWAYS CHECK STATFLG!

**framex** and **desktop** task objects also contain sizes and drawing surfaces.

### Example 1
_Say we want a window thats filled with purple:_


	class purple:
		def __init__(self):
			return
		def drawdisp(self, frameobj):
			frameobj.surface.fill((255, 0, 255))
		def pumpcall1(self, frameobj, data=None):
			if frameobj.statflg==1:
				self.drawdisp(frameobj)
			if frameobj.statflg==2:
				#need to redraw after resize events.
				self.drawdisp(frameobj)


### Example 2
_But what if we want an orange one too? And what about rendering while resizing?_

	
	class colored:
		def __init__(self, color=(255, 0, 255)):
			self.color=color
		def drawdisp(self, frameobj):
			frameobj.surface.fill(self.color)
		def pumpcall1(self, frameobj, data=None):
			if frameobj.statflg==1:
				self.drawdisp(frameobj)
			if frameobj.statflg==11:
				self.drawdisp(frameobj)


With **colored** we can create both purple and orange colored windows.
This is why classes are reccomended, as you can have the same code
in multiple instances, with different parameters. we can even redraw on
code 11 instead of code 2, to redraw while the frame is resizing!

_stz-test.py shows off **colored** in use._

### Chart of what codes are sent where:

code|description               |desktop|frames|ghosts
:--:|:------------------------:|:-----:|:----:|:----:
   0|pump __3.__               |Yes    |Yes   |Yes
   1|init                      |Yes    |yes   |Yes
   2|after frame resize        |No     |Yes   |No
   3|terminate __4.__          |Yes    |Yes   |Yes
   4|Click DOWN                |__2.__ |__1.,5.__|Yes
   5|Click UP                  |Yes    |__1.,5.__|Yes
   6|Keydown                   |Yes    |__1.,5.__|Yes
   7|Keyup                     |Yes    |__1.,5.__|Yes
   8|resize desktop            |Yes    |No    |No
   9|frame shade               |No     |Yes   |No
  10|frame unshade             |No     |Yes   |No
  11|frame resizing __6.__     |No     |Yes   |No
  12|desktop quit check __7.__ |Yes     |No   |No


1. Only the frame that is 'active' will receive mouse and keyboard events.
As well, **mouse DOWN** events will only be sent when they are **WITHIN** the
frame's surface. bare in mind, **mouse UP** events will at times be sent
**WITHOUT** an accompanying **mouse DOWN** event.

2. Only when the **click DOWN** event lies outside of any frame window
(this includes outside of frame window decoration and title bars.)

3. Pump is called every frame. use for things that need constant checking/updating.

4. terminate events have an additional flag.

5. The 'data' value (second argument of callback function), will contain a
pygame event object on _clickup_, _clickdown_, _keyup_, and _keydown_ events.

6. Unlike code **2**, code **11** is called repeatedly **while** the frame is resizing, 
so it can be used to render during frame resizing.

7. Called upon `pygame.QUIT`. set `code12_askbeforequit=True`, then return False to
ignore quit event, or return True to obey it.
The `framescape.shutdown()` method can be used to then manually quit. 
(for example, via an "are you sure you want to quit?" dialog.)

### Notes:

Also note: framex mouse events are NOT ALIGNED WITH FRAMEX SURFACE!
However the mousehelper function can help:


	strazoloidwm.mousehelper(pos, frameobj)


`pos` should be a _tuple_ containing the x and y position (as returned by pygame)
`frameobj` should be a reference to the _frame object_ instance.
will return a _tuple_ with the adjusted coordinates.