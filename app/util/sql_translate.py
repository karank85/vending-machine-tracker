class SQLParser:
    """Helps convert logics to mysql query syntax."""

    table: str
    attributes: list[str]

    def __init__(self, table: str, attributes: list[str]):
        """Initialize parser by taking in the table and the corresponding attributes."""
        self.table = table
        self.attributes = attributes

    def select_all(self, specific_columns: str = "*") -> str:
        """Query to select all records from table."""
        return f"SELECT {specific_columns} FROM {self.table}"

    def select_with_condition(self, condition: str, specific_columns: str = "*") -> str:
        """Query to select certain records from table."""
        return f"SELECT {specific_columns} FROM {self.table} WHERE {condition}"

    def delete_record(self, condition: str) -> str:
        """Query to delete records from table."""
        return f"DELETE FROM {self.table} WHERE {condition}"

    def add_record(self, values: list[any]) -> str:
        """Query to add a record into the table."""
        attributes_joined: str = ",".join(self.attributes)
        values_joined: str = ",".join(values)
        return f"INSERT INTO {self.table}({attributes_joined}) VALUES({values_joined})"

    def edit_record(self, values: list[any], condition: str, columns: list[any] = None) -> str:
        """Query to edit a record into the table."""
        attributes_sliced = self.attributes[1:]
        if columns is None:
            setting_values = ",".join([f"{attributes_sliced[i]}={values[i]}" for i in range(len(values))])
        else:
            setting_values = ",".join([f"{columns[i]} = {values[i]}" for i in range(len(values))])
        return f"UPDATE {self.table} SET {setting_values} WHERE {condition}"
