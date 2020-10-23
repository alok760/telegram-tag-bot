CREATE TABLE groups (
	group_name TEXT NOT NULL,
	description TEXT
);


CREATE TABLE members (
	group_name TEXT NOT NULL,
	member_id TEXT NOT NULL
);
