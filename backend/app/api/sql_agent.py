from fastapi import APIRouter
from app.services.sql_generator import generate_sql
from app.database.query_executor import run_query
from app.graphs.sql_graph import sql_graph


router = APIRouter()


@router.get("/ask")
async def ask_database(question: str):
    result=sql_graph.invoke({
        "question":question,
        "retry_count":0
    })    

    return result