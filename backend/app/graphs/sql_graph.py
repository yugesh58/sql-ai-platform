from typing_extensions import TypedDict
from app.services.sql_generator import generate_sql
from app.database.query_executor import run_query
from langgraph.graph import StateGraph, START, END

class SQLState(TypedDict):
    question:str
    sql_query:str
    validation_status:str
    result:list

def sql_generation_node(state:SQLState):
    question=state['question']

    sql_query=generate_sql(question)

    return {"sql_query": sql_query }

def validate_sql_node(state:SQLState):
    sql_valid_query=state["sql_query"]

    if "customers" in sql_valid_query:
        return{"validation_status":"invalid"}
    else:
        return{"validation_status":"valid"}

def query_executor_node(state:SQLState):
    sql_query=state['sql_query']
    result=run_query(sql_query)

    return{"result":result}


graph_builder=StateGraph(SQLState)

graph_builder.add_node("generate_sql",sql_generation_node)
graph_builder.add_node("validate_sql",validate_sql_node)
graph_builder.add_node("execute_sql",query_executor_node)

graph_builder.add_edge(START,"generate_sql")
graph_builder.add_edge("generate_sql","validate_sql")
graph_builder.add_edge("validate_sql","execute_sql")
graph_builder.add_edge("execute_sql",END)

sql_graph=graph_builder.compile()