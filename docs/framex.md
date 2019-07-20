# Special framex features:

[Index](index.md)

# overview:

the framex class is the cornerstone of strazoloid's window manager implementation. Each framex instance 
is a single "subwindow". Called a "frame" to distinguish it from the main program window.

topics not covered here may be found in other sections of the documentation.

## how do i set the icon?

the icon must be loaded as a pygame surface first. see pygame's documentation.

Aside from the optional icon=pygame_surface argument, you can also use this framex method:

`framex.seticon(pygame_surface)`       

it is recommended to use an icon matching the hudsize library variable (default 20).  
Icons that don't match this size will be scaled automatically.

## how do i tell if a frame is on top?

check if `framex.wo` equals zero.

## how do I raise a frame?
use the following method on your framescape instance.

`framescape.raise_frame(framex_instance)`

## how do I restore/add a closed/new frame?
use the following method on your framescape instance.

`framescape.add_frame(framex_instance)`

Note: **PID** will change when restoring closed window!

## how do i close a frame using code?

`framescape.close_frame(framex_instance)`

**OR**
You can use the **PID** method: 

`framescape.close_pid((framex_pid)`

You can find the **PID** of any task object via the taskobject.pid attribute. eg.:

- framex.pid
- ghost.pid
- desktop.pid
