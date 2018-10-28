# Status Flag Events:

[Index](index.md)

All task types require a pumpcall function with 2 arguments. the first
contains a reference to the task object instance, the other any data
relevant to the current status code.

Using classes is HIGHLY reccomended. this lets you spin up multiple instances easily. 
For example, a help viewer.

EVERY STATUS CODE GETS RUN THROUGH THESE PUMPCALL FUNCTIONS. YOU MUST ALWAYS CHECK STATFLG!

```
def some_class_method(frameobj, data):
	if frameobj.statflg==0:
		print(
	if frameobj.statflg==1:
		print("Init")
	if frameobj.statflg==2:
		print("resize")
	#note the extra flag checked.
	if frameobj.statflg==3:
		if frameobj.runflg==0:
			print("Strazoloid is shutting down! goodbye!")
		if frameobj.runflg==2:
			print("If im a framex instance, this means i was closed!")
```

**framex** and **desktop** task objects also contain sizes and drawing surfaces.
Say we want a window thats filled with purple:

```
def some_class_method(frameobj, data):
	if frameobj.statflg==1:
		frameobj.surface.fill((255, 0, 255))
	if frameobj.statflg==2:
		frameobj.surface.fill((255, 0, 255))
```

We need to redraw after resize events, as we now have a new surface.


### Chart of what codes are sent where:

code|description     |desktop|frames|ghosts
:--:|:--------------:|:-----:|:----:|:----:
   0|pump __3.__     |Yes    |Yes   |Yes
   1|init            |Yes    |yes   |Yes
   2|resize frame    |No     |Yes   |No
   3|terminate __4.__|Yes    |Yes   |Yes
   4|Click DOWN      |__2.__ |__1.,5.__|Yes
   5|Click UP        |Yes    |__1.,5.__|Yes
   6|Keydown         |Yes    |__1.,5.__|Yes
   7|Keyup           |Yes    |__1.,5.__|Yes
   8|resize desktop  |Yes    |No    |No
   9|frame shade     |No     |Yes   |No
  10|frame unshade   |No     |Yes   |No


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


### Notes:

Also note: framex mouse events are NOT ALIGNED WITH FRAMEX SURFACE!
However the mousehelper function can help:

```
strazoloidwm.mousehelper(pos, frameobj)
```

`pos` should be a _tuple_ containing the x and y position (as returned by pygame)
`frameobj` should be a reference to the _frame object_ instance.
will return a _tuple_ with the adjusted coordinates.