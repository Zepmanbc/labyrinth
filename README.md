# Labyrinthe

---

## 1. Presentation

I made this Maze game to learn python and pyganme.

There is 3 sizes of mazes, each is generated randomly. the Goal is to reach the treasure with the less moves (not a big chalenge...). The treasure is positionned at the end of the longuest path.

## 2. Installation
clone the repo
> git clone 

go in the folder
> cd labyrinth

create a virtual environment
> virtualenv env -p python3

install requirements
> pip install -r requirements.txt

allow execution of the game
> chmod +x main.py

## 3. How to play
launch the game
> ./main.py

_Title menu_

![Main title](doc/title.png)

Use arrow keys tu go **up** or **down**

Select with ̀**Enter**

press **Q** if you want to go back to title menu

_Small Maze 10x10_

![Small Maze](doc/small.png)

_Medium Maze 15x13_

![Medium Maze](doc/medium.png)

_Large Maze 21x15_

![Large Maze](doc/large.png)

When you reach the treasure, the game is over.

Red dots show you the shorter path.

![You Win](doc/win.png)

## 4. Code notes

_to do..._

## 5. To do list

* Stop the game when the treasure has been reached
* Lean that there is a 'e' at the end of labyrinthe
* add a time record
* record best times with longuest path?
* any idea for cool feature ? tell me