# setup 
required installs 

install Django from pip 
```
py -m pip install Django

```
install cryptodome for Rsa 
install djangorestframework

## start server 

make neassory migrations
```
py manage.py makemigrations 
py manage.py migrate
```
start server
```
py manage.py runserver
```
navigate to /admin to data 

navigate to /polls to generate auth tockens 

# version info
$ py --version = Python 3.11.0

$ pip --version pip 23.3.1 from D:\python\Lib\site-packages\pip (python 3.11)

$ py -m django --version
4.2.6

# API server objective 

## validate Adhar numbers

- validate adhar number with its details 
- generate otp for users
- verify otp 
- verified users get auth-tocken to which used in regestration for voteing

