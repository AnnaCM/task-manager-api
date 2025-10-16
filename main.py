from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter

from database import get_db
from schema import schema

async def get_context(db=Depends(get_db)):
    return {"db": db}

app = FastAPI()

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")
