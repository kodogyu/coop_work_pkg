from setuptools import find_packages, setup

import os
from glob import glob

package_name = 'coop_work_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # Launch files
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*launch.py'))),    # launch files

        # Model files (sdf, config files)
        (os.path.join('share', package_name, 'models/turtlebot3_waffle'),
            glob('models/turtlebot3_waffle/model*')),  # turtlebot3_waffle model
        (os.path.join('share', package_name, 'models/turtlebot3_waffle/meshes'),
            glob('models/turtlebot3_waffle/meshes/*')),  # mesh files
        (os.path.join('share', package_name, 'models/turtlebot3_waffle_stereo'),
            glob('models/turtlebot3_waffle_stereo/model*')),  # turtlebot3_waffle_stereo model
        (os.path.join('share', package_name, 'models/turtlebot3_waffle_stereo/meshes'),
            glob('models/turtlebot3_waffle_stereo/meshes/*')),  # mesh files
        (os.path.join('share', package_name, 'models/turtlebot3_waffle_depth'),
            glob('models/turtlebot3_waffle_depth/model*')),  # turtlebot3_waffle_depth model
        (os.path.join('share', package_name, 'models/turtlebot3_waffle_depth/meshes'),
            glob('models/turtlebot3_waffle_depth/meshes/*')),  # mesh files
        (os.path.join('share', package_name, 'models/turtlebot3_waffle_mk0'),
            glob('models/turtlebot3_waffle_mk0/model*')),  # turtlebot3_waffle_mk0 model
        (os.path.join('share', package_name, 'models/turtlebot3_waffle_mk0/meshes'),
            glob('models/turtlebot3_waffle_mk0/meshes/*')),  # mesh files
        (os.path.join('share', package_name, 'models/maze'),
            glob('models/maze/model*')),  # model sdf, config files (maze1)

        # World files
        (os.path.join('share', package_name, 'worlds'),
            glob(os.path.join('worlds', '*.world'))),  # world files

        # URDF files
        (os.path.join('share', package_name, 'urdf'),
            glob(os.path.join('urdf', '*.urdf'))),  # urdf files

        # Map files
        (os.path.join('share', package_name, 'maps'),
            glob(os.path.join('maps', '*'))),  # map files

        # params files
        (os.path.join('share', package_name, 'params'),
            glob(os.path.join('params', '*.yaml'))),  # navigation parameter files

        # BehaviorTree files
        (os.path.join('share', package_name, 'behavior_tree'),
            glob(os.path.join('behavior_tree', '*.xml'))),  # behavior tree xml files
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kodogyu',
    maintainer_email='kodogyu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'offboard_control = coop_work_pkg.offboard_control:main',
            'keyboard_reader = coop_work_pkg.keyboard_reader:main',
            'drone_controller = coop_work_pkg.drone_controller:main',
            'drone_image_server = coop_work_pkg.drone_image_capture_server:main',
            'teleop_custom = coop_work_pkg.teleop_custom:main',
        ],
    },
)
