Here’s a complete list of the **parameters (template variables)** your `server_management.html` Jinja2 template needs, based on the placeholders used:

---

### 🔧 Functional Parameters (from backend)
| Parameter         | Type          | Description |
|------------------|---------------|-------------|
| `user_name`       | `str`         | (Optional) Current user’s name, if used for greetings |
| `templates`       | `list[dict]`  | Server templates available for cloning/creating new ones. Each `dict` should have `id` and `name`. |
| `config_files`    | `list[str]`   | List of server config files to edit (e.g. `server.properties`, `bukkit.yml`, etc.) |
| `online_players`  | `list[dict]`  | Active players online. Each `dict` should have `name` (and optionally `uuid`, `ip`, etc.) |
| `mods`            | `list[dict]`  | Installed mods/plugins. Each `dict` should include `name` and `url`. |
| `stats`           | `dict`        | System performance stats with keys: `cpu`, `ram`, `disk_io` (values as strings or numbers) |
| `backups`         | `list[dict]`  | Backup history. Each `dict` should have `id` and `timestamp`. |
| `server`          | `dict`        | The current server instance object. Should at least include `id` (for URLs). |

---

### 🔗 Required Routes (for Flask’s `url_for`)
| Route Name          | Expected Parameters      | Purpose |
|---------------------|--------------------------|---------|
| `create_server`     | None                     | POST target for new server creation |
| `edit_file`         | `name`                   | Link to config file editor |
| `server_action`     | `server_id`              | GET API to run `start`, `stop`, `restart` commands |

---

### ✅ Example Data Structure

Here's a Python-style example of what you might pass in:

```python
render_template("server_management.html",
  user_name="Isma",
  templates=[
    {"id": "vanilla-1.20.1", "name": "Vanilla 1.20.1"},
    {"id": "paper", "name": "PaperMC"}
  ],
  config_files=["server.properties", "bukkit.yml", "whitelist.json"],
  online_players=[
    {"name": "Steve"},
    {"name": "Alex"}
  ],
  mods=[
    {"name": "JourneyMap", "url": "https://www.curseforge.com/journeymap"},
    {"name": "WorldEdit", "url": "https://enginehub.org/worldedit"}
  ],
  stats={"cpu": 23, "ram": 62, "disk_io": 1.2},
  backups=[
    {"id": "b1", "timestamp": "2025-04-17 22:45"},
    {"id": "b2", "timestamp": "2025-04-16 18:20"}
  ],
  server={"id": "main-survival"}
)
```

Let me know if you want me to help build the corresponding Flask view or dummy data for testing!