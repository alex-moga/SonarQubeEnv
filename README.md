SonarQube enviroment
====================

Скрипты сборки окружения для анализа качества исходного кода на основе SonarQube (CheckStyle, PMD, FindBugs).

Требования к окружению
----------------------

Для сборки потребуется **docker** версии 18.06 и выше, **docker compose** версии 1.18 и выше, установленные 
на машине, на которой будет производится сборка и запуск, а так же клиент **git**.  У пользователя, выполняющего 
операции по сборке контейнеров докер должны быть права на запуск комманд docker.

Описание репозитория
--------------------

* config - файлы конфигурации SonarQube
* plugins - плагины к SonarQube
* profiles - профили оценки качетва (quality profile)
* scripts - скрипт запуска и постконфигурирования приложения SonarQube 
* sonar_img - скрипт сборки докер образа базовой версии Sonar 7.5

Процедура сборки
----------------

Примечание: Все комманды сборки выполняются относительно директории репозитория.

1. Выполните сборку образа SonarQube 17.4:

```bash
    cd sonar_img 
    docker build . -t dit-sonar-img:7.5
```

2. Выполните сборку стека sonarq через скрипт docker compose:

```bash
    ./compose-rebuild.sh
```

3. Присоединитесь к контейнеру и контролируйте процедуру запуска:

```bash
    docker container logs -f sonarq_sonar_app_1
```

Проследите окончание запуска контейнера по наличию строки в логе и скопируйте токен. 
Токен понадобится для конфигурирования jenkins.  

```
	2019.04.22 13:48:17 INFO  app[][o.s.a.SchedulerImpl] SonarQube is up
	INFO:root:Config quality gate DitJavaSevirity using metrics: ('blocker_violations', 'critical_violations')
	INFO:root:append metric blocker_violations to DitJavaSevirity
	INFO:root:append metric critical_violations to DitJavaSevirity
	INFO:root:append user sonar
	INFO:root:generate token for sonar
	INFO:root:token exists!
	INFO:root:revoke token for sonar
	INFO:root:enable organization support
	*** tooken: {"login":"sonar","name":"sonar","token":"1aea94002558639d38f32ef6214622cf943f14c1","createdAt":"2019-04-22T13:48:20+0000"}
```
