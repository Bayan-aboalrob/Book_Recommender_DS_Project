# LitWise - Your Literary Pathfinder

LitWise is a book recommendation system that leverages the power of collaborative filtering to transform your reading experience. In an era dominated by web services like YouTube, Amazon, and Netflix, recommender systems have become an integral part of our daily lives. From suggesting products to matching user preferences with relevant content, these systems are essential for delivering personalized experiences.

## The Challenge of Book Recommendations

As a book enthusiast, you've likely encountered the frustration of searching for your next captivating read across various websites, only to find recommendations that fall short of your expectations. This dilemma isn't just an inconvenience for readers; it poses a significant challenge for websites. User dissatisfaction can trigger a domino effect, leading to user departures and decreased website activity.

## LitWise: Your Literary Solution

Enter **LitWise**, your literary pathfinder! We've harnessed the formidable capabilities of machine learning to tackle this challenge head-on. Our system is meticulously designed to comprehend your unique reading preferences and connect you with like-minded readers. LitWise serves as your guiding light, recommending your next literary treasure with precision and ease.

## Data Description

To make our recommendation system shine, we've gathered three essential datasets:

- **Book Data:** Contains details such as ISBN, Book Title, Book Author, Year of Publication, Publisher, and Image URLs.

- **Users Data:** Includes User ID, Location, and Age.

- **Ratings Data:** Comprises User ID, ISBN, and Book Rating.

The interactions between users and books are pivotal for our recommendation engine. To build a robust collaborative filtering model, we carefully prepare our data. This includes cleaning book data by dropping unnecessary URL features and refining column names for easier usage. Our feature engineering efforts lead to insightful analysis.

## Attribute Information

- **Book Data:** (ISBN, Book Title, Book Author, Year of Publication, Publisher, Image URL-S, Image URL-M, Image URL-L)

- **Users Data:** (User ID, Location, Age)

- **Ratings Data:** (User ID, ISBN, Book Rating)

## How LitWise Recommends Books

LitWise utilizes collaborative filtering to identify user similarities and preferences. By comparing users' behaviors, we predict book ratings for each user. The system then offers personalized recommendations, presenting the top 10 books that best match the user's interests. This process is powered by the K-Nearest Neighbors (KNN) algorithm, which assesses user closeness to refine recommendations. LitWise aims to make your reading journey effortless and enjoyable by tailoring book choices to your unique preferences.


