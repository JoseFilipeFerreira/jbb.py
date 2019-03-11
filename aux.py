import json

def save_stats(bot):
#save server stats
    with open(bot.STATS_PATH, 'w') as file:
        json.dump(
            {"last_giveaway":bot.last_giveaway, "stats": bot.stats}
            , file, indent=4)
    
def hours_passed(past, present):
#gets two timestamps in seconds and returns how many hours have passed
    return (present - past)/3600

def checkArray(tester, s):
    result = False
    for test in tester:
        result = result or test in s
    return result

def round_down(num, divisor):
#round down a num to the nearest multiple of a divisor
    return num - (num%divisor)

def enough_cash(bot, id, amount):
    if bot.stats[id]["cash"] >= amount:
        return True
    else:
        return False

def spend_cash(bot, id, amount):
#spend a users money
    if bot.stats[id]["cash"] >= amount:
        bot.stats[id]["cash"] -= amount
        return True
    else:
        return False
    
def get_cash(bot, id, amount):
#spend a users money
    bot.stats[id]["cash"] += amount

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False