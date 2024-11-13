from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Helper function to get character data
def get_character_data(character_id):
    try:
        response = requests.get(f'https://swapi.py4e.com/api/people/{character_id}')
        if response.status_code != 200:
            return None, "Character not found or invalid ID"
        character_data = response.json()

        # Fetch homeworld data
        homeworld_response = requests.get(character_data['homeworld'])
        homeworld_name = homeworld_response.json()['name']

        # Fetch films data
        films = []
        for film_url in character_data['films']:
            film_response = requests.get(film_url)
            films.append(film_response.json()['title'])

        return {
            "name": character_data['name'],
            "height": character_data['height'],
            "mass": character_data['mass'],
            "hair_color": character_data['hair_color'],
            "eye_color": character_data['eye_color'],
            "homeworld": homeworld_name,
            "films": films
        }, None

    except requests.exceptions.RequestException as e:
        return None, f"Error: {e}"

# Main route to handle form and display results
@app.route("/", methods=["GET", "POST"])
def index():
    character_data = None
    error_message = None

    if request.method == "POST":
        character_id = request.form["character_id"]
        character_data, error_message = get_character_data(character_id)

    return render_template("index.html", character_data=character_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
