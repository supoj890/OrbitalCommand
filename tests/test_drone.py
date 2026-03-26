import pytest
# Assuming your Drone class is in a file named models.py
# from src.models import Drone 

# For this simulation, we'll use a simplified version of our ShieldedDrone
class Drone:
    def __init__(self, callsign: str):
        self.callsign = callsign
        self.__battery = 100

    @property
    def battery(self):
        return self.__battery

    @battery.setter
    def battery(self, value):
        if value > 100: self.__battery = 100
        elif value < 0: self.__battery = 0
        else: self.__battery = value

    def fly(self, distance: int) -> bool:
        """
        Calculates battery consumption and executes a flight sequence.

        Args:
            distance (int): The total travel distance in orbital units.

        Returns:
            bool: True if the flight was completed with battery remaining, 
                  False if the unit lost power.
        """
        drain = distance // 2
        self.battery -= drain
        return self.battery > 0
    
class Mission:
    def __init__(self, drone, target):
        self.drone = drone
        self.target = target
        self.status = "Pending"

    def run(self) -> str:
        """
        Executes the flight sequence to the target location.

        Returns:
            str: 'Success' if the drone reaches the target with battery > 0, 
                 'Failure' if the mission is aborted due to power loss.
        """
        distance = abs(self.target.x) + abs(self.target.y)
        success = self.drone.fly(distance)
        self.status = "Success" if success else "Failure"
        return self.status
    
        
# --- The Test Suite ---

def test_battery_overflow():
    """Test 1: Ensure battery caps at 100% even if overcharged."""
    drone = Drone("Test-Alpha")
    drone.battery = 150  # Attempt to overcharge
    
    # The 'assert' keyword checks if the statement is True. 
    # If False, the test fails.
    assert drone.battery == 100

def test_battery_drain():
    """Test 2: Ensure 1:2 battery drain logic is accurate."""
    drone = Drone("Test-Bravo")
    # Initial battery is 100
    drone.fly(40)
    
    # 100 - (40 // 2) = 80
    assert drone.battery == 80

def test_battery_underflow():
    """Extra Credit: Ensure battery never goes below 0%."""
    drone = Drone("Test-Charlie")
    drone.fly(300) # Should drain 150, but cap at 0
    
    assert drone.battery == 0