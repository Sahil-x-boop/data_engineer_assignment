import os, json

input_folder = "../applications"
output_folder = "../processed"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        data = {}
        with open(os.path.join(input_folder, filename)) as f:
            line = f.read().strip()
            parts = line.split("|")
            for part in parts: 
                key, value = part.split("=", 1)
                data[key.strip()] = value.strip()
        out_path = os.path.join(output_folder, filename.replace(".json", ".json"))
        with open(out_path, "w") as result:
            json.dump(data, result, indent=4)
print("Now All Converted to Json Files")

