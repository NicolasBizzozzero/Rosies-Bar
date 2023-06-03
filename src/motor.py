from logger import logger

class MotorInterface:
    def __init__(self):
        pass

    def rotation(self, quadrant: int):
        """ Rotate the motor until a given number of quadrants."""
        logger.info(f"Motor rotation of {quadrant} quadrants")
