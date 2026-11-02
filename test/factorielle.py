def factorielle(n):
    if n == 1: 
        return 1 
    elif n < 0: 
        raise ValueError(f"{n} est négatif, la factorielle n'est pas définie")
    else: 
        return n * factorielle(n - 1)