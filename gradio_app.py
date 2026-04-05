import asyncio
import os

import gradio as gr
from dotenv import load_dotenv

from src.services.agent_service import MultiAgentService

load_dotenv()

MAX_QUERY_LENGTH = 2000

# Initialize the multi-agent service
service = MultiAgentService()


def process_query(query: str, agent_type: str = "auto-detect") -> str:
    """
    Send the query to the multi-agent service and return the response.
    """
    # Input validation
    if not query or not query.strip():
        return "### Error\nPlease enter a query."

    query = query.strip()
    if len(query) > MAX_QUERY_LENGTH:
        return f"### Error\nQuery is too long ({len(query)} characters). Maximum allowed is {MAX_QUERY_LENGTH} characters."

    try:
        # Run the async service method in a sync context
        loop = asyncio.new_event_loop()
        try:
            response = loop.run_until_complete(service.process_query(query))
        finally:
            loop.close()

        # Build formatted markdown response
        steps_md = ""
        if response.steps:
            steps_md = "\n".join([f"- **{step}**" for step in response.steps])

        markdown_response = f"""### Answer
{response.answer}
"""
        if steps_md:
            markdown_response += f"""
### Steps Executed
{steps_md}
"""
        return markdown_response

    except Exception as e:
        return f"### Error\nFailed to process query: {str(e)}"


# Create the Gradio interface
with gr.Blocks(title="LangChain Multi-Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
        # LangChain Multi-Agent with Gradio

        This intelligent agent can:
        - **Perform mathematical calculations** with precision
        - **Search for information** across various sources
        - **Generate creative stories** based on your ideas

        Simply type your query and the agent will choose the most appropriate tool.
        """)

    with gr.Row():
        with gr.Column(scale=3):
            query_input = gr.Textbox(
                label="Your query",
                placeholder="Ask the agent something...",
                lines=3,
                max_lines=10,
            )
            agent_selector = gr.Dropdown(
                choices=["auto-detect", "calculator", "search", "story"],
                value="auto-detect",
                label="Agent type (optional)",
            )
            submit_btn = gr.Button("Submit query", variant="primary")

        with gr.Column(scale=5):
            output = gr.Markdown(label="Agent response")

    submit_btn.click(
        fn=process_query,
        inputs=[query_input, agent_selector],
        outputs=output,
    )

    query_input.submit(
        fn=process_query,
        inputs=[query_input, agent_selector],
        outputs=output,
    )

    gr.Examples(
        examples=[
            ["What is 125 x 48?", "calculator"],
            ["What are the most important tourist spots in Peru?", "search"],
            ["Tell me a story about a detective in a futuristic city", "story"],
            ["What is the height of Mount Everest?", "auto-detect"],
        ],
        inputs=[query_input, agent_selector],
    )

if __name__ == "__main__":
    print("Gradio app is running.")
    demo.launch()
