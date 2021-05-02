DROP TABLE actor CASCADE CONSTRAINTS;
DROP TABLE acts_movie CASCADE CONSTRAINTS;
DROP TABLE acts_tv CASCADE CONSTRAINTS;
DROP TABLE director CASCADE CONSTRAINTS;
DROP TABLE directs_movie CASCADE CONSTRAINTS;
DROP TABLE directs_tv CASCADE CONSTRAINTS;
DROP TABLE writer CASCADE CONSTRAINTS;
DROP TABLE writes_movie CASCADE CONSTRAINTS;
DROP TABLE writes_tv CASCADE CONSTRAINTS;
DROP TABLE movie CASCADE CONSTRAINTS;
DROP TABLE tv_show CASCADE CONSTRAINTS;
DROP TABLE review CASCADE CONSTRAINTS;
DROP TABLE season CASCADE CONSTRAINTS;
DROP TABLE known_for CASCADE CONSTRAINTS;
DROP TABLE plot_keywords CASCADE CONSTRAINTS;
DROP TABLE genre CASCADE CONSTRAINTS;

CREATE TABLE actor (
	imdb_id 		VARCHAR2(9) CONSTRAINT actor_imdb_id_pk PRIMARY KEY,
	w_id 			VARCHAR2(9), 
	d_id 			VARCHAR2(9), 
	f_name 			VARCHAR2(15), 
	l_name 			VARCHAR2(15), 
	birthdate 		DATE, 
	city 			VARCHAR2(15), 
	country			VARCHAR2(15), 
	starmeter_rank 	NUMBER(4)
);

CREATE TABLE acts_movie (
	a_id 			VARCHAR2(9),
	movie_id 		VARCHAR2(9),
	CONSTRAINT actor_in_movie_pk PRIMARY KEY(a_id, movie_id)
);

CREATE TABLE acts_tv (
	a_id 			VARCHAR2(9),
	tv_show_id 		VARCHAR2(9),
	CONSTRAINT actor_in_tv_pk PRIMARY KEY(a_id, tv_show_id)
);

CREATE TABLE director ( 
	imdb_id 		VARCHAR2(9) CONSTRAINT director_imdb_id_pk PRIMARY KEY,
	a_id 			VARCHAR2(9),
	w_id 			VARCHAR2(9),
	f_name 			VARCHAR2(15),
	l_name 			VARCHAR2(15),
	birthdate 		DATE,
	city 			VARCHAR2(15),
	country 		VARCHAR2(15),
	starmeter_rank 	NUMBER(4)
);

CREATE TABLE directs_movie (
	d_id 			VARCHAR2(9),
	movie_id 		VARCHAR2(9),
	CONSTRAINT director_in_movie_pk PRIMARY KEY(d_id, movie_id)
);

CREATE TABLE directs_tv (
	d_id 			VARCHAR2(9),
	tv_show_id 			VARCHAR2(9),
	CONSTRAINT director_in_tv_pk PRIMARY KEY(d_id, tv_show_id)
);


CREATE TABLE writer ( 
	imdb_id 		VARCHAR2(9) CONSTRAINT writer_imdb_id_pk PRIMARY KEY,
	a_id 			VARCHAR2(9),
	d_id			VARCHAR2(9),
	f_name 			VARCHAR2(15),
	l_name 			VARCHAR2(15),
	birthdate 		DATE,
	city 			VARCHAR2(15),
	country 		VARCHAR2(15),
	starmeter_rank 	NUMBER(4)
);

CREATE TABLE writes_movie (
	w_id 			VARCHAR2(9),
	movie_id 		VARCHAR2(9),
	CONSTRAINT writer_in_movie_pk PRIMARY KEY(w_id, movie_id)
);

CREATE TABLE writes_tv (
	w_id 			VARCHAR2(9),
	tv_show_id 		VARCHAR2(9),
	CONSTRAINT writer_in_tv_pk PRIMARY KEY(w_id, tv_show_id)
);

CREATE TABLE movie ( 
	imdb_id 		VARCHAR2(9) CONSTRAINT movie_id_pk PRIMARY KEY,
	title 			VARCHAR2(25),
	runtime 		NUMBER(3),
	release_date 	DATE
);

CREATE TABLE tv_show ( 
	imdb_id 		VARCHAR2(9) CONSTRAINT tv_show_id_pk PRIMARY KEY,
	title 			VARCHAR2(25)
);

CREATE TABLE review (
	username 		VARCHAR2(15),
	movie_id 		VARCHAR2(9),
	publish_date 	DATE,
	content 		VARCHAR2(4000),
	stars 			NUMBER(2),
	num_votes 		NUMBER(3),
	CONSTRAINT review_username_movie_id_pk PRIMARY KEY(username, movie_id)
);

CREATE TABLE season ( 
	tv_show_id		VARCHAR2(9),
	title 			VARCHAR2(20),
	CONSTRAINT season_imdb_id_ssn_title_pk PRIMARY KEY(tv_show_id, title)
);

CREATE TABLE known_for ( 
	actor_id 		VARCHAR2(9),
	prod_title	 	VARCHAR2(25),
	CONSTRAINT known_for_pk PRIMARY KEY(actor_id, prod_title)
);

CREATE TABLE plot_keywords ( 
	movie_id		VARCHAR2(9),
	keyword 		VARCHAR2(15),
	CONSTRAINT plot_keywords_keyword_pk PRIMARY KEY(movie_id, keyword)
);

CREATE TABLE genre (
	tv_show_id 		VARCHAR2(9),
	genre 			VARCHAR2(15),
	CONSTRAINT genre_tv_show_id_genre_pk PRIMARY KEY(tv_show_id, genre)
);

ALTER TABLE actor
ADD CONSTRAINT actor_is_writer_id_fk FOREIGN KEY (w_id)
	REFERENCES writer(imdb_id);

ALTER TABLE actor
ADD CONSTRAINT actor_is_director_id_fk FOREIGN KEY (d_id)
	REFERENCES director(imdb_id);

ALTER TABLE writer
ADD CONSTRAINT writer_is_actor_id_fk FOREIGN KEY (a_id)
	REFERENCES actor(imdb_id);
	
ALTER TABLE writer
ADD CONSTRAINT writer_is_director_id_fk FOREIGN KEY (d_id)
	REFERENCES director(imdb_id);

ALTER TABLE director
ADD CONSTRAINT director_is_actor_id_fk FOREIGN KEY (a_id)
	REFERENCES actor(imdb_id);

ALTER TABLE director
ADD CONSTRAINT director_is_writer_id_fk FOREIGN KEY (w_id)
	REFERENCES writer(imdb_id);


ALTER TABLE acts_movie
ADD CONSTRAINT acts_movie_actor_id_fk FOREIGN KEY (a_id)
	REFERENCES actor(imdb_id);

ALTER TABLE acts_movie
ADD CONSTRAINT acts_movie_movie_id_fk FOREIGN KEY (movie_id)
	REFERENCES movie(imdb_id);

ALTER TABLE acts_tv
ADD CONSTRAINT acts_tv_actor_id_fk FOREIGN KEY (a_id)
	REFERENCES actor(imdb_id);

ALTER TABLE acts_tv
ADD CONSTRAINT acts_tv_tv_show_id_fk FOREIGN KEY (tv_show_id)
	REFERENCES tv_show(imdb_id);


ALTER TABLE writes_movie
ADD CONSTRAINT writes_movie_writer_id_fk FOREIGN KEY (w_id)
	REFERENCES writer(imdb_id);

ALTER TABLE writes_movie
ADD CONSTRAINT writes_movie_movie_id_fk FOREIGN KEY (movie_id)
	REFERENCES movie(imdb_id);

ALTER TABLE writes_tv
ADD CONSTRAINT writes_tv_writer_id_fk FOREIGN KEY (w_id)
	REFERENCES tv_show(imdb_id);

ALTER TABLE writes_tv
ADD CONSTRAINT writes_tv_tv_show_id_fk FOREIGN KEY (tv_show_id)
	REFERENCES tv_show(imdb_id);


ALTER TABLE directs_movie
ADD CONSTRAINT directs_movie_director_id_fk FOREIGN KEY (d_id)
	REFERENCES director(imdb_id);

ALTER TABLE directs_movie
ADD CONSTRAINT directs_movie_movie_id_fk FOREIGN KEY (movie_id)
	REFERENCES director(imdb_id);

ALTER TABLE directs_tv
ADD CONSTRAINT directs_tv_director_id_fk FOREIGN KEY (d_id)
	REFERENCES director(imdb_id);

ALTER TABLE directs_tv
ADD CONSTRAINT directs_tv_tv_show_id_fk FOREIGN KEY (tv_show_id)
	REFERENCES tv_show(imdb_id);


ALTER TABLE review
ADD CONSTRAINT review_movie_id_fk FOREIGN KEY (movie_id)
	REFERENCES movie(imdb_id);

ALTER TABLE known_for
ADD CONSTRAINT known_for_actor_id_fk FOREIGN KEY (actor_id)
	REFERENCES actor(imdb_id);

ALTER TABLE plot_keywords
ADD CONSTRAINT plot_keywords_movie_id_fk FOREIGN KEY (movie_id)
	REFERENCES movie(imdb_id);

ALTER TABLE genre
ADD CONSTRAINT genre_tv_show_id_fk FOREIGN KEY (tv_show_id)
	REFERENCES tv_show(imdb_id);

ALTER TABLE season
ADD CONSTRAINT season_tv_show_id_fk FOREIGN KEY (tv_show_id)
	REFERENCES tv_show(imdb_id);
