# General FAQ

[Index](index.md)

### Q: How does strazoloid multitask?

A: Well, from an OS level, it uses 1 thread for its main engine. triggering all
relevant events in task objects in sequence, each frame, 30 times a second (by default).

In a sense, this is cooperative multitasking, rather than preemptive.
So its best to do long operations in a separate thread using python's
own threading features.

The exception of course is with rendering frame content. This MUST remain IN
SEQUENCE with the whole engine. I recommend placing your rendering code in
another method of your classes. this lets you re-render upon multiple events,
without duplicated code.

YOU MUST NEVER RENDER IN A SEPARATE THREAD
FROM THE FRAMESCAPE ENGINE CLASS!!!!


### Q: Where do i start?
A: A good place to start, aside from reading the documentation, is by reading through `stz-test.py`

### Q: How should i arrange my code? Any tips?
A: For most applications, i recommend keeping your
task classes in a secondary file. Frames, Desktop, ghosts and all.
This lets you just have startup code in your main file; and makes such code
much easier to manage.

### Q: I sure could use practical examples. Where can I find some?

For real examples of Strazoloid-powered applications, check out this wiki page:
[Strazoloid In Action](https://github.com/ThomasTheSpaceFox/Strazoloid-windowing-framework/wiki/Strazoloid-in-action)

### Q: Can i have things in the background?

A: YES! The (mandatory) desktop object's pumpcall method can be used to draw things
on the background just like how things are drawn in frames. most of the status
codes are also identical.

### Q: I need to do something in sync with my frame objects! How can i do this?

A: Ghosts are what you need. they behave similar to framex tasks,
but are 'headless' in a sense. (no pun intended)

They get all keyboard and mouse events, and can be closed and opened using
their own add_ghost and close_ghost methods in framescape, or via their
strazoloid pid.



