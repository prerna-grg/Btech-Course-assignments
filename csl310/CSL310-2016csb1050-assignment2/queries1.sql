/*
Average sales grouped by language, sum of amounts i.e. including earnings from all sources : late returns, damage cost etc.
*/
SELECT name,sales FROM language INNER JOIN (SELECT language_id , AVG(amount) as sales FROM film INNER JOIN (SELECT film_id , rental_id , amount FROM inventory INNER JOIN (SELECT payment.rental_id , amount , inventory_id FROM payment INNER JOIN rental ON rental.rental_id = payment.rental_id)alias1 ON alias1.inventory_id = inventory.inventory_id)alias2 ON film.film_id = alias2.film_id GROUP BY language_id)alias3 ON alias3.language_id = language.language_id;

/*
Average sales grouped by film category, sum of amounts i.e. including earnings from all sources : late returns, damage cost etc.
*/
SELECT name , sales FROM category INNER JOIN (SELECT category_id , AVG(amount) as sales FROM film_category INNER JOIN (SELECT film_id , rental_id , amount FROM inventory INNER JOIN (SELECT payment.rental_id , amount , inventory_id FROM payment INNER JOIN rental ON rental.rental_id = payment.rental_id)alias1 ON alias1.inventory_id = inventory.inventory_id)alias2 ON film_category.film_id = alias2.film_id GROUP BY category_id)alias3 ON alias3.category_id = category.category_id;

/*
Average sales grouped by film rating, sum of amounts i.e. including earnings from all sources : late returns, damage cost etc.
*/
SELECT rating , AVG(amount) as sales FROM film INNER JOIN (SELECT film_id , rental_id , amount FROM inventory INNER JOIN (SELECT payment.rental_id , amount , inventory_id FROM payment INNER JOIN rental ON rental.rental_id = payment.rental_id)alias1 ON alias1.inventory_id = inventory.inventory_id)alias2 ON film.film_id = alias2.film_id GROUP BY rating;

/*
Store wise earnings from late return have been calculated by subtracting rental_rate from amount paid and removing entries with negative values to take into account the rentals whose payment has not yet been done.
*/
SELECT SUM( CASE WHEN alias2.Amss-rental_rate>0 THEN alias2.Amss-rental_rate ELSE 0 END ) as summ , alias2.store_id FROM film INNER JOIN (SELECT film_id, alias1.Ams as Amss,store_id  FROM (SELECT payment.rental_id , rental.inventory_id as InID, payment.amount as Ams FROM payment INNER JOIN rental ON rental.rental_id = payment.rental_id)alias1 INNER JOIN inventory ON alias1.InID = inventory.inventory_id)alias2 ON film.film_id = alias2.film_id GROUP BY store_id;

/*
Top 5 actors have been selected on the basis of month wise earnings, month has been taken from payment_date not rental_date, if year has to included then WHERE clause will change to:
WHERE LEFT(monthname(payment_date),3) = 'AUG' AND year(rental_date) = 2005
*/
SELECT alias3.actor_id, actor.first_name, actor.last_name ,SUM(alias3.amount) as sums FROM actor INNER JOIN (SELECT actor_id , amount , film_actor.film_id FROM film_actor INNER JOIN (SELECT film_id,amount FROM inventory INNER JOIN (SELECT inventory_id , rental.rental_id,amount FROM payment INNER JOIN rental ON payment.rental_id = rental.rental_id WHERE LEFT(monthname(payment_date),3) = 'AUG')alias1 ON inventory.inventory_id = alias1.inventory_id)alias2 ON film_actor.film_id = alias2.film_id)alias3 ON alias3.actor_id = actor.actor_id GROUP BY actor_id ORDER BY sums DESC LIMIT 5;

/*
For finding Most rented genre I have considered number of rentals sold for a film not the amount. To add year WHERE CLAUSE changes to:
WHERE LEFT(monthname(payment_date),3) = 'AUG' AND year(rental_date) = 2005
*/
SELECT name , COUNT(rental_id) as sales FROM category INNER JOIN (SELECT category_id,rental_id FROM film_category INNER JOIN (SELECT film.film_id , rental_id FROM film INNER JOIN (SELECT film_id,rental_id FROM rental INNER JOIN inventory ON inventory.inventory_id = rental.inventory_id WHERE LEFT(monthname(rental_date),3) = 'AUG')alias1 ON alias1.film_id = film.film_id)alias2 ON alias2.film_id = film_category.film_id)alias3 ON alias3.category_id = category.category_id GROUP BY name ORDER BY sales DESC LIMIT 1;

/*
Top performing staff member has been found on the basis total amount of sales he earns in a given month, and the month has been considered from the payment_date
*/
SELECT first_name,last_name,SUM(amount) as sales FROM staff INNER JOIN (SELECT payment.rental_id , payment.staff_id as id, amount FROM payment WHERE LEFT(monthname(payment_date),3) = 'MAY' )alias1 ON staff.staff_id = alias1.id GROUP BY id ORDER BY sales DESC LIMIT 1;
