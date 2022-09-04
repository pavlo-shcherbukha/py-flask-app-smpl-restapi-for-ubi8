# py-flask-app-smpl-restapi-for-ubi8
Flask app з простеньким Rest API та його deployment в RedHat UBI8 контейнер

В якосіт шаблона викорситано [ python-sample-vscode-flask-tutorial](https://github.com/microsoft/python-sample-vscode-flask-tutorial)


## Підготовка до запуску локально

- створити віртуальну environment

```bash
py -m venv env
```

- ЗАвантажити потрібні бібліотеки


```bash

py -m pip install -r requirements.txt

```

##  Запуск локально в developent mode

- Створити env variable в terminal VSC

    * PowerShell
```bash
$env:FLASK_APP="hello_app.webapp"

$env:FLASK_APP

```

    * CMD
```bash
SET FLASK_APP=hello_app.webapp

ECHO %FLASK_APP%

```

Для запуска в режимі debug  налаштувати  **.vscode/launch.json**


```json
      {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "hello_app.webapp",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "0"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"

            ],
            "jinja": true
        }

```


- Запуск в режимі development

```bash
python -m flask run
```

- Запуск в режимі DEBUG

 Запуск описано за лінком: [Створення найпростішого скрипта для flask app та запуск applicaiton з індивідуальн ою назвою в режимі DEBUG](https://pavlo-shcherbukha.github.io/posts/2022-09-02/python-flask-1/#p-6).


Сервіс стартує локально за адресою: http://localhost:5000

Rest API  доступне  за адресою: http://localhost:5000/api



## Розроблені API

### Health check GET  /api/health

Використовується для перевірки працездатності сервісу

Повертає JSON

```json
{
  "success": true
}
```

### Створити Branch POST /api/branch

- Запит

    * http headers

    ``` text
       content-type: application/json

    ``` 

    * request

    ```json
            {
            "brn_code": "12345",
            "brn_name": "Head Quarters"
            }

    ```

- Відповідь OK

    **Status Code**=200

                ```json
            {
            "brn_id": "1234-5678-0001"
            }

    ```

- Відповідь Error in request (не коректний або не вказаний content type) 

**Status Code**=400

```json
    {
        "Error": {
            "code": "InvalidAPIRequest",
            "description": "Помилка при отриманні запиту",
            "target": "branch_srvc",
            "Inner": {
            "code": "Bad Request",
            "description": "The browser (or proxy) sent a request that this server could not understand."
            }
        }
    }
```

- Відповідь Error in request, не передані обов'язкові параметри

**Status Code**=422

```json
{
  "Error": {
    "code": "InvalidAPIRequestParams",
    "description": "No key [brn_code]",
    "target": "branch_srvc",
    "Inner": {
      "code": "NoKey",
      "description": "Перевіряю наявність  brn_code"
    }
  }
}

```


### Повернути список всіх Branch-ів GET /api/branch

- Запит

    * http headers

    ``` text
       content-type: application/json

    ``` 

- Відповідь

```json

[{
  "brn_id": "1234-5678-0001",
  "brn_code": "001",
  "brn_name": "Head q"
}, {
  "brn_id": "2222-2222-2222-2222",
  "brn_code": "002",
  "brn_name": "Cheald 1"
}, {
  "brn_id": "3333-3333-3333-3333",
  "brn_code": "004",
  "brn_name": "Cheald 2"
}]

```

### Видалити Branch по ID DELETE /api/branch/<brn_id>

- Запит

    * http headers

    ``` text
       content-type: application/json

    ``` 

- Відповідь

```json
        {
        "ok": true
        }

```

### Прочитати Branch по ID GET /api/branch/<brn_id>


- Запит

    * http headers

    ``` text
       content-type: application/json

    ``` 

- Відповідь

```json
    {
    "brn_id": 123,
    "brn_code": "001",
    "brn_name": "Head q"
    }

```

### Update Branch по ID PUT /api/branch/<brn_id>


- Запит

    * http headers

    ``` text
       content-type: application/json

    ``` 

    * Request

    ```json
            {
            "brn_code": "12345",
            "brn_name": "Head Quarters"
            }

    ```



- Відповідь -OK

```json
    {
    "brn_id": 123,
    "brn_code": "001",
    "brn_name": "Head q"
    }

```

- Відповідь - ERR


**Status Code**=422

```json
{
  "Error": {
    "code": "InvalidAPIRequestParams",
    "description": "No key [brn_code]",
    "target": "branch_srvc_id_PUT",
    "Inner": {
      "code": "NoKey",
      "description": "Перевіряю наявність  brn_code"
    }
  }
}

```

### Розрахувати статистику в запитиі з параметрами GET api/branchstat?brn_id=111&dts=2022-01-01&dtf=2022-03-30&mode=ALL


- Запит

    * http headers

    ``` text
       content-type: application/json

    ``` 

- Відповідь -OK

```json
{
  "brn_id": "111",
  "dts": "2022-01-01",
  "dtf": "2022-03-30",
  "mode": "ALL"
}

```

- Відповідь - ERR

```json
{
  "Error": {
    "code": "InvalidAPIRequestParams",
    "description": "No key [brn_id]",
    "target": "branch_stat",
    "Inner": {
      "code": "NoKey",
      "description": "Перевіряю наявність  brn_id"
    }
  }
}

```

