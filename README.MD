# ToDoList Application

The ToDoList application allows users to create their own tasks, categories, and to-do lists. Each user has their own set of tasks but can read all tasks of other users. Deletion and updating are allowed only for tasks that the user owns.

## Deployment

To deploy the application, use the following commands:

```bash
docker-compose up -d
docker exec -it [container_name_or_id] /bin/bash
cd /home/apps/todolist/


to run tests 
python3 manage.py test

to make migrations

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py makemigrations another_todo_list
python3 manage.py migrate another_todo_list
```

## Description
In my opinion, Redoc provides the best documentation for endpoints. It is widely used and can significantly increase the speed of development. After deploying the application, you can access the API documentation by visiting /redoc.

If you don't want to do it, I deployed this app to my test environment with Docker Compose and Cloudflare Zero Trust. Visit https://pleasevisitme.cityinminutes.me (the domain name is used for another project, so its name may seem unusual).
