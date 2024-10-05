CREATE DATABASE IF NOT EXISTS dibimbing;

CREATE TABLE dibimbing.users (id INT, nama VARCHAR(100));

INSERT INTO
    dibimbing.users (id, nama)
VALUES (1, 'john'),
    (2, 'paul'),
    (3, 'maya'),
    (4, 'alex'),
    (5, 'tony'),
    (6, 'brian'),
    (7, 'stephen');

SELECT * FROM dibimbing.users;