'''
@author: Youwei Zheng
@target: Data Models
@update: 2024.07.26
'''

from pydantic import BaseModel

class Level(BaseModel):
    starting_level: float = 565.16
    target_level: float = 540.00

    def update(self) -> None:
        """Update the model with new values.
        
        Args:
            starting_level (str): The new starting level as a string.
            target_level (str): The new target level as a string.
        
        Raises:
            ValueError: If the input values cannot be converted to float.
        """

        try:
            self.starting_level = float(self.starting_level)
            self.target_level = float(self.target_level)
        except ValueError:
            raise ValueError("Invalid input values")

class Point(BaseModel):
    points_net: float = 0.0
    points_pct: float = 0.0
    
    def update(self) -> None:
        """Update the model with new values or formats.
        
        Args: 
            self
        
        Raises:
            ValueError: If the input values cannot be rounded.
        """

        # convert to float first?
        try:
            self.points_net = round(self.points_net, 2)
            self.points_pct = round(self.points_pct, 2)
        except ValueError:
            raise ValueError("Invalid input values")    
