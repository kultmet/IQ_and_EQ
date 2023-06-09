# IQ_and_EQ

This application generates a unique login for tests. IQ and EQ test results are linked to this login

## How to start?

You are in your directory... If you deploy the project locally

Clone the project

```
git clone https://github.com/kultmet/IQ_and_EQ.git
```

next - install package manager, - poetry

```
pip install poetry
```

next - install all requirements

```
# go to poenty dir
cd poetry-iq_and_eq
# install requirements
poetry install
# back to root catalog
cd ..
```

next - apply migrations

```
python manage.py migrate
```

next - start

```
python manage.py runserver
```

Well done! You did it!

## Request/Response examples

[POST]: http://127.0.0.1:8000/api/login/

```
# request:

send an empty request. No request body
```

```
# response:

{
    "login": "FVeFpgunlP"
}
```


[GET]: http://127.0.0.1:8000/api/login/<login:str>/

```
# response http://127.0.0.1:8000/api/login/FVeFpgunlP/

{
    "login": "FVeFpgunlP",
    "iq": {
        "point": 10,
        "created_at": "2023-06-09T06:15:30.003206Z"
    },
    "eq": {
        "letters": [
            "д",
            "б",
            "а",
            "г",
            "в"
        ],
        "created_at": "2023-06-09T06:14:37.773804Z"
    }
}

if test values not recorded:

{
    "login": "QnJKgNqwTi",
    "iq": null,
    "eq": null
}
```

[POST]: http://localhost:8000/api/iq/

```
# request:

{
    "login": "FVeFpgunlP",
    "point": 10
}
```

```
# response

{
    "login": "FVeFpgunlP",
    "point": 10
}
```


[POST]: http://localhost:8000/api/eq/

```
# request 

{
    "login": "FVeFpgunlP",
    "letters": ["д", "б", "а", "г", "в"]
}
```

```
# response

{
    "message": "Сохранен успешно"
}
```

## Development plans

1) This application uses a simple SQLite database. It is supposed to launch a PostgreSQL docker container and connect projects to Postgres

2) Here everything is prepared for local deployment. Deployment via docker-compose is pre-ready. If the customer wants, then the containers will be finalized

3) It is planned to optimize SQL queries, as they may not be optimal

## Thanks for your time!
