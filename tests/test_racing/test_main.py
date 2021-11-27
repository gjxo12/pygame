import pytest
from src.racing_game.main import *
import os

def test_Car_info():
    player_car = PlayerCar(4,4)
    assert player_car.x == 180
    assert player_car.y == 200


