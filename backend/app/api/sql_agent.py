from fastapi import APIRouter
from app.services.sql_generator import generate_sql
from app.database.query_executor import run_query

router = APIRouter()


@router.get("/ask")
async def ask_database(question: str):

    # Generate SQL
    sql_query = generate_sql(question)

    # Execute SQL
    result = run_query(sql_query)

    return {
        "question": question,
        "generated_sql": sql_query,
        "result": result
    }