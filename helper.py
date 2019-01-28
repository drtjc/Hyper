def underline(s):
    try:
        return ''.join([chr + "\u0332" for chr in str(s)])
    except:
        return str


def join_multiline(s1, s2):

    spl_1 = s1.split('\n')
    spl_2 = s2.split('\n')

    if len(spl_1) != len(spl_2):
        raise ValueError("Both strings must have the same number of lines")

    return '\n'.join([x + " " + y for x, y in zip(spl_1, spl_2)])