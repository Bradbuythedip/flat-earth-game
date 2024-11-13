"""
Unit tests for the Flat Earth Debate Game.
"""

import unittest
from flat_earth_game.game import FlatEarthDebateGame
from flat_earth_game.argument_analyzer import ArgumentAnalyzer
from flat_earth_game.game_state import GameState

class TestFlatEarthDebateGame(unittest.TestCase):
    """Test cases for the main game functionality."""
    
    def setUp(self):
        """Set up test cases."""
        self.game = FlatEarthDebateGame()
        
    def test_argument_analysis(self):
        """Test that arguments are correctly categorized."""
        analyzer = ArgumentAnalyzer()
        
        # Test satellite evidence
        category, weight = analyzer.analyze_argument("NASA has many satellite photos of Earth")
        self.assertEqual(category, "satellite")
        self.assertEqual(weight, 15)
        
        # Test gravity evidence
        category, weight = analyzer.analyze_argument("Gravity proves Earth is round")
        self.assertEqual(category, "gravity")
        self.assertEqual(weight, 20)
        
    def test_score_updating(self):
        """Test that scores are properly updated."""
        state = GameState()
        initial_score = state.credibility_score
        state.update_score(20)
        
        self.assertEqual(state.credibility_score, initial_score + 20)
        self.assertEqual(state.attempts, 1)
        
    def test_repeated_arguments(self):
        """Test that repeated arguments have reduced effectiveness."""
        # First use of satellite argument
        result = self.game.process_argument("NASA has satellite photos")
        initial_score = result["score"]
        
        # Repeat the same type of argument
        result = self.game.process_argument("There are many satellite images")
        self.assertEqual(result["score"], initial_score // 2)
        
    def test_winning_condition(self):
        """Test that the game can be won."""
        # Use different types of strong arguments
        arguments = [
            "Ships disappear bottom-first over the horizon",  # curvature
            "Gravity pulls everything to the center",         # gravity
            "Different time zones prove Earth is round",      # time zones
            "People have sailed around the world",           # circumnavigation
            "Satellites show Earth from space"               # satellite
        ]
        
        for arg in arguments:
            self.game.process_argument(arg)
            
        self.assertTrue(self.game.game_state.is_convinced())

if __name__ == '__main__':
    unittest.main()