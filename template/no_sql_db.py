# This file provides a very simple "no sql database using python dictionaries"
# If you don't know SQL then you might consider something like this for this course
# We're not using a class here as we're roughly expecting this to be a singleton

# If you need to multithread this, a cheap and easy way is to stick it on its own bottle server on a different port
# Write a few dispatch methods and add routes

# A heads up, this code is for demonstration purposes; you might want to modify it for your own needs
# Currently it does basic insertions and lookups
import hashlib
class Table():
    def __init__(self, table_name, *table_fields):
        self.entries = []
        self.fields = table_fields
        self.name = table_name
        for field in self.fields:
            print(field)
    def create_entry(self, *data):
        '''
        Inserts an entry in the table
        Doesn't do any type checking
        '''

        # Bare minimum, we'll check the number of fields
        if len(data) != len(self.fields):
            print(f"(given {len(data)} expected {len(self.fields)})")
            for field in self.fields:
                print(field)
            raise ValueError('Wrong number of fields for table')

        self.entries.append(data)
        return

    def search_table(self, target_field_name, target_value):
        '''
            Search the table given a field name and a target value
            Returns the first entry found that matches
        '''
        # Lazy search for matching entries
        for entry in self.entries:
            for field_name, value in zip(self.fields, entry):
                if target_field_name == field_name and target_value == value:
                    return entry

        # Nothing Found
        return None

    def search_corr_value(self, target_field_name, target_value, corr_field):
        '''
            Search the table given a field name, a target value, and a corresponding value
            Returns the first entry found that matches
        '''
        # Lazy search for matching entries
        for entry in self.entries:
            found = False
            for field_name, value in zip(self.fields, entry):
                if found == True:
                    if field_name == corr_field:
                        print(f"found pass ({field_name}) {value}")
                        return value
                if target_field_name == field_name and target_value == value:
                    print(f'FOUND USER! user: {value}')
                    found = True
                    # return entry

        # Nothing Found
        return None


class DB():
    '''
    This is a singleton class that handles all the tables
    You'll probably want to extend this with features like multiple lookups, and deletion
    A method to write to and load from file might also be useful for your purposes
    '''
    def __init__(self):
        self.tables = {}

        # Setup your tables
        self.add_table('users', "id", "username", "password", "admin")
        admin_pass = "poiuytrewq098765@#"
        hashed_admin_pass = hashlib.sha256(str(admin_pass).encode('utf-8')).hexdigest()
        self.create_table_entry("users", 0, "admin", hashed_admin_pass, 1)
        
        return

    def add_table(self, table_name, *table_fields):
        '''
            Adds a table to the database
        '''
        table = Table(table_name, *table_fields)
        self.tables[table_name] = table

        return


    def search_table(self, table_name, target_field_name, target_value):
        '''
            Calls the search table method on an appropriate table
        '''
        return self.tables[table_name].search_table(target_field_name, target_value)

    def search_2_values(self, table_name, target_field_name, target_value, corr_field):
        '''
            Calls the search table method on an appropriate table
        '''
        return self.tables[table_name].search_corr_value(target_field_name, target_value, corr_field)

    def create_table_entry(self, table_name, *data):
        '''
            Calls the create entry method on the appropriate table
        '''
        return self.tables[table_name].create_entry(*data)

    def get_table(self, table_name):
        for name in self.tables:
            if table_name == name:
                return self.tables[name]


# Our global database
# Invoke this as needed
DATABASE = DB()
