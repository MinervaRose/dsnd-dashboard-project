from .query_base import QueryBase

# Define a subclass of QueryBase called Employee


class Employee(QueryBase):

    # Set the class attribute `name`
    name = "employee"

    # This method returns a list of tuples (full_name, employee_id)
    def names(self) -> list[tuple]:
        query = """
            SELECT first_name || ' ' || last_name AS full_name,
                   employee_id
            FROM employee;
        """
        return self.query(query)

    # This method returns a single employee's full name
    def username(self, id: int) -> list[tuple]:
        query = f"""
            SELECT first_name || ' ' || last_name AS full_name
            FROM employee
            WHERE employee_id = {id};
        """
        return self.query(query)

    # This method returns a pandas dataframe for ML model input
    def model_data(self, id: int):
        query = f"""
            SELECT SUM(positive_events) positive_events,
                   SUM(negative_events) negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
        """
        return self.pandas_query(query)
