import random
def arrReader():
    choice = bool(random.getrandbits(1))
    if choice:
        print("Nothing")
        return []
    else:
        choice = bool(random.getrandbits(1))
        if choice:
            print("dot")
            return [1]
        else:
            choice = bool(random.getrandbits(1))
            if choice:
                print("dot")
                return [-1]
            else:
                return [0]