-- Init.sql

-- Dumped by pg_dump version 9.6.3
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SELECT 'CREATE DATABASE omdb'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'omdb')\gexec

\c omdb

-- Rest of init.sql script here

-- create the 'movies' table
-- CREATE TABLE movies (
--   id BIGINT PRIMARY KEY,
--   name TEXT,
--   parent_id BIGINT,
--   date DATE,
--   series_id BIGINT,
--   kind TEXT,
--   runtime INT,
--   budget NUMERIC,
--   revenue NUMERIC,
--   homepage TEXT,
--   vote_average NUMERIC,
--   votes_count BIGINT
-- );

CREATE TABLE movies (
  id bigint UNIQUE,
  name text,
  parent_id bigint,
  date date,
  series_id bigint,
  kind text,
  -- from all_*
  runtime int,
  budget numeric,
  revenue numeric,
  homepage text,
  -- from movie_details
  vote_average numeric,
  votes_count bigint -- from votes
);


-- create the 'users' table
CREATE TABLE public.users (
	id varchar NULL,
	"name" varchar NULL
);

-- create the 'bookings' table
CREATE TABLE public.bookings (
	id serial4 NOT NULL,
	user_id varchar NULL,
	movie_id int4 NULL,
	CONSTRAINT bookings_pkey PRIMARY KEY (id)
);

-- insert data into the 'movies' table
-- COPY movies (id, name, parent_id, date, series_id, kind, runtime, budget, revenue, homepage, vote_average, votes_count) FROM stdin;
-- 1	'Movie 1'	\N	'2023-05-25'	\N	'movie'	120	1000000	5000000	'http://www.movie1.com'	7.5	10000
-- 2	'Movie 2'	\N	'2023-05-26'	\N	'movie'	130	2000000	6000000	'http://www.movie2.com'	8.0	20000
-- \.
COPY movies (id, name, parent_id, date, series_id, kind, runtime, budget, revenue, homepage, vote_average, votes_count) FROM '/data/movies_202305250226.csv' WITH (FORMAT csv, HEADER true);
