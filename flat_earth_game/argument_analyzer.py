"""
Module for analyzing and evaluating player arguments in the Flat Earth Debate Game.
"""

class ArgumentAnalyzer:
    """
    Analyzes player arguments and provides appropriate AI responses.
    
    This class contains the logic for evaluating player arguments based on keywords
    and maintaining a database of possible AI rebuttals.
    """
    
    def __init__(self):
        """Initialize the argument analyzer with evidence types and rebuttals."""
        self.evidence_weights = {
            "satellite": {
                "keywords": ["satellite", "space", "photo", "image", "picture", "nasa"],
                "weight": 15,
                "description": "Evidence from satellite imagery and space observation"
            },
            "gravity": {
                "keywords": ["gravity", "gravitational", "mass", "attraction", "force"],
                "weight": 20,
                "description": "Arguments based on gravitational effects and physics"
            },
            "curvature": {
                "keywords": ["curve", "horizon", "curvature", "ship", "disappear"],
                "weight": 25,
                "description": "Observations of Earth's curvature"
            },
            "time_zones": {
                "keywords": ["time zone", "sun", "day", "night", "shadow", "timezone"],
                "weight": 20,
                "description": "Evidence from time zones and day/night cycles"
            },
            "circumnavigation": {
                "keywords": ["circumnavigation", "sail", "around", "magellan", "flight"],
                "weight": 20,
                "description": "Evidence from global circumnavigation"
            }
        }
        
        self.rebuttals = {
            "satellite": [
                "Those images could be manipulated or fake.",
                "NASA could be part of a grand conspiracy.",
                "CGI technology can create very convincing images these days."
            ],
            "gravity": [
                "What you call gravity could just be density and buoyancy.",
                "If gravity pulled everything to the center, why don't the oceans fall off?",
                "Heavy things fall because they're dense, not because of gravity."
            ],
            "curvature": [
                "The horizon appears flat when you look at it.",
                "Ships don't really disappear bottom-first; that's just perspective.",
                "If Earth was curved, buildings would appear tilted."
            ],
            "time_zones": [
                "The sun is just a spotlight moving across a flat plane.",
                "Time zones could work the same way on a flat disk.",
                "The sun circles above the flat Earth like a carousel."
            ],
            "circumnavigation": [
                "You can travel in a circle on a flat surface too.",
                "The edge of the Earth is surrounded by an ice wall (Antarctica).",
                "Nobody has actually circumnavigated north to south."
            ]
        }
    
    def analyze_argument(self, text):
        """
        Analyze a player's argument and determine its category and weight.
        
        Args:
            text (str): The player's argument text
            
        Returns:
            tuple: (category, weight) where category is the type of argument
                  and weight is its persuasive value
        """
        text = text.lower()
        max_weight = 0
        best_category = None
        
        for category, data in self.evidence_weights.items():
            for keyword in data["keywords"]:
                if keyword.lower() in text:
                    if data["weight"] > max_weight:
                        max_weight = data["weight"]
                        best_category = category
        
        return best_category, max_weight

    def get_rebuttal(self, category):
        """
        Get a random rebuttal for a given argument category.
        
        Args:
            category (str): The category of argument
            
        Returns:
            str: A rebuttal appropriate for the argument category
        """
        import random
        return random.choice(self.rebuttals[category])

    def get_evidence_description(self, category):
        """
        Get the description of an evidence category.
        
        Args:
            category (str): The category of evidence
            
        Returns:
            str: Description of the evidence category
        """
        return self.evidence_weights[category]["description"]