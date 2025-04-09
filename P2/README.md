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
