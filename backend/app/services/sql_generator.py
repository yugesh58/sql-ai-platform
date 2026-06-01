from app.services.llm import llm
from app.prompts.sql_prompt import SQL_SYSTEM_PROMPT



def generate_sql(user_question: str, schema: str):
    
    prompt = f"""
    {SQL_SYSTEM_PROMPT}
    
    Database Schema:
    {schema}

    User Question:
    {user_question}
    """
    

    response = llm.invoke(prompt)

    sql_query = response.content.strip()

    # Remove markdown formatting
    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")

    return sql_query.strip()