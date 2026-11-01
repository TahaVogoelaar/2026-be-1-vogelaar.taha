import curses
import random

def maakRandomArray(lengte, hoogte):
    return [random.randint(1, hoogte) for _ in range(lengte)]

def drawArr(stdscr, arr, arrW, height, highlight=-1, fixed=-1):
    stdscr.erase()
    stdscr.border()
    for x in range(arrW):
        attr = curses.A_NORMAL
        if x < fixed:
            attr = curses.A_DIM          # already sorted
        if x == highlight:
            attr = curses.A_REVERSE      # currently being examined
        for j in range(arr[x]):
            stdscr.addstr(height - 2 - j, 1 + x, "█", attr)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    height, width = stdscr.getmaxyx()

    arrH = height - 2
    arrW = width - 2
    arr  = maakRandomArray(arrW, arrH)

    drawArr(stdscr, arr, arrW, height)

    stdscr.erase()
    stdscr.border() 

    # display array


    stdscr.refresh()
    stdscr.getch()

    # sort
    for i in range(arrW):
        current = arr[i]

        # find smallest number
        smallest = i
        for j in range(i + 1, arrW):
            drawArr(stdscr, arr, arrW, height, highlight=j, fixed=i)
            if arr[j] < arr[smallest]:
                smallest = j

        # for end

        temp = arr[smallest]
        arr[smallest] = arr[i]
        arr[i] = temp

        drawArr(stdscr, arr, arrW, height)

    # for end

    stdscr.erase()
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)