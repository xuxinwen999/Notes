# Git


## Commonly used commands
* git remote -v: 查看当前local project连接的远程repo地址，分别返回fetch和push的地址；
* git push [-u] origin [main:]master：
    - -u:
    - [main:]: local branch main推到remote branch master, local和remote分支名一样的话不用加
    - origin: 
* git 


## .gitignore
.gitignore文件不在.git/目录下，需要手动添加/删除。【[常用模板地址](https://github.com/github/gitignore/tree/main)】<br>
***Pattern***:
* 特殊extension的文件：\*.ext, 如 \*.log表示忽略以log结尾的所有文件；
* 特殊命名的文件夹：name/, 如 log/ 表示忽略所有项目下的log文件夹内容