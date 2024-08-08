# Git


## Commonly used commands
* origin: 如果本地project同时映射了多个远程repo, 默认指代本地project最初映射到的remote repo
* local & remote connection:
    - disconnection直接删除.git目录：rm -rf .git
    - connection: 
        1) git init
        2) git remote add origin <remote url>
* git remote -v: 查看当前local project连接的远程repo地址，分别返回fetch和push的地址；
* git remote set-url origin <url>: 设置remote origin地址(可以切换http/ssh连接方式)
* git remote remove <repo_name>: 移除本地和remote <repo_name>的connection
* git push [-u] origin [main:]master：
    - -u:
    - [main:]: local branch main推到remote branch master, local和remote分支名一样的话不用加
* git log: 显示所有分支操作logs
* git三种同步状态:
    - committed: 数据已经安全的保存在本地数据库中
    - modified: 修改了文件，但是还没保存到数据库中，发生在工作区
    - staged: (git add) 对修改的文件的当前版本做了标记，让他包含在下次提交的快照当中。发生在暂存区
* git reset <pre-code>: reset the state of your repository to a previous commit (pre-code), 有三种reset模式:
    - --soft: HEAD回退到pre-code, 已发生的修改暂存到staging area (即执行add命令之后，未执行commit之前)和工作区(即当前IDE页面中code不变)，只是commit时以pre-code为base；
    - --mixed: 默认模式，staging area变化，相当于git add到pre-code提交时的状态，而工作区的code不变
    - --hard: 丢失所有修改，完全恢复到pre-code状态

## 分支管理
* git branch: 查看本地所有分支
* git remote show origin: 查看远程所有分支的同步信息
* git branch -vv: 查看对应的远程分支
* git branch: 查看对应的本地分支
* git checkout <branch>: 切换到branch
* git merge <branch name>: 将指定branch合并到当前所在分支：
    ```git
    # 合并远程master到当前分支
    git merge origin/master
    # 合并本地master到当前分支
    git merge master
* git diff <branch1> <branch2>: 比较两个分支


## .gitignore
.gitignore文件不在.git/目录下，需要手动添加/删除。【[常用模板地址](https://github.com/github/gitignore/tree/main)】<br>
***Pattern***:
* 特殊extension的文件：\*.ext, 如 \*.log表示忽略以log结尾的所有文件；
* 特殊命名的文件夹：name/, 如 log/ 表示忽略所有项目下的log文件夹内容