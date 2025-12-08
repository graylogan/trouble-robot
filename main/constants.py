from serial_protocol import PlayerColor
encode_player_color = {"BLUE": PlayerColor.BLUE, "RED": PlayerColor.RED, "GREEN": PlayerColor.GREEN, "YELLOW": PlayerColor.YELLOW}
player_color_to_home_index = {"BLUE": 0, "RED": 4, "GREEN": 11, "YELLOW": 15}
BOARD_SIZE: int = 22
ROLL_AGAIN: int = 6