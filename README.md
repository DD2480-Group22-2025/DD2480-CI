# DD2480-CI

## FastAPI server

```bash
fastapi dev app/main.py
```



**Project structure**

```
DD2480-CI/
├── requirements.txt           # Dependencies
├── start_services.sh          # Service starter script
├── stop_services.sh           # Service stop script
├── report.md                  # report 
├── README.md                  # readme file
├── LICENSE                    # MIT license
├── app/
│   ├── __init__.py            # init file
│   ├── mail.py                # main endpoint
│   |── lib/
│   |    ├── database_api.py   # querying the database
│   |    └── util.py           # utility functions
|   └── routers/
│         ├── builds.py        # build pages
│         └── notify.py        # router 
├── tests/
│   ├── test_syntax.py         # Tests for P1
│   ├── test_runner.py         # Tests for P2
│   ├── test_notifier.py       # Tests for P3
│   └── example_files.py       # Tests for P1
|── scripts/
|    ├── create_database.sh    # create database script
|    ├── deploy.sh             # Deployment script
|    ├── run_tests.sh          # Auto-test script
|    └── start_ngrok.sh        # ngrok starter script
├── database/
│    └── database_tables.sql   # initial table setup
└── deployment/
     ├── ci-server.service     # ci setup file
     ├── ngrok.service         # ngrok setup file
     └── ngrok.yml             # YAML file for ngrok

```
