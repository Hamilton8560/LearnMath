CREATE TABLE users_questions(
    userID INT NOT NULL,
    questionID INT NOT NULL,
    correct BOOLEAN NOT NULL,
    PRIMARY KEY (userID, questionID),
    FOREIGN KEY (userID) REFERENCES users(ID) ON DELETE CASCADE,
    FOREIGN KEY (questionID) REFERENCES questions(ID) ON DELETE CASCADE
);