A console implementation of the classic minesweeper game

## How to use
### Clone the repo
```bash
git clone https://github.com/lee-ros/minesweeper.git
```

### Install the package
```bash
# inside repo directory
pip install -e .
```
### Run
```bash
minesweeper
```

## Game Instructions:
To win the game one must find all the mines that are spread around the board.
To accomplish this goal the player needs to move around the board, open the cells and avoid the mines in it's way.
The numbers on the opened cells represent the number of mines surrounding the cell. Each cell can have a maximum of 8
mines around it.
Blank cells, cell with no surrounding mines, are expanded and expose a larger area of the board.
Use the above knowledge to open cells, mark the mines found and win the board!


## TODO
- [ ] Add a timer for the board statistics
- [ ] Add score board