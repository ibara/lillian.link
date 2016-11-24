# Zoe & Molly: Choo Goo Release (0.1.0)

So I made my first real release of Zoe & Molly on GitHub, specifically
[Release 0.1.0 "Choo Goo."](https://github.com/lily-seabreeze/zoe-and-molly/releases/tag/v0.1.0)
I call it that because there's a lot of slime and also a train minigame.
Please keep in mind this is a rough draft of a very incomplete game, an early sneak peak.
Here's the official release video:

<iframe width="560" height="315" src="https://www.youtube.com/embed/gQreAbWf3CA" frameborder="0" allowfullscreen></iframe>

Zoe & Molly is a game based off of my dreams, I encourage you to read about that in
[my first blog post about Zoe & Molly](/blog/zoe-and-molly/2016-11-10_redid-zoe-slime/).

I try to Tweet regularly to the [#zoemolly Hashtag on Twitter](https://twitter.com/hashtag/zoemolly).

## How can I play?

Checkout
[the Zoe & Molly v0.1.0 download page](https://github.com/lily-seabreeze/zoe-and-molly/tree/v0.1.0/distrib)
and follow the instructions in the `README.md`/on the page there.

## Hows it made?

I have a lot of details on that on the 
[Zoe & Molly GitHub repo](https://github.com/lily-seabreeze/zoe-and-molly)  itself,
but in short, I use a game engine called
[OHRRPGCE](http://rpg.hamsterrepublic.com/ohrrpgce/Main_Page).

## The train minigame

I had to introduce some scripts in this release, namely for the minigame. The minigame
is a simple board game where you roll the die and you get to move that many spaces
from your current position in any direction. However, you have a limited number of
die rolls. You collect points by ending your turn on a dot/green tile, thus collecting
that tile's point. You win by making it to the goal (yellow tile) with points, on your
last roll.

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">end roll on a dot to gain point. play until out of rolls, but if out of rolls &amp; you&#39;re not on the goal square, you lose/no points <a href="https://twitter.com/hashtag/zoemolly?src=hash">#zoemolly</a> <a href="https://t.co/cMWBhH91d1">pic.twitter.com/cMWBhH91d1</a></p>&mdash; SpaceSlimeComplexity (@LilySeabreeze) <a href="https://twitter.com/LilySeabreeze/status/801682343455027200">November 24, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

The script that makes the magic happen is `scripts/trainy.hss`, which is written in
HamsterSpeak (AKA "plotscripting"), something specific to
[OHRRPGCE](http://rpg.hamsterrepublic.com/ohrrpgce/Main_Page).

Some interesting bits about HamsterSpeak:

  * There are no lists or arrays, just global variables #0 to #16383. I used a
    "fake array" to accomplish keeping the move history in the minigame. This
    method is documented in the
    [OHRRPGCE Wiki's "Fake Arrays" article](http://rpg.hamsterrepublic.com/ohrrpgce/Scripts:Fake_arrays)
  * Likewise, strings are stored like globals, whereas a string is created with
    a manually specified integer identifier, and is later referenced by such.
  * `th  i s` is the same as `this`

If you wanna read more about HamsterSpeak, be sure to checkout the
[Official Dictionary of Plotscripting Commands](http://hamsterrepublic.com/ohrrpgce/plotdictionary.html).

I also wanted to thank the generous people in the OHRRPGCE IRC channel (#slimesalad on
Espernet), including the creator Bob the Hamster, SDHawk, and Harlock199X for their
input and assistance. Some funny tricks used in this script:


  * To see if the goal is achieved I check if the train is over a "vehicle type a"
    tile (if the player is out of rolls)
  * To gain points, the train moves under dot NPCs. Then, a check at the spot of
    the train NPC is done, for the second NPC result in that area, whereas 0 is
    the backmost and >0 is increasingly foremost.
  * The way spaces you're allowed to move is calculated by keeping track of directions/
    keys pressed, so that if the opposite is pressed, the history can be undone and more
    movement regained. The spaces are stored in a series of global variables with a
    "fake array" (as mentioned above). Once you return to the original roll value, the
    history is just reset (this solved some bug, I can't remember what...)

I also have a secret/alternate spriteset for this, that includes a
Burlington Northern SD45 as the train/player's piece. I plan to use this
in a later part of the game (I'll probably touch up later, too).

![The Burlington Northern SD45 Train Walkabout](burlington-northern.png)

## Where to go from here

I've been thinking what I'm going to do with that Daisy character,
if I wanna keep the small walkabout characters for battle, or if I wanna go nuts and
make Daisy the "Zoe" character, and workon battle animations for both Zoe and Molly.

I need to redo a lot of the writing (at least to
have characters talk in a more interesting way than "I AM THING FOR THIS PURPOSE),

I'd really like to make some cutscenes and an intro. Start letting people load and
see a title screen.

I'd also like to make sure I'm intelligently managing my palettes more. The
colors in the crayon world need a real palette.

Other stuff I wanna touch up on before I make a more official "demo" is
better sound effects, bug fixes, add cutscenes (namely intro cutscene),
add title screen, allow people to load saves, polish the minigame.

Eventually make an portable computer that's like a gameboy but takes floppies,
so you can save on the fly. But, I want to make it so in some parts, someone
steals your floppy so you can't save.

Make slime monsters appear once Zoe joins (in random encounters; by tag). Attacking
slime with slime either heals or makes slimes bigger; hurting slimes splits them
into smaller pieces until they die.

## Pictures!

![Demo GIF on GitHub](https://github.com/lily-seabreeze/zoe-and-molly/raw/v0.1.0/demo.gif)

![First thing you see](start.png)

![Punchin a laughin hand](punch.png)

![Zoe](zoe.png)

![Blobs](blobs.png)

![Diasy](daisy.png)

![Crayon Ghost](crayon-ghost.png)

![Minigame](minigame.png)

![Stoplight Boss](stoplight.png)

![Heart Eyes](heart-eyes.png)

![Dither](dither.png)
