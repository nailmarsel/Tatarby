CREATE TABLE Author (
	AuthorID SERIAL PRIMARY KEY,
	Aname VARCHAR(500),
	Asurname VARCHAR(500),
	Amiddlename VARCHAR(500),
	DateOfBirth DATE,
	Astyle VARCHAR(500)
);

CREATE TABLE Book (
	BookID SERIAL PRIMARY KEY,
	BookName VARCHAR(500) NOT NULL UNIQUE,
	Description VARCHAR(8000),
	Conent VARCHAR(500) NOT NULL UNIQUE,
	AuthorID INT,
	YearOFWriting INT,
	CONSTRAINT fk_author_id FOREIGN KEY (AuthorID) REFERENCES Author (AuthorID)
);

CREATE TABLE ReadBook (
	UserID INT,
	BookID INT,
	CONSTRAINT fk_user_id FOREIGN KEY (UserID) REFERENCES Users (UserID),
	CONSTRAINT fk_book_id FOREIGN KEY (BookID) REFERENCES Book (BookID)
);

CREATE TABLE SelectedBook (
	UserID INT,
	BookID INT,
	CONSTRAINT fk_user_id_sel FOREIGN KEY (UserID) REFERENCES Users (UserID),
	CONSTRAINT fk_book_id_sel FOREIGN KEY (BookID) REFERENCES Book (BookID)
);

CREATE TABLE CurrentBook (
	UserID INT,
	BookID INT,
	PageNumber INT,
	CONSTRAINT fk_user_id_cur FOREIGN KEY (UserID) REFERENCES Users (UserID),
	CONSTRAINT fk_book_id_cur FOREIGN KEY (BookID) REFERENCES Book (BookID)
);

CREATE TABLE BookVector (
	BookID INT,
	Component1 DOUBLE PRECISION,
	Component2 DOUBLE PRECISION,
	Component3 DOUBLE PRECISION,
	Component4 DOUBLE PRECISION,
	Component5 DOUBLE PRECISION,
	Component6 DOUBLE PRECISION,
	Component7 DOUBLE PRECISION,
	Component8 DOUBLE PRECISION,
	Component9 DOUBLE PRECISION,
	Component10 DOUBLE PRECISION,
	Component11 DOUBLE PRECISION,
	Component12 DOUBLE PRECISION,
	Component13 DOUBLE PRECISION,
	Component14 DOUBLE PRECISION,
	Component15 DOUBLE PRECISION,
	Component16 DOUBLE PRECISION,
	CONSTRAINT fk_book_id_vec FOREIGN KEY (BookID) REFERENCES Book (BookID)
);

CREATE TABLE BookMark(
	BookID INT,
	MarkOfBook INT,
	BookFeedback INT,
	CONSTRAINT fk_book_id_mark FOREIGN KEY (BookID) REFERENCES Book (BookID)
);

CREATE TABLE TranslationMark(
        TranslationMarkID SERIAL PRIMARY KEY,
	BookID INT,
	MarkOfTranslation INT,
	TranslationFeedback INT,
	CONSTRAINT fk_book_id_trans_mark FOREIGN KEY (BookID) REFERENCES Book (BookID)
);

CREATE TABLE TatarTranslation(
	BookID INT,
	BookTatarTranslation VARCHAR(500),
        TatPage INT,
        TatAudioId VARCHAR(500),
	CONSTRAINT fk_book_id_trans FOREIGN KEY (BookID) REFERENCES Book (BookID)
);
