基于flask的个人论坛
==================
#### 地址 
www.dolyvvvv.com 
#### 测试账号
账户:cwm  密码:123 
<br>

简介
-------
* 实现了板块分区、话题发布与浏览、评论回复、更改用户个人信息、私信、邮箱密码找回、@提醒等功能
* 利用`JavaScript`、`CSS`实现了`Markdown`渲染和语法高亮、
* 使用`MySQL`进行数据存储，基于`SQLAlchemy`的常见操作封装新的ORM，解决`n+1`问题，并支持`事务`功能
* 实现了对`CSRF`、`XSS`、`SQL`注入攻击的防御
* 使用`Nginx`缓存静态资源和反向代理提升访问速度，同时配合`Gunicorn`开启多个`Worker`实现多进程负载均衡，用`gevent`开启协程充分利用机器效能
* 使用`Redis`存储`Session`和`CSRF Token`，解决了在多进程下出现的数据共享问题，同时对计算量较大的数据进行缓存
* 使用`Celery`任务队列和`Redis`组合，解决请求高并发的问题，实现削峰，同时保证了数据的安全性
* 使用`Shell`脚本实现一键部署，加快开发测试速率

功能演示
-------
- 注册/登录<br><br>
![avatar](https://github.com/chenweiming812/Web-MVC-Socket/raw/master/static/readme/login.gif)
<br>
- 通过邮箱找回密码<br><br>
- 发帖/回帖<br><br>
![avatar](https://github.com/chenweiming812/Web-MVC-Socket/raw/master/static/readme/fatie.gif)
<br>
- 个人资料修改<br><br>
![v](https://github.com/chenweiming812/Web-MVC-Socket/raw/master/static/readme/setting.gif)
<br>
- 站内信<br><br>

依赖
----
* Ubuntu 18.04
* Python 3.6

