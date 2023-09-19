import toml

output_file = ".streamlit/key.toml"

with open(".streamlit/firestore-key.json") as json_file:
    json_text = json_file.read()

config = {"textkey": json_text}
toml_config = toml.dumps(config)

with open(output_file, "w") as f:
    f.write(toml_config)
