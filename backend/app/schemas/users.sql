create table users(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    difficulty INTEGER NOT NULL,
    active BOOLEAN NOT NULL
);
