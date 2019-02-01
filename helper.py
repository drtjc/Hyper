def underline(s):
    try:
        return ''.join([chr + "\u0332" for chr in str(s)])
    except:
        return str





def join_multiline_(it, divide_1 = ' ',  divide_1_at = None, divide_2 = None):

    # for each multiline block, split into individual lines
    spl = [x.split('\n') for x in it]
    
    # create list of tuples with tuple i containing line i from each multiline block
    tl = [i for i in zip(*spl)]
    
    # and create a string from each tuple, with tuple elements separated by the divides
    if divide_1_at is not None:
        st = [divide_2.join([divide_1.join(t[:divide_1_at]), 
                             divide_2.join(t[divide_1_at:])]) 
              for t in tl]
    else:
        st = [divide_1.join(t) for t in tl]

    # finally, join each string separated by a new line 
    return '\n'.join(st)
    
    # TEST IF DIFF LENGTHS
    #if len(spl_1) != len(spl_2):
    #    raise ValueError("Both strings must have the same number of lines")

def join_multiline(it, divide = ' '):

    # for each multiline block, split into individual lines
    spl = [x.split('\n') for x in it]
    
    # create list of tuples with tuple i containing line i from each multiline block
    tl = [i for i in zip(*spl)]
    
    
    st = [divide.join(t) for t in tl]

    # finally, join each string separated by a new line 
    return '\n'.join(st)
    
    # TEST IF DIFF LENGTHS
    #if len(spl_1) != len(spl_2):
    #    raise ValueError("Both strings must have the same number of lines")
