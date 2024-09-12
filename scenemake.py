# You have no idea how long I had to gaslight ChatGPT to make it write out this

import json
import uuid
import re

def extract_and_create_scenes(json_file_path, output_file_path, num_new_scenes=100):
    # Read the input JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Extract existing scenes
    scenes = data.get('scenes', [])
    
    # Get available backgrounds from the JSON
    backgrounds = data.get('backgrounds', [])

    # Helper function to extract the number from the background name
    def get_frame_number(bg):
        match = re.search(r'(\d+)', bg['name'])
        return int(match.group(1)) if match else 0

    # Sort backgrounds by the number in their name (e.g., bw_output_frame_0001 -> 1)
    backgrounds.sort(key=get_frame_number)

    # Ensure we have enough backgrounds for the number of scenes we want to create
    if len(backgrounds) < num_new_scenes:
        raise ValueError("Not enough backgrounds to create the specified number of scenes.")

    # Create a base template for new scenes
    def create_new_scene(index, background, next_scene_id):
        scene_id = str(uuid.uuid4())  # Unique scene ID
        return {
            "name": f"Generated Scene {index + 1}",
            "backgroundId": background['id'],  # Assign the sorted background ID
            "tilesetId": "",
            "width": 20,
            "height": 18,
            "type": "TOPDOWN",
            "paletteIds": [],
            "spritePaletteIds": [],
            "collisions": [],
            "autoFadeSpeed": 1,
            "id": scene_id,
            "symbol": f"generated_scene_{index + 1}",
            "x": 60 + (index * 10),  # Increment x for variety
            "y": 159 + (index * 5),  # Increment y for variety
            "actors": [],
            "triggers": [],
            "script": [
                {
                    "command": "EVENT_SWITCH_SCENE",
                    "args": {
                        "sceneId": next_scene_id,
                        "x": {
                            "type": "number",
                            "value": 0
                        },
                        "y": {
                            "type": "number",
                            "value": 0
                        },
                        "direction": "",
                        "fadeSpeed": 0
                    },
                    "id": f"switch_{index + 1}"
                }
            ],
            "playerHit1Script": [],
            "playerHit2Script": [],
            "playerHit3Script": []
        }, scene_id

    # Generate new scenes in addition to existing ones
    generated_scenes = []
    next_scene_id = None  # For the last scene, there is no next scene

    for i in reversed(range(num_new_scenes)):  # Iterate in reverse to build forward references
        background = backgrounds[i % len(backgrounds)]  # Use modulo to cycle if needed
        new_scene, current_scene_id = create_new_scene(i, background, next_scene_id)
        generated_scenes.insert(0, new_scene)  # Insert at the beginning of the list
        next_scene_id = current_scene_id  # Set next_scene_id to the current scene's ID for chaining

    # Append the newly generated scenes to the existing ones
    scenes.extend(generated_scenes)

    # Write the output JSON to a new file
    with open(output_file_path, 'w') as file:
        json.dump(scenes, file, indent=4)

# Define your file paths
input_file_path = 'input.json'  # Replace with the actual path to your input JSON file
output_file_path = 'out.json'  # Replace with the desired output file path

# Run the extraction and scene creation
extract_and_create_scenes(input_file_path, output_file_path, num_new_scenes=36)  # Adjust num_new_scenes as needed

# Check the output to confirm correct processing
with open(output_file_path, 'r') as file:
    fixed_output_data = json.load(file)

# Display part of the output to confirm correct processing
print(fixed_output_data[:5])  # Showing the first 5 scenes as an example