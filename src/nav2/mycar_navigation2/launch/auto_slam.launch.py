from launch import LaunchDescription
from launch_ros.actions import Node

# 封装终端指令相关
# from launch.actions import ExecuteProcess
# from launch.substitutions import FindExecutable

# 参数声明与获取
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration


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
    use_sim_time=DeclareLaunchArgument("use_sim_time",default_value="true")
    start_simulator=DeclareLaunchArgument("start_simulator",default_value="true")

    simulator_node=Node(
        package="stage_ros2",
        executable="stage_ros2",
        parameters=[{
            "world_file": os.path.join(
                get_package_share_directory("demo_stage_sim"),
                "world",
                "sim.world"
            )
        }],
        remappings=[("base_scan", "scan")],
        condition=IfCondition(LaunchConfiguration("start_simulator")),
        output="screen"
    )
    
    slam_pkg=get_package_share_directory("mycar_slam_toolbox")
    
    slam_launch=IncludeLaunchDescription(
            launch_description_source=PythonLaunchDescriptionSource(
                launch_file_path=os.path.join(slam_pkg,"launch","online_sync.launch.py")
            ),
            launch_arguments=[('use_sim_time', LaunchConfiguration('use_sim_time'))]
        )
    nav2_pkg=get_package_share_directory("mycar_navigation2")
    nav2_launch=IncludeLaunchDescription(
            launch_description_source=PythonLaunchDescriptionSource(
                launch_file_path=os.path.join(nav2_pkg,"launch","nav2.launch.py")
            ),launch_arguments=[('use_sim_time', LaunchConfiguration('use_sim_time'))]
        )
    rviz_path=os.path.join(get_package_share_directory("mycar_navigation2"),"rviz","nav2.rviz")
    rviz2_node=Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d",rviz_path],
        parameters=[{"use_sim_time": LaunchConfiguration("use_sim_time")}]
    )

    navigation_stack=TimerAction(
        period=2.0,
        actions=[slam_launch, nav2_launch, rviz2_node]
    )

    return LaunchDescription([
        use_sim_time,
        start_simulator,
        simulator_node,
        navigation_stack
    ])
