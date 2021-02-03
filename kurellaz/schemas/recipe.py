from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from kurellaz.schemas.user import UserSchema

def validate_num_of_servings(n):
    if n < 1:
        raise ValidationError('Number of servings needs to be greater then 0.')

class RecipeSchema(Schema):
    class Meta:
        ordered=True

    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(required=True, validate=[validate.Length(max=200)])
    num_of_servings = fields.Integer(validate=validate_num_of_servings)
    cook_time = fields.Integer()
    directions = fields.String(required=True, validate=[validate.Length(max=4000)])
    is_publish = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    #user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id','username'])

    @validates('cook_time')
    def validate_cook_time(self, n):
        if n < 1:
            raise ValidationError('Cook Time must be greater than 0.')

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data


