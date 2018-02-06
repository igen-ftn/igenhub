# IgenHub
Application that allows users to manage projects and work progress. Topic of class Software Configuration Management, at the University of Novi Sad, Serbia.

Authors:
* Kim Novak (team leader)
* Ana Marojević
* Božo Bjeković
* Danilo Zeković

## Dependencies
Python     
PostgreSQL    
Docker    
Docker-compose

## Run The Application

First clone the project:
```
git clone https://github.com/igen-ftn/igenhub.git
```

Run the following commands to start the application:
```
docker-compose up -d
docker-compose run web python3 manage.py makemigrations
docker-compose run web python3 manage.py migrate
```
Note: if these commands do not work, try using `sudo` in front of them  

After starting the application, in your browser go to:
```
http://localhost:8000
```

## License

* MIT
