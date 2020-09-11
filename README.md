# A* Pathfinding visualizer
The idea of this project is for it to be a interesting new way to teach myself more advanced algorithms.Starting with A* pathfinding algorithm.


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

- `c` : Toogle on/off the coordinate system on the grid

- Left click or drag: Add walls (obstacles)
- Right click or drag: Remove walls

## TODO:

- [ ] Fix bug of inserting node on a wall (This should not be possible)
- [ ] Put all the current colors of the squares in a dictionary
- [ ] Reset visualizer option
- [ ] Make a noticable notification for No solution found case and ended visualization (Maybe use Tkinter)
- [ ] Show time it took to find the path
- [ ] Add option for A* algorithm G, H and F scores on each square



