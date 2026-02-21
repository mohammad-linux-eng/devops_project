from flask import Flask, request, jsonify
import datetime
import random
import psutil
import json
import os

app = Flask(__name__)

CONFIG_PATH = "config/colors.json"

ALL_COLORS = [
    "#FF6B6B", "#6BCB77", "#4D96FF", "#FFD93D", "#FF8FAB",
    "#845EC2", "#00C9A7", "#FFC75F", "#F9F871", "#C34A36"
]

DEFAULT_COLORS = [
    "#FF6B6B", "#6BCB77", "#4D96FF"
]

# ساخت config اولیه
def ensure_config():
    if not os.path.exists("config"):
        os.makedirs("config")

    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump({"colors": DEFAULT_COLORS}, f)

# خواندن رنگ‌ها
def load_colors():
    ensure_config()
    with open(CONFIG_PATH) as f:
        return json.load(f).get("colors", [])

# ذخیره رنگ‌ها
def save_colors(colors):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"colors": colors}, f)

@app.route("/")
def home():
    now = datetime.datetime.now().strftime("%Y/%m/%d     %H:%M:%S")
    cpu = psutil.cpu_percent(interval=0.2)
    ram = psutil.virtual_memory().percent

    selected_colors = load_colors()

    # فقط از رنگ‌های انتخاب‌شده استفاده کن
    if selected_colors:
        bg = random.choice(selected_colors)
    else:
        bg = "#ffffff"  # اگر هیچ رنگی انتخاب نشده

    # ساخت باکس‌ها
    color_boxes = ""
    for c in ALL_COLORS:
        selected = "selected" if c in selected_colors else ""
        color_boxes += f'''
        <div class="color-box {selected}" data-color="{c}" style="background:{c};"></div>
        '''

    return f"""
<html>
<head>
<style>
body {{
    text-align:center;
    font-family: sans-serif;
}}

.container {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin: 20px;
}}

.color-box {{
    width: 60px;
    height: 60px;
    border: 2px solid black;
    cursor: pointer;
    transition: transform 0.1s;
}}

.color-box:hover {{
    transform: scale(1.1);
}}

.selected {{
    outline: 4px solid black;
}}
</style>
</head>

<body style="background-color:{bg}; padding-top:30px;">

    <h1>Hello World</h1>
    <h2>{now}</h2>
    <h3>CPU: {cpu}%</h3>
    <h3>RAM: {ram}%</h3>

    <hr>

    <h3>Select Colors</h3>

    <div class="container">
        {color_boxes}
    </div>

    <button onclick="saveColors()">Save</button>

<script>
let selectedColors = new Set({selected_colors});

// کلیک روی رنگ
document.querySelectorAll('.color-box').forEach(box => {{
    box.addEventListener('click', () => {{
        const color = box.dataset.color;

        if (selectedColors.has(color)) {{
            selectedColors.delete(color);
            box.classList.remove('selected');
        }} else {{
            selectedColors.add(color);
            box.classList.add('selected');
        }}
    }});
}});

// ذخیره
function saveColors() {{
    fetch('/save-colors', {{
        method: 'POST',
        headers: {{
            'Content-Type': 'application/json'
        }},
        body: JSON.stringify({{
            colors: Array.from(selectedColors)
        }})
    }})
    .then(res => res.json())
    .then(() => alert("Saved!"));
}}
</script>

</body>
</html>
"""

@app.route("/save-colors", methods=["POST"])
def save():
    data = request.get_json()
    colors = data.get("colors", [])

    # فقط رنگ‌های معتبر ذخیره بشن
    valid_colors = [c for c in colors if c in ALL_COLORS]

    save_colors(valid_colors)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    ensure_config()
    app.run(host="0.0.0.0", port=5000)
