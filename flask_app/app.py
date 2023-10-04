from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
from website.models import User
from website.auth import auth
import numpy as np 
from instance import database

app = Flask(__name__)
app.register_blueprint(auth)

# Loading models and data 
model = pickle.load(open('artifacts/model.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))
model_item_based = pickle.load(open('artifacts/model_item_based.pkl', 'rb'))
book_pivot_item_based = pickle.load(open('artifacts/book_pivot_item_based.pkl', 'rb'))

# Defining  book recommendation function 
def recommend_books(user_id, n_neighbors=5, n_recommendations=10):
    # Finding the user's row index in the 'book_pivot' DataFrame
    user_ratings = book_pivot.loc[user_id, :]

    # Finding the nearest neighbors of the user
    distances, neighbor_indices = model.predict([user_ratings], n_neighbors=n_neighbors)

    # Getting the user IDs of the nearest neighbors
    neighbor_user_ids = book_pivot.index[neighbor_indices[0]]

    # Creating a dictionary to store book recommendations
    book_recommendations = {}

    for neighbor_user_id in neighbor_user_ids:
        # Find books rated by the neighbor but not by the user
        neighbor_ratings = book_pivot.loc[neighbor_user_id, :]
        recommended_books = neighbor_ratings[user_ratings == 0]  # Select unrated books

        # Storeingthe recommendations in the dictionary
        book_recommendations[neighbor_user_id] = recommended_books

    # Combining all recommendations and recommend the top 'n_recommendations' books
    all_recommendations = pd.concat(book_recommendations.values()).groupby(level=0).sum()
    top_recommendations = all_recommendations.sort_values(ascending=False).head(n_recommendations)

    return top_recommendations

def get_book_info(isbn_list):
    """
    Retrieve unique book information (title and image URL) from the 'final_rating' DataFrame based on a list of ISBNs.
    
    Parameters:
    - isbn_list (list): List of ISBNs to retrieve book information for.
    
    Returns:
    - book_info (list): List of dictionaries containing book title and image URL corresponding to the given ISBNs.
    """
    # Using 'final_rating' DataFrame to map ISBNs to book information
    book_info = final_rating[final_rating['ISBN'].isin(isbn_list)][['title', 'img_url']].drop_duplicates().to_dict('records')

    return book_info


def recommend_book(book_name):
    book_id = np.where(book_pivot_item_based.index == book_name)[0][0]
    distance, suggestion = model_item_based.kneighbors(book_pivot_item_based.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

    recommended_books = []  # Create an empty list to store recommendations

    for i in range(len(suggestion)):
        books = book_pivot_item_based.index[suggestion[i]]
        for j in books:
            # Append the book title and image URL to the recommended_books list
            recommended_books.append({'title': j, 'img_url': get_img_url_for_title(j)})

    return recommended_books
app = Flask(__name__, template_folder='website/templates')

@app.route('/')
def home():
    return render_template('home.html')

# Recommendation route with login_required decorator to protect it
from flask import render_template

@app.route('/recommend', methods=['POST'])
@login_required
def recommend():
    try:
        # Using the ID of the current logged-in user
        user_id = current_user.id
        
        recommended_books = recommend_books(user_id)
        recommended_isbns = recommended_books.index.tolist()
        recommended_info = get_book_info(recommended_isbns)

        # Rendering the 'recommendationBooks.html' template and passing the recommendations as context
        return render_template('recommendationBooks.html', recommendations=recommended_info)

    except Exception as e:
        return jsonify({'error': str(e)})

existing_user_ids= pickle.load(open('artifacts/user_ids.pkl', 'rb'))

user_index = int(existing_user_ids[-1])

def generate_unique_user_id(existing_user_ids):
    global user_index  # Declare user_index as a global variable
    user_index += 1
    return existing_user_ids[user_index ]


@app.route("/register", methods=["POST"])
@cross_origin()
def register_user():
    #this function handles the registration of a new user, ensuring they don't already exist, securely hashing their password, storing the user in the database, and using sessions to keep them authenticated. It then returns information about the registered user in JSON format.
    email = request.json["email"]
    password = request.json["password"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    session["user_id"] = new_user.id

    return jsonify({
        "id": generate_unique_user_id(existing_user_ids),
        "email": new_user.email
    })

@app.route("/login", methods=["POST"])
def login_user():
    
    #this function handles user login. It checks if the user exists and if the provided password matches the stored hashed password. If authentication is successful, it uses sessions to keep the user authenticated and returns information about the authenticated user in JSON format. If authentication fails (due to incorrect email or password), it returns an unauthorized error.
    
    email = request.json["email"]
    
    password = request.json["password"]
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })

@app.route("/logout", methods=["POST"])
@cross_origin()
def logout_user():
    session.pop("user_id")
    return "200"

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        recommended_books = recommend_book(search_query)  # Call your recommendation function here with the search query

        return render_template('recommendationBooks.html', recommendations=recommended_books )

    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)