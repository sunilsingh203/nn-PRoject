from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit
import json
import ast
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add tools to path
tools_dir = os.path.join(os.path.dirname(__file__), 'tools')
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

from browser_tools import BrowserTools
from file_tools import FileTools
from search_tools import SearchTools
from template_tools import TemplateTools

load_dotenv()

# Set the API key for LiteLLM
if os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


@CrewBase
class ExpandIdeaCrew:
    """ExpandIdea crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def senior_idea_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_idea_analyst'],
            allow_delegation=False,
            tools=[],
            verbose=True,
            llm="google/gemini-2.5-flash"
        )
    
    @agent
    def senior_strategist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_strategist'],
            allow_delegation=False,
            tools=[],
            verbose=True,
            llm="google/gemini-2.5-flash"
        )
    
    @task
    def expand_idea(self) -> Task: 
        return Task(
            config=self.tasks_config['expand_idea_task'],
            agent=self.senior_idea_analyst_agent(),
        )
    
    @task
    def refine_idea(self) -> Task: 
        return Task(
            config=self.tasks_config['refine_idea_task'],
            agent=self.senior_strategist_agent(),
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )

@CrewBase
class ChooseTemplateCrew:

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    toolkit = FileManagementToolkit(
      root_dir='workdir',
      selected_tools=["read_file", "list_directory"]
    )

    @agent
    def senior_react_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_react_engineer'],
            allow_delegation=False,
            tools=[],
            verbose=True,
            llm="google/gemini-2.5-flash"
        )
    
    @task
    def choose_template(self) -> Task: 
        return Task(
            config=self.tasks_config['choose_template_task'],
            agent=self.senior_react_engineer_agent(),
        )
        
    @task
    def update_page(self) -> Task: 
        return Task(
            config=self.tasks_config['update_page_task'],
            agent=self.senior_react_engineer_agent(),
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
    
    
@CrewBase
class CreateContentCrew:

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    toolkit = FileManagementToolkit(
      root_dir='workdir',
      selected_tools=["read_file", "list_directory"]
    )

    @agent
    def senior_content_editor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_content_editor'],
            allow_delegation=False,
            tools=[
            ],
            verbose=True,
            llm="google/gemini-2.5-flash"
        )
    
    @agent
    def senior_react_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_react_engineer'],
            allow_delegation=False,
            tools=[],
            verbose=True,
            llm="google/gemini-2.5-flash"
        )
    
    @task
    def create_content(self) -> Task: 
        return Task(
            config=self.tasks_config['component_content_task'],
            agent=self.senior_content_editor_agent(),
        )
    
    @task
    def update_component(self) -> Task: 
        return Task(
            config=self.tasks_config['update_component_task'],
            agent=self.senior_content_editor_agent(),
        )
    
    
    @task
    def qa_component(self) -> Task: 
        return Task(
            config=self.tasks_config['qa_component_task'],
            agent=self.senior_content_editor_agent(),
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
    
class LandingPageCrew():
    def __init__(self, idea):
        self.idea = idea
    
    def run(self):
        print("\n" + "="*60)
        print("🚀 STARTING LANDING PAGE GENERATION WORKFLOW")
        print("="*60 + "\n")
        
        print("📋 PHASE 1: Expanding Your Idea")
        print("-" * 60)
        expanded_idea = self.runExpandIdeaCrew(self.idea)
        print(f"✅ Idea expanded successfully\n")
            
        print("📋 PHASE 2: Choosing Template")
        print("-" * 60)
        components_paths_list = self.runChooseTemplateCrew(expanded_idea)
        print(f"✅ Template chosen successfully\n")
            
        print("📋 PHASE 3: Creating Content")
        print("-" * 60)
        self.runCreateContentCrew(components_paths_list, expanded_idea)
        print(f"✅ Content creation completed\n")
        
        print("="*60)
        print("🎉 LANDING PAGE GENERATION COMPLETE!")
        print("="*60 + "\n")
    
    def runExpandIdeaCrew(self, idea):
        print(f"\n🔄 Starting ExpandIdeaCrew with idea: {idea[:100]}...\n")
        inputs1 = {
                "idea": str(idea)
        }
        expanded_idea = ExpandIdeaCrew().crew().kickoff(inputs=inputs1)
        print(f"\n📊 Expanded Idea Result:\n{str(expanded_idea)[:500]}...\n")
        return str(expanded_idea)

    def runChooseTemplateCrew(self, expanded_idea):
        print(f"\n🔄 Starting ChooseTemplateCrew...\n")
        inputs2 = {
            "idea": expanded_idea
        }
        components = ChooseTemplateCrew().crew().kickoff(inputs=inputs2)
        components = str(components)
        
        components = components.replace("\n", "").replace(" ",
                                                        "").replace("```","").replace("\\", "")
        
        # Convert the string to a Python list
        try:
            components_paths_list = ast.literal_eval(components)  # Safely parse the string
            print(f"✅ Found {len(components_paths_list)} components")
        except Exception as e:
            print(f"⚠️ Error parsing the string: {e}")
            components_paths_list = []
        result = json.dumps(components_paths_list, indent=4)

        return json.loads(result)

    def runCreateContentCrew(self, components, expanded_idea):
        from pathlib import Path
        import re
        
        # Establish safe working directory
        workdir = Path("./workdir").resolve()

        for idx, component_path in enumerate(components, 1):
            try:
                print(f"\n🔄 Processing component {idx}/{len(components)}: {component_path}")
                
                # Validate component_path
                if not isinstance(component_path, str):
                    print(f"⚠️ Skipping invalid component path: {component_path}")
                    continue
                
                # Extract filename safely
                filename = component_path.split('./')[-1]
                
                # Validate filename contains only safe characters
                if not re.match(r'^[a-zA-Z0-9._\-]+$', filename):
                    print(f"⚠️ Skipping component with invalid filename: {filename}")
                    continue
                
                # Validate the filename doesn't contain path traversal
                if ".." in filename or "/" in filename:
                    print(f"⚠️ Skipping component with unsafe filename: {filename}")
                    continue
                
                # Create safe file path
                file_path = workdir / filename
                
                # Resolve and validate the path is within workdir
                resolved_path = file_path.resolve()
                if not str(resolved_path).startswith(str(workdir)):
                    print(f"⚠️ Skipping component outside workdir: {filename}")
                    continue
                
                # Check if file exists before reading
                if not resolved_path.exists():
                    print(f"⚠️ Component file does not exist: {resolved_path}")
                    continue
                
                # Read file content safely
                with open(resolved_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                
                print(f"📄 File content loaded ({len(file_content)} bytes)")
                
                inputs3 = {
                    "component": component_path,
                    "expanded_idea": expanded_idea,
                    "file_content": file_content
                }

                print(f"⚙️ Running CreateContentCrew for {filename}...")
                CreateContentCrew().crew().kickoff(inputs=inputs3)
                print(f"✅ Component {filename} processed successfully")
                
            except Exception as e:
                print(f"❌ Error processing component {component_path}: {str(e)}")
                continue
