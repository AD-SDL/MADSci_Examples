"""Example Robot Node Implementation"""

from typing import Optional

from madsci.common.types.action_types import (
    ActionFailed,
    ActionResult,
    ActionSucceeded,
)
from madsci.common.types.node_types import (
    RestNodeConfig,
)
from madsci.node_module.helpers import action
from madsci.node_module.rest_node_module import RestNode

from example_robot_interface import ExampleRobotInterface


class ExampleRobotConfig(RestNodeConfig):
    """Example Configuration options for our ExampleRobotNode."""

    robot_number: int = 0
    """An identifier for the robot we are controlling."""


class ExampleRobotNode(RestNode):
    """Define an Example Robot Node, with the full implementation from the node_notebook."""

    config: ExampleRobotConfig = ExampleRobotConfig()
    """The configuration model for the node."""
    robot_interface: Optional[ExampleRobotInterface] = None
    """The robot interface for controlling the robot."""
    node_state = {
        "joint_angles": [0.0, 0.0, 0.0, 0.0],
    }
    """The state of the node, which is a dictionary containing the joint angles of the robot."""

    def startup_handler(self) -> None:
        """Handle the startup of the node."""
        self.logger.log_info(f"Connecting to robot {self.config.robot_number}...")
        self.robot_interface = ExampleRobotInterface(self.config.robot_number)
        self.logger.log_info(
            f"Connected to robot {self.robot_interface.get_robot_number()}"
        )

    def shutdown_handler(self) -> None:
        """Handle the shutdown of the node."""
        self.logger.log_info(f"Disconnecting from robot {self.config.robot_number}...")
        del self.robot_interface
        self.logger.log_info(f"Disconnected from robot {self.config.robot_number}")

    def state_handler(self) -> None:
        """This is where you can implement logic to periodically update the node's public-facing state information."""
        if self.robot_interface is not None:
            self.node_state = {"joint_angles": self.robot_interface.joint_angles}
        else:
            self.node_state = {"joint_angles": None}

    def status_handler(self) -> None:
        """
        This is where you can implement logic to periodically update the node's status information.
        """
        if self.robot_interface is not None and self.robot_interface.is_moving:
            self.node_status.busy = True
        else:
            self.node_status.busy = len(self.node_status.running_actions) > 0

    @action(
        name="move_joints", description="Move the robot to the specified joint angles"
    )
    def move_joints(self, joint_angles: list[float]) -> ActionResult:
        """
        An example action: moving the robot to a set of joint angles.
        """
        if self.robot_interface is None:
            self.logger.log_error("Robot interface not initialized")
            return ActionFailed(errors="Robot interface not initialized")
        if self.robot_interface.is_moving:
            self.logger.log_error("Robot is already moving")
            return ActionFailed(errors="Robot is already moving")
        if len(joint_angles) != 4:
            self.logger.log_error("Invalid number of joint angles. Expected 4.")
            return ActionFailed(errors="Invalid number of joint angles. Expected 4.")
        self.robot_interface.move_to_joint_angles(joint_angles)
        self.logger.log_info(f"Moved robot to joint angles: {joint_angles}")
        return ActionSucceeded()


if __name__ == "__main__":
    example_node = ExampleRobotNode()
    example_node.start_node()
