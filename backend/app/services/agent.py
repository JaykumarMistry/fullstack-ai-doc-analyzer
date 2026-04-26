import os
from loguru import logger
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from .document_processor import document_processor

@tool
def search_document_knowledge(query: str) -> str:
    """Useful for when you need to answer questions about the uploaded documents (PDFs, CSVs).
    Always use this tool when the user asks about specific data, policies, or facts from their documents.
    """
    logger.info(f"Agent invoked search_document_knowledge with query: {query}")
    if document_processor.vector_store is None:
        return "No documents have been uploaded or processed yet."
    
    docs = document_processor.vector_store.similarity_search(query, k=3)
    
    if not docs:
        return "I could not find any relevant information in the uploaded documents."
    
    context = "\n\n".join([f"Source ({doc.metadata.get('source', 'Unknown')}): {doc.page_content}" for doc in docs])
    return context

class TechTorchAgent:
    def __init__(self):
        # We use a simple system prompt instructing the agent to use tools
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant built for TechTorch. You have access to a tool to search through documents uploaded by the user. "
                       "If the user asks a general question, answer it directly. If the user asks about specific data or documents, ALWAYS use the 'search_document_knowledge' tool."),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # We initialize the LLM (requires OPENAI_API_KEY in .env)
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.tools = [search_document_knowledge]
        
        # Create the agent
        self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def invoke(self, query: str):
        logger.info(f"Executing agent query: {query}")
        try:
            response = self.agent_executor.invoke({"input": query})
            return response["output"]
        except Exception as e:
            logger.error(f"Error during agent execution: {e}")
            return "I'm sorry, I encountered an error while processing your request."

# Singleton instance
agent_service = TechTorchAgent()
