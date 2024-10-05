-- Active: 1728104859736@@127.0.0.1@5434@postgres
CREATE SCHEMA IF NOT EXISTS dibimbing;

CREATE TABLE dibimbing.users (id SERIAL, nama VARCHAR(100));

INSERT INTO
    dibimbing.users (nama)
VALUES ('john'),
    ('paul'),
    ('maya'),
    ('alex'),
    ('tony'),
    ('brian'),
    ('stephen');

SELECT * FROM dibimbing.users