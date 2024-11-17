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
    USER ||--o{ ADD-MOVIE : "can add movies"
    USER ||--o{ DELETE-MOVIE : "can delete movies"
    USER ||--o{ SEARCH-MOVIE : "can search movies"
    USER ||--o{ EDIT-MOVIE : "can edit movies"

    %% Add Movie Route
    ADD-MOVIE {
        string title
        int releaseYear
        string genre
        string director
        string description
        float rating
    }

    %% Delete Movie Route
    DELETE-MOVIE {
        int movieID
    }

    %% Search Movie Route
    SEARCH-MOVIE {
        string filters
        string searchTerm
    }

    %% Edit Movie Route
    EDIT-MOVIE {
        int movieID
        string newTitle
        int newReleaseYear
        string newGenre
        string newDirector
        string newDescription
        float newRating
    }
