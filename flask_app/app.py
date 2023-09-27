from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
from website.models import User
from website.auth import auth

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
    distances, neighbor_indices = model.kneighbors([user_ratings], n_neighbors=n_neighbors)

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


if __name__ == '__main__':
    app.run(debug=True)
