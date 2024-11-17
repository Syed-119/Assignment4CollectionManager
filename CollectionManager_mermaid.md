```mermaid
erDiagram
    USER ||--o{ COLLECTION : owns
    USER {
        int userID
        string username
        string email
        string password
    }
    COLLECTION ||--o{ COLLECTION-MOVIE : includes
    COLLECTION {
        int collectionID
        string collectionName
    }
    MOVIE ||--o{ COLLECTION-MOVIE : part of
    MOVIE {
        int movieID
        string title
        int releaseYear
        string genre
        string director
        string description
        float rating
    }
    COLLECTION-MOVIE {
        int collectionID
        int movieID
        string addedDate
    }
    %% User Actions
    USER ||--o{ ADD-MOVIE : "adds to collection"
    USER ||--o{ DELETE-MOVIE : "removes from collection"
    USER ||--o{ SEARCH-MOVIE : "searches in collection"
    USER ||--o{ EDIT-MOVIE : "edits in collection"

    %% Add Movie Route
    ADD-MOVIE {
        int collectionID
        string title
        int releaseYear
        string genre
        string director
        string description
        float rating
    }

    %% Delete Movie Route
    DELETE-MOVIE {
        int collectionID
        int movieID
    }

    %% Search Movie Route
    SEARCH-MOVIE {
        int collectionID
        string filters
        string searchTerm
    }

    %% Edit Movie Route
    EDIT-MOVIE {
        int collectionID
        int movieID
        string newTitle
        int newReleaseYear
        string newGenre
        string newDirector
        string newDescription
        float newRating
    }

