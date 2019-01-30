def underline(s):
    try:
        return ''.join([chr + "\u0332" for chr in str(s)])
    except:
        return str


# turn into iterable parameter
def join_multiline0(s1, s2):

    spl_1 = s1.split('\n')
    spl_2 = s2.split('\n')

    if len(spl_1) != len(spl_2):
        raise ValueError("Both strings must have the same number of lines")

    return '\n'.join([x + " " + y for x, y in zip(spl_1, spl_2)])


def join_multiline(it):

    # for each multiline block, split into individual lines
    spl = [x.split('\n') for x in it]
    
    # create list of tuples with tuple i containing line i from each multiline block
    tl = [i for i in zip(*spl)]
    
    # and create a string from each tuple, with tuple elements separated by a space
    st = [' '.join(t) for t in tl]

    # finally, join each string separated by a new line 
    return '\n'.join(st).rstrip(' ') 
    
    #if len(spl_1) != len(spl_2):
    #    raise ValueError("Both strings must have the same number of lines")

