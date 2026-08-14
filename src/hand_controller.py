class HandToggleController:

    def __init__(self, cooldown=1.0):
        self.enabled = True
        self.last_state = False
        self.last_toggle_time = 0
        self.cooldown = cooldown

    def update(self, hand_present, current_time):
        """
        Toggle detection when a hand first appears.
        """

        if hand_present and not self.last_state:

            if current_time - self.last_toggle_time > self.cooldown:
                self.enabled = not self.enabled
                self.last_toggle_time = current_time

        self.last_state = hand_present

        return self.enabled