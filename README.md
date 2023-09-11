# coop_work_pkg
KHU 캡스톤디자인 Drones and Rovers for Extraterrestrial Autonomous Mapping(**DREAM**) 팀.

Drone-Rover간의 협업으로 SLAM을 수행하는 프로젝트 리포지토리입니다.

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
    
    ```bash
    $ ros2 run coop_work_pkg keyboard_reader
    $ ros2 run coop_work_pkg drone_controller
    ```
    

## Nodes

- drone_controller
- keyboard_reader
- offboard_control

## Lanch files

- load_coop_robot.launch.py

## 참고 자료

아래의 오픈소스/문서를 참고하였습니다.

- https://github.com/ROBOTIS-GIT/turtlebot3_simulations
- https://github.com/Jaeyoung-Lim/px4-offboard
- https://github.com/PX4/px4_ros_com
