""" Provides functionalilty for working with celled hypercubes.

Hypercubes are extensions of lines, squares and cubes into higher dimensions.
Celled hypercubes can be thought as a grid or lattice structure.
From this point, hypercubes is used to mean celled hypercubes.

A celled hypercube can be described by its dimension and the number of
cells in any dimension. We denote this as h(d, n).
For example: h(2, 3) is a 3x3 grid; h(3, 4) is a 4x4x4 lattice.
A hypercube of dimension d may also be referred to as a d-cube.

A cell's position can be specified in coordinate style. 
For example, given h(3, 4) then some valid coordinates are (1,1,1), 
(2,1,3) and (4,4,4).

The term m-agonal is a shortened function version of 
"m-dimensional diagonal". So in 3-cube you would find a 1-agonal, 2-agonal
and 3-agonal. A 1-agonal is customarily known as a row, column or pillar. 
If 3 coordinates change in an 5-cube, while the others remain constant, this
constitutes a 3-agonal.
For a given h(d, n), 1 <= m <= n, a m-agonal always has n cells.

The term line is used to refer to any m-agonal in general.

A cell apppears in multiple lines, which are refered to as the 
scope of the cell.

The combination of lines and cell scopes is referred to
as the structure of the hypercube.

This module essentially has 2 classes of functions:
1. Those that use a numpy ndarray to implement the underlying
hypercube. These functions have the suffix _np. An array of d dimensions 
may be referred to as a d-array
2. Those that do not implement the undelying hypercube but
provide information as coordinates that can be used with
a user-implementation of the hypercube. These funtions have
the suffix _coord.
"""


# numpy and scipy don't yet have type annotations
import numpy as np 
from scipy.special import comb
import itertools as it
import numbers
import re
from collections import defaultdict, Counter as counter
from typing import List, Callable, Union, Collection, Tuple, Any, DefaultDict, TypeVar, Counter, Dict, Iterable

Cell_coord = Tuple[int, ...]

Cube_np = TypeVar('Cube_np', np.ndarray, np.ndarray) # line should really be a numpy array representing h(d, n)
Line_np = TypeVar('Line_np', np.ndarray, np.ndarray) # line should really be a 1d numpy array with n elements
Lines_np = List[Line_np]
Scopes_np = DefaultDict[Cell_coord, Lines_np]  
Structure_np = Tuple[Cube_np, Lines_np, Scopes_np]

Line_coord = List[Cell_coord]
Lines_coord = List[Line_coord]
Scopes_coord = DefaultDict[Cell_coord, Lines_coord]
Structure_coord = Tuple[Lines_coord, Scopes_coord]

Scopes = Union[Scopes_np, Scopes_coord]

def num_lines(d: int, n: int) -> int: 
    """ Calculate the number of lines in a hypercube.  

    Parameters
    ----------
    d : int
        The number of dimensions of the hypercube
    n : int
        The number of cells in any dimension
 
    Returns
    -------
    int:
        The number of lines in a hypercube h(d, n).

    Notes
    -----
    Consider a hypercube h(d, n).
    Let l be the number of lines, then

        l = sum{i=1, i=d} [ dCi * n^(d-i) * (2^i)/2 ]

    where dCi is 'd choose i'.

    Sketch of proof:
    Let l_i be the number of i-agonal lines (exist in exactly i dimensions).
    For example, consider the following square (2-cube):

        [[0, 1],
         [2, 3]]

    The 1-agonal lines are [0, 1], [2, 3], [0, 2] and [1, 3] and l_1 = 4.  
    The 2-agonal lines are [0, 3] and [1, 2]  and l_2 = 2.
    
    Hence l = l_1 + l_2 = 6

    It is trivially true that the l is the sum of l_i, i.e.,

        l = sum{i=1, i=d} l_i

    Next we show how l_i can be calculated. Firstly, we argue
    that the distinct number of h(i, n) is dCi * n^(d-i).
    
    The number of ways of choosing i dimensions from d is dCi.
    For example if d=3 and i=2, then the 3 combinations of 
    2 dimensions (squares) are (1, 2), (1, 3) and (2, 3).

    The number of remaining dimensions is d-i, and the number of cells
    in these dimensions is n^(d-i). Any one of theses cells could be 
    fixed relative to a given i-dimensional hypercube, h(i, n).

    Hence the distinct number of h(i, n) is dCi * n^(d-i).

    Finally, for any h(i, n), the number of i-agonal lines is (2^i)/2. 
    This is because an i-cube has 2^i corners and a line has 2 corners.

    Hence l_i = dCi * n^(d-i) * (2^i)/2 and thus:

        l = sum{i=1, i=d} [ dCi * n^(d-i) * (2^i)/2 ]
  
    Examples
    --------
    >>> num_lines(2, 3)
    8
    >>> num_lines(3, 4)
    76
    """

    count = 0
    for i in range(1, d + 1):
        count += comb(d, i, True) * (n ** (d - i)) * (2 ** (i - 1)) 
    return count


def get_diagonals_np() -> Callable[[Cube_np], Lines_np]:
    """ Returns a function that calculates the d-agonals of a d-array. 
    The returned function has the following structure:

    Parameters
    ----------
    arr : numpy.ndarray
        A d-array whose d-agonals are to be calculated

    Returns
    -------
    list :
        A list of numpy.ndarray views of the d-gonals of `arr`.

    Notes
    -----
    The number of corners of `arr` is 2^d. The number of d-agonals 
    is 2^d / 2 since two connecting corners form a line. 

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.arange(8).reshape(2, 2, 2)
    >>> arr
    array([[[0, 1],
            [2, 3]],
    <BLANKLINE>
           [[4, 5],
            [6, 7]]])
    >>> diagonals = get_diagonals_np()
    >>> diags = diagonals(arr)
    >>> diags
    [array([0, 7]), array([1, 6]), array([4, 3]), array([5, 2])]
    >>> arr[0, 0, 0] = 99
    >>> diags
    [array([99,  7]), array([1, 6]), array([4, 3]), array([5, 2])]

    Note that the diagonals function returned by get_diagonals maintains
    the list of diagonals returned between invocations.
    >>> arr = np.arange(2)
    >>> arr
    array([0, 1])
    >>> diagonals = get_diagonals_np()
    >>> diags = diagonals(arr)
    >>> diags
    [array([0, 1])]
    >>> diags = diagonals(arr)
    >>> diags
    [array([0, 1]), array([0, 1])]

    Call get_diagonals again in order to clear the list of 
    returned diagonals.
    >>> get_diagonals_np()(arr)
    [array([0, 1])]
    >>> get_diagonals_np()(arr)
    [array([0, 1])]
    """
    
    # The diagonals function is recursive. How it works is best shown by example.
    # 1d: arr = [0, 1] then the diagonal is also [0, 1].
    
    # 2d: arr = [[0, 1],
    #            [2, 3]]
    # The numpy diagonal method gives the main diagonal = [0, 3], a 1d array
    # which is recursively passed to the diagonals function.
    # To get the opposite diagonal we first use the numpy flip function to
    # reverse the order of the elements along the given dimension, 0 in this case.
    # This gives [[2, 3],
    #              0, 1]]
    # The numpy diagonal method gives the main diagonal = [2, 1], a 2d array
    # which is recursively passed to the diagonals function.

    # 3d: arr = [[[0, 1],
    #             [2, 3]],
    #            [[4, 5],
    #             [6, 7]]]
    # The numpy diagonal method gives the main diagonals in the 3rd dimension
    # as rows.
    #            [[0, 6],
    #             [1, 7]]
    # Note that the diagonals of this array are [0, 7] and [6, 1] which are
    # retrieved by a recurive call to the diagonals function.
    # We now have 2 of the 4 3-agonals of the orginal 3d arr.
    # To get the opposite 3-agonals we first use the numpy flip function which
    # gives
    #           [[[4, 5],
    #             [6, 7]],
    #            [[0, 1],
    #             [2, 3]]]
    # and a call to the numpy diagonal method gives
    #            [[4, 2],
    #             [5, 3]]
    # The diagonals of this array are [4, 3] and [2, 5]
    # We now have all 4 3-agonals of the original 3d arr.

    diags: Lines_np = []
    
    def diagonals_np(arr: Cube_np) -> Lines_np:
        if arr.ndim == 1:
            diags.append(arr)
        else:
            diagonals_np(arr.diagonal())
            diagonals_np(np.flip(arr, 0).diagonal())
        return diags

    return diagonals_np


def get_lines_grouped_np(arr: Cube_np) -> Tuple[List[Lines_np], int]: 
    """ Returns the lines in an array grouped by dimension

    Parameters
    ----------
    arr : numpy.ndarray
        The array whose lines are to be calculated

    Returns
    -------
    list :
        A list of numpy.ndarray views of the lines in `arr`.
        List is nested list of i-agonals
    int :
        The number of lines. 
            
    Raises
    ------
    AssertionError
        If number of lines returned by this function does not
        equal that calculated by the num_lines function.
        THIS IS A CRITCAL ERROR THAT MEANS THIS FUNCTION HAS
        A FLAWED IMPLEMENTATION.
    
    See Also
    --------
    num_lines
    get_diagonals_np

    Notes
    -----
    The notes section for the function num_lines provides a sketch of a 
    constructive proof for the number of lines in a hypercube. This has
    been used to implement this function. 

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.arange(4).reshape(2, 2)
    >>> arr
    array([[0, 1],
           [2, 3]])
    >>> lines, count = get_lines_grouped_np(arr)
    >>> lines
    [[array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3])], [array([0, 3]), array([2, 1])]]
    >>> count
    6
    >>> len(lines)
    2
    >>> arr[0, 0] = 99
    >>> lines
    [[array([99,  2]), array([1, 3]), array([99,  1]), array([2, 3])], [array([99,  3]), array([2, 1])]]
    """
    
    d = arr.ndim
    n = arr.shape[0]
    lines = []
    count = 0

    # loop over the numbers of dimensions
    for i in range(d):
        lines_i = [] 
        # loop over all possible combinations of i dimensions
        for i_comb in it.combinations(range(d), r = i + 1): 
            # a cell could be in any position in the other dimensions
            other_d = set(range(d)) - set(i_comb)
            for cell in it.product(range(n), repeat = d - i - 1):
                # take a slice of i dimensions given cell
                sl = slice_ndarray(arr, other_d, cell)
                # get all possible lines from slice
                diags = get_diagonals_np()(sl)
                count += len(diags)
                lines_i.extend(diags)

        lines.append(lines_i)

    assert count == num_lines(d, n)
    return lines, count


def get_lines_flat_np(arr: Cube_np) -> Lines_np: 
    """ Returns the lines in an array

    Parameters
    ----------
    arr : numpy.ndarray
        The array whose lines are to be calculated

    Returns
    -------
    list :
        A list of numpy.ndarray views of the lines in `arr`.
                
    See Also
    --------
    get_lines_grouped_np
    num_lines
    get_diagonals_np

    Notes
    -----
    Calls the function get_lines_grouped_np.

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.arange(4).reshape(2, 2)
    >>> arr
    array([[0, 1],
           [2, 3]])
    >>> lines = get_lines_flat_np(arr)
    >>> lines
    [array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3]), array([0, 3]), array([2, 1])]
    >>> len(lines)
    6
    >>> arr[0, 0] = 99
    >>> lines
    [array([99,  2]), array([1, 3]), array([99,  1]), array([2, 3]), array([99,  3]), array([2, 1])]
    """

    grouped = get_lines_grouped_np(arr)[0]
    flat = [x for y in grouped for x in y]
    return flat


def get_scopes_np(lines: Lines_np, d: int) -> Scopes_np:
    """ Calculate the scope of each cell in a hypercube

    Parameters
    ----------
    lines : list
        The returned value from get_lines_flat_np(arr) where arr is of the
        form np.arange(n ** d, dtype = int64).reshape([n] * d).
        That is, arr is populated with the values 0,1,2,...,n^d - 1.

    dim : int 
        The dimension of the array (hypercube) that was used to
        generate the `lines` parameter.

    Returns
    -------
    defaultdict :
        A dictionary with keys equal to each cell coordinates of the 
        hypercube. For each cell key, the value is cell's
        scope - a list of numpy.ndarray views that are lines containing
        the cell.
            
    See Also
    --------
    get_lines_flat_np

    Notes
    -----
    The implementation of this function uses np.unravel_index, and relies
    uopn the lines parameter being generated from an array populated with
    values 0,1,2,...
 
    Examples
    --------
    >>> import numpy as np
    >>> from pprint import pprint
    >>> arr = np.arange(4).reshape(2, 2)
    >>> arr
    array([[0, 1],
           [2, 3]])
    >>> lines = get_lines_flat_np(arr)
    >>> lines
    [array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3]), array([0, 3]), array([2, 1])]
    >>> scopes = get_scopes_np(lines, 2)
    >>> pprint(scopes) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [array([0, 2]), array([0, 1]), array([0, 3])],
                 (0, 1): [array([1, 3]), array([0, 1]), array([2, 1])],
                 (1, 0): [array([0, 2]), array([2, 3]), array([2, 1])],
                 (1, 1): [array([1, 3]), array([2, 3]), array([0, 3])]})
    >>> arr[0, 0] = 99
    >>> pprint(scopes) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [array([99,  2]), array([99,  1]), array([99,  3])],
                 (0, 1): [array([1, 3]), array([99,  1]), array([2, 1])],
                 (1, 0): [array([99,  2]), array([2, 3]), array([2, 1])],
                 (1, 1): [array([1, 3]), array([2, 3]), array([99,  3])]})  
    """
    
    n = lines[0].size
    shape = [n] * d
    scopes: DefaultDict = defaultdict(list)

    for line in lines:
        for j in range(n):
            cell = np.unravel_index(line[j], shape)
            scopes[cell].append(line) 
    return scopes


def structure_np(d: int, n: int, zeros: bool = True, OFFSET: int = 0) -> Structure_np:
    """ Return a celled hypercube, its lines, and the scopes of its cells.

    Parameters
    ----------
    d : int
        The number of dimensions of the hypercube
    n : int
        The number of cells in any dimension
    zeros: bool, default = True
        If true, all values in array are 0, else they are 0,1,2,...
    base: int
        Tne number of cells is n^d. If this greater than 
        (2^31 - OFFSET - 1) then we use np.int64 (instead of np.int32)
        as the dtype  of numpy array.
 
    Returns
    -------
    tuple :
        A tuple containing the hypercube, its lines, and the scopes of
        its cells.
            
    See Also
    --------
    get_lines_flat_np
    get_scopes_np
 
    Examples
    --------
    >>> import numpy as np
    >>> from pprint import pprint
    >>> struct = structure_np(2, 2) 
    >>> struct[0]
    array([[0, 0],
           [0, 0]])
    >>> struct[1]
    [array([0, 0]), array([0, 0]), array([0, 0]), array([0, 0]), array([0, 0]), array([0, 0])]
    >>> pprint(struct[2]) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [array([0, 0]), array([0, 0]), array([0, 0])],
                 (0, 1): [array([0, 0]), array([0, 0]), array([0, 0])],
                 (1, 0): [array([0, 0]), array([0, 0]), array([0, 0])],
                 (1, 1): [array([0, 0]), array([0, 0]), array([0, 0])]})
    >>> struct = structure_np(2, 2, False) 
    >>> struct[0]
    array([[0, 1],
           [2, 3]])
    >>> struct[1]
    [array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3]), array([0, 3]), array([2, 1])]
    >>> pprint(struct[2]) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [array([0, 2]), array([0, 1]), array([0, 3])],
                 (0, 1): [array([1, 3]), array([0, 1]), array([2, 1])],
                 (1, 0): [array([0, 2]), array([2, 3]), array([2, 1])],
                 (1, 1): [array([1, 3]), array([2, 3]), array([0, 3])]})
    """

    # number of cells is n^d. If this greater than (2^31 - OFFSET - 1)
    # then we use int64. This is because the the get_scopes 
    # function populates the arrays with values 0,1,2, ...
    dtype = np.int64 if n ** d > 2 ** 31 - OFFSET - 1 else np.int32
    arr = np.arange(n ** d, dtype = dtype).reshape([n] * d)
    lines = get_lines_flat_np(arr)
    scopes = get_scopes_np(lines, d)
    if zeros:
        arr.fill(0)
    return (arr, lines, scopes)


def get_diagonals_coord(d: int, n: int) -> Lines_coord:
    """ Returns the d-agonals coordinates of h(d, n). 

    Parameters
    ----------
    d : int
        The number of dimensions of the hypercube
    n : int
        The number of cells in any dimension

    Returns
    -------
    list :
        A list of d-gonals coordinates of the diagonals in h(d,n).

    See Also
    --------
    num_lines
    get_diagonals_np

    Notes
    -----
    The number of corners of h(d, n) is 2^d. The number of d-agonals 
    is 2^d / 2 since two connecting corners form a line. 

    Examples
    --------
    >>> diags = get_diagonals_coord(2, 3)
    >>> diags
    [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
    """    
    
    # comments below use an example with h(2, 3)

    # get an iterator of all corners. E.g.: (0,0), (0,2), (2,0), (2,2)
    corners_all = it.product([0, n - 1], repeat = d)
    # restrict to corners with 0 as first coordinate. E.g.: (0,0), (0,2)
    corners_0 = [corner for corner in corners_all if corner[0] == 0]

    diagonals = []
    for corner in corners_0: 
        # create the diagonals for each corner
        diagonal: Line_coord = []
        diagonal.append(corner) # add corner as first cell in diagonal
        # add rest of diagonal
        for i in range(1, n): 
            # find next cell. Start by decrementing coords.
            # E.g.: (0,0) -> (-1,-1); (0,2) -> (-1,1)
            # E.g.: (0,0) -> (-2,-2); (0,2) -> (-2,0)
            tmp = tuple(c - i for c in corner)
            # Take absolute values of coords. 
            # E.g.: (-1,-1) -> (1,1); (-1,1) -> (1,1)
            # E.g.: (-2,-2) -> (2,2); (-2,0) -> (2,0) 
            coords = tuple(abs(t) for t in tmp)
            diagonal.append(coords)
        diagonals.append(diagonal)

    return diagonals


def get_lines_grouped_coord(d: int, n: int) -> Tuple[List[Lines_coord], int]: 
    """ Returns the lines in a hypercube, h(d, n) grouped by dimensdion

    Parameters
    ----------
    d : int
        The number of dimensions of the hypercube
    n : int
        The number of cells in any dimension

    Returns
    -------
    list :
        A list of d-gonals coordinates for the lines in h(d, n).
    int :
        The number of lines. 
            
    Raises
    ------
    AssertionError
        If number of lines returned by this function does not
        equal that calculated by the num_lines function.
        THIS IS A CRITCAL ERROR THAT MEANS THIS FUNCTION HAS
        A FLAWED IMPLEMENTATION.
    
    See Also
    --------
    num_lines
    get_digonals_coord

    Notes
    -----
    The notes section for the function num_lines provides a sketch of a 
    constructive proof for the number of lines in a hypercube. This has
    been used to implement this function. 

    Examples
    --------
    >>> lines, count = get_lines_grouped_coord(2, 2)
    >>> lines
    [[[(0, 0), (1, 0)], [(0, 1), (1, 1)], [(0, 0), (0, 1)], [(1, 0), (1, 1)]], [[(0, 0), (1, 1)], [(0, 1), (1, 0)]]]
    >>> count
    6
    >>> len(lines)
    2
    """
    
    lines = []
    count = 0

    # loop over the numbers of dimensions
    for i in range(d): 
        lines_i = []
        # loop over all possible combinations of i dimensions
        diagonals = get_diagonals_coord(i + 1, n)
        for i_comb in it.combinations(range(d), r = i + 1): 
            # a cell could be in any position in the other dimensions
            other_d = set(range(d)) - set(i_comb)
            for cell in it.product(range(n), repeat = d - i - 1):                                  
                diags: Lines_coord = []
                for diagonal in diagonals:
                    diag = []
                    for c in diagonal:
                        diag.append(insert_into_tuple(c, other_d, cell))
                    diags.append(diag)
                    
                count += len(diags)
                lines_i.extend(diags)
        
        lines.append(lines_i)
    
    assert count == num_lines(d, n)
    return lines, count


def get_lines_flat_coord(d: int, n: int) -> Lines_coord: 
    """ Returns the lines in a hypercube, h(d, n)

    Parameters
    ----------
    d : int
        The number of dimensions of the hypercube
    n : int
        The number of cells in any dimension

    Returns
    -------
    list :
        A list of d-gonals coordinates for the lines in h(d, n).
                
    See Also
    --------
    get_lines_grouped_coord
    num_lines
    get_diagonals_coord

    Notes
    -----
    Calls the function get_lines_grouped_coord

    Examples
    --------
    >>> lines = get_lines_flat_coord(2, 2)
    >>> lines
    [[(0, 0), (1, 0)], [(0, 1), (1, 1)], [(0, 0), (0, 1)], [(1, 0), (1, 1)], [(0, 0), (1, 1)], [(0, 1), (1, 0)]]
    >>> len(lines)
    6
    """
    
    grouped = get_lines_grouped_coord(d, n)[0]
    flat = [x for y in grouped for x in y]
    return flat


def get_scopes_coord(lines: Lines_coord, d: int) -> Scopes_coord:
    """ Calculate the scope of each cell in a hypercube

    Parameters
    ----------
    lines : list
        The first returned value from get_lines_coord(d, n).

    dim : int 
        The dimension of the hypercube that was used to
        generate the `lines` parameter.

    Returns
    -------
    defaultdict :
        A dictionary with keys equal to each cell coordinates of the 
        hypercube. For each cell key, the value is cell's
        scope - a list of coordinates that are lines containing
        the cell.
            
    See Also
    --------
    get_lines_coord
 
    Examples
    --------
    >>> from pprint import pprint
    >>> lines = get_lines_flat_coord(2, 2)
    >>> pprint(lines) #doctest: +NORMALIZE_WHITESPACE
    [[(0, 0), (1, 0)],
     [(0, 1), (1, 1)],
     [(0, 0), (0, 1)],
     [(1, 0), (1, 1)],
     [(0, 0), (1, 1)],
     [(0, 1), (1, 0)]]
    >>> scopes = get_scopes_coord(lines, 2)
    >>> pprint(scopes) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [[(0, 0), (1, 0)], [(0, 0), (0, 1)], [(0, 0), (1, 1)]],
                 (0, 1): [[(0, 1), (1, 1)], [(0, 0), (0, 1)], [(0, 1), (1, 0)]],
                 (1, 0): [[(0, 0), (1, 0)], [(1, 0), (1, 1)], [(0, 1), (1, 0)]],
                 (1, 1): [[(0, 1), (1, 1)], [(1, 0), (1, 1)], [(0, 0), (1, 1)]]})
    """

    n = len(lines[0])
    scopes: DefaultDict = defaultdict(list)
    cells = it.product(range(n), repeat = d) # get all possible cells

    for cell in cells:
        for line in lines:
            if cell in line:
                scopes[cell].append(line)
    return scopes


def structure_coord(d: int, n: int) -> Structure_coord:
    """ Return lines, and the scopes of its cells, for h(d, n)

    Parameters
    ----------
    d : int
        The number of dimensions of the hypercube
    n : int
        The number of cells in any dimension
 
    Returns
    -------
    tuple :
        A tuple lines, and the scopes of its cells, for h(d, n)
            
    See Also
    --------
    get_lines_flat_coord
    get_scopes_coord
 
    Examples
    --------
    >>> from pprint import pprint
    >>> struct = structure_coord(2, 2) 
    >>> struct[0]
    [[(0, 0), (1, 0)], [(0, 1), (1, 1)], [(0, 0), (0, 1)], [(1, 0), (1, 1)], [(0, 0), (1, 1)], [(0, 1), (1, 0)]]
    >>> pprint(struct[1]) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [[(0, 0), (1, 0)], [(0, 0), (0, 1)], [(0, 0), (1, 1)]],
                 (0, 1): [[(0, 1), (1, 1)], [(0, 0), (0, 1)], [(0, 1), (1, 0)]],
                 (1, 0): [[(0, 0), (1, 0)], [(1, 0), (1, 1)], [(0, 1), (1, 0)]],
                 (1, 1): [[(0, 1), (1, 1)], [(1, 0), (1, 1)], [(0, 0), (1, 1)]]})
    """

    lines = get_lines_flat_coord(d, n)
    scopes = get_scopes_coord(lines, d)
    return (lines, scopes)


def scopes_size(scopes: Scopes) -> Counter:
    """ Calculate the different scope lengths.

    Parameters
    ----------
    scopes : DefaultDict
        Dictionary of cells (keys) and their scopes
 
    Returns
    -------
    Counter :
        Counter of scopes lengths (key) and their frequency (values).
            
    See Also
    --------
    get_scopes
 
    Examples
    --------
    >>> import numpy as np
    >>> scopes = structure_np(2, 3)[2] 
    >>> scopes_size(scopes) == Counter({2: 4, 3: 4, 4: 1})
    True
    >>> scopes = structure_coord(2, 3)[1]
    >>> scopes_size(scopes) == Counter({2: 4, 3: 4, 4: 1})
    True
    """
    
    return counter([len(scope) for scope in scopes.values()])


def scopes_size_cell(scopes: Scopes) -> DefaultDict[int, List[Cell_coord]]:
    """ Group cells by length of their scope.

    Parameters
    ----------
    scopes : DefaultDict
        Dictionary of cells (keys) and their scopes
 
    Returns
    -------
    DefaultDict :
        Dictonary of scopes lengths (key) and the list of cells with scopes of that length.
            
    See Also
    --------
    get_scopes_flat_np
    get_scopes_flat_coord
 
    Examples
    --------
    >>> import numpy as np
    >>> from pprint import pprint
    >>> scopes = structure_np(2, 3)[2] 
    >>> pprint(scopes_size_cell(scopes))
    defaultdict(<class 'list'>,
                {2: [(1, 0), (0, 1), (2, 1), (1, 2)],
                 3: [(0, 0), (2, 0), (0, 2), (2, 2)],
                 4: [(1, 1)]})
    >>> scopes = structure_coord(2, 3)[1] 
    >>> pprint(scopes_size_cell(scopes))
    defaultdict(<class 'list'>,
                {2: [(0, 1), (1, 0), (1, 2), (2, 1)],
                 3: [(0, 0), (0, 2), (2, 0), (2, 2)],
                 4: [(1, 1)]})
    """

    scopes_size_cell: DefaultDict = defaultdict(list)
    for cell, scope in scopes.items():
        scopes_size_cell[len(scope)].append(cell)

    return scopes_size_cell


# The following 3 functions are for the displaying of a
# hypercube to a terminal. 
# It is assumed that an numpy ndarray has been used to
# represent the hypercube

def display_np(arr: Cube_np, display_cell: Callable[[Any], Tuple[str, str, str]] = None, ul = False) -> str:
    """ Construct a string to display the hypercube in the terminal.

    Parameters
    ----------
    arr: numpy.ndarray
        The array to be displayed
    display_cell: callback function, optional
        A callback function called with the value of each cell value.
        It returns a tuple of strings - the character/string to be displayed, 
        and any formatting to be applied (typically ansi color sequences). 
        See Examples for how colors are specified.
        If display_cell is not provided, the cell value is displayed.
    ul: bool, optional
        display_np calls itself recursively (see Notes). This parameter is used 
        to track whether a cell is on the bottom row of a 2-d array. It has direct
        impact when the user calls dislay_np unless the array is 1-d, in which
        case it determines if cell values are underlined when displayed. 

    Returns
    -------
    str:
        a string that can be printed to the terminal to display the hypercube

    See Also
    --------
    underline
    join_multiline
    
    Notes
    -----
    The '|' character is used to represent the board horizontally.
    Cell contents are underlined in order to represent the board vertically. For example,
    the character 'X' is underlined to give 'X̲'. 
    This function is recursive, it starts with hypercube and keeps removing dimensions
    until at a single cell, which can be given a string value.
    We are trying to display d dimensions in 2 dimension. to do this, odd dimensions are 
    shown horizontally; even dimensions are shown vertically.

    Examples
    --------
    >>> import numpy as np
    >>> from pprint import pprint

    >>> def dc(v: Any) -> Tuple[str, str, str]:
    ...
    ...    # define colors - could also use colorama module
    ...    # red foreground + yellow background
    ...    pre_fmt = '\033[31;43m'
    ...    post_fmt = '\033[0m' # removes color settings
    ...
    ...    if v > 0:
    ...        return 'X', pre_fmt, post_fmt
    ...    elif v < 0:
    ...        return 'O', pre_fmt, post_fmt
    ...    else:
    ...        return ' ', '', ''
    
    >>> d = 3
    >>> n = 3 
    >>> arr = np.zeros((n,) * d, dtype = int)
    >>> arr[0, 0, 0] = 1
    >>> arr[1, 1, 1] = -1
    >>> disp = display_np(arr, dc)
    >>> print(disp) #doctest: +SKIP
    X̲|_|_   _|_|_   _|_|_
    _|_|_   _|O̲|_   _|_|_
     | |     | |     | | 
    """

    if arr.size == 1: # arr is a single cell
        if display_cell is None:
            s, pre_fmt, post_fmt = str(arr), '', ''
        else:
            s, pre_fmt, post_fmt = display_cell(arr)

        # underline displayed string (to repsent board structure) unless 
        # string is in the bottom row of array
        if ul:
            s = '_' * len(s) if s.isspace() else underline(s)
            
        return pre_fmt + s + post_fmt

    # arr is not a single cell
    d = arr.ndim
    # break the array into sub arrays along the first dimension
    sub_arr = [arr[i] for i in range(arr.shape[0])]

    # constuct a string for each sub array
    sub_arr_str = []
    for c, a in enumerate(sub_arr):
        if d == 2 and c == len(sub_arr) - 1:
            # sub arr is 2-dimensional and last row - don't underline
            ul = False
        elif d != 1:
            ul = True

        sub_arr_str.append(display_np(a, display_cell, ul))

    # join the sub strings
    if d % 2 == 0: # even number of dimensions - display down the screen
        if d == 2:
            return ''.join('\n'.join(sub_arr_str))
        else:
            sp = '\n' + '\n' * (int((d / 2) ** 1.5) - 1) # increase space between higher dimesions  
            return sp.join(sub_arr_str)
    else: # odd number of dimensions - display across the screen
        if d == 1:
            return '|'.join(sub_arr_str)
        else:
            return join_multiline(sub_arr_str, ' ' + ' ' * int((d - 2) ** 1.5) + ' ', False)


def underline(s: str, alpha_only = True) -> str:
    """ Underlines a string

    Parameters
    ----------
    s: str
        The string to be underlined

    Returns
    -------
    str:
        An underlined string 

    Notes
    -----
    The code appears only to work properly with alphabetic characters

    Examples
    --------
    >>> underline('X')
    'X̲'
    >>> underline('XX')
    'X̲X̲'
    >>> underline('1')
    '1'
    >>> underline('1', False)
    '1̲'
    """

    try:
        if alpha_only:
            s_ = ""
            for chr in str(s):
                if chr.isalpha():
                    s_ = s_ +  chr + "\u0332"
                else:
                    s_ = s_ + chr
            return s_
        else:
            return ''.join([chr + "\u0332" for chr in str(s)])      
    except:
        return s


def join_multiline(iter: Iterable[str], divider: str = ' ', divide_empty_lines: bool = False,
                   fill_value: str = '_') -> str:
    """ Join multiline string line by line.

    Parameters
    ----------
    iter: iterable
        An iterable of multiline (or single line) strings 
    divider: str, optional
        string to divided the corresponding lines in each iterable
    divide_empty_lines: bool, optional
        If the corresponding line in each iterable is blank, then determines if the lines
        are still divided by divider, or divided by ''.
    fill_value: str, optional
        If the number of lines in each multiline string in iter differs, then fill_value
        is used to fill in values of the shorter strings.

    Returns
    -------
    str:
        The joined string.

    Examples
    --------
    >>> # note that newline has to be escaped to work in doctest examples below.
    >>> ml_1 = 'AA\\nMM\\nXX'
    >>> ml_2 = 'BB\\nNN\\nYY'
    >>> ml_3 = 'CC\\nOO\\nZZ'
    >>> ml = join_multiline([ml_1, ml_2, ml_3])
    >>> print(ml) #doctest: +NORMALIZE_WHITESPACE
    AA BB CC
    MM NN OO
    XX YY ZZ
    >>> ml = join_multiline([ml_1, ml_2, ml_3], divider = '_')
    >>> print(ml) #doctest: +NORMALIZE_WHITESPACE
    AA_BB_CC
    MM_NN_OO
    XX_YY_ZZ
    >>> ml_3 = 'CC\\nOO'
    >>> ml = join_multiline([ml_1, ml_2, ml_3], fill_value = '@')
    >>> print(ml) #doctest: +NORMALIZE_WHITESPACE
    AA BB CC
    MM NN OO
    XX YY @
    >>> ml_1 = 'AA\\n\\nMM'
    >>> ml_2 = 'BB\\n\\nNN'
    >>> ml_3 = 'CC\\n\\nZZ'
    >>> ml = join_multiline([ml_1, ml_2, ml_3], divider = '_')
    >>> print(ml) #doctest: +NORMALIZE_WHITESPACE
    AA_BB_CC
    <BLANKLINE>
    MM_NN_ZZ    
    >>> ml = join_multiline([ml_1, ml_2, ml_3], divider = '_', divide_empty_lines = True)
    >>> print(ml) #doctest: +NORMALIZE_WHITESPACE
    AA_BB_CC
    __
    MM_NN_ZZ
    """
    # for each multiline block, split into individual lines
    spl = [x.split('\n') for x in iter]
    
    # create list of tuples with tuple i containing line i from each multiline block
    tl = [i for i in it.zip_longest(*spl, fillvalue = fill_value)]
        
    if divide_empty_lines:
        st = [divider.join(t) for t in tl]
    else:
        st = []
        for t in tl:
            if all([not x.strip() for x in t]):
                st.append('')
            else:
                st.append(divider.join(t))

    # finally, join each string separated by a new line 
    return '\n'.join(st)            


# The following functions are helper functions

def slice_ndarray(arr: np.ndarray, axes: Collection[int], 
                coords: Collection[int]) -> np.ndarray:
    """ Returns a slice of an array. 

    Parameters
    ----------
    arr : numpy.ndarray
        The array to be sliced
    axes : Iterable[int]
        The axes that are fixed
    coords : Iterable[int]
        The coordinates corresponding to the fixed axes

    Returns
    -------
    numpy.ndarray:
        A view of a slice of `arr`.

    Raises
    ------
    ValueError
        If length of `axes` is not equal to length of `coords`

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.arange(8).reshape(2, 2, 2)
    >>> arr
    array([[[0, 1],
            [2, 3]],
    <BLANKLINE>
           [[4, 5],
            [6, 7]]])
    >>> slice_ndarray(arr, (0,), (0,))
    array([[0, 1],
           [2, 3]])
    >>> slice_ndarray(arr, (1, 2), (0, 0))
    array([0, 4])
    """

    # create a list of slice objects, one for each dimension of the array
    # Note: slice(None) is the same as ":". E.g. arr[:, 4] = arr[slice(none), 4)]
    sl: List[Union[slice, int]] = [slice(None)] * arr.ndim    
    if len(axes) != len(coords):
        raise ValueError("axes and coords must be of the same length")
    
    for axis, coord in zip(axes, coords):
        sl[axis] = coord
    
    return arr[tuple(sl)]


def insert_into_tuple(tup: Tuple, pos: Union[int, Collection[int]], 
                      val: Union[Any, Collection[Any]]) -> Tuple[int, ...]:
    """ Insert values into a tuple. 

    Parameters
    ----------
    tup : tuple
        the tuple into which values are to be inserted
    pos : int of sized iterable container class of ints
        The positions into which values are to be inserted
    val : any value or sized iterable container class of any values
        The values corresponding to the positions in `pos`

    Returns
    -------
    Tuple:
        A copy of `tup` with values inserted.

    Raises
    ------
    ValueError
        If length of `pos` is not equal to length of `val`

    See Also
    --------
    list.insert
 
    Notes
    -----
    `tup` is converted to a list and the list.insert method is used to
    insert values. the list is then converted to a tuple and returned.

    Examples
    --------
    >>> tup = (0, 1, 2, 3)
    >>> pos = (5, 1)
    >>> val = (9, 8)
    >>> insert_into_tuple(tup, pos, val)
    (0, 8, 1, 2, 3, 9)
    >>> insert_into_tuple(tup, (), ())
    (0, 1, 2, 3)
    """

    tl = list(tup)

    if isinstance(pos, int):
        tl.insert(pos, val)
    else:
        if len(pos) != len(val):
            raise ValueError("pos and val must be of the same length")

        if len(pos) == 0:
            return tup

        # sort pos so from low to high; sort val correspondingly
        stl = list(zip(*sorted(zip(pos, val)))) 
        for p, v in zip(stl[0], stl[1]):
            tl.insert(p, v)

    return tuple(tl)


def str_to_tuple(d: int, n: int, cell: str, offset: int = 1) -> Cell_coord:
    """ Returns cells coordinates provided as a string as a tuple of integers.

    Parameters
    ----------
    d : int
        The number of dimensions of the hypercube
    n : int
        The number of cells in any dimension
    cell: str
        cell coordinates specified as a string (see Notes).
        Will accept a non-string arguments which is attempted to
        be cast to a string.
    offset: int
        idx offset - typically 0 or 1.
 
    Raises
    ------
    ValueError:
        1. if digits are not separated and the n is greater than 9
        2. Incorrect numbers of coordinates provided
        3. One or more coordinates is not valid

    Notes
    -----
    If the string is all digits then assumes that each digit is a coordinate.
    If non-digit character as provided then assumes that these split coordinates.

    Returns
    -------
    tuple :
        A tuple containing the cell coordinates.
             
    Examples
    --------
    >>> d = 3
    >>> n = 3 
    >>> str_to_tuple(d, n, '123')
    (0, 1, 2)
    >>> str_to_tuple(d, n, '012', offset = 0)
    (0, 1, 2)
    >>> str_to_tuple(d, n, '1,2::3')
    (0, 1, 2)
    >>> str_to_tuple(d, n, 123)
    (0, 1, 2)
    >>> str_to_tuple(d, n, '12')
    Traceback (most recent call last):
        ...
    ValueError: Incorrect number of coordinates provided
    >>> str_to_tuple(d, n, '125')
    Traceback (most recent call last):
        ...
    ValueError: One or more coordinates are not valid
    >>> d = 3
    >>> n = 10
    >>> str_to_tuple(d, n, '123')
    Traceback (most recent call last):
        ...
    ValueError: Board is too big for each dimension to be specified by single digit
    """

    cell = str(cell)
    # check to see if there are any non-digits
    nd = re.findall(r'\D+', cell) 
    if len(nd) == 0: 
        if n > 9:
            raise ValueError("Board is too big for each dimension to be specified by single digit")
        else:
            tup = tuple(int(coord) - offset for coord in cell) 
    else: # there are non-digits, use these as separators
        tup = tuple(int(coord) - offset for coord in re.findall(r'\d+', cell)) 
    
    # check that correct number of coordinates specified
    if len(tup) != d:
        raise ValueError("Incorrect number of coordinates provided")

    # check that each coordinate is valid
    if all(t in range(n) for t in tup):
        return tup
    else:
        raise ValueError("One or more coordinates are not valid")           


def _lines_np_coord_check(d: int, n: int) -> bool:
    """ Checks if lines_np and lines_coord give the same lines.

    Parameters
    ----------
    d : int
        The number of dimensions of the hypercube
    n : int
        The number of cells in any dimension

    Returns
    -------
    bool :
        True if lines_np and lines_coord give the same lines.
        False otherwise.

    See Also
    --------
    get_lines_flat_np
    get_lines_flat_coord

    Notes
    -----
    This function is a private function used in testing.
    """

    dtype = np.int64 if n ** d > 2 ** 31 else np.int32
    arr = np.arange(n ** d, dtype = dtype).reshape([n] * d)

    lines_np = get_lines_flat_np(arr)
    lines_coord = get_lines_flat_coord(d, n)

    t_np = [tuple(sorted(l.tolist())) for l in lines_np]
    t_coord = [tuple(sorted([arr[c] for c in l])) for l in lines_coord] 

    return set(t_np) == set(t_coord)
    



def get_scope_cell_coord(d: int, n: int, cell: Cell_coord) -> Lines_coord: 
    
    lines = []

    # loop over the numbers of dimensions
    for i in range(d): 
        # loop over all possible combinations of i dimensions
        diagonals = get_diagonals_coord(i + 1, n)

        for i_comb in it.combinations(range(d), r = i + 1): 
              
            other_d = set(range(d)) - set(i_comb)
            
            for diagonal in diagonals:
                for c in diagonal:
                    # if selected dimensions of c match cell, then c
                    # # with other dimensions of cell are in scope 
                    cc = tuple(cell[i] for i in i_comb)
                    fc = tuple(c[i] for i in i_comb)
                    oc = tuple(cell[i] for i in other_d)
                    if fc == cc:
                        tt = insert_into_tuple(cc, other_d, oc)
                        lines.append(tt)
                        break

    return lines