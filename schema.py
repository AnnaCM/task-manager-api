import strawberry
from datetime import datetime
from models import Tasks
from strawberry import Schema
from typing import List, Optional
from graphql import GraphQLError


@strawberry.type
class TaskType:
    id: strawberry.ID
    title: str
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime]


@strawberry.type
class Query:
    @strawberry.field
    async def tasks(self, info: strawberry.Info, search: Optional[str] = None) -> List[TaskType]:
        db = info.context['db']
        if search:
            tasks = db.query(Tasks).filter(Tasks.title.ilike(f"%{search}%")).all()
        else:
            tasks = db.query(Tasks).all()

        return [get_task_type(task) for task in tasks]

    @strawberry.field
    async def task(self, id: strawberry.ID, info: strawberry.Info) -> TaskType | None:
        if not id.isdigit() or int(id) <= 0:
            raise GraphQLError("Invalid task ID: must be a positive integer.")

        db = info.context['db']
        task = db.query(Tasks).filter(Tasks.id == id).first()
        if not task:
            return None

        return get_task_type(task)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_task(self, title: str, info: strawberry.Info) -> TaskType:
        if not title.strip():
            raise GraphQLError("Title cannot be empty")

        db = info.context['db']
        task = Tasks(title=title, created_at=int(datetime.utcnow().timestamp()))

        db.add(task)
        db.commit()
        db.refresh(task)

        return get_task_type(task)
    
    @strawberry.mutation
    async def toggle_task(self, id: strawberry.ID, info: strawberry.Info) -> TaskType | None:
        if not id.isdigit() or int(id) <= 0:
            raise GraphQLError("Invalid task ID: must be a positive integer.")

        db = info.context['db']
        task = db.query(Tasks).filter(Tasks.id == id).first()
        if not task:
            return None
        
        task.completed = not task.completed
        task.updated_at = int(datetime.utcnow().timestamp())

        db.add(task)
        db.commit()
        db.refresh(task)

        return get_task_type(task)

    @strawberry.mutation
    async def edit_task(self, id: strawberry.ID, title: str, info: strawberry.Info) -> TaskType | None:
        if not id.isdigit() or int(id) <= 0:
            raise GraphQLError("Invalid task ID: must be a positive integer.")

        if not title.strip():
            raise GraphQLError("Title cannot be empty")

        db = info.context['db']
        task = db.query(Tasks).filter(Tasks.id == id).first()
        if not task:
            return None
        
        task.title = title
        task.updated_at = int(datetime.utcnow().timestamp())

        db.add(task)
        db.commit()
        db.refresh(task)

        return get_task_type(task)

    @strawberry.mutation
    async def delete_task(self, id: strawberry.ID, info: strawberry.Info) -> TaskType | None:
        if not id.isdigit() or int(id) <= 0:
            raise GraphQLError("Invalid task ID: must be a positive integer.")

        db = info.context['db']
        task = db.query(Tasks).filter(Tasks.id == id).first()
        if not task:
            return None

        task_response = get_task_type(task)
        
        db.delete(task)
        db.commit()
        
        return task_response


def get_task_type(task: Tasks) -> TaskType:
    return TaskType(
        id=task.id,
        title=task.title,
        completed=task.completed,
        created_at=convert_timestamp(task.created_at),
        updated_at=convert_timestamp(task.updated_at) if task.updated_at else None
    )


def convert_timestamp(timestamp: int):
    return datetime.fromtimestamp(timestamp)


schema = Schema(query=Query, mutation=Mutation)
