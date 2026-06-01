from app.graphs.sql_graph import sql_graph

result = sql_graph.invoke(
    {
        "question": "Show all employees",
        "retry_count": 0
    }
)

print(result)