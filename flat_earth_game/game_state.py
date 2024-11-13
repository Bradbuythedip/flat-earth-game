"""
Module for managing the game state in the Flat Earth Debate Game.
"""

class GameState:
    """
    Manages the current state of the game, including scores and progress.
    """
    
    def __init__(self):
        """Initialize a new game state with default values."""
        self.credibility_score = 0
        self.attempts = 0
        self.confidence_threshold = 100
        self.used_arguments = set()
        self.current_skepticism = 100
        
    def update_score(self, score_change):
        """
        Update the game state based on a new argument.
        
        Args:
            score_change (int): The points to add to the credibility score
        """
        self.credibility_score += score_change
        self.attempts += 1
        self.current_skepticism = max(0, self.current_skepticism - (score_change / 2))
        
    def is_convinced(self):
        """
        Check if the AI has been convinced.
        
        Returns:
            bool: True if the credibility score exceeds the confidence threshold
        """
        return self.credibility_score >= self.confidence_threshold
        
    def get_status(self):
        """
        Get a dictionary containing the current game status.
        
        Returns:
            dict: Current game state information
        """
        return {
            "credibility_score": self.credibility_score,
            "attempts": self.attempts,
            "skepticism": self.current_skepticism,
            "convinced": self.is_convinced(),
            "used_arguments": list(self.used_arguments)
        }