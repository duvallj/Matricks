# Matricks
A semi-golfing language built around matrix operations

# Documentation
### How to run
 * `matricks.py <filename> <matrix> <input> [flags]`
  * Matrix will be padded with 0s to become retangular if it is not already.
  * `--asciiprint`: Prints values of cells as ascii characters formatted in a rectangle with newlines. 0 is assumed to be a single space.
  * `--prettyprint`: Prints numerical values of the cells.
  * `--asciiinput`: Instead of reading matrix of numerical values, read as the value of the ascii charactes. `[],\` are special, need to be escaped with `\`.

### File structure
* **Matricks** programs are made up of multiple lines
* Command pointer for each line starts at 0
* Commands are read one at a time from each line
* Lines are read until end of line reached
* Memory starts out as 0x0 matrix

### Data types
 * Only 2 data types, 2d matrix and float
 * Float cast to 1x1 matrix containing value
 * Matrix cast to float as sum of elements

### Scope
 * New scopes created using `[...]` or `{...}`
 * Code inside brackets evaulated to make new matrix
 * `[...]` starts with blank matrix
 * `{...}` starts with copy of current matrix

## Commands
 * All non-arithmetic commands take arguments like so: `<command>:<arg1>:<arg2>;`
  * Empty arguments are assumed to be 0
  * However, all args must exist

| Command  | # args | Description  |
|---|---|---|
| m  |  3 [expression f][float x][float y] | Makes a new matrix (x rows by y cols) with the formula (f) specified  |
| r  |  0 | Substitute row # in the forumla in `m` |
| c  |  0 | Substitute col # in the formula in `m`  |
| F  |  3 [expression f][float x][float y] | Runs a double-nested for loop `{0..y-1}{0..x-1}` with the formula specified |
| W  |  0 | Substitute row # in the formula in `F` |
| Q  |  0 | Substitute col # in the formula in `F` |
| L  |  0 | Substitute # of rows for current matrix  |
| l  |  0 | Substitute # of cols for current matrix  |
| k  |  1 [matrix x] | Sets to current matrix to `x`  |
| s  |  3 [float r][float c][float v] |  Sets the spot at `(r,c)` to `v` |
| g  |  2 [float r][float c] |  Gets the value at `(r,c)` |
| j  |  1 [float n] | Jumps to line number `n`  |
| i  |  3 [float e][expression t][expression f] | If `e` evaluates to anything but 0, expression `t` is evaluated. Otherwise, expression `f` is evaluated.  |
| a  |  1 [matrix x] |  Adds matrix `x` to the right of the current matrix (think "after") |
| b  |  1 [matrix x] |  Adds matrix `x` to the right of the current matrix ("before")|
| v  |  1 [matrix x] |  Adds matrix `x` above the current matrix ("aboVe")|
| u  |  1 [matrix x] |  Adds matrix `x` below the current matrix ("beloU"?)|
| A  |  1 [float u] | Rotates the current matrix right by `u` units  |
| B  |  1 [float u] | Rotates the current matrix left by `u` units  |
| V  |  1 [float u] | Rotates the current matrix up by `u` units  |
| U  |  1 [float u] | Rotates the current matrix down by `u` units  |
| q  |  2 [float d][float l] |  Slices the current matrix, cutting down `d` units and right `r` units from the top left. |
| z  |  2 [float u][float r] |  Slices the current matrix, cutting up `u` units and left `l` units from the bottom right. |
| "  |  1 [character c] | Returns the ASCII value of `c`.  |
| '  |  1 [float f] | Prints out the ASCII character with value `f`.  |
| y  | 0 |  Returns the next byte of input. 0 for eof |
| n  | 0 | Returns the next valid float from input. 0 for no more values. |
| p  | 1 [matrix x] | Returns all elements in `x` multiplied together |
| d  | 1 [matrix x] | Returns all elements in `x` added together |
| ~  | 1 [float f] | Returns the bitwise not of `f` |
| ~  | 1 [matrix x] | Returns all elements of `x` bitwise not-ed. |
| w  | 1 [float f] | Rotates the current matrix up `f` units |
| x  | 1 [float f] | Rotates the current matrix down `f` units |
| I  | 1 [float f] | Rotates the current matrix left `f` units |
| K  | 1 [float f] | Rotates the current matrix right `f` units |
| Y  | 0  | Flips the current matrix on the y axis |
| X  | 0  | Flips the current matrix on the x axis |
| M  | 0  | Turns the current matrix left 90 degrees |
| R  | 0  | Turns the current matrix right 90 degrees |
| ?  | 2 [float a][float b]  | Returns a random number. Equvalent to `random.uniform(a,b)` |
| `_` | 1 [float a] | Returns the float rounded towards negative infinity |
| `_` | 1 [matrix x] | Returns a matrix with every element in the original rounded towards negative infinity |

* All arithmetic commands have arguments on the right and left sides, like so: `<arg1><command><arg2>`
  * Empty arguments with throw an error
* 1st arg is float
 * 2nd arg is float = 2 floats with the operation done
 * 2nd arg is matrix = operation applied to every value in matrix
* 1st arg is matrix
 * 2nd arg is matrix = Overlap where corresponding
* Boolean operators return 1 for true and 0 for false.
  
|  Command |  Description |
|---|---|
| P  |  Needs 2 matricies. Returns product |
| D  |  Needs 2 matricies. Returns sum |
| `+`  |  Sum |
| `-`  |  Difference |
| `*`  |  Product |
| `/`  |  Quotient |
| `%`  |  Modulus |
| `^`  |  Exponent |
| `&`  |  Bitwise AND |
| `|`  |  Bitwise OR |
| `$`  |  Bitwise XOR |
| `=`  |  Equals |
| `!`  |  Not euals |
| `e`  |  Less than |
| `E`  |  Less than or equal to |
| `t`  |  Greater than |
| `T`  |  Greater than or equal to |
