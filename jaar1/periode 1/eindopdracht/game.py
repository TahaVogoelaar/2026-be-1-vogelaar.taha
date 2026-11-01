import curses
import random
import time

# gemaakt met ai
POKEMON = {
    "pikachu":    {"type": "electric", "hp": 35, "power": 12},
    "charmander": {"type": "fire",     "hp": 39, "power": 11},
    "squirtle":   {"type": "water",    "hp": 44, "power": 10},
    "bulbasaur":  {"type": "grass",    "hp": 45, "power": 9},
    "eevee":      {"type": "normal",   "hp": 40, "power": 10},
    "geodude":    {"type": "rock",     "hp": 40, "power": 13},
    "machop":     {"type": "fighting", "hp": 45, "power": 12},
    "gastly":     {"type": "ghost",    "hp": 30, "power": 14},
    "onix":       {"type": "rock",     "hp": 35, "power": 15},
    "mewtwo":     {"type": "psychic",  "hp": 50, "power": 16},
}

# gemaakt met ai help maar zelf geschreven
def drawTarget(stdscr, cursor, target):
    stdscr.erase()
    stdscr.border()
    height, width = stdscr.getmaxyx()
    height -= 2
    width -= 2
    ch = "#"

    curses.start_color()
    curses.use_default_colors()                                # -1 = default bg
    curses.init_pair(1, curses.COLOR_RED, -1)                  # pair 1 = red on default
    curses.init_pair(2, curses.COLOR_GREEN, 2)                  # pair 1 = red on default

    # 2) build the attribute once
    red_bold = curses.color_pair(1) | curses.A_BOLD
    green_bold = curses.color_pair(2) | curses.A_BOLD

    for i in range(width):
        i += 1
        for j in range(height):
            j += 1
            stdscr.addstr(j, i, ch)


    # draw target
    for i in range(height):
        i+=1
        stdscr.addstr(i, target-1, "|", red_bold)
        stdscr.addstr(i, target, "|", red_bold)
        stdscr.addstr(i, target+1, "|", red_bold)

    # draw cursor
    for i in range(height):
        i+=1
        stdscr.addstr(i, cursor-1, "|", green_bold)
        stdscr.addstr(i, cursor, "|", green_bold)
        stdscr.addstr(i, cursor+1, "|", green_bold)
    

    stdscr.refresh()


# gemaakt met ai help maar zelf geschreven
def attack(stdscr):
    stdscr.nodelay(True)
    curses.curs_set(0)
    height, width = stdscr.getmaxyx()

    hitPrecentage = 0
    cursorDir = True
    hit = False
    cursor = 1
    target = random.randint(2, width - 2)

    while not hit:
        # cursor bounce
        if cursor > width - 3:
            cursorDir = False
        elif cursor < 2:
            cursorDir = True

        if(cursorDir):
            cursor+=1
        elif not cursorDir:
            cursor-=1

        drawTarget(stdscr, cursor, target)
        time.sleep(.005)

        key = stdscr.getch()
        if key == ord(' '):
            hitPrecentage = abs(cursor - target)
            hit = True


    
    stdscr.erase()
    stdscr.refresh()

    stdscr.nodelay(False)
    print(hitPrecentage)
    stdscr.getch()

    return hitPrecentage


def ask_name():
    while True:
        name = input("Wat is je naam? ").strip()
        if name == "":
            print("Je moet wel iets invullen!")
        else:
            return name


def choose_pokemon2():
    names = list(POKEMON.keys())
    for i, n in enumerate(names, 1):
        s = POKEMON[n]
        print(f"{i:2}. {n.title():12} | {s['type']:10} {s['hp']} HP  {s['power']} pwr")
    while True:
        try:
            c = int(input(f"Kies (1-{len(names)}): "))
            if 1 <= c <= len(names):
                return names[c-1]
        except ValueError:
            pass
        print("Ongeldige keuze")

# gemaakt met ai help maar zelf geschreven
def choose_pokemon():
    names = list(POKEMON.keys())
    for i, n in enumerate(names, 1):
        s = POKEMON[n]
        print(str(i) + ". " + n.title() + " | Stats: " + s['type'] + " HP: " + str(s['hp']) + " Power: " + str(s['power']))
    while True:
        try:
            c = int(input("Kies een nummer: "))
            if 1 <= c <= len(names):
                return names[c-1]
        except ValueError:
            pass
        print("Ongeldige keuze")


def fight(p_name, p_stats, e_name, e_stats):
    p_hp = p_stats['hp']
    e_hp = e_stats['hp']

    print(p_name.title() + " vs " + e_name.title() + " ===")
    print("Druk op SPATIE als de groene lijn de rode raakt!")

    while p_hp > 0 and e_hp > 0:
        # jouw aanval
        dist = curses.wrapper(attack)
        dmg = max(1, p_stats['power'] - dist // 2)
        e_hp = e_hp - dmg
        if e_hp < 0:
            e_hp = 0
        print("Je raakt " + e_name.title() + " voor " + str(dmg) + "! (vijand: " + str(e_hp) + " HP)")

        if e_hp <= 0:
            print("Je versloeg " + e_name.title() + "!")
            return True

        # vijand valt aan
        edmg = random.randint(1, e_stats['power'])
        p_hp = p_hp - edmg
        if p_hp < 0:
            p_hp = 0
        print(e_name.title() + " raakt jou voor " + str(edmg) + "! (jij: " + str(p_hp) + " HP)")

    print("Je bent verslagen door " + e_name.title() + "!")
    return False


def game_loop(name):
    p_name = choose_pokemon()
    print(f"Je koos {p_name.title()}!")
    while True:
        e_name = random.choice(list(POKEMON.keys()))
        e_stats = POKEMON[e_name]
        print(f"\nEen wilde {e_name.title()} verschijnt! ({e_stats['hp']} HP, {e_stats['power']} pwr)")
        if input("Wil je vechten? (j/n): ").strip().lower() != 'j':
            print("Je vlucht weg.")
            continue
        if fight(p_name, POKEMON[p_name], e_name, e_stats):
            if input("Nog een gevecht? (j/n): ").strip().lower() != 'j':
                print(f"Tot ziens, {name}!")
                break
        else:
            print("Game over!")
            break


def main():
    name = ask_name()
    game_loop(name)


main()
