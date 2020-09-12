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

![Coordinate update](videos/coordinateUpdate.gif)

&nbsp;
&nbsp;

![Random case1](videos/case1.gif)



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

- `c` : Toogle on/off the coordinate system renderer on the grid

- `n` : Toogle on/off the score system renderer on the grid
    - `Bottom left` &nbsp; &nbsp;: G score --> movement cost from current square to start square
    - `Bottom right`&nbsp; : H score --> movement cost from current square to end square
    - `Top left`&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; : F score --> total score (h + g = f)
&nbsp;
- `L_Shift+R` : Restart the game

- Left click or drag: Add walls (obstacles)
- Right click or drag: Remove walls

## TODO:

- [x] Put all the current colors of the squares in a dictionary for easy change of color choice
- [x] Reset visualizer option
- [ ] Refactor mouse and key handlers out of the main function (Clean it)
- [ ] Make a noticable notification for No solution found case and ended visualization (Maybe use Tkinter)
- [ ] Show time it took to find the path
- [ ] Optimize scores and coordinates renderer to handle different window sizes
- [ ] Add option for A* algorithm G, H and F scores on each square
- [ ] Make a separate window to handle the settings such as diagonals, coordinates etc.



