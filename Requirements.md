Purpose:
The idea of this application is to create a collection manager which will show a collection of items. For my application, I have decided to create a collection of movies. This collection manager will make it easier to view and edit the items in the collection. For example, filters can be added to only show specific items instead of the entire collection manager at once. 

Requirements:
1.	Users should be able to add additional items to the collection manager.
2.	Users should be able to edit existing items in the collection manager.
3.	Users should be able to group items into categories, filtering on those categories (e.g. genre, duration, age rating, favourites).
4.	Users can also add different type of movies such as kids movies and dictionaries, which can be filtered by additional fields, such as age rating.
5.	Specific movies can also be added to favourites, which can be used in filtering.

Stakeholders:
This collection manager can be used by anyone who requires a space where they can organise their movies. They can manage the movies they want to watch and remove any movie items once they watch it. Once the movies have been added, they can then filter searches to find specific movies to watch. For example, searches could be made based on the year the movie was released, the name of the movies and even specific genre's. This application should be easy to use for a wide range of users, including those who are not tech-savvy.

User Stories:
1. As a casual movie watcher, I want to add movies I've watched to my collection, so I can keep track of what I've seen.
2. As a movie collectorm, I want to be able to favourite movies in my collection so I can remember which ones I liked the most.
3. As a busy parent, I want to be able to filter and search movies by genre and duration so I can find something suitable for family movie night.

User Personas:
1. Name: Jordan
   Background: A 20 year old university student who loves watching movies in his free time. He often streams movies and occasionaly buys Blu-rays of his favourites.
   Goals: Jordan wants to track his movies by adding, removing and also keeping track of his favourites.
   Challenges: He often forgets, which movies he has already watched and which ones he needs to watch next.

2. Name: Mark
   Background: A 40-year-old father of two who organises family movie nights every weekend.
   Goals: Mark wants to maintain a list of family-friendly movies and wants to be able to add movies to a collection which both kids and adults can enjoy.
   Challenges: He struggles to remember movies that are suitable for children.


Data:
In this application, I am going to require specific data to build the collection manager. The application will require a dataset of different movies, which can be categorised by genre's, year of release and name. To use this data, I will use an object oriented approach with classes to to store any movie in the data set as an object. Using the class will make my desgin more efficieint, as I can use attributes to store information about a specific item. I can then have associated methods to ammend items in the collection manager. Due to this OOP approach, I can benefit from abstraction, as once I create the class, it can reuse it as a black box in my code. Encapsulation will also benefit my design, as attributes can be protected, and therefore they cannot be ammended accidently or by users with malicious intentions. To filter and store the entire collection manager, I have decided to use an SQL lite file which can be used to save the state of the collection manager. This will allow me to efficieintly search and add movies, as I will be able to use libraries to perfrom SQL queries. 



