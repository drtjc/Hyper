def underline(str):
    try:
        return ''.join([chr + "\u0332" for chr in str])
    except:
        return str