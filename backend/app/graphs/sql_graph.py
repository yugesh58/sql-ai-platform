from typing_extensions import TypedDict
from app.services.sql_generator import generate_sql
from app.database.query_executor import run_query
from app.database.schema_retriever import get_schema
from langgraph.graph import StateGraph, START, END

class SQLState(TypedDict):
    question: str
    schema: str
    sql_query: str
    validation_status: str
    retry_count: int
    result: list

def retrieve_schema_node(state: SQLState):
    schema=get_schema()

    return {"schema":schema}
def sql_generation_node(state:SQLState):
    question=state['question']
    schema=state["schema"]
    sql_query=generate_sql(question, schema)

    return {"sql_query": sql_query }

def validate_sql_node(state:SQLState):
    sql_valid_query=state["sql_query"]

    if "customers" in sql_valid_query:
        return{"validation_status":"invalid"}
    else:
        return{"validation_status":"valid"}
    
def regenrate_sql_node(state:SQLState):
    question=state["question"]
    schema=state['schema']
    sql_query=generate_sql(question, schema)

    retry_count=state.get("retry_count",0)+1
    return{"sql_query":sql_query,"retry_count":retry_count}

def validation_router(state:SQLState):
    if state["validation_status"]=="valid":
        return "execute_sql"
    if state.get("retry_count",0) < 2:
        return "retry_sql"
    return "end"

def query_executor_node(state:SQLState):
    sql_query=state['sql_query']
    result=run_query(sql_query)

    return{"result":result}


graph_builder=StateGraph(SQLState)


#nodes
graph_builder.add_node("generate_sql",sql_generation_node)

graph_builder.add_node("validate_sql",validate_sql_node)

graph_builder.add_node("execute_sql",query_executor_node)
graph_builder.add_node("retry_sql",regenrate_sql_node)
graph_builder.add_node("schema_node",retrieve_schema_node)


#edges
graph_builder.add_conditional_edges(
    "validate_sql",
    validation_router,
    {
        "execute_sql": "execute_sql",
        "retry_sql":"retry_sql",
        "end": END
    }
)


graph_builder.add_edge(START,"schema_node")
graph_builder.add_edge("schema_node","generate_sql")
graph_builder.add_edge("generate_sql","validate_sql")
graph_builder.add_edge("retry_sql","validate_sql")
graph_builder.add_edge("execute_sql",END)

sql_graph=graph_builder.compile()