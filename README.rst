Python Arcade Roguelike
=======================

.. image:: doc/screenshot.png
   :width: 50%

This game is an a `roguelike`_. A roguelike is a role-playing, turn-based dungeon crawler
with procedural dungeons and permanent death.

This code is based off the excellent tutorial from `Roguelike Tutorials`_. The Roguelike
tutorial uses the TCOD and SDL2 libraries. This tutorial uses the `Arcade Library`_.

.. _Arcade library: https://arcade.academy
.. _Roguelike Tutorials: http://rogueliketutorials.com/
.. _roguelike: https://en.wikipedia.org/wiki/Roguelike

Keybindings
-----------

* Move with the number pad in 8 directions (num lock off)
* Pick up an item with ``G`` or ``Num 5``
* Select an item with the numbers ``1`` - ``5``
* Use and item with ``U``
* Drop an item with ``D``
* Save game with ``S``
* Load game with ``L``
* Bring up the character screen with ``C``
* Cancel grid selection, character screen, etc. with ``Esc``

Tests
-----

To test install requirements

``pip install -r requirements``

and the package itself

``pip install -e .``

run tests

``pytest``


Contact the Maintainer: paul@cravenfamily.com
