# trini.energy 
A FastAPI/React project created to collate energy data for Trinidad and Tobago

Notes on running this app:
1) Set up an SSH tunnel to the VM to allow the FastAPI local code to access the database on your laptop using this command: ssh -L 5432:127.0.0.1:5432 <username>@<public_ip> -p 2222
2) Run these commands to detect changes in the SQLAlchemy models and apply those migrations:
    a) alembic revision --autogenerate
    b) alembic upgrade head