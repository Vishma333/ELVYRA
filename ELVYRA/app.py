from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# Dummy user credentials (Replace with database logic later)
users = {"user1": "password123", "trooper1": "securepass"}

# Your Groq API Key
GROQ_API_KEY = "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"

@app.route("/")
def loading():
    return render_template("loading.html")  # Start with loading page

@app.route("/index")
def home():
    return render_template("index.html")  # Redirects to the main page

@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        elv_id = request.form.get("elv_id")
        password = request.form.get("password")
        if users.get(elv_id) == password:
            return redirect(url_for("user_dashboard"))
        else:
            return "Invalid Credentials. Try again!"
    return render_template("user_login.html")

@app.route("/user_dashboard", methods=["GET", "POST"])
def user_dashboard():
    if request.method == "POST":
        return redirect(url_for("transport_system"))
    return render_template("user_dashboard.html")

@app.route("/transport_system", methods=["GET", "POST"])
def transport_system():
    if request.method == "POST":
        return redirect(url_for("map_interface"))
    return render_template("transport_system.html")

@app.route("/map_interface", methods=["GET", "POST"])
def map_interface():
    if request.method == "POST":
        selected_bus = request.form.get("bus")
        if selected_bus:
            return redirect(url_for("show_map", bus=selected_bus))
        else:
            return "No bus selected", 400  # Bad request if no bus is selected
    return render_template("map_interface.html")

@app.route("/show_map")
def show_map():
    bus = request.args.get("bus", "Unknown Bus")
    return f"Showing map for bus: {bus}"

@app.route("/trooper_login", methods=["GET", "POST"])
def trooper_login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        if users.get(user_id) == password:
            return redirect(url_for("trooper_dashboard"))
        else:
            return "Invalid Credentials. Try again!"
    return render_template("trooper_login.html")

@app.route("/trooper_dashboard")
def trooper_dashboard():
    return render_template("trooper_dashboard.html")

@app.route("/get_chatbot_response")
def get_chatbot_response():
    user_message = request.args.get("msg", "").lower()

    # Groq API endpoint
    url = "https://api.groq.com/v1/chat/completions"

    # Headers for Groq API
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Body for Groq API
    payload = {
        "model": "mixtral-8x7b-32768",  # or change model if needed
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant designed to guide users about safety, safe travel routes, and general queries regarding Elvyra platform."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0.5,
        "max_tokens": 500
    }

    try:
        # Make request to Groq API
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        chatbot_reply = data['choices'][0]['message']['content']

    except Exception as e:
        print(f"Error contacting Groq API: {e}")
        chatbot_reply = "I'm sorry, I'm facing some issues. Please try again later."

    return jsonify(response=chatbot_reply)

if __name__ == "__main__":
    app.run(debug=True)
