--1. Identify the top 10 customers and their email so we can reward them
SELECT c.customer_id, CONCAT(first_name,' ',last_name) AS full_name, c.email, SUM(p.amount) AS total_amount_paid
FROM customer c
INNER JOIN payment p 
ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY total_amount_paid DESC
LIMIT 10;

--2. Identify the bottom 10 customers and their emails
SELECT c.customer_id, CONCAT(first_name,' ',last_name) AS full_name, c.email, SUM(p.amount) AS total_amount_paid
FROM customer c
INNER JOIN payment p 
ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY total_amount_paid ASC
LIMIT 10;

--3. What are the most profitable movie genres (ratings)?
SELECT c.name AS genre_name, COUNT(r.customer_id) AS total_rent, SUM(p.amount) AS total_amount_paid
FROM category c
INNER JOIN film_category fc 
ON c.category_id = fc.category_id
INNER JOIN film f
ON fc.film_id = f.film_id
INNER JOIN inventory i 
ON f.film_id = i.film_id
INNER JOIN rental r
ON i.inventory_id = r.inventory_id 
INNER JOIN payment p 
ON p.rental_id = r.rental_id
GROUP BY genre_name
ORDER BY total_amount_paid DESC
--LIMIT 1;

--4. How many rented movies were returned late, early, and on time?
WITH tempo AS (
	SELECT *, date_part ('day', return_date - rental_date) AS date_difference
	FROM rental),

tempo2 AS (
	SELECT rental_duration, date_difference,
	CASE
		WHEN rental_duration > date_difference THEN 'returned early'
		WHEN rental_duration = date_difference THEN 'returned on time'
		ELSE 'returned late'
	END AS status_of_return
	FROM film f
	INNER JOIN inventory i
	ON f.film_id = i.film_id 
	INNER JOIN tempo t
	ON i.inventory_id = t.inventory_id)

SELECT status_of_return, COUNT(*) AS total_of_rental
FROM tempo2
GROUP BY 1
ORDER BY 2 DESC;

--5. What is the customer base in the countries where we have a presence?
SELECT co.country, COUNT(DISTINCT c.customer_id) AS total_customer
FROM country co
INNER JOIN city ci
ON co.country_id = ci.country_id 
INNER JOIN address a
ON ci.city_id = a.city_id
INNER JOIN customer c
ON a.address_id = c.address_id
GROUP BY co.country
ORDER BY total_customer DESC;

--6. Which country is the most profitable for the business?
SELECT co.country AS country_name, COUNT(DISTINCT p.customer_id) AS total_rent, SUM(p.amount) AS total_amount_paid
FROM country co
INNER JOIN city ci 
ON co.country_id = ci.country_id
INNER JOIN address a
ON ci.city_id = a.city_id
INNER JOIN customer c 
ON a.address_id = c.address_id
INNER JOIN payment p
ON c.customer_id = p.customer_id 
GROUP BY country_name
ORDER BY total_amount_paid DESC
LIMIT 1;

--7. What is the average rental rate per movie genre (rating)?
SELECT c.name AS genre_name, AVG(rental_rate) AS average_rental_rate
FROM category c
INNER JOIN film_category fc 
ON c.category_id = fc.category_id
INNER JOIN film f
ON fc.film_id = f.film_id
GROUP BY genre_name
ORDER BY average_rental_rate DESC;