# buddymap
0. Install python 3.5 on the computer and set it as the default python3.<br />
      Install and set up git account (optional: set up public and private key with git)
1. mkdir <folder_name>                 
2. cd <folder_name>
4. python3 -m venv myvirtualenv                            (create virtual env within the <folder_name>)
5. source myvirtualenv/bin/activate                        (activate the virtual env)
6. git clone git@github.com:herobaby71/buddymap.git        (clone this directory)
7. cd buddymap
8. pip install -r requirements.txt                         (install all required packages for python)
9. go to: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
10. follow the stepsand set up the postgresql with: <br />
      databasename(myproject): buddymap<br />
      username(myprojectuser): buddymap<br />
      password:123
11. python manage.py makemigrations                (make sure currently inside the buddyap repo)
12. python manage.py migrate
13. python manage.py createsuperuser                        (email and password of your own choice)
14. python manage.py runserver
15. in web browser go to:
      http://localhost:8000/<br />
      http://localhost:8000/admin<br />
      login using the superuser account you just created<br />
16. if all steps are successful gj
