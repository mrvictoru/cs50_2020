SELECT name FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies on movies.id = stars.movie_id
where movies.title = "Toy Story";