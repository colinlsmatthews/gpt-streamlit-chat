import EAGPT_lib as eagpt

schema = {
    "name": "TEXT PRIMARY KEY",
    "content": "TEXT",
    "description": "TEXT"
}

eagpt.update_db(db="profiles.db", clear=True, schema=schema)

name = "Atum"
description = "Atum is the god of creation"
content = "Atum is the god of creation and the setting sun. He is the first god of the Ennead."

eagpt.add_profile_to_db(
    name=name,
    description=description,
    content=content
)


# def initialize_db(db="profiles.db", schema):
#     conn = sqlite3.connect(db)
#     db_name = "."split(db)[0]
#     c = conn.cursor()
#     c.execute(f'''CREATE TABLE IF NOT EXISTS {db_name}
#                  (name TEXT PRIMARY KEY, content TEXT, description TEXT)''')
#     conn.commit()
#     conn.close()
