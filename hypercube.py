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
import numpy as np #type: ignore
from scipy.special import comb #type: ignore
import itertools as it
from collections import defaultdict, Counter as counter
from typing import List, Callable, Union, Collection, Tuple, Any, DefaultDict, TypeVar, Counter, Dict

# type aliases
Line = TypeVar('Line') # line should really be a 1d numpy array
Lines = List[Line]
Cell = Tuple[int]
Scopes = DefaultDict[Cell, Lines]  
Structure = Tuple[np.ndarray, Lines, Scopes]


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


def get_diagonals_np() -> Callable[[Line], Lines]:
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

    diags = []
    
    def diagonals_np(arr: np.ndarray) -> Lines:
        if arr.ndim == 1:
            diags.append(arr)
        else:
            diagonals_np(arr.diagonal())
            diagonals_np(np.flip(arr, 0).diagonal())
        return diags

    return diagonals_np


def get_lines_np(arr: np.ndarray, flatten: bool = True) -> \
              Tuple[Union[Lines, List[Lines]], int]: 
    """ Returns the lines in an array

    Parameters
    ----------
    arr : numpy.ndarray
        The array whose lines are to be calculated

    flatten : bool, optional 
        Determines if the lines are returned as a flat list, or
        as a nested lists of i-agonals.
        A flat list is return by default.

    Returns
    -------
    list :
        A list of numpy.ndarray views of the lines in `arr`.
        The `flatten` arguments determines if the list is flat or 
        nested listed of i-agonals
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
    >>> lines, count = get_lines_np(arr)
    >>> lines
    [array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3]), array([0, 3]), array([2, 1])]
    >>> count
    6
    >>> len(lines)
    6
    >>> arr[0, 0] = 99
    >>> lines
    [array([99,  2]), array([1, 3]), array([99,  1]), array([2, 3]), array([99,  3]), array([2, 1])]
    >>> arr[0, 0] = 0
    >>> lines, count = get_lines_np(arr, False)
    >>> lines
    [[array([0, 2])], [array([1, 3])], [array([0, 1])], [array([2, 3])], [array([0, 3]), array([2, 1])]]
    >>> count
    6
    >>> len(lines)
    5
    """
    
    d = arr.ndim
    n = arr.shape[0]
    lines = []
    count = 0

    # loop over the numbers of dimensions
    for i in range(d): 
        # loop over all possible combinations of i dimensions
        for i_comb in it.combinations(range(d), r = i + 1): 
            # a cell could be in any position in the other dimensions
            for cell in it.product(range(n), repeat = d - i - 1):
                # take a slice of i dimensions given cell
                sl = slice_ndarray(arr, set(range(d)) - set(i_comb), cell)
                # get all possible lines from slice
                diags = get_diagonals_np()(sl)
                count += len(diags)
                if flatten:
                    lines.extend(diags)
                else:
                    lines.append(diags)
    
    assert count == num_lines(d, n)
    return lines, count


def get_scopes_np(lines: Lines, d: int) -> Scopes:
    """ Calculate the scope of each cell in a hypercube

    Parameters
    ----------
    lines : list
        The first returned value from get_lines(arr) where arr is of the
        form np.arange(n ** d, dtype = int64).reshape([n] * d).
        That is, arr is populated with the values 0,1,2,...,n^d - 1.

    dim : int 
        The dimension of the array (hypercube) that was used to
        generate the `lines` parameter.

    Returns
    -------
    defaultdict :
        A dictionary with keys equal to each cell of the hypercube 
        (represented as a tuple). For each cell key, the value is cell's
        scope - a list of numpy.ndarray views that are lines containing
        the cell.
            
    See Also
    --------
    get_lines_np

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
    >>> lines, _ = get_lines_np(arr)
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


def structure_np(d: int, n: int) -> Structure:
    """ Return a celled hypercube, its lines, and the scopes of its cells.

    Parameters
    ----------
    d : int
        The number of dimensions of the hypercube
    n : int
        The number of cells in any dimension
 
    Returns
    -------
    tuple :
        A tuple containing the hypercube, its lines, and the scopes of
        its cells.
            
    See Also
    --------
    get_lines_np
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
    """

    # number of cells is n^d. If this greater than 2^31 then
    # we use int64. This is because the the get_scopes function
    # populates the arrays with values 0,1,2, ...
    dtype = np.int64 if n ** d > 2 ** 31 else np.int32
    arr = np.arange(n ** d, dtype = dtype).reshape([n] * d)
    lines, _ = get_lines_np(arr)
    scopes = get_scopes_np(lines, d)
    #arr.fill(0)
    return (arr, lines, scopes)


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
    """
    
    return counter([len(scope) for scope in scopes.values()])


def scopes_size_cells(scopes: Scopes) -> DefaultDict[int, List[Cell]]:
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
    get_scopes
 
    Examples
    --------
    >>> import numpy as np
    >>> from pprint import pprint
    >>> scopes = structure_np(2, 3)[2] 
    >>> pprint(scopes_size_cells(scopes))
    defaultdict(<class 'list'>,
                {2: [(1, 0), (0, 1), (2, 1), (1, 2)],
                 3: [(0, 0), (2, 0), (0, 2), (2, 2)],
                 4: [(1, 1)]})
    """

    scopes_size_cells: DefaultDict = defaultdict(list)
    for cell, scope in scopes.items():
        scopes_size_cells[len(scope)].append(cell)

    return scopes_size_cells


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
