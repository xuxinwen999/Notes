# Docker


## Commonly used commands
* ***docker pull***: Pulls a Docker image from a registry (e.g., Docker Hub).
* ***docker run***: Runs a Docker container from a Docker image.
* ***docker build***: Builds a Docker image from a Dockerfile.
* ***docker ps***: Lists running containers.
* ***docker images***: Lists Docker images on the host.
* ***docker image inspect [image_name]***: check the info of image.
* ***docker exec***: Execute a command in a running container, (ctrl+p然后ctrl+q退出)，ex. 
    ```docker command
    # -i以interactive方式
    # 进入mycontainer，打开bash
    # 可以使用vim之类的工具编辑scripts，注意这类变动是临时的，container重启动后不会保留这类改动
    docker exec -it mycontainer /bin/bash
* ***docker cp***: Copy Files from the Container to local
    ``` docker command
    docker cp <container_id>:/path/to/file /local/path/to/save
* ***docker rm***: stop container并没有移除它，The container still exists and retains its name, which prevents the creation of a new container with the same name.
    ```docker command
    # Force removes a running or stopped container
    docker rm -f <container_name>


## From project dir to container
* create a Dockerfile in the root directory of project
* navigate to the directory containing your Dockerfile and run:
    ```cmd
    docker build -t myproject .
* once the image being built, run it to start a container:
    ```cmd
    # 允许指定多个ports，ex. docker run -d -p 8000:8000 -p 9000:9000 myproject
    # -d 是指以detached模式运行（后端运行），以便继续使用terminal
    docker run -d -p 8000:8000 myproject
* container使用host GPU
    <br>默认情况下，container runtime无法获取gpu, docker19以后可以通过在docker run时指定***--gpus all***参数向container添加主机gpu, cuda版本由image指定，但是要[保证主机的nvidia driver版本支持cuda版本](https://stackoverflow.com/questions/63960319/does-it-matter-if-the-version-of-cuda-on-docker-is-different-from-the-version-of)


## 调试
* debug无法启动的镜像：
    ```cmd
    # 进入镜像内部
    docker run -it --entrypoint /bin/bash <image_name>
    
    # 检查镜像
    docker inspect <image_name>

    # 查看日志
    docker logs <container_id>
* 挂载路径修改：container内部和local的挂载（bind），the modification on both path will sync on each side.


## Volume Mount
container内部代码挂载host后，runtime时修改host可以立即映射到container内部（而非image上），并且"docker stop" -> "docker start" 方式restart后仍然保存了修改，也就是run最新修改的版本。但是container如果被"docker rm"，所有container build后的修改也随之丢失，"docker run"是基于image构建时的代码创建container。


## docker network
[官网介绍](https://docs.docker.com/engine/tutorials/networkingcontainers/)<br>
**Key Points**:
* 同一网络下的pods相互访问ip：**http://pod_name:port**，其中port应该是pod中的端口，而不是映射到主机上的端口


## Dockerfile
A Dockerfile is simply a text file named Dockerfile ***(without any extension)*** that contains the instructions for building a Docker image.
* Build under the root path of project
* 注释前缀：#
* an example of dockerfile content: [ref](https://iphysresearch.github.io/blog/post/programing/docker-tutorial/)
    ```dockerfile
    # 该 image 文件继承我自己的 gwave image，冒号表示标签，这里标签是2.0.0，即2.0.0版本的 gwave。
    FROM iphysreserch/gwave:2.0.0

    # 将当前目录下的所有文件(除了.dockerignore排除的路径),都拷贝进入 image 文件里微系统的/waveform目录
    COPY . /waveform

    # 指定接下来的工作路径为/waveform (也就是微系统的 pwd)
    WORKDIR /waveform

    # 定义一个微系统里的环境变量
    ENV VERSION=2.0.0	# optional

    # 将容器 3000 端口暴露出来， 允许外部连接这个端口
    EXPOSE 3000			# optional

    # 在/waveform目录下，运行以下命令更新系统程序包。注意，安装后所有的依赖都将打包进入 image 文件
    RUN apt-get update && apt-get upgrade	# optional

    # 将我这个 image 做成一个 app 可执行程序，容器启动后自动执行下面指令
    # ref link里面对启动命令entrypoint/run还有更多解释
    ENTRYPOINT ["bash", "setup.sh"]


## Docker Compose
A Docker Compose YAML file defines services (containers), networks, volumes, and other configurations using a declarative syntax. Each service is configured with details like the Docker image to use, ports to expose, environment variables, volumes to mount, and dependencies.
    ```yaml
    version: '3.8'
    services:
        web:
            image: nginx:latest
            ports:
            - "80:80"
        db:
            image: mysql:latest
            environment:
            MYSQL_ROOT_PASSWORD: example
    

## Docker image
Docker image files are ***not stored in a human-readable format*** like text files. Instead, they are binary files that contain all the files, libraries, dependencies, and configurations needed to run a Docker container.When you build a Docker image using a Dockerfile, Docker takes the instructions in the Dockerfile and creates layers. ***Each layer represents a step*** in the image build process, such as installing packages, copying files, or running commands. These layers are combined to form the final Docker image.
* 镜像导入导出：[tutorial](https://www.hangge.com/blog/cache/detail_2411.html), 保留原始tag的导出命令：
```
docker save -o myimage_latest.tar myimage:latest
