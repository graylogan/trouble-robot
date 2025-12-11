class Player:
    def __init__(self, current_location=None, team=None):
        self.team = team

        # Default starting locations by team
        if team == "Blue":
            current_location = ["X13", "Y30"]
        elif team == "Green":
            current_location = ["X255", "Y30"]
        elif team == "Red":
            current_location = ["X255", "Y170"]
        elif team == "Yellow":
            current_location = ["X8", "Y170"]

        self.current_location = current_location
