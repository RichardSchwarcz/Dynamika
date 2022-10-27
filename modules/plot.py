def plotSchema(points):
    point_1 = [A.x, A.y]
    point_2 = [B.x, B.y]


def highlightNotZero(x):
    if -1*10**-3 < x < 1*10**-3:
        # gray
        color = "#f2f2f2"
    elif x > 1*10**-3:
        # green
        color = "#E1FFD5"
    elif x < 1*10**-3:
        # red
        color = "#FFDCD5"
    return f"background: {color}"
