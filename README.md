<h1 align="center" style="font-size: 2.5rem;">
A* Pathfinding Visualizer
</h1>


*insert some project description here*

## Installation

Clone this repo

```bash
git clone https://github.com/emanuel2718/AstarPathfinding
cd AstarPathfinding
```

Install requirements

```bash
pip install -r requirements.txt
```

## Preview

![Premade](videos/premade.gif)

&nbsp;
&nbsp;

![Custom](videos/custom.gif)



## How to use
Run the visualizer:
```bash
python main.py
```
### Command line argument options:

Diagonal movement during the A* star algorithm
```bash
python main.py -d
```

&nbsp;
### Keybindings:

- `s` : Add starting node (hover over desired square and press the key)

- `e` : Add ending node (hover over desired square and press the key)

- `i` : Invert grid background color (White -> Black or Blac -> White)

- `c` : Toogle on/off the coordinate system renderer on the grid

- `?` : Toogle on/off keybinds help panel

- `n` : Toogle on/off the score system renderer on the grid
    - `Bottom left` &nbsp; &nbsp;: G score --> movement cost from current square to start square
    - `Bottom right`&nbsp; : H score --> movement cost from current square to end square
    - `Top left`&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; : F score --> total score (h + g = f)
&nbsp;
- `Esc` : Toogle on/off the settings panel

- `L_Shift+R` : Restart the game


- Left click or drag: Add walls (obstacles)
- Right click or drag: Remove walls

## TODO:

- [ ] Add close game keybind (i.e press 'q' to quit)
- [ ] Make it possible to de-select an initial node with right click (like the walls)
- [ ] Show notification with a tkinter window
- [ ] Make the UI look more polished (i.e Settings panel, keybinds panel etc.)
- [ ] Make a better settings panel (interactive with buttons)
- [ ] Refactor majority of the code (Mouse and key handlers etc.)
- [ ] Show time it took to find the path
- [ ] Optimize scores and coordinates renderer to handle different window sizes



