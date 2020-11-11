# docker 基本操作

## docker基本概念



### 镜像

Docker 镜像（Image），就相当于是一个 root 文件系统。比如官方镜像 ubuntu:16.04 就包含了完整的一套 Ubuntu16.04 最小系统的 root 文件系统

### 容器

镜像（Image）和容器（Container）的关系，就像是面向对象程序设计中的类和实例一样，镜像是静态的定义，容器是镜像运行时的实体。容器可以被创建、启动、停止、删除、暂停等。

### 仓库

- **仓库（Repository）**：仓库可看成一个代码控制中心，用来保存镜像。

## docker常用命令



* docker build -t {name} {dir} 构建镜像

* docker images 查看镜像列表

* docker ps 查看当前正在运行的容器 加上-a参数可以查看所有的容器

* docker run -itd -p {主机端口}:{容器端口} {image} {命令}运行一个容器,其中命令会覆盖镜像的CMD,一般镜像为 /bin/bash

* docker exec -it {容器}  /bin/bash 进入容器

  更多命令:https://www.runoob.com/docker/docker-command-manual.html

## Dockerfile

Dockerfile 是一个用来构建镜像的文本文件，文本内容包含了一条条构建镜像所需的指令和说明。

具体命令可以参考:https://www.runoob.com/docker/docker-dockerfile.html

### 构建自己的环境

Dockerfile

```
FROM centos:7.6.1810
COPY python3.8 /usr/local/python3.8
ENV PATH $PATH:/usr/local/python3.8/bin


WORKDIR /root

```

 使用命令:docker build -t {名称} . 构建环境

FROM centos:7.6.1810 :引用环境,这个引用一个centos环境

COPY python3.8 /usr/local/python3.8将python3.8这个文件夹拷贝到镜像中

ENV PATH $PATH:/usr/local/python3.8/bin 设置环境变量

WORKDIR /root  设置工作路径

### 构建docker服务

Dockerfile

```
FROM {上面镜像的名称}
COPY django_demo /app/django_demo
WORKDIR /app/django_demo
CMD ["python", "manage.py","runserver","0.0.0.0:8000"]

```

CMD ["python", "manage.py","runserver","0.0.0.0:8000"] 运行命令,在运行是会被docker run的命令 覆盖

使用命令:docker build -t {名称} . 构建环境

## 镜像仓库

* docker pull {仓库地址}/{镜像名称}:{版本}  拉取镜像
* docker tag {镜像名称}:{版本} {仓库地址}/{镜像名称}:{版本} 打上tag,根据tag 可以push镜像
* docker push{仓库地址}/{镜像名称}:{版本} 推送镜像

对容器进行操作后,可以反过来更新镜像

 ```
docker commit -m="更新内容" -a="作者" {容器} {镜像名称}:{版本}
 ```



