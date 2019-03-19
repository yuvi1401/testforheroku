drop database if exists ssc;
create database ssc;

\c ssc;

create table users (
	user_id SERIAL PRIMARY KEY,
	username VARCHAR,
	password VARCHAR );

create table workspaces (
	workspace_id SERIAL PRIMARY KEY,
	name VARCHAR);

create table workspace_users (
	user_id INT REFERENCES users(user_id),
	workspace_id INT REFERENCES workspaces(workspace_id),
	is_admin BOOLEAN);

create table workspace_files (
	workspace_id INT REFERENCES workspaces(workspace_id),
	file_name VARCHAR(42),
	audio_key VARCHAR);

create table invites (
	invite_id SERIAL PRIMARY KEY,
	user_id INT REFERENCES users(user_id),
	workspace_id INT REFERENCES workspaces(workspace_id),
	invited_by_id INT REFERENCES users(user_id));



insert into users (username, password)
values
('Coddzilla', 123),
('Shruminator', 456),
('OllieOllie123', 789),
('Willmaaaa', 101),
('RajAgainstTheMachine', 112);

insert into workspaces (name)
values
('workspace1'),
('workspace2'),
('workspace3'),
('workspace4'),
('workspace5');

insert into workspace_users (user_id, workspace_id, is_admin)
values
(1, 1, false),
(2, 1, true),
(3, 2, false),
(4, 2, true),
(5, 3, true);


insert into workspace_files (workspace_id, file_name, audio_key)
values
(1, 'file1', 234567),
(2, 'file2', 987634),
(3, 'file3', 029685);

insert into invites (invite_id, user_id, workspace_id, invited_by_id)
values
(1, 1, 2, 2),
(2, 2, 1, 2),
(3, 3, 1, 2);
