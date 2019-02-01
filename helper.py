def underline(s):
    try:
        return ''.join([chr + "\u0332" for chr in str(s)])
    except:
        return str


def join_multiline(it, divider = ' ', divide_empty_lines = False):

    # for each multiline block, split into individual lines
    spl = [x.split('\n') for x in it]
    
    # create list of tuples with tuple i containing line i from each multiline block
    tl = [i for i in zip(*spl)]
    
    
    if divide_empty_lines:
        st = [divider.join(t) for t in tl]
    else:
        st = []
        for t in tl:
            if all([x.strip() == '' for x in t]):
                st.append('')
            else:
                st.append(divider.join(t))

    # finally, join each string separated by a new line 
    return '\n'.join(st)
    
    # TEST IF DIFF LENGTHS
    #if len(spl_1) != len(spl_2):
    #    raise ValueError("Both strings must have the same number of lines")
