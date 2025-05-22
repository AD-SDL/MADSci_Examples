"""Interface for interacting with our (fake) example robot"""

import time


class ExampleRobotInterface:
    """Example Robot Interface. This is a simple interface for controlling a (fake) robot arm."""

    robot_number: int = 0
    """An identifier for the robot we are controlling."""
    joint_angles: list[float] = [0.0, 0.0, 0.0, 0.0]
    """The joint angles of the robot."""
    gripper_closed: bool = False
    """The state of the gripper, open or closed."""
    is_moving: bool = False
    """Whether the robot is currently moving."""

    def __init__(self, robot_number: int = 0):
        """Initialize the robot interface with a robot number."""
        self.robot_number = robot_number

    def get_robot_number(self) -> int:
        """Get the robot number."""
        return self.robot_number

    def move_to_joint_angles(self, angles: list[float]) -> None:
        """Move the robot to the specified joint angles."""
        if self.is_moving:
            raise RuntimeError("Robot is already moving.")
        if len(angles) != 4:
            raise ValueError("Expected 4 joint angles.")
        self.is_moving = True
        time.sleep(5)
        self.is_moving = False
        self.joint_angles = angles

    def close_gripper(self) -> None:
        """Close the gripper."""
        if self.is_moving:
            raise RuntimeError("Robot is already moving.")
        self.is_moving = True
        time.sleep(1)
        self.is_moving = False
        self.gripper_closed = True

    def open_gripper(self) -> None:
        """Open the gripper."""
        if self.is_moving:
            raise RuntimeError("Robot is already moving.")
        self.is_moving = True
        time.sleep(1)
        self.is_moving = False
        self.gripper_closed = False
