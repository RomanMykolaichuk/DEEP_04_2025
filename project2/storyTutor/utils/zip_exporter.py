import zipfile
import os

def export_story_zip(scenes, choices, output_name="story_export.zip"):
    txt_content = ""
    for i, scene in enumerate(scenes):
        txt_content += f"Scene {i+1}:\n{scene['text']}\n"
        txt_content += f"Choice: {choices[i]}\n\n"

    story_filename = "static/export/story.txt"
    os.makedirs("static/export", exist_ok=True)
    with open(story_filename, "w", encoding="utf-8") as f:
        f.write(txt_content)

    zip_path = f"static/export/{output_name}.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(story_filename, arcname="story.txt")
        for i, scene in enumerate(scenes):
            if "image" in scene and os.path.exists(scene["image"]):
                zipf.write(scene["image"], arcname=os.path.basename(scene["image"]))
            if "audio" in scene and os.path.exists(scene["audio"]):
                zipf.write(scene["audio"], arcname=os.path.basename(scene["audio"]))
    
    return zip_path
