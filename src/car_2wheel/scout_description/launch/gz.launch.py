import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    use_sim_time=DeclareLaunchArgument("use_sim_time",default_value="true")
    # this_pkg = get_package_share_directory("demo_gazebo_sim")
    mycar_desc_pkg = get_package_share_directory("scout_description")
    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")
    world_file = DeclareLaunchArgument("world",default_value=os.path.join(
     mycar_desc_pkg,
            "world",
            "demo.sdf",
        ),
        description="World SDF file to load",
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")),
        launch_arguments={
            "gz_args": ["-r ", LaunchConfiguration("world")]
        }.items(),
    )
    
    mycar_desc = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(launch_file_path=
            os.path.join(mycar_desc_pkg,"launch","car2.launch.py")
        )
    )
    spawn = Node(package="ros_gz_sim", executable="create",
                arguments=[
                "-name", "mycar",
                "-x", "0",
                "-z", "0.01", #设置为0,可能会陷进地里
                "-y", "0",
                "-topic", "/robot_description"],
            output="screen")
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                   "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                   "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
                   "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                   "/depth_camera@sensor_msgs/msg/Image[gz.msgs.Image",
                   "/depth_camera/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked",
                   "/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",
                   "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                   "/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked",
                   "/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model",
                   "/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",
                   
     ])
   
    return LaunchDescription([
        use_sim_time,
        world_file,
        # AppendEnvironmentVariable(
        #     name="GZ_SIM_RESOURCE_PATH",
        #     value=os.path.dirname(mycar_desc_pkg),
        # ),
        gz_sim,
        mycar_desc,
        spawn,
        bridge,

        ])