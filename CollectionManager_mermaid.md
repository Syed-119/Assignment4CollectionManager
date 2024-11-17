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

