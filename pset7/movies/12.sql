SELECT title FROM movies

WHERE id IN (
SELECT movie_id FROM stars WHERE stars.person_id =
(SELECT people.id FROM people where name = "Johnny Depp")

AND id IN (
SELECT movie_id FROM stars WHERE stars.person_id =
(SELECT people.id FROM people where name = "Helena Bonham Carter")));