# src/code_interpreter_project/crew.py
from crewai import Agent, Task, Crew, Process, LLM
from codeinterpreter_tool import CodeInterpreterTool
from crewai_tools import FileWriterTool
import os

llm = LLM(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])

# Define the agent
code_agent = Agent(
    role="Code Interpreter for a given problem",
    goal="Solve the given problem with python  \
     code with given tools and return the results.",
    backstory="A skilled programmer capable of \
    interpreting and running Python scripts.",
    tools=[CodeInterpreterTool()],
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="File Writer",
    goal="write the code in code fences along with its solution to {output_file} using available tools",
    backstory="You are expert markdown writer, you are excellent in handling tools.",
    tools=[FileWriterTool()],
    verbose=True,
    llm=llm,
)

# Define the task
code_execution_task = Task(
    description="""Write the python code for the {problem}, then execute
        the Python code with given tools and return the result.""",
    expected_output="Result of the executed code.",
    agent=code_agent,
)

result_write_task = Task(
    description="""Write the python code for the {problem} and its solution to {output_file}.""",
    expected_output="Result of file writing status.",
    agent=writer,
)

# Create the crew
code_crew = Crew(
    agents=[code_agent, writer],
    tasks=[code_execution_task, result_write_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    # Input: Python code to execute
    inputs = {
        "problem": "Find the sum of 1, 2, 3, 4",
        "output_file": "result/result.md",
    }

    # Run the crew
    result = code_crew.kickoff(inputs=inputs)
    print(result)
