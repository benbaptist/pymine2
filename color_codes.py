section = u"\xa7" #167 hex

black = section + "0"
darkblue = section + "1"
darkgreen = section + "2"
darkaqua = section + "3"
darkred = section + "4"
darkpurple = section + "5"
gold = section + "6"
gray = section + "7"
darkgray = section + "8"
blue = section + "9"
green = section + "a"
aqua = section + "b"
red = section + "c"
lightpurple = section + "d"
yellow = section + "e"
white = section + "f"

def replace_color_codes(text):
    replaced = text
    replaced = replaced.replace("&0", black)
    replaced = replaced.replace("&1", darkblue)
    replaced = replaced.replace("&2", darkgreen)
    replaced = replaced.replace("&3", darkaqua)
    replaced = replaced.replace("&4", darkred)
    replaced = replaced.replace("&5", darkpurple)
    replaced = replaced.replace("&6", gold)
    replaced = replaced.replace("&7", gray)
    replaced = replaced.replace("&8", darkgray)
    replaced = replaced.replace("&9", blue)
    replaced = replaced.replace("&a", green)
    replaced = replaced.replace("&b", aqua)
    replaced = replaced.replace("&c", red)
    replaced = replaced.replace("&d", lightpurple)
    replaced = replaced.replace("&e", yellow)
    replaced = replaced.replace("&f", white)
    return replaced