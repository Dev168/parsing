

def get_bookmakers():

    from bookmakers.sbobet import Sbobet
    from bookmakers.marathonbet import Marathonbet

    return Sbobet, Marathonbet
