# Project 2: Boston Area Activities

## The Databasers Team
**Team Lead:** Osamudiamen (Mudia) Eastwood - mudia5

**E-R Diagram Analysis and SQL Engineer:** Matt Eichelman - meichelman

**E-R Diagram Analysis and Narration:** Andrew Kallmeyer - AndrewKallmeyer1

**E-R Diagram Reduction and Normalization:** Julia Lin - julialin214

<br><br>






## Set Up

### 1. Clone this repository 

`git clone https://github.com/mudia5/northwind-ecommerce.git`

### 2. Create a local copy of the Boston Area Activities database

Enter the P2 directory and run the command:

`sqlite3 boston_activities.db < schema.sql`

### 3. Create and activate a virtual environment
On macOS/Linux:
`python -m venv venv`
`source venv/bin/activate`

On Windows:
`python -m venv venv`
`venv\Scripts\activate`

Ensure you are using Python 3.11.

### 4. Population `boston_actitivies.db` with data

`python3 generate_data.py`

### 5. Test the data

Now explore the database!


<br><br>

## Narrative 
### I. Introduction
Our group focused on designing a database to support activity groups in the greater Boston area. We began by considering what features we and our peers would find most useful in a system designed to accommodate a wide range of interests. Using the Boston College student organization database as a reference point, we identified additional information that could enhance user experience and improve overall utility.
### II. E-R Analysis 
We began our E-R analysis by defining core entities such as **User**, **Event**, and **Location**. One of the first design challenges we encountered was modeling the **Waitlist** for joining groups. Initially, we considered representing the waitlist as a separate entity. However, we realized this would duplicate data already present in the **User** and **Group** entities. To avoid redundancy, we redefined the waitlist as a relationship set between **User** and **Group**, with descriptive attributes such as `register_time` to capture the order in which users joined the waitlist for each group. We later recognized that the waitlist could be integrated into the existing **Membership** relationship set, also relating **User** and **Group**. By using the `role` attribute, we distinguished between waitlisted and active members (including admins and general members). We also added the `register_time` attribute to **Membership**  to preserve the ordering among waitlisted users.

When designing the **Location** entity, we initially used a composite attribute `address` with components like `street`, `city`, `state`, and `country`. However, since the database is limited to Boston-area activities, we removed `state` and `country` to reduce redundancy and prevent inconsistencies. We also opted to use `location_name` as the primary key instead of introducing a separate `location_id`, assuming that location names within the Boston area would be sufficiently unique. This choice encourages more descriptive names (e.g., “Brookline Public Library” instead of simply “Library”), improving clarity for users. Similarly, we chose `group_name` as the primary key for **Group**, to enforce uniqueness and promote user-friendly identification.

Another key challenge came when deciding how to represent reviews of events written by users. Originally, we had a ternary relationship among the three, intending to associate one user with one review about one event. However, as ternary relationships allow at most one arrow out the relationship to avoid ambiguity, we realized this was not possible. Instead, we split this into two many-to-one relationship sets relating **Review** to **User** and **Event** separately, preserving our intended cardinality.

### III. Reduction to database schema 
We made a number of additions in reducing our E-R diagram to relation schemas. First, multivalued attributes were reduced to new schemas, creating **User_Phone** to allow the storage of multiple phone numbers per user. Many-to-many relationship sets were reduced to new schemas with the primary key being the union of the primary keys from participating entity sets, creating schemas like **Belongs** and **Hosts**. To eliminate redundancies, many-to-one relationship sets were simply reduced to adding a foreign key attribute to the relation on the “many” side, such as adding `user_id` and `event_id` to the **Review** schema to represent the **Writes** and **About** relationship sets respectively. Since all our many-to-one relationships involved total participation on the many side, we did not need to consider potential null values. Our E-R analysis did not include any one-to-one relationship sets. 

After following these principles to reduce our E-R diagram to a database schema, we then evaluated the resulting schema by checking that all relation schemas were in “good form,” specifically in BCNF. Luckily, owing to our thoughtfulness in the E-R design, we only identified one schema that was not in BCNF, Location. Specifically, we identified a nontrivial functional dependency that was not a superkey: `zip -> city`. Given the real world purpose of a zip, a zip code will always define the city. Thus, every time the same zip code was in the relation, the city would be the same as well and could introduce inconsistencies. It would be better practice to only each zip and city combination only once in a separate relation. Thus, we followed the general rule for decomposing schemas that are not in BCNF, resulting in the schemas **Location** (now with only `zip` and no `city`) and **Zip_City**. Both relations were now in BCNF.

