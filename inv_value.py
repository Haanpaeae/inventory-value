import os
import interbase
import configparser
import pwinput


def calculate_inventory_value(host, database, username, password):
    # Connect to the database
    conn = interbase.connect(
        host=host,
        database=database,
        user=username,
        password=password,
        charset='ISO8859_1'
    )
    cursor = conn.cursor()

    # SQL query to select required data for calculating inventory value
    query = """
        SELECT 
            IC.PRODUCT_CODE,
            IC.ON_HAND_QTY,
            IC.ON_INV_QTY,
            IC.ON_SALES_QTY,
            IC.ON_SRV_QTY,
            IC.PRODUCTION_RESERVED_QTY,
            P.UNIT_COST,
            P.VOLUME,
            P.NET_WEIGHT
        FROM IC_PRODUCT IC
        JOIN PRODUCT P ON IC.PRODUCT_CODE = P.CODE
        WHERE P.IS_ACTIVE = 'T' AND P.CAN_SELL = 'T'
    """

    # Execute the query
    cursor.execute(query)

    # Variable to store the total inventory value
    total_inventory_value = 0

    # Process each row to calculate inventory values
    for row in cursor.fetchall():
        product_code = row[0]
        on_hand_qty = row[1] if row[1] is not None else 0
        on_inv_qty = row[2] if row[2] is not None else 0
        on_sales_qty = row[3] if row[3] is not None else 0
        on_srv_qty = row[4] if row[4] is not None else 0
        production_reserved_qty = row[5] if row[5] is not None else 0
        unit_cost = row[6] if row[6] is not None else 0

        # Step 1: Calculate the total quantity incrementally if the fields are not null
        total_qty = 0
        if row[1] is not None:  # on_hand_qty is not null
            total_qty += on_hand_qty
        if row[2] is not None:  # on_inv_qty is not null
            total_qty += on_inv_qty
        if row[3] is not None:  # on_sales_qty is not null
            total_qty += on_sales_qty
        if row[4] is not None:  # on_srv_qty is not null
            total_qty += on_srv_qty
        if row[5] is not None:  # production_reserved_qty is not null
            total_qty += production_reserved_qty

        # Step 2: Ensure the total quantity is not negative
        if total_qty < 0:
            total_qty = 0

        # Step 3: Calculate the inventory value for the product
        inventory_value = total_qty * unit_cost

        # Add to total inventory value
        total_inventory_value += inventory_value

    # Print the total inventory value for all products
    print(f"\nTotal inventory value: {total_inventory_value:.2f}")

    # Close the connection
    cursor.close()
    conn.close()


# Read settings from the udconfig.ini file
config = configparser.ConfigParser()
config.read('ivconfig.ini')

host = config.get('settings', 'host')
database = config.get('settings', 'database')

# Ensure the user has a backup before proceeding with the update
print("Make sure you have a backup of the database before running any operations!")
proceed = input("Do you want to continue? (y/n): ").lower()

if proceed == 'y':
    # Ask for the username and password
    username = input("Database username: ")
    password = pwinput.pwinput("Database password: ")

    # Execute the calculation
    calculate_inventory_value(host, database, username, password)
else:
    print("Operation cancelled.")
    exit()

# Pause and wait for a key press to close the window
os.system("pause")
