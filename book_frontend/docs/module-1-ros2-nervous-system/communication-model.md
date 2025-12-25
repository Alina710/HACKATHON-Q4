---
title: Communication Model in ROS 2
sidebar_position: 2
---
### **Overview**

As we discussed earlier, ROS 2 is built on a **distributed communication model** where software components (called **nodes**) communicate with each other over **Topics**, **Services**, or **Actions**. In this section, we’ll dive deeper into these communication patterns, supported by practical coding examples.

---

### **1. Nodes in ROS 2**

Each node is a process that performs a specific task. For example, one node might handle reading sensor data, while another node handles robot movement.

#### **Example: Creating a Simple Node**

Here’s a simple example of a ROS 2 Python node that prints "Hello, ROS 2!" to the console.

**hello_ros2.py**:

```python
import rclpy
from rclpy.node import Node

class HelloRos2Node(Node):
    def __init__(self):
        super().__init__('hello_ros2_node')
        self.get_logger().info('Hello, ROS 2!')

def main(args=None):
    rclpy.init(args=args)
    hello_ros2_node = HelloRos2Node()
    rclpy.spin(hello_ros2_node)
    hello_ros2_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

In this example:

* The node is named `hello_ros2_node`.
* It logs "Hello, ROS 2!" when it starts.

---

### **2. Topics (Publisher-Subscriber Model)**

ROS 2 Topics use a **Publisher-Subscriber** model to send continuous data streams between nodes. A publisher sends data on a topic, and any subscribers to that topic receive it.

#### **Example: Camera Node (Publisher)**

Let’s create a publisher that publishes an integer (representing the number of frames captured by a camera).

**camera_publisher.py**:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class CameraPublisherNode(Node):
    def __init__(self):
        super().__init__('camera_publisher_node')
        self.publisher_ = self.create_publisher(Int32, 'camera_frames', 10)
        self.timer = self.create_timer(1.0, self.publish_frame_count)  # Publish every 1 second
        self.frame_count = 0

    def publish_frame_count(self):
        msg = Int32()
        msg.data = self.frame_count
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing frame count: {self.frame_count}")
        self.frame_count += 1

def main(args=None):
    rclpy.init(args=args)
    camera_publisher_node = CameraPublisherNode()
    rclpy.spin(camera_publisher_node)
    camera_publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### **Example: Camera Subscriber Node**

Now, let’s create a subscriber that listens to the `camera_frames` topic and prints the received frame count.

**camera_subscriber.py**:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class CameraSubscriberNode(Node):
    def __init__(self):
        super().__init__('camera_subscriber_node')
        self.subscription = self.create_subscription(
            Int32,
            'camera_frames',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f"Received frame count: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    camera_subscriber_node = CameraSubscriberNode()
    rclpy.spin(camera_subscriber_node)
    camera_subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

In the publisher:

* We use the `create_publisher` method to publish `Int32` messages on the `camera_frames` topic.
* The frame count is incremented and published every second using the `create_timer`.

In the subscriber:

* We use `create_subscription` to subscribe to the `camera_frames` topic.
* When a new frame count message is received, it prints the value.

---

### **3. Services (Request-Response Model)**

Services are used for **synchronous** communication when a node needs an immediate response. In ROS 2, a service client sends a request, and a service server processes the request and responds.

#### **Example: Service Server (Reset Position)**

Let’s create a service that resets the robot's position to `(0, 0)` when requested.

**reset_position_server.py**:

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class ResetPositionServer(Node):
    def __init__(self):
        super().__init__('reset_position_server')
        self.srv = self.create_service(Trigger, 'reset_position', self.reset_position_callback)

    def reset_position_callback(self, request, response):
        self.get_logger().info('Resetting robot position to (0, 0)')
        response.success = True
        response.message = "Position reset successful"
        return response

def main(args=None):
    rclpy.init(args=args)
    reset_position_server = ResetPositionServer()
    rclpy.spin(reset_position_server)
    reset_position_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### **Example: Service Client (Request Reset)**

Now let’s create a client that requests the reset position service.

**reset_position_client.py**:

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class ResetPositionClient(Node):
    def __init__(self):
        super().__init__('reset_position_client')
        self.cli = self.create_client(Trigger, 'reset_position')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.request = Trigger.Request()

    def send_request(self):
        self.future = self.cli.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    reset_position_client = ResetPositionClient()
    response = reset_position_client.send_request()
    print(f"Response: {response.message}")
    reset_position_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

In the **server**:

* We use `create_service` to create a service of type `Trigger`.
* When the request is received, we log a message and return a successful response.

In the **client**:

* We create a client using `create_client` and call the service using `call_async`.
* The client waits for a response, and upon receiving it, prints a confirmation message.

---

### **4. Actions (Long-Running Tasks)**

Actions are used for tasks that take time to complete and need continuous feedback or can be canceled during execution. An example might be a robot navigating to a target location.

#### **Example: Action Server (Navigate to Goal)**

Here’s an action server that processes a navigation goal, provides feedback, and completes the task.

**navigate_goal_server.py**:

```python
import rclpy
from rclpy.node import Node
from action_msgs.msg import GoalStatus
from example_interfaces.action import Fibonacci

class NavigateGoalServer(Node):
    def __init__(self):
        super().__init__('navigate_goal_server')
        self._action_server = self.create_action_server(
            Fibonacci,
            'navigate_to_goal',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info(f"Executing goal: {goal_handle.goal.order}")
        feedback_msg = Fibonacci.Feedback()
        for i in range(goal_handle.goal.order):
            feedback_msg.sequence.append(i)
            goal_handle.publish_feedback(feedback_msg)
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        return result

def main(args=None):
    rclpy.init(args=args)
    navigate_goal_server = NavigateGoalServer()
    rclpy.spin(navigate_goal_server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### **Example: Action Client (Send Navigate Goal)**

Here’s an action client that sends a goal to the action server.

**navigate_goal_client.py**:

```python
import rclpy
from rclpy.node import Node
from example_interfaces.action import Fibonacci
from rclpy.action import ActionClient

class NavigateGoalClient(Node):
    def __init__(self):
        super().__init__('navigate_goal_client')
        self._action_client = ActionClient(self, Fibonacci, 'navigate_to_goal')

    def send_goal(self):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = 10
        self._action_client.wait_for_server()
        send_goal_future = self._action_client.send_goal_async(goal_msg)
        result = send_goal_future.result()
        return result

def main(args=None):
    rclpy.init(args=args)
    navigate_goal_client = NavigateGoalClient()
    result = navigate_goal_client.send_goal()
    print(f"Result: {result.sequence}")
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

### **Summary**

The **ROS 2 Communication Model** provides various ways for nodes
