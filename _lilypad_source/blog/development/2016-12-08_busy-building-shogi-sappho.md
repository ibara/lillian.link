# Busy Building Sappho & Shogi

I've been keeping busy working on a Spatial Partition system in Sappho, my 2D game
engine. Also, I've been talking about/making plans for implementing web-based Shogi.

## Sappho: Spatial Partitions

I'm going to explain how I've implemented Spatial Partitions in Sappho (in an experimental
branch; see [PR #105](https://github.com/lily-seabreeze/sappho/pull/105)). Spatial partitions will do the following things for the end
developer:

  * Substantially increase the efficiency of collision checks, especially in bullet hells,
    any game that uses a lot of collision checks
  * Update sections of a map/screen's physics based on "locality"
  * Peform actions on objects based on locality, in general

Note that this PR/branch is still experimental. I'm working on updating the demo to use it... I should
probably clean up the demo in general.

## Shogi: Drafting Ideas, Research

I've been doing my research on how I'd implement a web-based Shogi game. I'm really
unhappy with the options available now, so I aim to develop a simple multiplayer
Shogi. Currently thinking about websockets, Python, flask-restful...

I'll be doing this with a friend, who's gonna do the frontend.

Luckily for me there's [the `python-shogi` package on Pypi](http://pypi.python.org/pypi/python-shogi),
which handles all of the pure Shogi logic.
