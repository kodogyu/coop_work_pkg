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
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),    # launch files
        (os.path.join('share', package_name, 'models/turtlebot3_waffle'), glob('models/turtlebot3_waffle/model*')),   # model sdf, config files (turtlebot3_waffle)
        (os.path.join('share', package_name, 'models/turtlebot3_waffle/meshes'), glob('models/turtlebot3_waffle/meshes/*')),  # model mesh files
        (os.path.join('share', package_name, 'models/turtlebot3_waffle_mk0'), glob('models/turtlebot3_waffle_mk0/model*')),   # model sdf, config files (turtlebot3_waffle_mk0)
        (os.path.join('share', package_name, 'models/turtlebot3_waffle_mk0/meshes'), glob('models/turtlebot3_waffle_mk0/meshes/*')),  # model mesh files
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.urdf'))), # urdf files   
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
        ],
    },
)
