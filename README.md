云学在线-web应用
==
##python环境: <br> 
python 3.6.4 和 对应的虚拟环境 <br>
最终版本是在linux平台下能直接运行，代码运行在虚拟环境中
## 缺点
发现这个web有个缺点，前端页面和后端页面逻辑紧紧的咬合在一起，一旦更改前端逻辑，后端也要进行相应的更改。
这种情况下，很容易前后端开发互相等待
## 上线步骤
1. cd / <br>
默认根目录下布置站点<br>
2. git clone ...... <br>
3. 
4. [配置nginx环境](http://www.cnblogs.com/2bjiujiu/p/8117166.html)<br>
仅供参考代码： https://github.com/beimenchuixue/shells<br>
4. 配置python环境： http://www.cnblogs.com/2bjiujiu/p/8457790.html <br>
一键配置shell https://github.com/beimenchuixue/shells<br>
5. mkenv OnlineSchool <br>
6. pip install -r requirements.txt <br>
安装相关依赖<br>
7. ln -s /OnlineSchool/online_school_nginx.conf /etc/nginx/conf.d/
创建项目目录下的nginx文件软链接到nginx能够找到的路径<br>
8. id nginx<br>
获取nginx的用户
9. 启动nginx<br> 
10. uwsgi --ini /OnlineSchool/online_school_uwsgi.ini --uid xxx <br>
