Python Arcade Library Rogue-Like
================================

This is a rogue-like adventure written in Python using the Arcade library.
It is designed to be a springboard for creating your own rogue-like.

Keybindings
-----------

* Move with the number pad in 8 directions (num lock off)
* Pick up an item with ``G`` or ``Num 5``
* Select an item with the numbers ``1`` - ``9``
* Use the selected item with ``U``
* Drop the selected item with ``D``
* Save game with ``S``
* Load game with ``L``
* Bring up the character screen with ``C``

    * If you have ability points, click on the + to increase that stat

* Cancel the grid selection, character screen, etc. with ``Esc``

Other notes
-----------
* Move 'into' a monster to attack it
* Fireball is an area of effect weapon, and can damage the player.
* Lightning attacks the closest monster

Features
--------

* Procedural dungeons
* Character leveling system
* Ranged lighting spell
* Area of effect spell
* Field of vision
* Monster table
* Inventory management system
* A-star path-finding for monsters
* Can save/restore dungeon via JSON formatted data
* Message/event system
