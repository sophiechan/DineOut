# DineOut
DineOut is designed for diners to discover every aspect about restaurants in US. The diners can also rate and
comment on restaurants, as well as create their own personal favorite restaurant lists and share their experience with
others. The App also provides service for the manager to post some dishes and change the dish menu to attract
customers.

## Entity Sets and Realtionship Sets 
### All features in the original proposal have been implemented.
DineOut contains entity sets such as diners, managers, restaurants, personal lists, reviews and dishes.
  * A diner could have the following attributes: diner ID, name and the login password.
  * A manager could have the following attributes: manager ID, name and the login password.
  * A dish could have the following attributes: dish name.
  * A Restaurant could have the following attributes: restaurant ID, name, average rating score and the detailed information of its address.
  * A Personal list could have the following attributes: list name.
  * A review could have the following attributes: review ID, the rating score and the detailed comments.

Regarding the relationship, the manager could manage the restaurant (such as modifying address) and add dishes for
the restaurant, and one dish could only be added by one manager for one restaurant. Each restaurant will have at least
one dish on the menu. Each diner could write reviews about the restaurants, and a review could only written by one
diner about one restaurant on one day. And the average rating of the restaurant will be affected by every single review's rating. A diner could also create several personal dining lists, in which they could save several restaurants according to their preference.

## Interesting Web Pages and Database Queries.
  * When you logged in as a Diner (feel free to [sign up](http://35.196.5.152:8111/signup) as a diner or use our existing user (username: Cin, password: 12345678)), you will see your personal dining list. You can add your own personal list, such as Spicy Restaurant, etc. And you can also view all the reviews given by you to those restaurant you visited. When you click [Restaurants](http://35.196.5.152:8111/restaurants) on the navigation bar, you can see a list of all the restaurants with their addresses and average rating scores. On a specific restaurant page, you can view its dishes on the menu, as well as all the reviews given to this restaurant. The most interesting parts are as followed:

    - You can add a new review with rating from 1 to 5 stars to this restaurant. After your review is published, the average rating of this restaurant will be changed. When you go back to the home page and delete your review, the average rating of the restaurant will be affected as well. The Database query is as followed:
    ```sql
    -- Add a Review
    INSERT INTO Write_Review_About (dt, comments, star, did, restid) 
    VALUES (today.isoformat(), input.comments, input.star, input.uid, input.restid);
    
    UPDATE Restaurants SET stars = 
    	(SELECT AVG(star) 
    	FROM Write_Review_About 
    	WHERE restid = input.restid) 
    WHERE restid = input.restid;

    -- Delete a Review
    DELETE FROM Write_Review_About WHERE dt = input.dt AND restid = input.restid AND did = input.uid;

    UPDATE Restaurants SET stars = 
    	(SELECT AVG(star) 
    	FROM Write_Review_About 
    	WHERE restid = input.restid) 
    WHERE restid = input.restid;
	```

    - You can also add a restaurant to your personal lists. Pay attention to the drop down menu of personal lists. When this restaurant has been added to a personal list A, the list's name A will not appear in this drop down menu, which means you could only add this restaurant to those personal lists which does not contain this restaurant.
    ```sql
	SELECT P.lname FROM PersonalLists_Save AS P
	WHERE
		P.did = input.uid
		AND P.lname NOT IN 
			(SELECT lname FROM Contain WHERE did = input.uid AND restid = input.restid);
	```

- When you logged in as a Manager (feel free to use the existing one (username: Sophie, password: 12345678)), on the restaurants list page you can only view those restaurants you are authorized to manage. On a single restaurant page, You could update the basic information of the restaurant (sorry, no operation to the average rating, we are honest to diners' reviews). And you can add and delete dishes on the menu as well.

## Data Source
Our main data source will be Yelp Open Dataset, which could be found on https://www.yelp.com/dataset.
