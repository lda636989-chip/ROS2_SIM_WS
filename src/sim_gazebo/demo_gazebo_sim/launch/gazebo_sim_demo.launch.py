from launch import LaunchDescription
from launch_ros.actions import Node

# 封装终端指令相关
from launch.actions import ExecuteProcess
# from launch.substitutions import FindExecutable

# 参数声明与获取
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration

# 文件包含相关
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

# 分组相关
# from launch_ros.actions import PushRosNamespace
# from launch.actions import GroupAction

# 事件相关
# from launch.event_handlers import OnProcessStart, OnProcessExit
# from launch.actions import RegisterEventHandler, LogInfo

# 获取功能包下share目录路径
from ament_index_python.packages import get_package_share_directory

import os
def generate_launch_description():
   
    ros_gz_sim_path=get_package_share_directory("ros_gz_sim")
    this_pkg_path=get_package_share_directory("demo_gazebo_sim")
    world_path = os.path.join(this_pkg_path, "world", "visualize_lidar.sdf")
    # sim_cmd= ExecuteProcess(
    #     cmd=["gz", "sim", world_path, "-v", "4", "-r"],
    #     output="both",
    #     shell=True
    # )

    rviz2_node=Node(package="rviz2", 
                    executable="rviz2",
                    arguments=["-d",os.path.join(this_pkg_path,"rviz","sim.rviz")])
    bridge=Node(package="ros_gz_bridge",
                        executable="parameter_bridge",
                        arguments=[
                        "/model/vehicle_blue/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                        "/model/vehicle_blue/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                        "/model/vehicle_blue/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
                        ],
                        remappings=[("/model/vehicle_blue/tf","/tf"),
                                    ("/model/vehicle_blue/cmd_vel","/cmd_vel")
                                    ])
    
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_path, "launch", "gz_sim.launch.py")),
        launch_arguments={
            "gz_args": "-r " + world_path
        }.items(),
    )

    return LaunchDescription([rviz2_node, gz_sim,bridge])

