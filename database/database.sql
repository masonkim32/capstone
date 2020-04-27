--
-- PostgreSQL database dump
--

-- Dumped from database version 11.6 (Debian 11.6-1.pgdg90+1)
-- Dumped by pg_dump version 11.6 (Debian 11.6-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: actors; Type: TABLE; Schema: public; Owner: castingagency
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying(80) NOT NULL,
    age integer,
    gender character varying
);


ALTER TABLE public.actors OWNER TO castingagency;

--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: castingagency
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO castingagency;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: castingagency
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- Name: movies; Type: TABLE; Schema: public; Owner: castingagency
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying(80) NOT NULL,
    release_date date
);


ALTER TABLE public.movies OWNER TO castingagency;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: castingagency
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO castingagency;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: castingagency
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: castingagency
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: castingagency
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: castingagency
--

COPY public.actors (id, name, age, gender) FROM stdin;
1	Morgan Freeman	83	male
2	Leonardo DiCaprio	46	male
3	Natalie Portman	39	female
4	Anne Hathaway	38	female
5	Robert De Niro	77	male
6	Diane Keaton	74	female
7	Keira Knightley	35	female
8	Cillian Murphy	44	male
9	Jack Nicholson	83	male
10	Tom Hardy	43	male
11	Mark Ruffalo	53	male
12	Elle Fanning	22	female
13	Scarlett Johansson	36	female
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: castingagency
--

COPY public.movies (id, title, release_date) FROM stdin;
1	The High Note	2020-05-08
2	The Painted Bird	2020-07-17
3	Mulan	2020-07-24
4	The Avengers	2012-05-04
5	City of God	2004-02-13
6	Gladiator	2004-05-05
7	Avatar3	2023-12-22
8	Mission: Impossible 8	2022-08-05
9	Uncharted	2021-10-08
10	The Matrix 	1999-03-31
11	Saving Private Ryan	1998-07-24
12	Forrest Gump	1994-07-06
\.


--
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: castingagency
--

SELECT pg_catalog.setval('public.actors_id_seq', 15, true);


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: castingagency
--

SELECT pg_catalog.setval('public.movies_id_seq', 13, true);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: castingagency
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: castingagency
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

