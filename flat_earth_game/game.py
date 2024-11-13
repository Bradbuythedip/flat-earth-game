"""
Main game module for the Flat Earth Debate Game.
"""

from .argument_analyzer import ArgumentAnalyzer
from .game_state import GameState

class FlatEarthDebateGame:
    """
    Main game class that coordinates the gameplay elements.
    """
    
    def __init__(self):
        """Initialize a new game instance."""
        self.game_state = GameState()
        self.analyzer = ArgumentAnalyzer()
        
    def process_argument(self, argument):
        """
        Process a player's argument and return the game's response.
        
        Args:
            argument (str): The player's argument text
            
        Returns:
            dict: Game response including scores and AI rebuttal
        """
        category, score = self.analyzer.analyze_argument(argument)
        
        if category is None:
            return {
                "success": False,
                "message": "I don't understand how that proves the Earth is round. Please provide clearer evidence.",
                "state": self.game_state.get_status()
            }
            
        if category in self.game_state.used_arguments:
            score = score // 2
            repeat_message = "This type of argument has been used before. Reduced effectiveness."
        else:
            repeat_message = None
            
        self.game_state.used_arguments.add(category)
        self.game_state.update_score(score)
        
        rebuttal = self.analyzer.get_rebuttal(category)
        
        return {
            "success": True,
            "category": category,
            "score": score,
            "rebuttal": rebuttal,
            "repeat_message": repeat_message,
            "state": self.game_state.get_status(),
            "evidence_type": self.analyzer.get_evidence_description(category)
        }
        
    def get_hint(self):
        """
        Get a gameplay hint based on current state.
        
        Returns:
            str: A helpful hint for the player
        """
        unused_categories = set(self.analyzer.evidence_weights.keys()) - self.game_state.used_arguments
        if unused_categories:
            import random
            category = random.choice(list(unused_categories))
            return f"Try using evidence about {self.analyzer.get_evidence_description(category)}"
        return "Try combining different types of evidence in your argument"

def main():
    """Run the game in console mode."""
    game = FlatEarthDebateGame()
    
    print("\n=== Flat Earth Debate Game ===")
    print("\nYour goal: Convince the AI that the Earth is round using scientific arguments.")
    print("Win condition: Reach a credibility score of 100 points.")
    print("\nTip: Use clear, scientific explanations. Different types of evidence have different weights.")
    
    while not game.game_state.is_convinced():
        state = game.game_state.get_status()
        print(f"\nCurrent Credibility Score: {state['credibility_score']}")
        print(f"AI Skepticism Level: {state['skepticism']}%")
        print(f"Attempts so far: {state['attempts']}")
        
        print("\nPresent your argument (or type 'quit' to exit):")
        player_argument = input("> ").strip()
        
        if player_argument.lower() == 'quit':
            print("\nGame ended by player.")
            break
            
        result = game.process_argument(player_argument)
        
        if not result["success"]:
            print(f"\nAI: {result['message']}")
            continue
            
        if result["repeat_message"]:
            print(f"\nNote: {result['repeat_message']}")
            
        print(f"\nAI: {result['rebuttal']}")
        
        if game.game_state.is_convinced():
            print(f"\nCongratulations! You've convinced the AI in {state['attempts']} attempts!")
            print(f"Final Credibility Score: {state['credibility_score']}")
            break
            
        if state['attempts'] % 3 == 0:
            print(f"\nHint: {game.get_hint()}")

if __name__ == "__main__":
    main()