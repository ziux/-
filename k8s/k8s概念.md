## 核心组件

Kubernetes 主要由以下几个核心组件组成：

- etcd 保存了整个集群的状态；
- apiserver 提供了资源操作的唯一入口，并提供认证、授权、访问控制、API 注册和发现等机制；
- controller manager 负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；
- scheduler 负责资源的调度，按照预定的调度策略将 Pod 调度到相应的机器上；
- kubelet 负责维护容器的生命周期，同时也负责 Volume（CVI）和网络（CNI）的管理；
- Container runtime 负责镜像管理以及 Pod 和容器的真正运行（CRI）；
- kube-proxy 负责为 Service 提供 cluster 内部的服务发现和负载均衡

![img](.media/architecture.png)



## 核心概念	

### Container



### pod
最小调度和资源单元
一组容器的抽象,包含一个或多个容器 

### Node

Node 是 Pod 真正运行的主机，可以是物理机，也可以是虚拟机。为了管理 Pod，每个 Node 节点上至少要运行 container runtime（比如 docker 或者 rkt）、`kubelet` 和 `kube-proxy` 服务

### Namespace

Namespace 是对一组资源和对象的抽象集合，比如可以用来将系统内部的对象划分为不同的项目组或用户组

### Volume
卷,用来管理k8s存储
用于声明pod中容器可以访问的文件目录,卷可以被挂载到pod中的一个或多个容器的指定目录下

### deployment
pod的一个抽象, 一组pod的副本数目,以及这个pod版本
pod是组成deployment的最小单元
### service
Service 提供了一个或者多个 Pod 实例的稳定访问地址

### Label

Label 是识别 Kubernetes 对象的标签，以 key/value 的方式附加到对象上, 不具有唯一性



