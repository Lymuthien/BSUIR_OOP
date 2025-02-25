# LAB 1
Completed by Kozlova Tatsiana, group 353504

## Functional requirements

The program must be able to draw 3 types of figures:
rectangle, triangle, ellipse; destroy, fill, move them.

_Warning: all numeric input values must be integers._

_Objects may be displayed with altered proportions due to the 
peculiarities of console output._

### Menu

* _0_ - exit (without saving)
* _1_ - choose figure for drawing
  * _1_ - rectangle
  * _2_ - triangle
  * _3_ - ellipse
  * _0_ - exit
* _2_ - object selection menu
  * _i_ - info
  * _left arrow_ - previous object
  * _right arrow_ - next object
  * _m_ - move
    * _d_ - by directions
    * _c_ - by new coords
  * _e_ - erase
  * _bg_ - change background
  * _0_ - exit
* _3_ - save file
* _4_ - load file
* _5_ - undo action
* _6_ - redo action

### Drawing

Coordinate axes for figures come from the upper left
corner to the right and down. Figures must be in canvas
space (their coordinates). 

To draw choose type (_1, 2, 3_). Then enter:

* For rectangle - x, y, width, height. (x, y) - coordinates
of the top left corner. 
* For triangle - x1, y1, x2, y2, x3, y3. (xi, yi) - coordinates
of the corner point.
* For ellipse - x, y, r1, r2. (x, y) - coordinates of the top
left corner of enclosing rectangle, r1 - horizontal radius, r2 -
vertical radius.

### Choosing existing objects

To go for object selection menu, enter _1_. You will see current 
object id. To see info about object enter _i_. To select other 
object use arrow keys (_left, right_). To move enter _m_. To erase
enter _e_. To change background enter _bg_.

### Information about objects

For every object should be printed type of it, its background.
* For rectangle - (x, y), width, height, square, perimeter.
* For triangle - (x1, y1), (x2, y2), (x3, y3) (as soon), square, 
perimeter, length of every side.
* For ellipse - (x, y), r1, r2 (as soon), square, perimeter.

### Moving objects

After entering _m_, you can move object to different directions (_d_)
or by entering new coordinates (_c_). 

If object is moving by direction (everyone), you must enter x-shift,
y-shift. To move left/up enter negative values, right/down - positive.

If object is moving with new coordinates, enter:
* For rectangle - x, y - new coords of the top left corner
* For triangle - x, y - new coords of the topmost(+leftmost) corner
* For ellipse - x, y - new coords of the top left corner of 
enclosing rectangle

### Changing background

After entering _bg_ print RGB-format color (#xxxxxx).

### Saving file 

Enter name of file (possibly with a pass) to save it.

### Loading file

Enter existing name of file (possibly with a pass) to load it.

### Undo/redo actions

Until you close the file, the history of all actions for the current
session is saved.
If you undo action and perform a new one, you will not be able to
restore the old history. 