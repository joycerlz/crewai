from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.stock_analyst.tools.stock_data_tool import StockDataTool

# Uncomment the following line to use an example of a custom tool
# from stock_analyst.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class StockAnalyst():
	"""StockAnalyst crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def data_retriever(self) -> Agent:
		return Agent(
			config=self.agents_config['data_retriever'],
			verbose=True,
			tools=[StockDataTool("Tesla")]
		)

	@agent
	def technical_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['technical_analyst'],
			verbose=True
		)

	@agent
	def reporter(self) -> Agent:
		return Agent(
			config=self.agents_config['reporter'],
			verbose=True
		)

	@task
	def fetch_data_task(self) -> Task:
		return Task(
			config=self.tasks_config['fetch_data_task'],
		)

	@task
	def analyze_data_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_data_task'],
		)

	@task
	def generate_report_task(self) -> Task:
		return Task(
			config=self.tasks_config['generate_report_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the StockAnalyst crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
