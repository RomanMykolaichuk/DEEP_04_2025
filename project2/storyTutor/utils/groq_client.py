import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def build_prompt(topic, scenes, choices):
    prompt = f"You are an educational storyteller for adults. The topic is: '{topic}'.\n"
    prompt += "The story must be written in clear, engaging English with educational content. At the end of each part, suggest 3 short, plausible options to continue the story.\n\n"

    for i, scene in enumerate(scenes):
        prompt += f"Scene {i+1}:\n{scene['text']}\n"
        if i < len(choices):
            prompt += f"Chosen Option: {choices[i]}\n"

    prompt += "\nNow continue the story with the next scene (about 30 words), "
    "and provide three short, user-selectable continuation options.\n"
    "Only return the story scene as plain text. List the 3 options on separate lines, without bullet points.\n"
    "Answer should be given in format:\nScene:\n[Text]\n Options:\n [Option 1]\n[Option 2]\n[Option 3]"
    return prompt

def generate_scene_and_options(topic, scenes, choices):
    prompt = build_prompt(topic, scenes, choices)

    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    content = response.choices[0].message.content

    # Parse the response
    try:
        scene_text = content.split("Scene:")[1].split("Options:")[0].strip()
        options_block = content.split("Options:")[1].strip()
        options = [opt.strip("- ").strip() for opt in options_block.split("\n") if opt.strip()]
    except Exception as e:
        print("Parsing error:", e)
        scene_text = content.strip()
        options = ["Option A", "Option B", "Option C"]

    return scene_text, options
