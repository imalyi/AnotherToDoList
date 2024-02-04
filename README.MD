# ToDoList Application

The ToDoList application allows users to create their own tasks, categories, and to-do lists. Each user has their own set of tasks but can read all tasks of other users. Deletion and updating are allowed only for tasks that the user owns.

## Deployment

To deploy the application, use the following commands:

```bash
docker-compose up -d
docker exec -it [container_name_or_id] /bin/bash
```

Run tests: 
```bash
python3 manage.py test
```
Make migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py makemigrations another_todo_list
python3 manage.py migrate another_todo_list
```

Create superuser:
```bash
python3 manage.py createsuperuser
```

Visit http://127.0.0.1:8121/
Admin panel: http://127.0.0.1:8121/admin

## Examples:
Full documentation can be found at http://127.0.0.1:8121/redoc. I am providing a few examples here:

Authorize:
```bash
curl -X POST http://127.0.0.1:8121/token/ \
-H "Content-Type: application/json" \
-d '{
  "username": "<YOUR USERNAM>",
  "password": "<YOUR PASSWORD>"
}'
```

Create category:
```bash
curl -X POST http://127.0.0.1:8121/categories/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-d '{
    "name": "new category"
}'
```

Create task:
```bash
curl -X POST http://127.0.0.1:8121/tasks/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-d '{
    "title": "string",
    "description": "string",
    "completed": true,
    "due_to": "2019-08-24T14:15:22Z",
    "category": 0
}'
```

Find not completed tasks
```bash
curl -X GET 'http://127.0.0.1:8121/tasks/?completed=false' \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
