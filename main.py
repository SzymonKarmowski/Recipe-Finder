from flask import Flask, render_template, redirect, url_for, request
import requests

API_KEY = '70e0c5fab0d049b5bb535174b3c16d6a'

no_of_dishes = 9
query = []


random_recipes_url = f"https://api.spoonacular.com/recipes/random?number=9&apiKey={API_KEY}"
random_data = requests.get(random_recipes_url).json()

recipe_data = []
if 'recipes' in random_data:
    for recipe in random_data['recipes']:
        title = recipe['title']
        image = recipe['image']
        random_id = recipe['id']
        recipe_data.append({'title': title, 'image': image, 'id': random_id})
else:
    print("Error: 'recipes' key not found in random_data")


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template("index.html", recipe_data=recipe_data)


@app.route('/search', methods=['POST', 'GET'])
def search_recipie():
    if request.method == 'POST':
        ingredient = request.form['ingredients']
        query.append(ingredient)
        ingredients_str = ','.join(query)
        url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_str}&number={no_of_dishes}&apiKey={API_KEY}"
        data = requests.get(url).json()

        return render_template("index.html", recipe_data=data, selected_ingredients=query)
    return redirect(url_for('home'))


@app.route('/details_page', methods=['POST', 'GET'])
def details_page():
    dish_id = request.args.get('id')
    details_url = f"https://api.spoonacular.com/recipes/{dish_id}/information?apiKey={API_KEY}"
    details_data = requests.get(details_url).json()
    print(details_data)
    return render_template("details.html", details_data=details_data)


if __name__ == "__main__":
    app.run(debug=True)
