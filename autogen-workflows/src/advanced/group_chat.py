from typing import Dict
from autogen.agentchat.groupchat import GroupChat
from autogen.agentchat.agent import Agent
from autogen.agentchat.assistant_agent import AssistantAgent


class CustomGroupChat(GroupChat):
    def __init__(self, agents):
        super().__init__(agents, messages=[], max_round=4)

    def append(self, message: Dict):
        if message["name"] != "Paraphrazer" and message["name"] != "Task_Creator":
            super().append(message)

    def select_speaker(self, last_speaker: Agent, selector: AssistantAgent):
        # The admin will always forward the note to the summarizer
        if last_speaker.name == "Admin":
            return self.agent_by_name("Section_Analyzer")

        # Forward the note to the title generator if the user wants a title
        if last_speaker.name == "Section_Analyzer":
            return self.agent_by_name("Paraphrazer")
        
        if last_speaker.name == "Paraphrazer":
            return self.agent_by_name("Task_Creator")

        # Return the user agent by default
        return self.agent_by_name("Admin")
