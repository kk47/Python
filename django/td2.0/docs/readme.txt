��ϵͳ���ʲ�����ϵͳ+���ϵͳ�����ϰ汾���ϸ��汾��֧�����أ�����汾�����˺ܶ๦�� ������Կ�ѹ�������1.jpg��2.jpg����ʾͼ

�п��ܳ��ֵ�����:
ִ��python manage.py syncdb�����Ĵ���Warning: Incorrect string value: '\xE6\x9C\xBA\xE6\x88\xBF' for column 'name' at row 1
����취:create database testxxx default charset=utf8 

������ץȡ������������ͻ��˵�SNMP���ã�Ŀǰ����汾ֻ֧��LINUX���������ͽ������Ķ˿�����ץȡ,�¸��汾���Ƴ��ܶ��¹���.����snmp����д���� ���������SNMP���벻��public ����Ҫ�ı�getdata.py �����snmppass= 'public' ���뼴��

�кܶ�ط��������ƣ�������Ľ���



���𻷾�:

CENTOS  6.3�汾����  python 2.4 ���� Ҳ��֧����������ϵͳ ������Ҫ�������а�װ����������
��ʼ����yum install *mysql* rrdtool-python python-pysnmp *python*   MySQL-python

�����APACHE����Ļ� ��Ҫ��װpython-apacheģ�� ��APACHEĿ¼��MODULES������mod_python ģ�� ��Ȼ��Ҳ����python manage.py 127.0.0.1:80 ��DJANGO�Դ���WEB������ ���в��Է���

�������õ���DJANGO 1.5 ����APACHEҲ������ ֻ����APACHE�м�����������

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


�����ǻ����������� ������������

��������÷������Ժ� ִ��python manage.py syncdb  Ȼ����������Ҫ�趨��½�˺�����

��ر�selinux ����161 SNMP�˿�

�����ϴ���ȥ�Ժ� �轫getdata.py�ű�����crontab

��
*/5 * * * * /usr/bin/python2.6  /var/www/html/monit/app/getdata.py


����:LINUXQQ
���߲���:www.linuxqq.net 
��������:aksliyun@163.com


