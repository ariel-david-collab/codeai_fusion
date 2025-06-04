from typing import Type
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool, BaseTool
from crewai.tasks import TaskOutput

from pydantic import BaseModel, Field
import os


# Configurar LLM para CrewAI usando OpenRouter
llm = LLM(
    model="google/gemma-3-27b-it:free",
    api_key="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",
    base_url="https://openrouter.ai/api/v1",
    custom_llm_provider="openrouter"
)

class TranslateToSQLInput(BaseModel):
    nl_query: str = Field(..., description="Natural language query to translate to SQL")
    schema_info: str = Field(..., description="Database schema information for translation")

class ExecuteSQLInput(BaseModel):
    db_name: str = Field(..., description="Database name to execute the SQL query on")
    sql_query: str = Field(..., description="SQL query to execute")

class TranslateToSQLTool(BaseTool):
    """
    A tool to translate natural language queries into SQL queries.
    It requires the natural language query and the database schema information.
    """
    name: str = "SQL Query Translator"
    description: str = (
        "Translates a natural language query into an SQL query. "
        "Use this tool when you need to convert a user's question in plain English into a database-readable SQL query. "
        "You must provide the natural language query and the relevant database schema information."
    )
    args_schema: Type[TranslateToSQLInput] = TranslateToSQLInput

    def _run(self, nl_query: str, schema_info: str) -> str:
        """
        The core logic for translating natural language to SQL.
        In a real application, this would involve an LLM call or a sophisticated NL-to-SQL engine.
        """
        print(f"\n🤖 [TranslateToSQLTool AGENT ACTION]")
        print(f"   Translating NL Query: '{nl_query}'")
        print(f"   Using Schema Info: '{schema_info}'")
        
        # --- Placeholder Implementation ---
        # This is a very basic placeholder. A real implementation would be much more complex.
        # For example, it might use another LLM call specialized for SQL generation,
        # or a dedicated NL-to-SQL library.
        if "john doe's email" in nl_query.lower() and "users" in schema_info.lower() and "email" in schema_info.lower():
            generated_sql = f"SELECT email FROM users WHERE name = 'John Doe';"
            print(f"   Generated SQL: {generated_sql}")
            return generated_sql
        else:
            error_msg = "Could not translate the NL query to SQL with the provided information. The query might be too complex or the schema insufficient."
            print(f"   Error: {error_msg}")
            # Returning an error message or a specific "I don't know" SQL equivalent is important
            return f"/* Error: {error_msg} */ SELECT NULL;" 
        # --- End Placeholder ---

class ExecuteSQLTool(BaseTool):
    """
    A tool to execute SQL queries against a specified database.
    It requires the database name/connection and the SQL query.
    """
    name: str = "SQL Query Executor"
    description: str = (
        "Executes an SQL query on a specified database and returns the result. "
        "Use this tool after you have a valid SQL query that you need to run. "
        "You must provide the database identifier and the SQL query."
    )
    args_schema: Type[ExecuteSQLInput] = ExecuteSQLInput

    def _run(self, db_name: str, sql_query: str) -> str:
        """
        The core logic for executing an SQL query.
        In a real application, this would connect to a database and run the query.
        """
        print(f"\n🤖 [ExecuteSQLTool AGENT ACTION]")
        print(f"   Executing SQL Query on DB '{db_name}':\n     {sql_query.strip()}")

        # --- Placeholder Implementation ---
        # This is a placeholder. A real implementation would use a database connector
        # (e.g., sqlite3, psycopg2, mysql.connector) to execute the query.
        # It should also handle potential SQL errors, empty results, etc.
        if sql_query.strip().upper() == "SELECT EMAIL FROM USERS WHERE NAME = 'JOHN DOE';":
            result = "john.doe@example.com"
            print(f"   Query Result: {result}")
            return result
        elif "/* Error:" in sql_query:
            error_msg = f"Cannot execute query due to a translation error: {sql_query}"
            print(f"   Error: {error_msg}")
            return error_msg
        else:
            # Simulating a generic query execution
            print(f"   Warning: Executing an unrecognized placeholder query. Returning generic success.")
            return "Query executed successfully (placeholder result)."
        # --- End Placeholder ---

def step_callback(step_name, result) -> str:
    print(f"Step '{step_name}' result: {result}")
    return result

def task_callback(output: TaskOutput):
    """
    Callback function executed after a task is completed.
    Prints details about the task execution.
    """
    print(f"\n✅ Task Completed: {output.description}")
    print(f"   Raw Output from Agent:\n   ------------------------\n{output.raw}\n   ------------------------")

sql_specialist_agent = Agent(
    role="SQL Database Specialist",
    goal=(
        "Accurately translate natural language questions into SQL queries based on the provided database schema, "
        "execute these SQL queries against the specified database, and return the results in a clear, "
        "concise, and human-readable format."
    ),
    backstory=(
        "You are a highly skilled SQL Database Specialist with years of experience in multiple database systems. "
        "You excel at understanding user intent from natural language, crafting precise SQL queries, "
        "and retrieving information efficiently. You are meticulous about using the correct schema information "
        "and ensuring query safety and correctness. You always double-check your generated SQL before execution."
    ),
    tools=[TranslateToSQLTool(), ExecuteSQLTool()],
    llm=llm,
    verbose=True, # Enables detailed logging of the agent's thought process
    allow_delegation=False, # For this simple setup, no delegation is needed
    # memory=True # You can enable memory if the agent needs to remember past interactions for a sequence of tasks
)

# The task description needs to be clear enough for the agent to understand the multi-step process.
nl_query_processing_task = Task(
    description=(
        "1. Take the following natural language query: '{nl_query}'.\n"
        "2. Use the provided database schema information: '{schema_info}'.\n"
        "3. Translate the natural language query into an SQL query using the 'SQL Query Translator' tool.\n"
        "4. Take the generated SQL query and execute it on the database named '{db_name}' using the 'SQL Query Executor' tool.\n"
        "5. Provide the final result obtained from the SQL query execution as your answer."
    ),
    expected_output=(
        "The direct result from the executed SQL query. For example, if the query asks for an email, "
        "the output should be the email address (e.g., 'user@example.com'). If the query returns multiple rows or columns, "
        "format it readably. If an error occurs, provide a clear error message."
    ),
    agent=sql_specialist_agent,
    callback=task_callback,
    # Inputs will be interpolated into the description from the `inputs` dict in `crew.kickoff()`
)

query_crew = Crew(
    agents=[sql_specialist_agent],
    tasks=[nl_query_processing_task],
    process=Process.sequential, # Tasks will be executed one after another
    verbose=True
)

# Execute workflow
task_inputs = {
    "nl_query": "What is John Doe's email?",
    "schema_info": "Table: users, Columns: id, name, email",
    "db_name": "example.db",
}

# Kickoff the crew with the defined inputs
# The `inputs` dictionary will be used to fill in the placeholders in the task's description
try:
    result = query_crew.kickoff(inputs=task_inputs)
        
    print("\n🎉 Crew Execution Finished!")
    print("------------------------------------")
    print("Final Result from Crew:")
    print(result)
    print("------------------------------------")

except Exception as e:
    print(f"\n❌ An error occurred during crew execution: {e}")
    import traceback
    traceback.print_exc()
