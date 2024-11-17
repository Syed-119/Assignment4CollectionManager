erDiagram
    USER {
        int user_id PK
        string username
        string email
        string password
    }
    
    MOVIE {
        int movie_id PK
        string title
        int release_year
        string genre
        string director
        string description
        float rating
    }
    
    COLLECTION {
        int collection_id PK
        string collection_name
        int user_id FK
    }

    COLLECTION_MOVIE {
        int collection_id FK
        int movie_id FK
        string added_date
    }

    USER ||--o{ COLLECTION : "owns"
    COLLECTION ||--o{ COLLECTION_MOVIE : "contains"
    MOVIE ||--o{ COLLECTION_MOVIE : "part of"
