""" Provides functionalilty for working with celled hypercubes.

Hypercubes are extensions of lines, squares and cubes into higher 
dimensions. Celled hypercubes can be thought as a grid or lattice
structure. From this point, hypercubes is used to mean celled
hypercubes.

A hypercube can be described by its dimension and the number of
cells in any dimension. We denote this as h(d, n).
For example: h(2, 3) is a 3x3 grid; h(3, 4) is a 4x4x4 lattice.
A hypercube of dimension d may also be referred to as a d-cube.

A cell's position can be specified in coordinate style. 
For example, given h(3, 4) and an agreed ordering of dimension
then some valid coordinates are (1,1,1), (2,1,3) and (4,4,4).

The term m-agonal is a short for "m-dimensional diagonal" and can be
thought of as a line of contiguous cells that span m dimensions. 
For example, in a 3-cube you would find many 1-agonals, 2-agonals and
3-agonals. A 1-agonal is customarily known as a row, column or pillar. 
In another example, if a line of contiguous cells in a 5-cell have the
property that 3 coordinates change, while the others remain constant,
these cells constitute a 3-agonal.
For a given h(d, n), 1 <= m <= n, a m-agonal always has n cells.
The term line is used to refer to any m-agonal in general.

A cell apppears in multiple lines, which are refered to as the 
scope of the cell.

The combination of lines and cell scopes is referred to
as the structure of the hypercube.

We define a slice as a sub-cube of a hypercube. For example,
consder h(2,3), a 3x3 hypercube. Let the dimensions be denoted as 
d1 and d2, respectively, where 1 <= d1, d2 <= 3.
If we consider d1 as rows, and d2 as columns, then the slice that is
the first column is defined by d1 = 1, 2, 3, and d2 = 1. This has the
form h(1, 3).
The slice that is the top left 2x2 corner is defined by d1, d2 = 1, 2.
This has the form h(2, 2).

This module essentially has 2 classes of functions:
1. Those that use a numpy ndarray to implement the underlying
hypercube. These functions have the suffix _np. An array of d dimensions 
may be referred to as a d-array
2. Those that do not implement the underlying hypercube but
provide information as coordinates that can be used with
a user-implementation of the hypercube. These functions have
the suffix _coord.

########################################################################
Type annotations are used in this module. In addition to the standard
types defined in the typing module, several aliases are also defined
which can be viewed in the source code.
"""


# numpy (and scipy) don't yet have type annotations
import numpy as np # type: ignore
from scipy.special import comb # type: ignore
import itertools as it
import numbers
import re
from typing import List, Callable, Union, Collection, Tuple, Any, Type, Deque
from typing import DefaultDict, TypeVar, Counter, Dict, Iterable, Generator, Sequence


Cell_coord = Tuple[int, ...]
Cube_np = TypeVar('Cube_np', np.ndarray, np.ndarray) # Cube_np should really be a numpy array representing h(d, n)

Line_np = TypeVar('Line_np', np.ndarray, np.ndarray) # Line_np should really be a 1d numpy array with n elements
Line_coord = List[Cell_coord]

Lines_np = List[Line_np]
Lines_enum_np = Dict[int, Line_np]
Lines_coord = List[Line_coord]
Lines_enum_coord = Dict[int, Line_coord]

Scopes_np = DefaultDict[Cell_coord, Lines_np]  
Scopes_coord = DefaultDict[Cell_coord, Lines_coord]
Scopes_enum = DefaultDict[Cell_coord, List[int]]  
Scopes = Union[Scopes_np, Scopes_coord, Scopes_enum]

Structure_np = Tuple[Cube_np, Lines_np, Scopes_np]
Structure_enum_np = Tuple[Cube_np, Lines_enum_np, Scopes_enum]
Structure_coord = Tuple[Lines_coord, Scopes_coord]
Structure_enum_coord = Tuple[Lines_enum_coord, Scopes_enum]


def num_lines_grouped(d: int, n: int) -> Generator[int, None, None]: 
    """ 
    num_lines_grouped(d: int, n: int) -> Generator[int, None, None]:
    
    Calculate the number of lines in a hypercube, grouped by the 
    number of dimensions spanned.  

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension
 
    Yields
    -------
    
        The number of lines in a hypercube, grouped by number of 
        dimensions spanned.

    Notes
    -----
    Consider a hypercube h(d, n).
    Let l be the number of lines, then

        l = sum{i=1, i=d} [ dCi * n^(d-i) * (2^i)/2 ]

    where dCi is 'd choose i'.

    Sketch of proof:
    Let l_i be the number of i-agonals (lines that span exactly 
    i dimensions). For example, consider the following square (2-cube):

        [[0, 1],
         [2, 3]]

    The 1-agonals are [0, 1], [2, 3], [0, 2] and [1, 3] and l_1 = 4.  
    The 2-agonals are [0, 3] and [1, 2]  and l_2 = 2.
    
    Hence l = l_1 + l_2 = 6

    It is trivially true that the l is the sum of l_i, i.e.,

        l = sum{i=1, i=d} l_i

    Next we show how l_i can be calculated. Firstly, we argue
    that the distinct number of h(i, n) is dCi * n^(d-i).
    
    The number of ways of choosing i dimensions from d is dCi.
    For example if d=3 and i=2, then the 3 combinations of 
    2 dimensions (squares) are (1, 2), (1, 3) and (2, 3).

    Given a fixed set of i dimension, the number of remaining dimensions
    is d-i, and the number of cells in these dimensions is n^(d-i).
    Any one of these cells could be chosen relative to the
    fixed i dimensions.

    Hence the distinct number of h(i, n) is dCi * n^(d-i).

    Finally, for any h(i, n), the number of i-agonals is (2^i)/2. 
    This is because an i-cube has 2^i corners and a line has 2 corners.

    Hence l_i = dCi * n^(d-i) * (2^i)/2 and thus:

        l = sum{i=1, i=d} [ dCi * n^(d-i) * (2^i)/2 ]
  
    Examples
    --------
    >>> list(num_lines_grouped(2, 3))
    [6, 2]
    >>> list(num_lines_grouped(3, 4))
    [48, 24, 4]
    """

    for i in range(1, d + 1):
        yield comb(d, i, True) * (n ** (d - i)) * (2 ** (i - 1))


def num_lines(d: int, n: int) -> int: 
    """ 
    num_lines(d: int, n: int) -> int:
    
    Calculate the number of lines in a hypercube.  

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension
 
    Returns
    -------

        The number of lines in a hypercube.

    See Also
    --------
    num_lines_grouped

    Notes
    -----
    Calls the function num_lines_grouped

    Examples
    --------
    >>> num_lines(2, 3)
    8
    >>> num_lines(3, 4)
    76
    """
    
    return sum(list(num_lines_grouped(d, n)))


def get_diagonals_np(hc: Cube_np) -> Generator[Line_np, None, None]:
    """ 
    get_diagonals_np(hc: Cube_np) -> Generator[Line_np, None, None]:
    
    Calculate the d-agonals of a d-cube h(d, n). 

    Parameters
    ----------
    hc
        A d-cube whose d-agonals are to be calculated

    Yields
    -------

        numpy.ndarray views of the d-gonals of `hc`.

    Notes
    -----
    The number of corners of `hc` is 2^d. The number of d-agonals 
    is 2^d / 2 since two connecting corners form a line. 

    Examples
    --------
    >>> import numpy as np
    >>> hc = np.arange(8).reshape(2, 2, 2)
    >>> hc
    array([[[0, 1],
            [2, 3]],
    <BLANKLINE>
           [[4, 5],
            [6, 7]]])
    >>> diagonals = list(get_diagonals_np(hc))
    >>> diagonals
    [array([0, 7]), array([1, 6]), array([4, 3]), array([5, 2])]
    >>> hc[0, 0, 0] = 99
    >>> diagonals
    [array([99,  7]), array([1, 6]), array([4, 3]), array([5, 2])]
    """
    
    # The function is recursive. How it works is best shown by example.
    # 1d: hc = [0, 1] then the diagonal is also [0, 1].
    
    # 2d: hc = [[0, 1],
    #           [2, 3]]
    # The numpy diagonal method gives the main diagonal = [0, 3], a 1d array
    # which is recursively passed to the function.
    # To get the opposite diagonal we first use the numpy flip function to
    # reverse the order of the elements along the given dimension, 0 in this case.
    # This gives [[2, 3],
    #              0, 1]]
    # The numpy diagonal method gives the main diagonal = [2, 1], a 1d array
    # which is recursively passed to the function.

    # 3d: hc = [[[0, 1],
    #            [2, 3]],
    #           [[4, 5],
    #            [6, 7]]]
    # The numpy diagonal method gives the main diagonals in the 3rd dimension
    # as rows.
    #            [[0, 6],
    #             [1, 7]]
    # Note that the diagonals of this array are [0, 7] and [6, 1] which are
    # retrieved by a recurive call to the function.
    # We now have 2 of the 4 3-agonals of the orginal 3-cube hc.
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
    # We now have all four 3-agonals of the original 3-cube hc.

    if hc.ndim == 1:
        yield hc
    else:
        yield from get_diagonals_np(hc.diagonal())
        yield from get_diagonals_np(np.flip(hc, 0).diagonal())


def get_lines_grouped_np(hc: Cube_np) -> Generator[Lines_np, None, None]: 
    """ 
    get_lines_grouped_np(hc: Cube_np) -> 
        Generator[Lines_np, None, None]:
    
    Generate the lines of a hypercube, grouped by the number of
    dimensions spanned.

    Parameters
    ----------
    hc
        The hypercube whose lines are to be calculated

    Yields
    -------

        numpy.ndarray views of the lines in `hc`, grouped by the
        numbers of dimensions spanned.
            
    See Also
    --------
    get_lines_i_np

    Examples
    --------
    >>> import numpy as np
    >>> hc = np.arange(4).reshape(2, 2)
    >>> hc
    array([[0, 1],
           [2, 3]])
    >>> lines = list(get_lines_grouped_np(hc))
    >>> lines
    [[array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3])], [array([0, 3]), array([2, 1])]]
    >>> hc[0, 0] = 99
    >>> lines
    [[array([99,  2]), array([1, 3]), array([99,  1]), array([2, 3])], [array([99,  3]), array([2, 1])]]
    """
    
    for i in range(hc.ndim):
        yield from get_lines_i_np(hc, i)


def get_lines_i_np(hc: Cube_np, i: int) -> Generator[Lines_np, None, None]: 
    """ 
    get_lines_i_np(hc: Cube_np, i: int) -> 
        Generator[Lines_np, None, None]:
    
    Generates the lines of a hypercube that span the specified
    number of dimensions.

    Parameters
    ----------
    hc
        The hypercube whose lines are to be calculated
    i
        The number of dimensions that the returned lines must span

    Yields
    -------

        numpy.ndarray views of the lines in `hc` that span 
        `i` dimensions.
            
    See Also
    --------
    num_lines_grouped

    Notes
    -----
    The notes section for the function num_lines_grouped provides a
    sketchof a constructive proof for the number of lines in a 
    hypercube. This has been used to implement this function. 

    Examples
    --------
    >>> import numpy as np
    >>> hc = np.arange(4).reshape(2, 2)
    >>> hc
    array([[0, 1],
           [2, 3]])
    >>> lines = list(get_lines_i_np(hc, 0))
    >>> lines
    [[array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3])]]
    >>> lines = list(get_lines_i_np(hc, 1))
    >>> lines
    [[array([0, 3]), array([2, 1])]]
    >>> hc[0, 0] = 99
    >>> lines
    [[array([99,  3]), array([2, 1])]]
    """
 
    d = hc.ndim
    n = hc.shape[0]
    lines = []

    # loop over all possible combinations of i dimensions
    for i_comb in it.combinations(range(d), r = i + 1): 
        # a cell could be in any position in the other dimensions
        other_d = set(range(d)) - set(i_comb)
        for cell in it.product(range(n), repeat = d - i - 1):
            # take a slice of selected i dimensions given a cell
            sl = slice_ndarray(hc, other_d, cell)
            # get all possible lines from slice
            lines.extend(list(get_diagonals_np(sl)))

    yield lines


def get_lines_np(hc: Cube_np) -> Generator[Line_np, None, None]: 
    """ 
    get_lines_np(hc: Cube_np) -> Generator[Line_np, None, None]:
    
    Returns the lines in a hypercube

    Parameters
    ----------
    hc
        The hypercube whose lines are to be calculated

    Yields
    -------

        numpy.ndarray views of the lines in `hc`.
                
    See Also
    --------
    get_lines_grouped_np

    Examples
    --------
    >>> import numpy as np
    >>> hc = np.arange(4).reshape(2, 2)
    >>> hc
    array([[0, 1],
           [2, 3]])
    >>> lines = list(get_lines_np(hc))
    >>> lines
    [array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3]), array([0, 3]), array([2, 1])]
    >>> len(lines)
    6
    >>> hc[0, 0] = 99
    >>> lines
    [array([99,  2]), array([1, 3]), array([99,  1]), array([2, 3]), array([99,  3]), array([2, 1])]
    """

    grouped = get_lines_grouped_np(hc)
    flat = (x for y in grouped for x in y)
    yield from flat # return flat works as well but yield from this is explicit as to being a generator


def get_scopes_np(lines: Lines_np, d: int) -> Scopes_np:
    """ 
    get_scopes_np(lines: Lines_np, d: int) -> Scopes_np:

    Calculate the scope of each cell in a hypercube

    Parameters
    ----------
    lines
        The returned value from get_lines_np(hc) where hc is of the
        form np.arange(n ** d, dtype = intx__).reshape([n] * d).
        That is, hc is populated with the values 0,1,2,...,n^d - 1.

    dim
        The dimension of the hypercube that was used to
        generate `lines`.

    Returns
    -------

        A dictionary with keys equal to the coordinates of each cell in
        the hypercube. For each cell key, the value is the cell's
        scope - a list of numpy.ndarray views that are lines containing
        the cell.
            
    See Also
    --------
    get_lines_np

    Notes
    -----
    The implementation of this function uses np.unravel_index, and
    relies uopn the lines parameter being generated from an array
    populated with values 0,1,2,...
 
    Examples
    --------
    >>> import numpy as np
    >>> from pprint import pprint
    >>> hc = np.arange(4).reshape(2, 2)
    >>> hc
    array([[0, 1],
           [2, 3]])
    >>> lines = list(get_lines_np(hc))
    >>> lines
    [array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3]), array([0, 3]), array([2, 1])]
    >>> scopes = get_scopes_np(lines, 2)
    >>> pprint(scopes) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [array([0, 2]), array([0, 1]), array([0, 3])],
                 (0, 1): [array([1, 3]), array([0, 1]), array([2, 1])],
                 (1, 0): [array([0, 2]), array([2, 3]), array([2, 1])],
                 (1, 1): [array([1, 3]), array([2, 3]), array([0, 3])]})
    >>> hc[0, 0] = 99
    >>> pprint(scopes) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [array([99,  2]), array([99,  1]), array([99,  3])],
                 (0, 1): [array([1, 3]), array([99,  1]), array([2, 1])],
                 (1, 0): [array([99,  2]), array([2, 3]), array([2, 1])],
                 (1, 1): [array([1, 3]), array([2, 3]), array([99,  3])]})  
    """
    
    n = lines[0].size
    shape = [n] * d
    scopes: Scopes_np = DefaultDict(list)

    for line in lines:
        for j in range(n):
            cell = np.unravel_index(line[j], shape)
            scopes[cell].append(line) 
    return scopes


def structure_np(d: int, n: int, zeros: bool = True, OFFSET: int = 0) -> Structure_np:
    """ 
    structure_np(d: int, n: int, zeros: bool = True, OFFSET: int = 0) -> 
        Structure_np:
    
    Return a hypercube, its lines, and the scopes of its cells.

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension
    zeros
        If true, all values in array are 0, else they are 0,1,2,...
    OFFSET
        The number of cells is n^d. If this greater than 
        (2^31 - OFFSET - 1) then we use np.int64 (instead of np.int32)
        as the dtype of the numpy array.
 
    Returns
    -------

        The hypercube (as a numpy array), its lines, and the scopes of
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
    # then we use int64. This is because the get_scopes 
    # function populates the arrays with values 0,1,2, ...
    dtype = np.int64 if n ** d > 2 ** 31 - OFFSET - 1 else np.int32
    hc = np.arange(n ** d, dtype = dtype).reshape([n] * d)
    lines = list(get_lines_np(hc))
    scopes = get_scopes_np(lines, d)
    if zeros:
        hc.fill(0)
    return (hc, lines, scopes)


def get_lines_enum_np(hc: Cube_np) -> Lines_enum_np:
    """ 
    get_lines_enum_np(hc: Cube_np) -> Lines_enum_np
    
    Returns emunerated lines of a hypercube

    Parameters
    ----------
    hc
        The hypercube whose lines are to be calculated

    Returns
    -------
    
        Enumerated numpy.ndarray views of the lines in `hc`.
                
    See Also
    --------
    get_lines_np

    Examples
    --------
    >>> import numpy as np
    >>> hc = np.arange(4).reshape(2, 2)
    >>> hc
    array([[0, 1],
           [2, 3]])
    >>> lines = get_lines_enum_np(hc)
    >>> lines
    {0: array([0, 2]), 1: array([1, 3]), 2: array([0, 1]), 3: array([2, 3]), 4: array([0, 3]), 5: array([2, 1])}
    """
    
    lines: Lines_enum_np = dict()
    idx = 0
    for line in get_lines_np(hc):
        lines[idx] = line
        idx += 1
    return lines


def get_scopes_enum_np(lines: Lines_enum_np, d: int) -> Scopes_enum:
    """ 
    get_scopes_enum_np(lines: Lines_enum_np, d: int) -> Scopes_enum:
    
    Calculate the scope of each cell in a hypercube

    Parameters
    ----------
    lines
        The returned value from get_lines_enum_np(hc) where hc is of the
        form np.arange(n ** d, dtype = intxx).reshape([n] * d).
        That is, hc is populated with the values 0,1,2,...,n^d - 1.

    dim
        The dimension of the hypercube that was used to
        generate `lines`.

    Returns
    -------
    
        A dictionary with keys equal to each cell coordinates of the 
        hypercube. For each cell key, the value is the cell's
        scope - a list of line enumerations that are lines containing
        the cell.

    See Also
    --------
    get_lines_enum_np

    Examples
    --------
    >>> import numpy as np
    >>> from pprint import pprint
    >>> hc = np.arange(4).reshape(2, 2)
    >>> hc
    array([[0, 1],
           [2, 3]])
    >>> lines = get_lines_enum_np(hc)
    >>> lines
    {0: array([0, 2]), 1: array([1, 3]), 2: array([0, 1]), 3: array([2, 3]), 4: array([0, 3]), 5: array([2, 1])}
    >>> scopes = get_scopes_enum_np(lines, 2)
    >>> pprint(scopes) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [0, 2, 4],
                 (0, 1): [1, 2, 5],
                 (1, 0): [0, 3, 5],
                 (1, 1): [1, 3, 4]})
    """

    n = lines[0].size
    shape = [n] * d
    scopes: Scopes_enum = DefaultDict(list)

    for idx, line in lines.items():
        for j in range(n):
            cell = np.unravel_index(line[j], shape)
            scopes[cell].append(idx) 
    return scopes

def structure_enum_np(d: int, n: int, zeros: bool = True, OFFSET: int = 0) -> Structure_enum_np:
    """ 
    structure_enum_np(d: int, n: int, zeros: bool = True, 
                      OFFSET: int = 0) -> 
            Structure_enum_np:

    Return a hypercube, its enumerated lines and the scopes of 
    its cell scopes.

   Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension
    zeros
        If true, all values in array are 0, else they are 0,1,2,...
    base: int
        Tne number of cells is n^d. If this greater than 
        (2^31 - OFFSET - 1) then we use np.int64 (instead of np.int32)
        as the dtype of the numpy array.
 
    Returns
    -------
    
        A tuple containing the hypercube, its enumerated lines, and the
        scopes of its cells.
            
    See Also
    --------
    get_lines_enum_np
    get_scopes_enum_np
 
    Examples
    --------
    >>> import numpy as np
    >>> from pprint import pprint
    >>> struct = structure_enum_np(2, 2) 
    >>> struct[0]
    array([[0, 0],
           [0, 0]])
    >>> struct[1]
    {0: array([0, 0]), 1: array([0, 0]), 2: array([0, 0]), 3: array([0, 0]), 4: array([0, 0]), 5: array([0, 0])}
    >>> pprint(struct[2]) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [0, 2, 4],
                 (0, 1): [1, 2, 5],
                 (1, 0): [0, 3, 5],
                 (1, 1): [1, 3, 4]})
    >>> struct = structure_enum_np(2, 2, False) 
    >>> struct[0]
    array([[0, 1],
           [2, 3]])
    >>> struct[1]
    {0: array([0, 2]), 1: array([1, 3]), 2: array([0, 1]), 3: array([2, 3]), 4: array([0, 3]), 5: array([2, 1])}
    >>> pprint(struct[2]) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [0, 2, 4],
                 (0, 1): [1, 2, 5],
                 (1, 0): [0, 3, 5],
                 (1, 1): [1, 3, 4]})
    """

    # number of cells is n^d. If this greater than (2^31 - OFFSET - 1)
    # then we use int64. This is because the the get_scopes 
    # function populates the arrays with values 0,1,2, ...
    dtype = np.int64 if n ** d > 2 ** 31 - OFFSET - 1 else np.int32
    hc = np.arange(n ** d, dtype = dtype).reshape([n] * d)
    lines = get_lines_enum_np(hc)
    scopes = get_scopes_enum_np(lines, d)
    if zeros:
        hc.fill(0)
    return (hc, lines, scopes)


def get_diagonals_coord(d: int, n: int) -> Generator[Line_coord, None, None]:
    """ 
    get_diagonals_coord(d: int, n: int) -> 
        Generator[Line_coord, None, None]:
    
    Calculates the d-agonals coordinates of h(d, n). 

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension

    Yields
    -------
    
        d-gonals coordinates of the diagonals in h(d,n).

    Notes
    -----
    The number of corners of h(d, n) is 2^d. The number of d-agonals 
    is 2^d / 2 since two connecting corners form a line. 

    Examples
    --------
    >>> diags = get_diagonals_coord(2, 3)
    >>> list(diags)
    [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
    """    
    
    # comments below use an example with h(2, 3)

    # get an iterator of all corners. E.g.: (0,0), (0,2), (2,0), (2,2)
    corners_all = it.product([0, n - 1], repeat = d)
    # restrict to corners with 0 as first coordinate. E.g.: (0,0), (0,2)
    corners_0 = [corner for corner in corners_all if corner[0] == 0]
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
        
        yield diagonal


def get_lines_grouped_coord(d: int, n: int) -> Generator[Lines_coord, None, None]: 
    """ 
    get_lines_grouped_coord(d: int, n: int) -> 
        Generator[Lines_coord, None, None]:
    
    Generate the lines of a hypercube, h(d, n), grouped by the 
    number of dimensions spanned.

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension

    Yields
    -------

        lines (as coordinates) in h(d, n).
    
    See Also
    --------
    get_lines_i_coord

    Examples
    --------
    >>> lines = list(get_lines_grouped_coord(2, 2))
    >>> lines
    [[[(0, 0), (1, 0)], [(0, 1), (1, 1)], [(0, 0), (0, 1)], [(1, 0), (1, 1)]], [[(0, 0), (1, 1)], [(0, 1), (1, 0)]]]
    """
    
    for i in range(d): 
        yield from get_lines_i_coord(d, n, i)   
        

def get_lines_i_coord(d: int, n: int, i: int) -> Generator[Lines_coord, None, None]:
    """ 
    get_lines_i_coord(d: int, n: int, i: int) -> 
        Generator[Lines_coord, None, None]:

    Generates the lines of a hypercube that span the specified number
    of dimensions

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension
    i
        The number of dimensions that the returned lines must span

    Yields
    -------
    
        Lines in h(d, n) that span `i` dimensions.
                
    See Also
    --------
    num_lines_grouped

    Notes
    -----
    The notes section for the function num_lines_grouped provides a 
    sketch of a constructive proof for the number of lines in a 
    hypercube. This has been used to implement this function. 

    Examples
    --------
    >>> lines = list(get_lines_grouped_coord(2, 2))
    >>> lines
    [[[(0, 0), (1, 0)], [(0, 1), (1, 1)], [(0, 0), (0, 1)], [(1, 0), (1, 1)]], [[(0, 0), (1, 1)], [(0, 1), (1, 0)]]]
    """
    
    lines = []

    diagonals = list(get_diagonals_coord(i + 1, n))
    # loop over all possible combinations of i dimensions
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
            lines.extend(diags)
    
    yield lines


def get_lines_coord(d: int, n: int) -> Generator[Line_coord, None, None]: 
    """ 
    get_lines_coord(d: int, n: int) -> 
        Generator[Line_coord, None, None]:

    Returns the lines in a hypercube

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension

    Yields
    -------
    
        Lines in h(d, n).
                
    See Also
    --------
    get_lines_grouped_coord

    Examples
    --------
    >>> lines = list(get_lines_coord(2, 2))
    >>> lines
    [[(0, 0), (1, 0)], [(0, 1), (1, 1)], [(0, 0), (0, 1)], [(1, 0), (1, 1)], [(0, 0), (1, 1)], [(0, 1), (1, 0)]]
    >>> len(lines)
    6
    """
    
    grouped = get_lines_grouped_coord(d, n)
    flat = (x for y in grouped for x in y)
    yield from flat # return flat works as well but yield from this is explicit as to being a generator


def get_scopes_coord(lines: Lines_coord, d: int) -> Scopes_coord:
    """ 
    get_scopes_coord(lines: Lines_coord, d: int) -> Scopes_coord:

    Calculate the scope of each cell in a hypercube

    Parameters
    ----------
    lines
        The returned value from get_lines_coord(d, n).

    dim 
        The dimension of the hypercube that was used to
        generate `lines`.

    Returns
    -------
    
        A dictionary with keys equal to the coordinates of each cell in
        the hypercube. For each cell key, the value is the cell's
        scope - a list of coordinates that are lines containing
        the cell.
            
    See Also
    --------
    get_lines_coord
 
    Examples
    --------
    >>> from pprint import pprint
    >>> lines = list(get_lines_coord(2, 2))
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
    scopes: Scopes_coord = DefaultDict(list)
    cells = it.product(range(n), repeat = d) # get all possible cells

    for cell in cells:
        for line in lines:
            if cell in line:
                scopes[cell].append(line)
    return scopes


def structure_coord(d: int, n: int) -> Structure_coord:
    """ 
    structure_coord(d: int, n: int) -> Structure_coord:
    
    Return lines, and the scopes of its cells, for h(d, n)

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension
 
    Returns
    -------
    
        Lines, and the scopes of its cells, for h(d, n)
            
    See Also
    --------
    get_lines_coord
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

    lines = list(get_lines_coord(d, n))
    scopes = get_scopes_coord(lines, d)
    return (lines, scopes)


def get_lines_enum_coord(d: int, n: int) -> Lines_enum_coord: 
    """ 
    get_lines_enum_coord(d: int, n: int) -> Lines_enum_coord:

    Returns enumerated lines of a hypercube

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension

    Yields
    -------
    
        Enumerated lines in h(d, n).
                
    See Also
    --------
    get_lines_coord

    Examples
    --------
    >>> lines = get_lines_enum_coord(2, 2)
    >>> lines
    {0: [(0, 0), (1, 0)], 1: [(0, 1), (1, 1)], 2: [(0, 0), (0, 1)], 3: [(1, 0), (1, 1)], 4: [(0, 0), (1, 1)], 5: [(0, 1), (1, 0)]}
    """
    
    lines: Lines_enum_coord = dict()
    idx = 0
    for line in get_lines_coord(d, n):
        lines[idx] = line
        idx += 1
    return lines


def get_scopes_enum_coord(lines: Lines_enum_coord, d: int) -> Scopes_enum:
    """ 
    get_scopes_enum_coord(lines: Lines_enum_coord, d: int) -> 
        Scopes_enum:

    Calculate the scope of each cell in a hypercube

    Parameters
    ----------
    lines
        The returned value from get_lines_enum_coord(d, n).

    dim 
        The dimension of the hypercube that was used to
        generate `lines`.

    Returns
    -------
    
        A dictionary with keys equal to each cell coordinates of the 
        hypercube. For each cell key, the value is the cell's
        scope - a list of line enumerations that are lines containing
        the cell.
            
    See Also
    --------
    get_lines_enum_coord
 
    Examples
    --------
    >>> from pprint import pprint
    >>> lines = get_lines_enum_coord(2, 2)
    >>> pprint(lines) #doctest: +NORMALIZE_WHITESPACE
    {0: [(0, 0), (1, 0)],
     1: [(0, 1), (1, 1)],
     2: [(0, 0), (0, 1)],
     3: [(1, 0), (1, 1)],
     4: [(0, 0), (1, 1)],
     5: [(0, 1), (1, 0)]}
    >>> scopes = get_scopes_enum_coord(lines, 2)
    >>> pprint(scopes) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [0, 2, 4],
                 (0, 1): [1, 2, 5],
                 (1, 0): [0, 3, 5],
                 (1, 1): [1, 3, 4]})
    """

    n = len(lines[0])
    scopes: Scopes_enum = DefaultDict(list)
    cells = it.product(range(n), repeat = d) # get all possible cells

    for cell in cells:
        for idx, line in lines.items():
            if cell in line:
                scopes[cell].append(idx)
    return scopes


def structure_enum_coord(d: int, n: int) -> Structure_enum_coord:
    """ 
    structure_enum_coord(d: int, n: int) -> 
        Structure_enum_coord:
    
    Return enumerated lines, and the scopes of its cells, for h(d, n)

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension
 
    Returns
    -------
    
        Enumerated lines, and the scopes of its cells, for h(d, n)
            
    See Also
    --------
    get_lines_enum_coord
    get_scopes_enum_coord
 
    Examples
    --------
    >>> from pprint import pprint
    >>> struct = structure_enum_coord(2, 2) 
    >>> struct[0]
    {0: [(0, 0), (1, 0)], 1: [(0, 1), (1, 1)], 2: [(0, 0), (0, 1)], 3: [(1, 0), (1, 1)], 4: [(0, 0), (1, 1)], 5: [(0, 1), (1, 0)]}
    >>> pprint(struct[1]) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [0, 2, 4],
                 (0, 1): [1, 2, 5],
                 (1, 0): [0, 3, 5],
                 (1, 1): [1, 3, 4]})
    """

    lines = get_lines_enum_coord(d, n)
    scopes = get_scopes_enum_coord(lines, d)
    return (lines, scopes)


def get_scope_cell_coord(d: int, n: int, cell: Cell_coord) -> Generator[Line_coord, None, None]: 
    """ 
    get_scope_cell_coord(d: int, n: int, cell: Cell_coord) -> 
        Generator[Line_coord, None, None]:
    
    Calculate the scope for a cell.

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension
    cell
        The cell whose scope is to be calculated

    Yields
    ------

        Lines that form the scope of `cell`.

    See Also
    --------
    get_scopes_coord

    Notes
    -----    
    The scope for a specific cell can also be found by calling 
    get_scopes_coord and indexing with the cell. get_scopes_coord
    calculates the scope for every cell and stores this in a dictionary.
    get_scope_cell_coord only calculates the scope for the 
    specified cell.

    Examples
    --------
    >>> d = 3
    >>> n = 4
    >>> list(get_scope_cell_coord(d, n, (1,2,3))) # doctest: +NORMALIZE_WHITESPACE
    [[(0, 2, 3), (1, 2, 3), (2, 2, 3), (3, 2, 3)], [(1, 0, 3), (1, 1, 3), (1, 2, 3), (1, 3, 3)], 
     [(1, 2, 0), (1, 2, 1), (1, 2, 2), (1, 2, 3)], [(0, 3, 3), (1, 2, 3), (2, 1, 3), (3, 0, 3)]]
    """

    # loop over the numbers of dimensions
    for i in range(d): 
        # for each combination of i dimensions
        for i_comb in it.combinations(range(d), r = i + 1): 
            # increment call coordinates along all potential lines
            incr = it.product([-1, 1], repeat = i + 1) 
            seen: Line_coord = []
            for j in incr:
                
                # store potential lines. Could use a list but deque
                # makes it clear we are moving "up and down" the line
                d_line: Deque[Cell_coord] = Deque((cell,))
                
                # since we are moving "up and down" we don't need
                # to move "down and up" as well
                j_neg = tuple(-x for x in list(j))
                if j_neg not in seen:
                    seen.append(j)

                    for k in range(1, n):
                        jk = tuple(x * k for x in list(j)) # size of increments
                        # record cells positions of increments
                        d_line.appendleft(increment_cell_coord(cell, i_comb, jk))
                        d_line.append(increment_cell_coord(cell, i_comb, jk, False))                        
                
                    # some calculated cells will simply not be part of the board
                    line = remove_invalid_cells_coord(n, list(d_line))
                    # we only want lines that are winning lines
                    if len(line) == n:
                        yield line


def scopes_size(scopes: Scopes) -> Counter:
    """ 
    scopes_size(scopes: Scopes) -> Counter:

    Calculate the different scope lengths.

    Parameters
    ----------
    scopes
        Dictionary of cells (keys) and their scopes
 
    Returns
    -------
    
        Counter of scopes lengths (key) and their frequency (values).
            
    See Also
    --------
    get_scopes_np
    get_scopes_coord
 
    Examples
    --------
    >>> import numpy as np
    >>> scopes = structure_np(2, 3)[2] 
    >>> scopes_size(scopes) == Counter({2: 4, 3: 4, 4: 1})
    True
    >>> scopes = structure_enum_np(2, 3)[2] 
    >>> scopes_size(scopes) == Counter({2: 4, 3: 4, 4: 1})
    True
    >>> scopes = structure_coord(2, 3)[1]
    >>> scopes_size(scopes) == Counter({2: 4, 3: 4, 4: 1})
    True
    >>> scopes = structure_enum_coord(2, 3)[1]
    >>> scopes_size(scopes) == Counter({2: 4, 3: 4, 4: 1})
    True
    """
    
    return Counter([len(scope) for scope in scopes.values()])


def scopes_size_cell(scopes: Scopes) -> DefaultDict[int, List[Cell_coord]]:
    """ 
    scopes_size_cell(scopes: Scopes) -> 
        DefaultDict[int, List[Cell_coord]]:

    Group cells by length of their scope.

    Parameters
    ----------
    scopes
        Dictionary of cells (keys) and their scopes
 
    Returns
    -------

        Dictonary of scopes lengths (key) and the list of cells with scopes of that length.
            
    See Also
    --------
    get_scopes_np
    get_scopes_coord
    get_scopes_enum
 
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
    >>> scopes = structure_enum_np(2, 3)[2] 
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
    >>> scopes = structure_enum_coord(2, 3)[1] 
    >>> pprint(scopes_size_cell(scopes))
    defaultdict(<class 'list'>,
                {2: [(0, 1), (1, 0), (1, 2), (2, 1)],
                 3: [(0, 0), (0, 2), (2, 0), (2, 2)],
                 4: [(1, 1)]})
    """

    scopes_size_cell: DefaultDict[int, List[Cell_coord]] = DefaultDict(list)
    for cell, scope in scopes.items():
        scopes_size_cell[len(scope)].append(cell)

    return scopes_size_cell


####################################################################################################
# The following 3 functions are for the displaying of a hypercube to a terminal. 
# It is assumed that an numpy ndarray has been used to represent the hypercube

def display_np(hc: Cube_np, display_cell: Callable[[Any], Tuple[str, str, str]] = None, ul = False) -> str:
    """ 
    display_np(hc: Cube_np, display_cell: Callable[[Any], 
               Tuple[str, str, str]] = None, ul = False) -> 
        str:
    
    Construct a string to display the hypercube in the terminal.

    Parameters
    ----------
    hc
        The hypercube to be displayed
    display_cell
        A callback function called with the value of each cell value.
        It returns a tuple of strings - the character/string to be 
        displayed,  and any formatting to be applied (typically ansi 
        color sequences). See Examples for how colors are specified.
        If display_cell is not provided, the cell value is displayed.
    ul
        display_np calls itself recursively (see Notes). This parameter 
        is used to track whether a cell is on the bottom row of a 
        2-d array. It has direct impact when the user calls dislay_np
        unless the array is 1-d, in which case it determines if cell
        values are underlined when displayed. 

    Returns
    -------

        A string that can be printed to the terminal to display the
        hypercube.

    See Also
    --------
    underline
    join_multiline
    
    Notes
    -----
    The '|' character is used to represent the board horizontally.
    Cell contents are underlined in order to represent the board
    vertically. For example, the character 'X' is underlined to 
    give 'X̲'. This function is recursive, it starts with hypercube and 
    keeps removing dimensions until at a single cell, which can be
    given a string value. We are trying to display d dimensions in 
    two dimensions. To do this, odd dimensions are 
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
    >>> hc = np.zeros((n,) * d, dtype = int)
    >>> hc[0, 0, 0] = 1
    >>> hc[1, 1, 1] = -1
    >>> disp = display_np(hc, dc)
    >>> print(disp) #doctest: +SKIP
    X̲|_|_   _|_|_   _|_|_
    _|_|_   _|O̲|_   _|_|_
     | |     | |     | | 
    """

    if hc.size == 1: # hc is a single cell
        if display_cell is None:
            s, pre_fmt, post_fmt = str(hc), '', ''
        else:
            s, pre_fmt, post_fmt = display_cell(hc)

        # underline displayed string (to repsent board structure) unless 
        # string is in the bottom row of array
        if ul:
            s = '_' * len(s) if s.isspace() else underline(s)
            
        return pre_fmt + s + post_fmt

    # hc is not a single cell
    d = hc.ndim
    # break the array into sub arrays along the first dimension
    sub_hc = [hc[i] for i in range(hc.shape[0])]

    # constuct a string for each sub array
    sub_hc_str = []
    for c, a in enumerate(sub_hc):
        if d == 2 and c == len(sub_hc) - 1:
            # sub arr is 2-dimensional and last row - don't underline
            ul = False
        elif d != 1:
            ul = True

        sub_hc_str.append(display_np(a, display_cell, ul))

    # join the sub strings
    if d % 2 == 0: # even number of dimensions - display down the screen
        if d == 2:
            return ''.join('\n'.join(sub_hc_str))
        else:
            sp = '\n' + '\n' * (int((d / 2) ** 1.5) - 1) # increase space between higher dimesions  
            return sp.join(sub_hc_str)
    else: # odd number of dimensions - display across the screen
        if d == 1:
            return '|'.join(sub_hc_str)
        else:
            return join_multiline(sub_hc_str, ' ' + ' ' * int((d - 2) ** 1.5) + ' ', False)


def underline(s: str, alpha_only = True) -> str:
    """ 
    underline(s: str, alpha_only = True) -> str
    
    Underlines a string.

    Parameters
    ----------
    s
        The string to be underlined

    Returns
    -------

        An underlined string 

    Notes
    -----
    The code appears only to work properly with alphabetic characters.

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
    """ 
    join_multiline(iter: Iterable[str], divider: str = ' ', 
                   divide_empty_lines: bool = False, 
                   fill_value: str = '_') -> 
        str
    
    Join multiline string line by line.

    Parameters
    ----------
    iter
        An iterable of multiline (or single line) strings 
    divider
        String to divide the corresponding lines in each iterable
    divide_empty_lines
        If the corresponding line in each iterable is blank, then 
        determines if the lines are still divided by divider, or 
        divided by ''.
    fill_value
        If the number of lines in each multiline string in iter
        differs, then fill_value is used to fill in values of the
        shorter strings.

    Returns
    -------

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
####################################################################################################


####################################################################################################
# The following functions are helper functions

def slice_ndarray(arr: Cube_np, dims: Collection[int], coords: Collection[int]) -> Cube_np:
    """ 
    slice_ndarray(arr: Cube_np, dims: Collection[int], 
                  coords: Collection[int]) -> 
        Cube_np:
    
    Returns a slice of a hypercube. 

    Parameters
    ----------
    arr
        The hypercube to be sliced
    dims
        The dims to slice along
    coords
        The coordinates corresponding to the dimensions being sliced

    Returns
    -------

        A view of a slice of `arr`.

    Raises
    ------
    ValueError
        If length of `dims` is not equal to length of `coords`

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
    if len(dims) != len(coords):
        raise ValueError("dims and coords must be of the same length")
    
    for dim, coord in zip(dims, coords):
        sl[dim] = coord
    
    return arr[tuple(sl)]


def insert_into_tuple(tup: Tuple, pos: Union[int, Collection[int]], val: Any) -> Tuple[int, ...]:
    """ 
    insert_into_tuple(tup: Tuple, pos: Union[int, Collection[int]], 
                      val: Any) -> 
        Tuple[int, ...]:
    
    Insert values into a tuple. 

    Parameters
    ----------
    tup
        the tuple into which values are to be inserted
    pos
        The positions into which values are to be inserted
    val
        The values corresponding to the positions in `pos`

    Returns
    -------

        A copy of `tup` with values inserted.

    Raises
    ------
    ValueError
        If length of `pos` is not equal to length of `val`

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


def increment_cell_coord(cell: Cell_coord, pos: Sequence[int], incr: Sequence[int], add: bool = True) -> Cell_coord:
    """
    increment_cell_coord(cell: Cell_coord, pos: Sequence[int], 
                         incr: Sequence[int], add: bool = True) -> 
        Cell_coord:
    
    Increments coordinates of a cell.

    Parameters
    ----------
    cell
        the cell which will have coordinates incremented
    pos
        The coordinates which are to be incremented
    incr
        The increment values at the specified coordinates
    add
        If True, the the increments are added, else they are subtracted

    Returns
    -------

        A copy of `cell` with incremented coordinates.

    Raises
    ------
    ValueError
        If length of `pos` is not equal to length of `val`

    Examples
    --------
    >>> cell = (1, 2, 1)
    >>> pos = (0, 2)
    >>> incr = (1, -1)
    >>> increment_cell_coord(cell, pos, incr)
    (2, 2, 0)
    >>> increment_cell_coord(cell, pos, incr, False)
    (0, 2, 2)
    """

    if len(pos) != len(incr):
        raise ValueError("pos and incr must be of the same length")

    if len(pos) == 0:
        return cell

    cl = list(cell)
    for i in range(len(pos)):
        if add:
            cl[pos[i]] += incr[i]
        else:
            cl[pos[i]] -= incr[i]

    return tuple(cl)


def str_to_tuple(d: int, n: int, cell: str, offset: int = 1) -> Cell_coord:
    """ 
    str_to_tuple(d: int, n: int, cell: str, offset: int = 1) -> 
        Cell_coord:
    
    Returns cells coordinates provided as a string as a tuple 
    of integers.

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension
    cell
        Cell coordinates specified as a string (see Notes).
        Will accept a non-string argument which will be cast
        to a string.
    offset
        idx offset - typically 0 or 1.
 
    Raises
    ------
    ValueError
        1. if digits are not separated and the n is greater than 9
        2. Incorrect numbers of coordinates provided
        3. One or more coordinates is not valid

    Notes
    -----
    If the string is all digits then assumes that each digit is a 
    coordinate. If non-digit characters are provided then assumes that
    these split coordinates.

    Returns
    -------

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


def remove_invalid_cells_coord(n:int, line: Line_coord) -> Line_coord:
    """ 
    remove_invalid_cells_coord(n:int, line: Line_coord) -> Line_coord

    Remove cells that do not have valid coordinates.

    Parameters
    ----------
    n
        The number of cells in any dimension
    line
        list of tuples representing cell coordinates (possibly invalid)
 
    Returns
    -------

        list of tuples representing valid cell coordinate

    Examples
    --------
    >>> n = 3
    >>> line = [(1, 2, 0), (-1, 0, 3), (0, 1, 2), (1, 2, 3)]
    >>> remove_invalid_cells_coord(n, line)
    [(1, 2, 0), (0, 1, 2)]
    """

    rl = []
    for cell in line:
        if all(coord in range(n) for coord in cell):
            rl.append(cell)

    return rl

####################################################################################################


# used in internal testing
def _lines_np_coord_check(d: int, n: int) -> bool:
    """ 
    _lines_np_coord_check(d: int, n: int) -> bool

    Checks if lines_np and lines_coord give the same lines.

    Parameters
    ----------
    d
        The number of dimensions of the hypercube
    n
        The number of cells in any dimension

    Returns
    -------

        True if lines_np and lines_coord give the same lines.
        False otherwise.

    See Also
    --------
    get_lines_np
    get_lines_coord

    Notes
    -----
    This function is a private function used in testing.
    """

    dtype = np.int64 if n ** d > 2 ** 31 else np.int32
    arr = np.arange(n ** d, dtype = dtype).reshape([n] * d)

    lines_np = get_lines_np(arr)
    lines_coord = get_lines_coord(d, n)

    t_np = [tuple(sorted(l.tolist())) for l in lines_np] # type: ignore
    t_coord = [tuple(sorted([arr[c] for c in l])) for l in lines_coord] 

    return set(t_np) == set(t_coord)
    
