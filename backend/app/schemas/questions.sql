CREATE TABLE questions(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    level INT NOT NULL,
    operation TEXT NOT NULL,
    problem TEXT NOT NULL UNIQUE,
    options TEXT NOT NULL,
    answer TEXT NOT NULL
);