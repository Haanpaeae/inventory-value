Inventory value calculation 


Overview
This program calculates the inventory value based on data from two database tables: IC_PRODUCT and PRODUCT. It is designed to help users quickly assess the total value of items stored in a warehouse by combining information from both tables.


Features
-	Retrieves data from IC_PRODUCT and PRODUCT tables.
-	Calculates the inventory value using product quantities and pricing information.
-	Provides a summary of the total inventory value.


Requirements
-	Python 3.x
-	Database connection details (host, username, password, database path) in the configuration file (ivconfig.ini)
-	Required Python libraries: os, interbase, configparser, pwinput


Usage
1.	Configuration: Update the ivconfig.ini file with your database connection details:
		[settings]
		host = your host
		database = database path

2.	Run the program: Execute the Python script inv_value.py to calculate the inventory value.
		python inv_value.py

3.	The calculated inventory value will be displayed in the console.


How it works
-	The program reads the database connection details from the ivconfig.ini configuration file.
-	It connects to the database and retrieves data from the IC_PRODUCT and PRODUCT tables.
-	The program combines information about product quantities (IC_PRODUCT) and pricing (PRODUCT) to calculate the total value of the inventory.


Example Output
-	The output will be in the form of:
	Total inventory value: XXXXXX.XX


