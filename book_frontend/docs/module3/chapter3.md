---
title: Path Planning with Nav2
sidebar_label: Chapter 3 - Nav2 Path Planning
description: Using Nav2 for autonomous path planning and navigation in humanoid robots
---

# Path Planning with Nav2

## Introduction to Navigation in ROS2 (Nav2)

Navigation in ROS2 (Nav2) is the official navigation stack for ROS2, designed to provide path planning, obstacle avoidance, and autonomous navigation capabilities for mobile robots. For humanoid robots, Nav2 provides the essential infrastructure to move safely and efficiently through environments based on the localization information from VSLAM systems.

### Key Components of Nav2
- **Navigation System**: Core system managing navigation lifecycle
- **Global Planner**: Computes optimal paths from start to goal
- **Local Planner**: Handles obstacle avoidance and real-time adjustments
- **Controller**: Translates plans into robot commands
- **Recovery Behaviors**: Handles navigation failures and obstacles

### Nav2 Architecture
Nav2 uses a behavior tree architecture that allows for flexible and robust navigation:
- **Action Servers**: Provide navigation services to clients
- **Lifecycle Nodes**: Manage initialization, activation, and cleanup
- **Plugins**: Enable customization of planners, controllers, and behaviors
- **Costmaps**: Represent obstacles and drivable areas

## Nav2 Configuration for Humanoid Robots

### Humanoid-Specific Considerations

Humanoid robots have unique characteristics that require special configuration in Nav2:

#### Kinematic Differences
- Unlike wheeled robots, humanoid robots have complex kinematics
- Foot placement and balance considerations affect navigation
- Different turning and movement capabilities
- Height and body dimensions affect obstacle detection

#### Sensor Configuration
- Stereo cameras and depth sensors for 3D perception
- IMU integration for balance and motion compensation
- LIDAR (if available) for 360-degree obstacle detection
- Force/torque sensors for ground contact feedback

### Basic Nav2 Configuration

#### Main Configuration File
```yaml
# nav2_params.yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: False
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: True
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: "map"
    robot_base_frame: "base_link"
    odom_topic: "/odom"
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    # Note: Comment out the default tree if providing your own
    # default_bt_xml_filename: "navigate_w_replanning_and_recovery.xml"
    plugin_lib_names:
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_compute_path_through_poses_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_assisted_teleop_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_drive_on_heading_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_globally_consistent_localization_condition_bt_node
    - nav2_is_path_valid_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_on_amcl_reset_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_truncate_path_local_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_time_expired_condition_bt_node
    - nav2_path_expiring_timer_condition
    - nav2_distance_traveled_condition_bt_node
    - nav2_single_trigger_bt_node
    - nav2_is_battery_low_condition_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node
    - nav2_controller_cancel_bt_node
    - nav2_path_longer_on_approach_bt_node
    - nav2_wait_cancel_bt_node
    - nav2_spin_cancel_bt_node
    - nav2_back_up_cancel_bt_node
    - nav2_assisted_teleop_cancel_bt_node
    - nav2_drive_on_heading_cancel_bt_node

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # Progress checker parameters
    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0

    # Goal checker parameters
    goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
      stateful: True

    # Controller parameters
    FollowPath:
      plugin: "nav2_rotation_shim_controller::RotationShimController"
      progress_checker_plugin: "progress_checker"
      goal_checker_plugin: "goal_checker"
      primary_controller: "FollowPath"
      rotation_shim:
        plugin: "nav2_controller::SimpleProgressChecker"
        min_rotational_vel: 0.4
        max_rotational_vel: 1.0
        goal_tolerance: 0.1
        rotation_speed_slowdown_ratio: 0.33
        simulate_ahead_time: 1.0

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: "odom"
      robot_base_frame: "base_link"
      use_sim_time: True
      rolling_window: True
      width: 10
      height: 10
      resolution: 0.05
      robot_radius: 0.3
      plugins: ["voxel_layer", "inflation_layer"]
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: True
        publish_voxel_map: True
        origin_z: 0.0
        z_resolution: 0.2
        z_voxels: 10
        max_obstacle_height: 2.0
        mark_threshold: 0
        observation_sources: "scan"
        scan:
          topic: "/scan"
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 10.0
          raytrace_min_range: 0.0
          obstacle_max_range: 5.0
          obstacle_min_range: 0.0
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      always_send_full_costmap: True

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 0.5
      global_frame: "map"
      robot_base_frame: "base_link"
      use_sim_time: True
      robot_radius: 0.3
      resolution: 0.05
      track_unknown_space: True
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      obstacle_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: True
        publish_voxel_map: True
        origin_z: 0.0
        z_resolution: 0.2
        z_voxels: 10
        max_obstacle_height: 2.0
        mark_threshold: 0
        observation_sources: "scan"
        scan:
          topic: "/scan"
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 10.0
          raytrace_min_range: 0.0
          obstacle_max_range: 5.0
          obstacle_min_range: 0.0
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    use_sim_time: True
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner::NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

smoother_server:
  ros__parameters:
    use_sim_time: True
    smoother_plugins: ["simple_smoother"]
    simple_smoother:
      plugin: "nav2_smoother::SimpleSmoother"
      tolerance: 1.0e-10
      max_its: 1000
      do_refinement: True

behavior_server:
  ros__parameters:
    costmap_topic: "local_costmap/costmap_raw"
    footprint_topic: "local_costmap/published_footprint"
    cycle_frequency: 10.0
    behavior_plugins: ["spin", "backup", "wait"]
    spin:
      plugin: "nav2_behaviors::Spin"
      spin_dist: 1.57
    backup:
      plugin: "nav2_behaviors::BackUp"
      backup_dist: 0.15
      backup_speed: 0.025
    wait:
      plugin: "nav2_behaviors::Wait"
      wait_duration: 1.0

waypoint_follower:
  ros__parameters:
    loop_rate: 20
    stop_on_failure: false
    waypoint_task_executor_plugin: "wait_at_waypoint"
    wait_at_waypoint:
      plugin: "nav2_waypoint_follower::WaitAtWaypoint"
      enabled: true
      waypoint_pause_duration: 200
```

## Path Planning Algorithms

### Global Path Planning

Global planners compute the optimal path from the robot's current location to the goal:

#### Navfn Planner
- Dijkstra's algorithm for path planning
- Grid-based approach
- Guarantees optimal path in static environments
- Good for humanoid robots in known environments

#### A* Planner
- Heuristic search algorithm
- Faster than Dijkstra in many cases
- Balances optimality with computation time
- Good for complex humanoid navigation

#### Theta* Planner
- Any-angle path planning
- Produces more natural paths
- Better for humanoid robots with complex kinematics

### Local Path Planning

Local planners handle real-time obstacle avoidance:

#### DWA (Dynamic Window Approach)
- Considers robot dynamics
- Handles velocity constraints
- Good for humanoid robots with complex movement
- Real-time obstacle avoidance

#### TEB (Timed Elastic Band)
- Trajectory optimization approach
- Considers kinematic constraints
- Smooth trajectory generation
- Well-suited for humanoid robots

## Integration with VSLAM Localization

### Connecting Nav2 with VSLAM

To integrate Nav2 with the VSLAM system from Chapter 2:

#### TF Frame Configuration
```yaml
# TF frames for humanoid robot
- map (global reference)
- odom (odometry frame)
- base_footprint (robot base)
- camera (for VSLAM)
- imu (for additional sensing)
```

#### Message Flow
1. VSLAM provides pose estimates to `/amcl` or similar localization node
2. Nav2 uses this pose information for navigation
3. Costmaps are updated with sensor data
4. Path planning occurs using global and local planners
5. Velocity commands are sent to robot controllers

### Example Integration Node
```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf2_ros import TransformListener, Buffer
import tf2_geometry_msgs
import tf_transformations

class Nav2VSLAMIntegrator(Node):
    def __init__(self):
        super().__init__('nav2_vslam_integrator')

        # Subscribe to VSLAM pose
        self.vslam_pose_sub = self.create_subscription(
            PoseStamped,
            '/visual_pose',
            self.vslam_pose_callback,
            10
        )

        # Subscribe to odometry
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Publisher for AMCL pose (to Nav2)
        self.amcl_pose_pub = self.create_publisher(
            PoseStamped,
            '/initialpose',
            10
        )

        # TF buffer and listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.vslam_pose = None
        self.odom_pose = None

        # Timer to publish VSLAM pose to Nav2
        self.timer = self.create_timer(0.1, self.publish_to_nav2)

        self.get_logger().info('Nav2-VSLAM Integrator initialized')

    def vslam_pose_callback(self, msg):
        """Receive pose from VSLAM system"""
        self.vslam_pose = msg
        self.get_logger().debug(f'Received VSLAM pose: {msg.pose.position}')

    def odom_callback(self, msg):
        """Receive odometry data"""
        self.odom_pose = msg
        self.get_logger().debug(f'Received odometry pose')

    def publish_to_nav2(self):
        """Publish VSLAM pose to Nav2 system"""
        if self.vslam_pose is not None:
            # Transform VSLAM pose to map frame if needed
            try:
                # Wait for transform
                transform = self.tf_buffer.lookup_transform(
                    'map', 'camera',
                    rclpy.time.Time(),
                    timeout=rclpy.duration.Duration(seconds=1.0)
                )

                # Transform the pose
                transformed_pose = tf2_geometry_msgs.do_transform_pose(
                    self.vslam_pose, transform
                )

                # Publish to Nav2
                self.amcl_pose_pub.publish(transformed_pose)

            except Exception as e:
                self.get_logger().warn(f'Transform error: {e}')
                # If transform fails, publish original pose
                self.amcl_pose_pub.publish(self.vslam_pose)

def main(args=None):
    rclpy.init(args=args)
    integrator = Nav2VSLAMIntegrator()

    try:
        rclpy.spin(integrator)
    except KeyboardInterrupt:
        pass
    finally:
        integrator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Humanoid Robot Navigation Specifics

### Footstep Planning Considerations

For true humanoid navigation, additional considerations are needed:

#### High-Level Path Planning
- Plan paths that account for foot placement
- Consider balance and stability during navigation
- Account for step height and reach limitations

#### Integration Approaches
1. **Standard Nav2**: For basic humanoid navigation (simplified)
2. **Footstep Planner**: For advanced humanoid navigation
3. **Hybrid Approach**: Combine both approaches

### Behavior Trees for Humanoid Navigation

Nav2 uses behavior trees for flexible navigation:

#### Custom Behavior Tree Example
```xml
<!-- navigate_w_humanoid_recovery.xml -->
<root main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <PipelineSequence name="navigate_with_recovery">
      <RecoveryNode name="global_plan_with_recovery" number_of_retries="2">
        <PipelineSequence name="global_plan">
          <ComputePathToPose goal="{goal}" path="{path}" planner_id="GridBased"/>
          <SmoothPath input_path="{path}" output_path="{smoothed_path}" smoother_id="simple_smoother"/>
        </PipelineSequence>
        <RecoveryNode name="global_plan_recovery" number_of_retries="1">
          <ClearEntireCostmap name="clear_global_costmap" service_name="global_costmap/clear_entirely_global_costmap"/>
        </RecoveryNode>
      </RecoveryNode>

      <RecoveryNode name="local_plan_with_recovery" number_of_retries="4">
        <PipelineSequence name="local_plan">
          <FollowPath path="{smoothed_path}" controller_id="FollowPath"/>
        </PipelineSequence>
        <RecoveryNode name="local_plan_recovery" number_of_retries="2">
          <Sequence name="local_recovery">
            <ClearEntireCostmap name="clear_local_costmap" service_name="local_costmap/clear_entirely_local_costmap"/>
            <Spin spin_dist="1.57" name="backup"/>
          </Sequence>
        </RecoveryNode>
      </RecoveryNode>
    </PipelineSequence>
  </BehaviorTree>
</root>
```

## Launching and Operating Nav2

### Launch File Example
```xml
<!-- humanoid_nav2.launch.py -->
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    bt_xml_file = LaunchConfiguration('bt_xml_file')
    map_topic = LaunchConfiguration('map_topic')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')

    lifecycle_nodes = ['controller_server',
                       'planner_server',
                       'recoveries_server',
                       'bt_navigator',
                       'waypoint_follower']

    return LaunchDescription([
        # Launch Arguments
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='False',
            description='Use simulation time'),

        DeclareLaunchArgument(
            'autostart',
            default_value='True',
            description='Automatically start the Nav2 lifecycle nodes'),

        DeclareLaunchArgument(
            'params_file',
            default_value=[ThisPackagePrefix(), '/config/nav2_params.yaml'],
            description='Full path to the ROS2 parameters file to use for all launched nodes'),

        DeclareLaunchArgument(
            'default_bt_xml_filename',
            default_value=[ThisPackagePrefix(), '/behavior_trees/navigate_w_humanoid_recovery.xml'],
            description='Full path to the behavior tree xml file to use'),

        # Set environment variables
        SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_OUTPUT', '1'),

        # Lifecycle Manager
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time},
                        {'autostart': autostart},
                        {'node_names': lifecycle_nodes}]),

        # Controller Server
        Node(
            package='nav2_controller',
            executable='controller_server',
            output='screen',
            parameters=[parameters_file, {'use_sim_time': use_sim_time}]),

        # Planner Server
        Node(
            package='nav2_planner',
            executable='planner_server',
            output='screen',
            parameters=[parameters_file, {'use_sim_time': use_sim_time}]),

        # Behavior Tree Navigator
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            output='screen',
            parameters=[parameters_file, {'use_sim_time': use_sim_time}]),

        # Recovery Server
        Node(
            package='nav2_recoveries',
            executable='recoveries_server',
            output='screen',
            parameters=[parameters_file, {'use_sim_time': use_sim_time}]),

        # Waypoint Follower
        Node(
            package='nav2_waypoint_follower',
            executable='waypoint_follower',
            output='screen',
            parameters=[parameters_file, {'use_sim_time': use_sim_time}])
    ])
```

## Performance Optimization

### Computational Efficiency
- Optimize costmap resolution for humanoid robots
- Use appropriate planning frequencies
- Implement efficient sensor data processing
- Consider multi-threading for parallel processing

### Memory Management
- Efficient data structures for map representation
- Proper cleanup of old map data
- Optimize TF tree for humanoid-specific frames
- Monitor memory usage during navigation

### Real-time Performance
- Ensure consistent timing for navigation updates
- Implement proper error handling
- Optimize for humanoid-specific movement patterns
- Consider the computational constraints of humanoid platforms

## Troubleshooting Nav2 Issues

### Common Problems and Solutions

#### Localization Issues
- **Pose jumps**: Verify sensor synchronization and calibration
- **Drift**: Check VSLAM integration and IMU data quality
- **Initialization failures**: Ensure proper initial pose estimation

#### Path Planning Problems
- **No path found**: Check costmap configuration and inflation parameters
- **Suboptimal paths**: Adjust planner parameters and heuristics
- **Planning failures**: Verify map quality and robot footprint

#### Navigation Failures
- **Oscillation**: Tune controller parameters and velocity limits
- **Collision**: Adjust costmap inflation and obstacle detection
- **Stuck behavior**: Improve recovery behaviors and obstacle handling

### Debugging Tools
- RViz2 visualization for path and costmap display
- Nav2 logs and diagnostics
- TF tree visualization
- Behavior tree monitoring with Groot

## Academic Research and References

### Key Nav2 Publications
- The Navigation2 System (ROS2 Navigation Team)
- Behavior Trees in Robotics and AI (Colledanchise & Ögren)
- Path Planning for Humanoid Robots (Various authors)

### Integration Research
- VSLAM-Nav2 Integration Studies
- Humanoid Robot Navigation Research
- GPU-Accelerated Navigation Systems

## Summary

Nav2 provides a comprehensive navigation system for humanoid robots when properly configured for their unique characteristics. By integrating with VSLAM localization from Chapter 2, humanoid robots can achieve autonomous navigation capabilities. The key to success lies in proper configuration of costmaps, planners, and controllers to match the specific requirements of humanoid robot platforms.

The combination of Isaac Sim for simulation, Isaac ROS for perception, VSLAM for localization, and Nav2 for navigation creates a complete AI-powered robot control system as outlined in the overall module objectives.