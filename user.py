class User:
    """
    The class User is a model for user information.
    """
    def __init__(self):
        self.name = ""
        self.surname = ""
        self.username = ""
        self.password = ""
        self.type = ""

    def from_dict(self, user_dict):
        """
        Sets the attributes of the self object to the values retrieved from given dictionary
        :param user_dict: dictionary from which the fields of self object are populated
        """
        self.name = user_dict['Name']
        self.surname = user_dict['Surname']
        self.username = user_dict['Username']
        self.password = user_dict['Password']
        self.type = user_dict['Type']

    def to_dict(self):
        """
        Encode the attributes of the object in a dictionary.
        :return: the generated dictionary
        """
        dict_user = {'name': self.name,
                     'surname': self.surname,
                     'username': self.username,
                     'password': self.password,
                     'type': self.type}
        return dict_user
