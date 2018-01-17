# igenhub
Application that allows user to manage projects and work progress. Topic of class Software configuration management.

To change permissions on files if needed:
  sudo chmod -R 0777 dirName or file name

## Dependencies
Python    
PostgreSQL    



## run the application

(sudo) docker-compose run web python3 manage.py makemigrations
docker-compose up
if it does not work then:

sudo docker-compose up   
   
docker-compose up may not start the app properly the first time, try stopping it applying makemigration command and then trying again    
