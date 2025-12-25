import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',

    {
      type: 'category',
      label: 'Module 1: ROS2 Nervous System',
      items: [
        'module-1-ros2-nervous-system/introduction-to-ros2',
        'module-1-ros2-nervous-system/robot-structure-urdf',
        'module-1-ros2-nervous-system/communication-model',
      ],
    },

    {
      type: 'category',
      label: 'Module 2: Digital Twins & Simulation',
      items: [
        'module2/chapter1',
        'module2/chapter2',
        'module2/chapter3',
      ],
    },

    {
      type: 'category',
      label: 'Module 3: AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module3/chapter1',
        'module3/chapter2',
        'module3/chapter3',
      ],
    },

    {
      type: 'category',
      label: 'Module 4: Advanced Robotics',
      items: [
        'module4/chapter1',
        'module4/chapter2',
        'module4/chapter3',
      ],
    },
  ],
};

export default sidebars;
