<h1 align="center"> MicroKart </h1>
  

<p align="center">
  
  <img src="resources/sprite_itemmushroom.png" alt="MicroKart icon" width="90" height=auto>
</p>

<p align="center">
  <strong>A lightweight 2D kart racing game built with Python and Pyglet.</strong>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white">
  <img alt="Pyglet" src="https://img.shields.io/badge/Pyglet-1.5.7-2E8B57">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-macOS%20%7C%20Desktop-lightgrey">
</p>

## Overview

MicroKart is a retro-style kart racing game inspired by classic top-down and Mode 7-era racers. Players drive around pixel-art tracks, collect items, avoid hazards, and compete against another local player or CPU-controlled racers.

This improved version updates the original Python 2 project so it can run on modern Python environments, with compatibility fixes for newer macOS systems and basic CPU kart driving.

## Features

- 2D kart racing with sprite-based racers and track graphics
- Local two-player controls
- CPU-controlled racers using track beacon navigation
- Item pickups and usable power-ups
- Multiple track and character assets
- Zoomable race view
- Screenshot capture support

## Requirements

- Python 3
- `pyglet==1.5.7`
- macOS or another desktop environment with OpenGL/window support

Install dependencies:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Running The Game

From the project folder:

```sh
.venv/bin/python microkart.py
```

On macOS, you can also run:

```sh
./run_microkart.command
```

## Controls

| Action | Player 1 | Player 2 |
| --- | --- | --- |
| Accelerate | Up Arrow | W |
| Brake | Down Arrow | S |
| Turn Left | Left Arrow | A |
| Turn Right | Right Arrow | D |
| Jump | Space | X |
| Use Item | Enter | Left Shift |

Additional controls:

| Key | Action |
| --- | --- |
| Z | Change zoom |
| F3 | Save screenshot |
| 1-8 | Give Player 1 a test item |
| T | Spin Player 1 |

## How It Works

MicroKart uses Pyglet for the window, rendering, keyboard input, sprites, and the main game loop. Track data is loaded from image and PGM files in `resources/tracks`, while kart sprites and item graphics are loaded from `resources/characters` and `resources`.

The race system is split into small modules:

| File | Purpose |
| --- | --- |
| `microkart.py` | Game entry point, window setup, input handling, and main loop |
| `race.py` | Race state, lap timer, racer list, and update flow |
| `racer.py` | Player/CPU racer state, item handling, and CPU driving logic |
| `car.py` | Kart physics, movement, collision, jumping, and status effects |
| `track.py` | Track loading, terrain detection, item blocks, beacons, and hazards |
| `items.py` | Power-ups and moving item particles |
| `ui.py` | Side panel, racer icons, lap display, and camera/zoom behavior |
| `vector.py` | 2D vector math and grid path helpers |

## Project Status

This is a modernized version of an older Python 2 game. The current build includes compatibility fixes for Python 3, updated resource loading, and simple CPU racers. Some behavior may still feel experimental because the game comes from an older codebase.

## Credits

Original Python 2 game by **Zanapher**. Recreated by **kprosoft21** for python 3.
