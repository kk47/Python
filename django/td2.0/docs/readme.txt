本系统是资产管理系统+监控系统的整合版本。上个版本仅支持流控，这个版本更新了很多功能 具体可以看压缩包里的1.jpg和2.jpg的演示图

有可能出现的问题:
执行python manage.py syncdb遇到的错误Warning: Incorrect string value: '\xE6\x9C\xBA\xE6\x88\xBF' for column 'name' at row 1
解决办法:create database testxxx default charset=utf8 

若出现抓取不到数据请检查客户端的SNMP配置，目前这个版本只支持LINUX服务器，和交换机的端口流量抓取,下个版本将推出很多新功能.程序将snmp密码写死了 所以你如果SNMP密码不是public 那需要改变getdata.py 里面的snmppass= 'public' 密码即可

有很多地方还不完善，会继续改进。



部署环境:

CENTOS  6.3版本以上  python 2.4 以上 也可支持其他操作系统 但是需要你们自行安装以下依赖包
初始环境yum install *mysql* rrdtool-python python-pysnmp *python*   MySQL-python

如果用APACHE部署的话 需要安装python-apache模块 当APACHE目录的MODULES里面有mod_python 模块 当然你也可以python manage.py 127.0.0.1:80 用DJANGO自带的WEB发布端 进行测试访问

由于我用的是DJANGO 1.5 整合APACHE也很容易 只需在APACHE中加入以下配置

<VirtualHost *:82>
    WSGIScriptAlias / /var/www/html/monit/wsgi.py
    ServerAdmin linuxqq@linuxqq.net
    DocumentRoot /var/www/html/monit
    ServerName www.linuxqq.net
    ErrorLog "logs/linuxqq.net-error_log"
    CustomLog "logs/linuxqq.net-log" common
 <Directory "/var/www/html/monit">
     Options Indexes FollowSymLinks
     AllowOverride None
     Order allow,deny
     Allow from all
    </Directory>
 <Directory "/var/www/html/monit/wsgi.py">
<Files wsgi.py>
order deny,allow
allow from all
</Files>
</Directory>
</VirtualHost>


以上是基本部署需求 即可正常访问

将程序放置服务上以后 执行python manage.py syncdb  然后按需输入你要设定登陆账号密码

请关闭selinux 允许161 SNMP端口

程序上传上去以后 需将getdata.py脚本放入crontab

例
*/5 * * * * /usr/bin/python2.6  /var/www/html/monit/app/getdata.py


作者:LINUXQQ
作者博客:www.linuxqq.net 
作者邮箱:aksliyun@163.com


