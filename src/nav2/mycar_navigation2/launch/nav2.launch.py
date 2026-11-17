from launch import LaunchDescription
from launch_ros.actions import Node

# 封装终端指令相关
# from launch.actions import ExecuteProcess
# from launch.substitutions import FindExecutable

# 参数声明与获取
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

# 文件包含相关
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource

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
    current_pkg = get_package_share_directory('mycar_navigation2')
    bt_yaml = os.path.join(current_pkg, 'params', 'bt.yaml')
    planner_yaml = os.path.join(current_pkg, 'params', 'planner.yaml')
    controller_yaml = os.path.join(current_pkg, 'params', 'controller.yaml')
    behaviour_yaml = os.path.join(current_pkg, 'params', 'behaviour.yaml')
    waypoint_yaml=os.path.join(current_pkg, 'params', 'waypoint.yaml')
    smoother_yaml=os.path.join(current_pkg, 'params', 'smoother.yaml')
    velocity_yaml=os.path.join(current_pkg, 'params', 'velocity.yaml')
   #恢复行为节点
    planner_node = Node(
           package='nav2_planner',
           executable='planner_server',
           name='planner_server',
           parameters=[
               {'use_sim_time': LaunchConfiguration('use_sim_time')},
               planner_yaml
           ]
       )     
    smoother_node = Node(
                package='nav2_smoother',
                executable='smoother_server',
                name='smoother_server',
                parameters=[
                    {'use_sim_time': LaunchConfiguration('use_sim_time')},
                    smoother_yaml
                ]
            ) 
    velocity_node = Node(
         package='nav2_velocity_smoother',
         executable='velocity_smoother',
         name='velocity_smoother',
         parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                 velocity_yaml
                    ],
            remappings=[("cmd_vel","cmd_vel_nav"),
                        ("cmd_vel_smoothed","cmd_vel")]
                ) 
    controller_node = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            controller_yaml
        ],
        remappings=[("cmd_vel","cmd_vel_nav")]
    )   
    behaviour_node = Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                behaviour_yaml
            ]
        ) 
    waypoint_node=Node(
        package="nav2_waypoint_follower",
        executable="waypoint_follower",
        name="waypoint_follower",
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')},
                    waypoint_yaml]
        )
    bt_server = Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                {'default_nav_to_pose_bt_xml':os.path.join(current_pkg,'bts','nav2_pose.xml')},
                {'default_nav_through_poses_bt_xml':os.path.join(current_pkg,'bts','nav2_poses.xml')},
                bt_yaml
                ]
        ) 
    life_manage=Node(package="nav2_lifecycle_manager",
                                 executable="lifecycle_manager",
                                 name="lifecycle_manager_navigation",
                                 parameters=[{"use_sim_time": LaunchConfiguration('use_sim_time')},
                                             {"autostart": True},
                                             {"node_names": [
                                                 "controller_server",
                                                "planner_server",
                                                "smoother_server",
                                                "velocity_smoother",
                                               
                                               "behavior_server",
                                               "waypoint_follower",
                                               "bt_navigator"]}
                                            ]
                                        )

    rviz_path=os.path.join(get_package_share_directory("mycar_navigation2"),"rviz","nav2.rviz")
    rviz2_node=Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d",rviz_path],
            parameters=[{"use_sim_time": LaunchConfiguration("use_sim_time")}])
    return LaunchDescription([use_sim_time,controller_node,smoother_node,velocity_node,planner_node,behaviour_node,waypoint_node,bt_server,life_manage,rviz2_node])

