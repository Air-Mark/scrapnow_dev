--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3 (Debian 10.3-1.pgdg90+1)
-- Dumped by pg_dump version 10.3 (Debian 10.3-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: scrapnow
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO scrapnow;

--
-- Name: article; Type: TABLE; Schema: public; Owner: scrapnow
--

CREATE TABLE public.article (
    id integer NOT NULL,
    url text NOT NULL,
    title text NOT NULL,
    short_description text NOT NULL,
    datetime timestamp without time zone NOT NULL,
    body text,
    status text NOT NULL,
    error text
);


ALTER TABLE public.article OWNER TO scrapnow;

--
-- Name: article_id_seq; Type: SEQUENCE; Schema: public; Owner: scrapnow
--

CREATE SEQUENCE public.article_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.article_id_seq OWNER TO scrapnow;

--
-- Name: article_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: scrapnow
--

ALTER SEQUENCE public.article_id_seq OWNED BY public.article.id;


--
-- Name: scrap_document_fields; Type: TABLE; Schema: public; Owner: scrapnow
--

CREATE TABLE public.scrap_document_fields (
    id integer NOT NULL,
    scrap_task_id integer NOT NULL,
    name text NOT NULL,
    xpath text NOT NULL
);


ALTER TABLE public.scrap_document_fields OWNER TO scrapnow;

--
-- Name: scrap_document_fields_id_seq; Type: SEQUENCE; Schema: public; Owner: scrapnow
--

CREATE SEQUENCE public.scrap_document_fields_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.scrap_document_fields_id_seq OWNER TO scrapnow;

--
-- Name: scrap_document_fields_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: scrapnow
--

ALTER SEQUENCE public.scrap_document_fields_id_seq OWNED BY public.scrap_document_fields.id;


--
-- Name: scrap_task; Type: TABLE; Schema: public; Owner: scrapnow
--

CREATE TABLE public.scrap_task (
    id integer NOT NULL,
    handler text,
    url text NOT NULL,
    status text NOT NULL,
    result json,
    error text
);


ALTER TABLE public.scrap_task OWNER TO scrapnow;

--
-- Name: scrap_task_id_seq; Type: SEQUENCE; Schema: public; Owner: scrapnow
--

CREATE SEQUENCE public.scrap_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.scrap_task_id_seq OWNER TO scrapnow;

--
-- Name: scrap_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: scrapnow
--

ALTER SEQUENCE public.scrap_task_id_seq OWNED BY public.scrap_task.id;


--
-- Name: article id; Type: DEFAULT; Schema: public; Owner: scrapnow
--

ALTER TABLE ONLY public.article ALTER COLUMN id SET DEFAULT nextval('public.article_id_seq'::regclass);


--
-- Name: scrap_document_fields id; Type: DEFAULT; Schema: public; Owner: scrapnow
--

ALTER TABLE ONLY public.scrap_document_fields ALTER COLUMN id SET DEFAULT nextval('public.scrap_document_fields_id_seq'::regclass);


--
-- Name: scrap_task id; Type: DEFAULT; Schema: public; Owner: scrapnow
--

ALTER TABLE ONLY public.scrap_task ALTER COLUMN id SET DEFAULT nextval('public.scrap_task_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: scrapnow
--

COPY public.alembic_version (version_num) FROM stdin;
2540e3b1f0bd
\.


--
-- Data for Name: article; Type: TABLE DATA; Schema: public; Owner: scrapnow
--

COPY public.article (id, url, title, short_description, datetime, body, status, error) FROM stdin;
\.


--
-- Data for Name: scrap_document_fields; Type: TABLE DATA; Schema: public; Owner: scrapnow
--

COPY public.scrap_document_fields (id, scrap_task_id, name, xpath) FROM stdin;
\.


--
-- Data for Name: scrap_task; Type: TABLE DATA; Schema: public; Owner: scrapnow
--

COPY public.scrap_task (id, handler, url, status, result, error) FROM stdin;
\.


--
-- Name: article_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scrapnow
--

SELECT pg_catalog.setval('public.article_id_seq', 1, false);


--
-- Name: scrap_document_fields_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scrapnow
--

SELECT pg_catalog.setval('public.scrap_document_fields_id_seq', 1, false);


--
-- Name: scrap_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scrapnow
--

SELECT pg_catalog.setval('public.scrap_task_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: scrapnow
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: article pk__article; Type: CONSTRAINT; Schema: public; Owner: scrapnow
--

ALTER TABLE ONLY public.article
    ADD CONSTRAINT pk__article PRIMARY KEY (id);


--
-- Name: scrap_document_fields pk__scrap_document_fields; Type: CONSTRAINT; Schema: public; Owner: scrapnow
--

ALTER TABLE ONLY public.scrap_document_fields
    ADD CONSTRAINT pk__scrap_document_fields PRIMARY KEY (id);


--
-- Name: scrap_task pk__scrap_task; Type: CONSTRAINT; Schema: public; Owner: scrapnow
--

ALTER TABLE ONLY public.scrap_task
    ADD CONSTRAINT pk__scrap_task PRIMARY KEY (id);


--
-- Name: article uq__article__url; Type: CONSTRAINT; Schema: public; Owner: scrapnow
--

ALTER TABLE ONLY public.article
    ADD CONSTRAINT uq__article__url UNIQUE (url);


--
-- Name: scrap_document_fields fk__scrap_document_fields__scrap_task_id__scrap_task; Type: FK CONSTRAINT; Schema: public; Owner: scrapnow
--

ALTER TABLE ONLY public.scrap_document_fields
    ADD CONSTRAINT fk__scrap_document_fields__scrap_task_id__scrap_task FOREIGN KEY (scrap_task_id) REFERENCES public.scrap_task(id);


--
-- PostgreSQL database dump complete
--