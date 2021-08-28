create database if not exists netflix_movies;
use netflix_movies;

CREATE EXTERNAL TABLE IF NOT EXISTS rates_ext(
 movieId BIGINT,
 count BIGINT,
 sumRate BIGINT)
 ROW FORMAT DELIMITED
 FIELDS TERMINATED BY '\t'
 STORED AS TEXTFILE
 location '/user/${username}/output_mr3';

CREATE TABLE IF NOT EXISTS rates_orc(
 movieId BIGINT,
 count BIGINT,
 sumRate BIGINT)
 STORED AS ORC;

INSERT OVERWRITE TABLE rates_orc
SELECT * FROM rates_ext
WHERE movieId IS NOT NULL;


CREATE EXTERNAL TABLE IF NOT EXISTS movies_ext(
 movieId BIGINT,
 year BIGINT,
 name STRING)
 ROW FORMAT DELIMITED
 FIELDS TERMINATED BY ','
 STORED AS TEXTFILE
 location '/user/${username}/input/datasource4';

CREATE TABLE IF NOT EXISTS movies_orc(
 movieId BIGINT,
 year BIGINT,
 name STRING)
 STORED AS ORC;

INSERT OVERWRITE TABLE movies_orc
SELECT * FROM movies_ext
WHERE movieId IS NOT NULL;

add jar hdfs:///user/${username}/project_files/hive-hcatalog-core-3.1.2.jar;

CREATE EXTERNAL TABLE json_table(
   tytul_filmu string,
   rok_produkcji BIGINT,
   srednia_ocena DOUBLE)
ROW FORMAT SERDE
  'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION '/user/${username}/output6';

INSERT OVERWRITE TABLE json_table
SELECT
    ranked_movies.tytul_filmu as tytul_filmu,
    ranked_movies.rok_produkcji as rok_produkcji,
    ranked_movies.srednia_ocena as srednia_ocena
FROM (
    SELECT
        movies.tytul_filmu,
        movies.rok_produkcji,
        movies.srednia_ocena,
        rank() over (PARTITION BY movies.rok_produkcji ORDER BY movies.srednia_ocena DESC) as rank
    FROM (
        SELECT
            m.name as tytul_filmu,
            m.year as rok_produkcji,
            (r.sumRate/r.count) as srednia_ocena
        FROM movies_orc m inner join rates_orc r on m.movieId = r.movieId
        WHERE r.count > 1000
    ) as movies
) as ranked_movies
WHERE ranked_movies.rank < 4;

DROP TABLE rates_ext;
DROP TABLE rates_orc;
DROP TABLE movies_ext;
DROP TABLE movies_orc;
DROP TABLE json_table;
