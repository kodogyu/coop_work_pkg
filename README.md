# coop_work_pkg
KHU 캡스톤디자인 Drones and Rovers for Extraterrestrial Autonomous Mapping(**DREAM**) 팀.

Drone-Rover간의 협업으로 3D Reconstruction을 수행하는 프로젝트 리포지토리입니다.

## 사용 방법

1. `<워크스페이스>/src/` 아래에 리포지토리를 clone.
    
    ```bash
    $ cd <workspace>/src
    $ git clone https://github.com/kodogyu/coop_work_pkg.git
    ```
    
2. `<워크스페이스>`에서 빌드.
    
    ```bash
    $ cd ../
    $ colcon build
    ```
    
3. 워크스페이스의 `setup.bash` 파일 실행.
    
    ```bash
    $ source <workspace>/install/setup.bash
    ```
    
4. 이제 `coop_work_pkg` 패키지를 사용할 수 있습니다.

5. 

    
## URDFs

- common_properties.urdf :
- turtlebot3_burger.urdf :
- turtlebot3_waffle.urdf :
- turtlebot3_waffle_depth.urdf : depth 카메라를 탑재한 waffle입니다.
- turtlebot3_waffle_mk0.urdf :
- turtlebot3_waffle_pi.urdf :
- turtlebot3_waffle_stereo.urdf : stereo 카메라를 탑재한 waffle입니다.

## Launch files

- bringup_launch.py : planner_only.launch 실행 시 호출됩니다.
- load_coop_robot.launch.py :
- navigation_launch.py :
- planner_only.launch.py :
- robot_state_publisher.launch.py :
- spawn_turtlebot3.launch.py :
- turtlebot3_maze.launch.py :

## Worlds

- small_city.world : 
- maze_under_construct.world :
- border.world :
- maze.world :
- maze_light.world : 

## 참고 자료

아래의 오픈소스/문서를 참고하였습니다.

- https://github.com/ROBOTIS-GIT/turtlebot3_simulations
- https://github.com/Jaeyoung-Lim/px4-offboard
- https://github.com/PX4/px4_ros_com
- https://github.com/ros-planning/navigation2/tree/humble
