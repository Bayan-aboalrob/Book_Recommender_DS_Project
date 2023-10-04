from flask import Flask, request, jsonify, session, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_session import Session
from config import ApplicationConfig
from models import db, User  
import seeder 
# from flask import Flask, request, jsonify, session, render_template
# from flask_bcrypt import Bcrypt
# from flask_cors import CORS, cross_origin
from scipy.sparse import csr_matrix
# CORS is enabled for the entire application using CORS(app), and the cross_origin() decorator is applied to a specific route (/example) to allow cross-origin requests for that route. This is essential for enabling communication between a frontend client and a backend server when they are hosted on different domains or ports.
# from flask_session import Session
# from config import ApplicationConfig
# from models import db, User
import pickle
import pandas as pd
import numpy as np
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
from sklearn.neighbors import NearestNeighbors
from flask_login import LoginManager
# from seeder import seed_data


app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# Call the seed_data function directly

# login_manager = LoginManager()
# login_manager.login_view = '/login'  # Set the login view route
# login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#     # Load the user from your database or user storage based on the user_id
#     user = User.query.get(int(user_id))
#     return user
# login_manager = LoginManager()
# login_manager.login_view = "/login"  # Set the login view route
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
    # return User(user_id)


@app.route("/@me", methods=["GET", "POST"])
@cross_origin()
def get_current_user():
    # This route allows authenticated users to retrieve their user information (ID and email) using the /@me endpoint. If a user is not authenticated, it returns an unauthorized error.
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    })


@app.route("/register", methods=["GET", "POST"])
def register_user():
    # this function handles the registration of a new user, ensuring they don't already exist, securely hashing their password, storing the user in the database, and using sessions to keep them authenticated. It then returns information about the registered user in JSON format.
    email = request.json["email"]
    password = request.json["password"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(uder_id = user_id , email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # user_id = generate_unique_user_id(existing_user_ids)
    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })


#@login_manager.user_loader
@app.route("/login", methods=["GET", "POST"])
def login_user():

    # this function handles user login. It checks if the user exists and if the provided password matches the stored hashed password. If authentication is successful, it uses sessions to keep the user authenticated and returns information about the authenticated user in JSON format. If authentication fails (due to incorrect email or password), it returns an unauthorized error.

    email = request.json["email"]

    password = request.json["password"]
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    # if not bcrypt.check_password_hash(user.password, password):
    #     return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.user_id

    return jsonify({
        "id": user.user_id,
        "email": user.email
    })


@app.route("/logout", methods=["GET", "POST"])
@cross_origin()
def logout_user():
    session.pop("user_id")
    return "200"


model = pickle.load(open('artifacts/model.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))
model_item_based = pickle.load(open('artifacts/model_item_based.pkl', 'rb'))
book_pivot_item_based = pickle.load(
    open('artifacts/book_pivot_item_based.pkl', 'rb'))


# Defining  book recommendation function
def recommend_books(user_id, n_neighbors=5, n_recommendations=10):
    # Finding the user's row index in the 'book_pivot' DataFrame
    user_ratings = book_pivot.loc[user_id, :]

    # Finding the nearest neighbors of the user
    distances, neighbor_indices = model.kneighbors(
        [user_ratings], n_neighbors=n_neighbors)

    # Getting the user IDs of the nearest neighbors
    neighbor_user_ids = book_pivot.index[neighbor_indices[0]]

    # Creating a dictionary to store book recommendations
    book_recommendations = {}

    for neighbor_user_id in neighbor_user_ids:
        # Find books rated by the neighbor but not by the user
        neighbor_ratings = book_pivot.loc[neighbor_user_id, :]
        # Select unrated books
        recommended_books = neighbor_ratings[user_ratings == 0]

        # Storeingthe recommendations in the dictionary
        book_recommendations[neighbor_user_id] = recommended_books

    # Combining all recommendations and recommend the top 'n_recommendations' books
    all_recommendations = pd.concat(
        book_recommendations.values()).groupby(level=0).sum()
    top_recommendations = all_recommendations.sort_values(
        ascending=False).head(n_recommendations)

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
    book_info = final_rating[final_rating['ISBN'].isin(
        isbn_list)][['title', 'img_url']].drop_duplicates().to_dict('records')

    return book_info

    return top_recommendations

# @login_manager.user_loader


@app.route('/recommend', methods=["POST"])
# @login_required
def recommend():
    try:

        # Using the ID of the current logged-in user
        # user_id = current_user.id
        request_data = request.get_json()
        #print(request_data)  # Get the JSON data from the request
        user_id = request_data['userId']
        recommended_books = recommend_books(user_id)
        # print(recommended_books)
        recommended_isbns = recommended_books.index.tolist()
        recommended_info = get_book_info(recommended_isbns)

        # Rendering the 'recommendationBooks.html' template and passing the recommendations as context
        return recommended_info
    except Exception as e:
        return jsonify({'error': str(e)})


def recommend_book(book_name):
    book_id = np.where(book_pivot_item_based.index == book_name)[0][0]
    distance, suggestion = model_item_based.kneighbors(
        book_pivot_item_based.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

    recommended_books = []  # Create an empty list to store recommendations

    for i in range(len(suggestion)):
        books = book_pivot_item_based.index[suggestion[i]]
        for j in books:
            # Append the book title and image URL to the recommended_books list
            recommended_books.append(
                {'title': j, 'img_url': get_img_url_for_title(j)})

    return recommended_books


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        # Call your recommendation function here with the search query
        recommended_books = recommend_book(search_query)

        return recommended_books


if __name__ == "__main__":
    #seeder.seed_data()
    app.run(host='127.0.0.1', debug=True)
