# ToDoList Application

The ToDoList application allows users to create their own tasks, categories, and to-do lists. Each user has their own set of tasks but can read all tasks of other users. Deletion and updating are allowed only for tasks that the user owns.

## API Documentation

In my opinion, Redoc provides the best documentation for endpoints. It is widely used and can significantly increase the speed of development. After deploying the application, you can access the API documentation by visiting `/redoc`.

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

If you dont wont to do it, i deployed this app to my test environment with docker-compose and cloudflare zero trust, visit https://pleasevisitme.cityinminutes.me(domain name is used for our another project, so its name may be weird)
