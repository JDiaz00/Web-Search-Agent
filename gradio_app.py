import gradio as gr
import os
from dotenv import load_dotenv

# Importar el agente directamente
from src.main import agent_executor

# Cargar variables de entorno
load_dotenv()

def process_query(query, agent_type="auto-detect"):
    """
    Enviar la consulta al agente y devolver la respuesta
    """
    try:
        # Usar directamente el agente en lugar de llamar a la API
        response = agent_executor.invoke({"input": query})
        
        # Formatear la respuesta según el formato especificado
        result = {
            "answer": response["output"],
            "steps": [step[0].tool + ": " + str(step[0].tool_input) for step in response["intermediate_steps"]]
        }
        
        # Construir una respuesta bien formateada en Markdown
        steps_md = "\n".join([f"- **{step}**" for step in result.get("steps", [])])
        
        markdown_response = f"""
### Respuesta
{result['answer']}

### Pasos ejecutados
{steps_md}
"""
        return markdown_response
    except Exception as e:
        return f"### Error\nHa ocurrido un error al procesar la consulta: {str(e)}"

# Crear la interfaz de Gradio con diseño mejorado
with gr.Blocks(title="Agente LangChain", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🤖 Agente LangChain con Gradio
        
        Este agente inteligente puede:
        - 🧮 **Realizar cálculos matemáticos** con precisión
        - 🔍 **Buscar información** en distintas fuentes
        - 📚 **Generar historias** creativas basadas en tus ideas
        
        Simplemente escribe tu consulta y el agente elegirá la herramienta más adecuada.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=3):
            query_input = gr.Textbox(
                label="Tu consulta",
                placeholder="Pregunta algo al agente...",
                lines=3
            )
            agent_selector = gr.Dropdown(
                choices=["auto-detect", "calculator", "search", "story"],
                value="auto-detect",
                label="Tipo de agente (opcional)"
            )
            submit_btn = gr.Button("Enviar consulta", variant="primary")
        
        with gr.Column(scale=5):
            output = gr.Markdown(label="Respuesta del agente")
    
    # Configurar la acción del botón
    submit_btn.click(
        fn=process_query,
        inputs=[query_input, agent_selector],
        outputs=output
    )
    
    # También permitir enviar con Enter
    query_input.submit(
        fn=process_query,
        inputs=[query_input, agent_selector],
        outputs=output
    )
    
    # Añadir ejemplos
    gr.Examples(
        examples=[
            ["¿Cuánto es 125 × 48?", "calculator"],
            ["¿Cuáles son los lugares turísticos más importantes de Perú?", "search"],
            ["Cuéntame una historia sobre un detective en una ciudad futurista", "story"],
            ["¿Cuál es la altura del Monte Everest?", "auto-detect"]
        ],
        inputs=[query_input, agent_selector]
    )

# Iniciar la aplicación de Gradio
if __name__ == "__main__":
    # Información de ayuda
    print("La aplicación Gradio se está ejecutando.")
    print("No es necesario ejecutar el servidor FastAPI por separado.")
    
    # Iniciar Gradio
    demo.launch() 