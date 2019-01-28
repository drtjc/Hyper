def underline(s):
    try:
        return ''.join([chr + "\u0332" for chr in str(s)])
    except:
        return str