# recipe data model

recipe_list = []


def get_last_id():
    ''' 
        This function get the last recipe id from
        the recipe_list or will return 1
    '''
    if recipe_list:
        return recipe_list[-1].id + 1

    return 1


class Recipe:
    '''
    This is the recipe class which defined the data structure 
    and methods for the app
    '''

    def __init__(self, name, description, num_of_servings, cook_time, directions) -> None:
        self.id = get_last_id()
        self.name = name
        self.description = description
        self.num_of_servings = num_of_servings
        self.cook_time = cook_time
        self.directions = directions
        self.is_publish = False


    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'num_of_servings':self.num_of_servings,
            'cook_time': self.cook_time,
            'directions': self.directions
            }
