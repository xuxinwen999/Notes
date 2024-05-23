## Commonly used commands
- ***docker pull***: Pulls a Docker image from a registry (e.g., Docker Hub).
- ***docker run***: Runs a Docker container from a Docker image.
- ***docker build***: Builds a Docker image from a Dockerfile.
- ***docker ps***: Lists running containers.
- ***docker images***: Lists Docker images on the host.


## From project dir to container
- create a Dockerfile in the root directory of project
- navigate to the directory containing your Dockerfile and run:
    ```cmd
    docker build -t myproject .
- once the image being built, run it to start a container:
    ```cmd
    # 允许指定多个ports，ex. docker run -d -p 8000:8000 -p 9000:9000 myproject
    # -d 是指以detached模式运行（后端运行），以便继续使用terminal
    docker run -d -p 8000:8000 myproject


## Dockerfile
A Dockerfile is simply a text file named Dockerfile ***(without any extension)*** that contains the instructions for building a Docker image.
- Build under the root path of project
- 注释前缀：#
- an example of dockerfile content: [ref](https://iphysresearch.github.io/blog/post/programing/docker-tutorial/)
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
    


***Docker-compose.yml vs. Dockerfile***: Dockerfile is used to define the instructions for building a Docker image, while Docker Compose YAML is used to define the configuration for running multiple Docker containers as a unified application.


## Docker image
Docker image files are ***not stored in a human-readable format*** like text files. Instead, they are binary files that contain all the files, libraries, dependencies, and configurations needed to run a Docker container.When you build a Docker image using a Dockerfile, Docker takes the instructions in the Dockerfile and creates layers. ***Each layer represents a step*** in the image build process, such as installing packages, copying files, or running commands. These layers are combined to form the final Docker image.