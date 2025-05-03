# Aplicación Gradio para LangChain Agent

Esta aplicación proporciona una interfaz web sencilla para interactuar con el agente de LangChain existente.

## Requisitos previos

- Python 3.10 o superior
- Poetry (gestor de dependencias)

## Instalación

1. Instalar dependencias con Poetry:
   ```
   poetry install
   ```

2. Configurar variables de entorno:
   Asegúrate de que tienes un archivo `.env` con las variables necesarias (API keys, etc.).

## Ejecutar la aplicación

Para ejecutar la aplicación Gradio:

```bash
poetry run python gradio_app.py
```

Esto iniciará la interfaz de Gradio y mostrará una URL local (por lo general `http://127.0.0.1:7860`).

## Uso

1. Abre la URL de Gradio en tu navegador.
2. Escribe una consulta en el campo de texto.
3. Haz clic en "Enviar consulta" o presiona Enter.
4. El agente procesará tu consulta y mostrará la respuesta junto con los pasos que siguió.

## Funcionalidades

El agente puede:
- Realizar cálculos matemáticos
- Buscar información en la web
- Generar historias cortas

## Solución de problemas

- Si recibes errores, asegúrate de que las claves API necesarias estén configuradas correctamente en el archivo `.env`.
- Verifica que todas las dependencias estén instaladas correctamente con `poetry install`. 