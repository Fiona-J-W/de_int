de_int
======

Sane German keyboard-layout for international keyboards with great support for mathematics.

Installation
------------

On Debian copy `de_int` to `/usr/share/X11/xkb/symbols` and execute `setxkbmap de_int`.
You can set it permanently via `/etc/default/keyboard`.

In addition copy `XCompose` to `~/.XCompose` and set a compose key via `setxkbmap -option compose:caps de_int`.
