# Matricks
A semi-golfing language built around matrix operations

# Documentation
## How to run
 * `matricks.py <filename> [ARGS]`
 ### Command line arguments

| Argument | Default | Description |
|---|---|---|
| -a | `''` | Input matrix as a multi-line string, where `\n` is the newline character (entire string must be surrounded by quotes).|
| -A | 0 | Output matrix as a multi-line string, where each cell is converted to its corresponding ASCII character. |
| -i | `''` | Program input. |
| -m | `[[]]` |Input matrix in double-nested list form. |
| -P | 0 | Output matrix where each column is separated by a tab, and different rows are on different lines. |

##Program structure
 * 1 line of code, containing all commands and numbers.
 * Numbers must be distinguishable from each other by spaces

### Data types
 * Only 2 data types, 2d matrix and float
 * Float cast to 1x1 matrix containing value
 * Matrix cast to float as sum of elements

### Scope
 * New scopes created using `[...]`, `{...}`, or `<<...>,<...>>`
 * Code inside brackets evaulated to make new matrix
 * `[...]` starts with blank matrix
 * `{...}` starts with copy of current matrix
 * `<<..,..>,<..,..>>` interprets each command at each position to make a matrix
 
## Commands
 * All commands are prefix
 * All commands have a set number of arguments
 * Example: `m=rc5 5k|{}{X}`
  * `m` is taking `=rc`, `5`, and `5` as its arguments
   * `=` is taking `r` and `c` as its arguments.
    * `r` and `c` take no arguments
  * After `m` is evaluated, the interpreter moves on to `k`
  * `k` is taking `|` as its argument
   * `|` is taking `{}` and `{X}` as its arguments
    * `X` takes no arguments

| Command  | # args | Description  |
|---|---|---|
| m  |  3 [command f][float x][float y] | Makes a new matrix (x rows by y cols) with the formula (f) specified  |
| r  |  0 | Substitue row # in the forumla in `m`. Otherwise is the constant 32 |
| c  |  0 | Substitue col # in the formula in `m`. Otherwise is the constant 1  |
| F  |  3 [command f][float x][float y] | Runs a double-nested for loop `{0..y-1}{0..x-1}` with the formula specified |
| W  |  0 | Substitute row # in the formula in `F`. Otherwise is the constant 0 |
| Q  |  0 | Substitute col # in the formula in `F`. Otherwise is the constant 10 |
| L  |  0 | Substitue # of rows for current matrix  |
| l  |  0 | Substitue # of cols for current matrix  |
| k  |  1 [matrix x] | Sets to current matrix to `x`  |
| s  |  3 [float v][float r][float c] |  Sets the spot at `(r,c)` to `v` |
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
| q  |  2 [float d][float r] |  Slices the current matrix, cutting down `d` units and right `r` units from the top left. |
| z  |  2 [float u][float l] |  Slices the current matrix, cutting up `u` units and left `l` units from the bottom right. |
| '  |  1 [float f] | Prints out the ASCII character with value `f` (rounded towards negative infinity).  |
| y  | 0 |  Returns the next byte of input. 0 for no more input. |
| n  | 0 | Returns the next valid float from input. 0 for no more values. |
| N  | 0 | Returns the last input given out. If no input has been given yet, returns 0. |
| p  | 1 [matrix x] | Returns all elements in `x` multiplied together |
| d  | 1 [matrix x] | Returns all elements in `x` added together |
| ~  | 1 [float f] | Returns the bitwise not of `f` |
| ~  | 1 [matrix x] | Returns all elements of `x` bitwise not-ed. |
| Y  | 0  | Flips the current matrix on the y axis |
| X  | 0  | Flips the current matrix on the x axis |
| M  | 0  | Turns the current matrix left 90 degrees |
| R  | 0  | Turns the current matrix right 90 degrees |
| ?  | 2 [float a][float b]  | Returns a random number. Equvalent to `random.uniform(a,b)` |
| `_` | 1 [float a] | Returns the float rounded towards negative infinity |
| `_` | 1 [matrix x] | Returns a matrix with every element in the original rounded towards negative infinity |
| C  | 2 [matrix x][float f] | Returns 1 if `f` can be found in `x`, 0 otherwise. |
| ``` | 1 [float a] | Returns the float multiplied by -1 |
| ``` | 1 [matrix x] | Returns a matrix with every element in the original multiplied by -1 |

### Arithmetic commands

 * 1st arg is float and 2nd arg is float = 2 floats with the operation done
 * 1st arg is float and 2nd arg is matrix = operation applied to every value in matrix
  * It is the same the other way around
 * 1st arg is matrix and 2nd arg is matrix = Overlap where corresponding cells have the operation done
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
