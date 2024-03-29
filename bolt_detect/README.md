[TOC]

# 螺栓松动检测

[项目背景](#项目背景)

[文件备注](#文件备注)

[执行效果](#执行效果)

[硬件准备](#硬件准备)

[技术总结](#技术总结)

[更新日志](#更新日志)

## 项目背景

基本情况：风力发电机的塔筒部位和叶根部位有一圈螺栓，螺栓上有划线。

环境条件：叶根处直径3m，螺栓平面上下平面皆有挡板，螺栓平面和相机近乎平视，。塔筒处直径4m，相机安装可以平视也可以俯视。

## 文件备注

- Bolt_detect_jetson (检测程序文件夹)

  - build （编译文件夹）
  - include （.hpp文件）
  - src （.cpp文件）
  - CMakeLists.txt （cmake文件）
  - PyDescribe （python代码）

- Grab.xcodeproj （Xcode文件）

  更新代码后执行 `cd /root/nvidia/Bolt_detect_jetsonn/build` ，然后执行 `make` 重新编译，最后`./main`执行程序

## 执行效果

距离1.2m，500w像素相机，测试精度0.175度。精度根据摄像头像素和安装距离调整

## 硬件准备

- jetson (nx, nano)
- Basler 500wc /  USB 免驱摄像头

## 技术总结

- 阈值分割后波动很大，孤岛很多
  - 采集x相对位置，去噪求均值，减轻浮动概率影响，消除y轴波动影响
  - 先膨胀将划线内部孤岛连接，再腐蚀去除外部孤岛

- 外部伺服电机控制
  - 进程间通信


## 更新日志

2021-11-29

> - [x] 识别算法
> - [ ] 伺服电机控制



















