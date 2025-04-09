from .query_base import QueryBase

# Create a subclass of QueryBase
# called  `Team`


class Team(QueryBase):

    # Set the class attribute `name`
    # to the string "team"
    name = "team"

    # Define a `names` method
    # that receives no arguments
    # This method should return
    # a list of tuples from an sql execution
    def names(self) -> list[tuple]:

        # Query 5
        # Write an SQL query that selects
        # the team_name and team_id columns
        # from the team table for all teams
        # in the database
        query = """
            SELECT team_name, team_id
            FROM team;
        """
        return self.query(query)

    # Define a `username` method
    # that receives an ID argument
    # This method should return
    # a list of tuples from an sql execution
    def username(self, entity_id: int) -> list[tuple]:

        # Query 6
        # Write an SQL query
        # that selects the team_name column
        # Use f-string formatting and a WHERE filter
        # to only return the team name related to
        # the ID argument
        query = """
            SELECT team_name
            FROM team
            WHERE team_id = ?;
        """
        return self.query(query, [entity_id])

    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returned containing the execution of
    # the sql query
    def model_data(self, entity_id: int):

        query = """
            SELECT positive_events, negative_events FROM (
                SELECT employee_id,
                       SUM(positive_events) AS positive_events,
                       SUM(negative_events) AS negative_events
                FROM team
                JOIN employee_events
                    USING(team_id)
                WHERE team.team_id = ?
                GROUP BY employee_id
            )
        """
        return self.pandas_query(query, params=(entity_id,))
