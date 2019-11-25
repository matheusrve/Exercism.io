def flatten(iterable):

    output = []
    for e in iterable:
        if isinstance(e, int):
            output.append(e)
        else isinstance(e, (list, tuple, set, range)):
            output += flatten(e)
    return output