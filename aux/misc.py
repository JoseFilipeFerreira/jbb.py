def hours_passed(past, present):
#gets two timestamps in seconds and returns how many hours have passed
    return (present - past)/3600

def minutes_passed(past, present):
#gets two timestamps in seconds and returns how many hours have passed
    return (present - past)/60

def round_down(num, divisor):
#round down a num to the nearest multiple of a divisor
    return num - (num%divisor)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
