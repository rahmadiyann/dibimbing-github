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