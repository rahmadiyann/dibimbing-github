CREATE TABLE IF NOT EXISTS dibimbing_songs (
    song_id INT PRIMARY KEY,
    title VARCHAR(255),
    artist_id INT,
    album_id INT,
    duration INT,
    release_date DATE,
    genre_id INT
);

CREATE TABLE IF NOT EXISTS dibimbing_albums (
    album_id INT PRIMARY KEY,
    title VARCHAR(255),
    artist_id INT,
    release_date DATE
);

CREATE TABLE IF NOT EXISTS dibimbing_artists (
    artist_id INT PRIMARY KEY,
    name VARCHAR(255),
    country VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dibimbing_genres (
    genre_id INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dibimbing_playlists (
    playlist_id INT PRIMARY KEY,
    title VARCHAR(255),
    description VARCHAR(255),
    created_at TIMESTAMP
);

TRUNCATE TABLE dibimbing_songs;

TRUNCATE TABLE dibimbing_albums;

TRUNCATE TABLE dibimbing_artists;

TRUNCATE TABLE dibimbing_genres;

TRUNCATE TABLE dibimbing_playlists;

INSERT INTO
    dibimbing_songs (
        song_id,
        title,
        artist_id,
        album_id,
        duration,
        release_date,
        genre_id
    )
VALUES (
        1,
        'Song 1',
        1,
        1,
        200,
        '2022-01-01',
        1
    ),
    (
        2,
        'Song 2',
        2,
        2,
        250,
        '2022-02-01',
        2
    ),
    (
        3,
        'Song 3',
        3,
        3,
        300,
        '2022-03-01',
        3
    ),
    (
        4,
        'Song 4',
        4,
        4,
        350,
        '2022-04-01',
        4
    ),
    (
        5,
        'Song 5',
        5,
        5,
        400,
        '2022-05-01',
        5
    );

INSERT INTO
    dibimbing_albums (
        album_id,
        title,
        artist_id,
        release_date
    )
VALUES (1, 'Album 1', 1, '2022-01-01'),
    (2, 'Album 2', 2, '2022-02-01'),
    (3, 'Album 3', 3, '2022-03-01'),
    (4, 'Album 4', 4, '2022-04-01'),
    (5, 'Album 5', 5, '2022-05-01');

INSERT INTO
    dibimbing_artists (artist_id, name, country)
VALUES (1, 'Artist 1', 'Country 1'),
    (2, 'Artist 2', 'Country 2'),
    (3, 'Artist 3', 'Country 3'),
    (4, 'Artist 4', 'Country 4'),
    (5, 'Artist 5', 'Country 5');

INSERT INTO
    dibimbing_genres (genre_id, name)
VALUES (1, 'Genre 1'),
    (2, 'Genre 2'),
    (3, 'Genre 3'),
    (4, 'Genre 4'),
    (5, 'Genre 5');

INSERT INTO
    dibimbing_playlists (
        playlist_id,
        title,
        description,
        created_at
    )
VALUES (
        1,
        'Playlist 1',
        'Description 1',
        '2022-01-01 00:00:00'
    ),
    (
        2,
        'Playlist 2',
        'Description 2',
        '2022-02-01 00:00:00'
    ),
    (
        3,
        'Playlist 3',
        'Description 3',
        '2022-03-01 00:00:00'
    ),
    (
        4,
        'Playlist 4',
        'Description 4',
        '2022-04-01 00:00:00'
    ),
    (
        5,
        'Playlist 5',
        'Description 5',
        '2022-05-01 00:00:00'
    );