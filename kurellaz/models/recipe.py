# recipe data model
from kurellaz.extensions import db

# recipe_list = []


# def get_last_id():
#     ''' 
#         This function get the last recipe id from
#         the recipe_list or will return 1
#     '''
#     if recipe_list:
#         return recipe_list[-1].id + 1

#     return 1


class Recipe(db.Model):
    '''
    This is the recipe class which defined the data structure 
    and methods for the app
    '''
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255))
    num_of_servings = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    directions = db.Column(db.String(4000))
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'num_of_servings':self.num_of_servings,
            'cook_time': self.cook_time,
            'directions': self.directions,
            'user_id': self.user_id
            }

    @classmethod
    def get_by_recipename(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_id(cls, recipe_id):
        return cls.query.filter_by(id=recipe_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_publish=True).all()