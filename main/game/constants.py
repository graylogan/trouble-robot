ROLL_AGAIN = 6

# generate coordinate mapping
X_VALUES = [27, 68, 101, 136, 169, 200, 233, 270]
Y_VALUES = [14, 53, 85, 120, 158]
GRBL_COORDINATES: list[list[tuple[str, str]]] = []
for i, x in enumerate(X_VALUES):
    GRBL_COORDINATES.append([])
    for y in Y_VALUES:
        GRBL_COORDINATES[i].append(("X" + str(x), "Y" + str(y)))

PLAYER_TO_HOME = {"BLUE": (0, 0), "RED": (0, 4), "GREEN": (7, 4), "YELLOW": (7, 0)}

# plotter sleeps
BASE_SLEEP = 1
UNIT_SLEEP = 0.15

ENCODE_PLAYER_COLOR = {"BLUE": 0, "RED": 1, "GREEN": 2, "YELLOW": 3}

MAGNET_PIN = 11