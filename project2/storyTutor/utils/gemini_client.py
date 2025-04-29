from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

client = genai.Client()

def generate_image(scene_description, scene_number):
    prompt = f"""
    Main subject:
    Create a dreamlike educational scene based on the following description:
    {scene_description}

    Generate image with main subject and background:
    Style should be imaginative, surreal, but focused on learning, growth, and discovery.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
    )

    image_path = f"static/images/scene{scene_number}.png"

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(image_path)

    return image_path
