def unique(it: Iterable[Any]) -> bool:
    """ check if all elements of an iterable of unqiue
    Parameters
    ----------
    it : Iterable[Any]
        The iterable to be checked for unique elements
    Returns
    -------
    bool:
        True if all elements of `it` of unique; False otherwise
 
    Notes
    -----
    Iterates over every element until a match is found (or not
    found if all elements are unique).
    If the elements of `it` are hashable then code such as
    len(it) == len(set(it)) is more more efficient.
  
    Examples
    --------
    >>> it = [[0, 1], [0,2], [0,1]]
    >>> unique(it)
    False
    >>> it = [[0, 1], [0,2], [1,2]]
    >>> unique(it)
    True
    """

    seen = []
    return not any(i in seen or seen.append(i) for i in it)

    

