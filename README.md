![neuro-learn](neurolearn_v0314.png?raw=true "neuro-learn")

---

## Contents
- [Contents](#contents)
- [Django+VueJS+Celery](#djangovuejscelery)
  - [Environment](#environment)
  - [Build Project](#build-project)
  - [Architecture Design](#architecture-design)
  - [Integrate Vue into Django](#integrate-vue-into-django)
  - [Integrate Celery into Django](#integrate-celery-into-django)
- [NEURO-LEARN-WEB](#neuro-learn-web)
  - [UI Design](#ui-design)
  - [User Interface](#user-interface)
    - [Vue and Element-UI](#vue-and-element-ui)
    - [Data Transaction](#data-transaction)
    - [Visualization](#visualization)
  - [Service](#service)
    - [Celery and RabbitMQ](#celery-and-rabbitmq)
    - [Databases](#databases)
  - [Deployment](#deployment)
    - [GitHub](#github)

## Django+VueJS+Celery

### Environment

- For Django: Python, Django, MySQL, etc. Use pip to install modules including Django and MySQL is recommended;
- For Vue: Node.js. Use npm to install modules including Element-UI is recommended;
- For celery: rabbitmq, celery, django-celery. Use apt-get to install rabbitmq-server, and pip to install celery and django-celery;

### Build Project

- Create project;  
```
$ django-admin startproject neurolearn
```
- Create Django app as backend;  
```
$ cd neurolearn
$ python manage.py startapp backend
```
- Install mysql if none installed, refering to [*installation of MySQL on Ubuntu18.04*](https://blog.csdn.net/weixx3/article/details/80782479), [*solving access denied for user root@localhost*](https://www.cnblogs.com/cpl9412290130/p/9583868.html), and [*creating a database*](https://www.cnblogs.com/jiangxiaobo/p/7089345.html);
```
'NAME': 'neurolearn'
'USER': 'root'
'PASSWORD': 'root'
```
- Change the default database to mysql and add backend to apps in settings.py;
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djvuecelery',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
    }
}
```
- Initialize database and start server to test;
```
$ python manage.py makemigrations backend
$ python manage.py migrate
$ python manage.py runserver
```
- Install vue-cli to initialize a vue project;
```
$ npm install -g vue-cli
$ npm view vue-cli version // check the package version
```
- Create VueJS project as frontend;  
```
$ vue-init webpack frontend
```
- Install vue dependencies and build the vue project;
```
$ cd frontend
$ npm install # install dependencies
$ npm run build # build project
```
- Add 'backend' to the INSTALLED_APPS in neurolearn/neurolearn/settings.py;
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend',
]
```
- Create superuser of django in order to use django admin.
```bash
$ python manage.py createsuperuser
# username: root
# email: leibingye@outlook.com
# password: root
# localhost:8000/admin/
```

*References*  
[整合Django+Vue.js框架快速搭建web项目](https://cloud.tencent.com/developer/article/1005607)  
[后端Django+前段Vue.js快速搭建项目](https://blog.csdn.net/Jack_wise/article/details/80690826)  
[vue使用npm run build命令打包项目](https://www.haoht123.com/1678.html)

### Architecture Design

![architecture_design_web.png](architecture_design_web.png)

### Integrate Vue into Django

- Configure url paths in neurolearn/neurolearn/urls.py;
```python
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
]
```
- Configure the 'DIRS' in neurolearn/neurolearn/settings.py;
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['frontend/dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
- Change time zone and language code;
```python
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
```
- Add the path of static files rendered by django;
```python
# add at the end of the file
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend/dist/static")
]
```
- Run server to test frontend rendering by django;
```
$ python manage.py runserver
```
- Run the following command each time *frontend* is modified;
```
$ cd frontend
$ npm run build
```
- Using the following command allows debugging in Vue environment;
```
$ cd frontend
$ npm run dev
```
- Using Vue environment to visit Django API will result in cross-domain issues, one solution is using proxyTable in Vue, and the other is using django-cors-headers;
```
$ pip install django-cors-headers
```
- After installing django-cors-headers, we need to configure it in settings.py;
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # added
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
```python
CORS_ORIGIN_ALLOW_ALL = True # added
```

*References*  
[Vue+Django+MySQL搭建指南（个人全栈快速开发）](https://www.jianshu.com/p/9093894d2614)  
[我如何使用Django+Vue.js快速构建项目](https://zhuanlan.zhihu.com/p/25080236)  
[Django与Vue之间的数据传递](https://www.jianshu.com/p/dcd15f5731bf)

### Integrate Celery into Django

- Add 'djcelery' to the INSTALLED_APPS in neurolearn/neurolearn/settings.py;
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend',
    'djcelery',
]
```
- Configure RabbitMQ by add the following codes at the end of neurolearn/neurolearn/settings.py;
```python
import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"
```
- Running ```$ python manage.py``` will result in several new commands to control worker in celery;
```
[djcelery]
    celery
    celerybeat
    celerycam
    celeryd
    celeryd_detach
    celeryd_multi
    celerymon
    djcelerymon
```
- Add a file backend/tasks.py;
```python
from celery.decorators import task

@task
def add(x, y):
  return x + y
# @ is the decorator, making the add function a callback function
# when calling add in a webapp, the add function doesn't execute immediately
# instead the function name and parameters will be packed as a message and
# sent to the queue, then the worker will process these messages one by one
```
- Create a worker awaiting task messages;
```
$ python manage.py migrate
$ python manage.py celeryd -l info
```
- Open another console and use the following command to open interactive console;
```
$ python manage.py shell
>>> from backend.tasks import add
>>> r = add.delay(3, 5)
>>> r.wait()
8
```

*References*  
[使用django+celery+RabbitMQ实现异步执行](https://blog.csdn.net/dipolar/article/details/22162863)

---

## NEURO-LEARN-WEB

### UI Design

### User Interface

#### Vue and Element-UI

- Refer to [official site](http://element.eleme.io/#/en-US/component/) for installation and usage guide;
- Use template from [this repository](https://github.com/tmpbook/vue-template-with-element-ui), which looks like [this](https://tmpbook.github.io/vue-template-with-element-ui/#/table);
- Replace frontend in the project with template, type the following commands to build the vue project, integrating it into django framework;
```
$ npm install
$ npm install node-sass // if needed
$ npm run dev // serve with hot reload at localhost:8080
$ npm run build // build for Django to serve at localhost:8000
```
- To customize navigation menu and router, change the code in **NavMenu.vue** to configure the navigation, **routes.js** to configure the router, and **index.vue** in each page in **pages** to configure the template;
- The **pages** folder consists of **home** (routed by NEURO-LEARN title), **overview**, **newtask**, **submissions**, **viewer**, and **help**, which are routed by items in NavMenu except for home;
```
Note: 
The template is develped using element-ui 1.4, which is out of date. Use element-ui 2.7 when develop frontend.
```
- The way to pass eslint check is to add a comment like below at the end of the code;
```JavaScript
//eslint-disable-line
```
- To use scss, install node-sass and sass-loader;
```
$ npm install --save-dev sass-loader style-loader css-loader
```
- To change the theme colors in element-ui, refer to [this site](https://blog.csdn.net/youlinaixu/article/details/83447527) for help;
- When defining the style of a page by css, name the class carefully or use a nested css since it is effective across files;

*References*  
[Element-UI Documentation](http://element-cn.eleme.io/1.4/#/zh-CN/component/)  
#### Data Transaction

- Refer to [django_with_vue](https://github.com/rogerlh/django_with_vue) and [django-vue](https://github.com/RogersLei/django-vue) for examples of using axios and database for data transaction between Vue and Django;
- As mentioned above, the configuration of databases is in the **settings.py**, and by default the name of table created by **models.py** is 'appname_modelclassname', in which the modelclassname refer to the class defined in **models.py**;
- Models are called and instantiated by **views.py**, which received the http request from frontend and return a response;
- The urls of functions in views are defined in **urls.py**， which is included in the **urls.py** in project folder;
- The **urls.py** in project folder contains the urls when frontend sends request to http://127.0.0.1:8000/;
- As $http in vue requires an out-of-date module named vue-resource, it is recommended to use [axios](https://ykloveyxk.github.io/2017/02/25/axios%E5%85%A8%E6%94%BB%E7%95%A5/) instead;

*references*  
[Django模型Model自定义表名和字段列名](https://www.jianshu.com/p/dc71417c1dc2)  
[axios全攻略](https://ykloveyxk.github.io/2017/02/25/axios%E5%85%A8%E6%94%BB%E7%95%A5/)  
[vue $http请求服务](https://blog.csdn.net/qq_36947128/article/details/72832977)  
[Vue:axios中的POST请求传参问题](https://www.cnblogs.com/WQLong/p/8316152.html)  
[Vue + Django](https://www.jianshu.com/p/f271be791cce)

#### Visualization

- Refer to [ECharts](https://echarts.baidu.com/echarts2/index.html) for a JavaScript-based data visualization solution;

### Service

#### Celery and RabbitMQ

#### Databases

- To use Django-Model to manipulate databases, refer to [this site](https://www.cnblogs.com/yangmv/p/5327477.html);

### Deployment

#### GitHub

- To deploy a repository on GitHub, refer to [this site](http://www.cnblogs.com/yuanzm/p/3945814.html), basically after creating a project, pull a branch from it and replace all files with your own, then just commit;