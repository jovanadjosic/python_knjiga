class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # High score should never be reset.
        self.high_score = self.load_high_score()
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left=self.settings.ship_limit
        self.score = self.load_high_score()
        self.level = 1
    
    def load_high_score(self):
        """Load the high score from a file."""
        try:
            with open('high_score.txt', "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0
    
    def save_high_score(self):
        """Save the high score to a file."""
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))