import asyncio
import edge_tts
import os

async def _generate_audio_async(script: str, output_path: str):
    """Internal async function to handle edge-tts generation."""
    voice = "en-US-JennyNeural"
    communicate = edge_tts.Communicate(script, voice)
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    await communicate.save(output_path)
    return output_path

def generate_audio(script: str, output_path: str):
    """
    Converts tour script to speech using edge-tts.
    
    Args:
        script (str): The text script to convert.
        output_path (str): The file path to save the .mp3 (e.g., 'outputs/tour.mp3').
        
    Returns:
        str: The path to the saved audio file.
    """
    try:
        os.makedirs("outputs", exist_ok=True)
        # Run the async function in a new event loop or using current loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        path = loop.run_until_complete(_generate_audio_async(script, output_path))
        loop.close()
        return path
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
