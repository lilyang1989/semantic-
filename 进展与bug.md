# 已有的结果

<img src="D:\GithubHere\Newsemantic-\图床\1.jpg" style="zoom:50%;" />

<img src="D:\GithubHere\Newsemantic-\图床\2.png" style="zoom:50%;" />

![](D:\GithubHere\Newsemantic-\图床\3.png)

# 进展

## 数据预处理及引文网络构建（√）

### 基于引文网络识别的主路径提取

分歧点：先提取路径还是先划分社群？ 论文中的原理部分是先划分后提取，举的例子也是先划分后提取，因为中间还有一步要选出核心网络社群，但因为数据量小，这次的情况比较特殊

![](D:\GithubHere\Newsemantic-\图床\que1.jpg)

问题：以什么样的数据导入pajek  之后进行基于SPC的主路径提取？