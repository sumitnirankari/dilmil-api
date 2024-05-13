from marshmallow import Schema, fields


class TokenHeaderSchema(Schema):
    authorization = fields.String(required=True, description='Bearer Token')

class ProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    dob = fields.Date(required=True, description='yyyy-mm-dd')
    height = fields.Int(required=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class UserPrefSchema(Schema):
    age_min = fields.Int(required=True)
    age_max = fields.Int(required=True)
    height_min = fields.Int(required=True)
    height_max = fields.Int(required=True)

class ProfileViewSchema(ProfileSchema):
    age = fields.Int(dump_only=True)
    dob = fields.Date(load_only=True)
    user = fields.Nested(UserSchema(), dump_only=True)

class UserViewSchema(UserSchema):
    dob = fields.Date(load_only=True)
    profile = fields.Nested(ProfileSchema(), dump_only=True)
    preference = fields.Nested(UserPrefSchema(), dump_only=True)

class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)

class UserMeSchema(UserRegisterSchema):
    profile = fields.Nested(ProfileSchema(), dump_only=True)
    preference = fields.Nested(UserPrefSchema(), dump_only=True)
    
class UserLikesSchema(Schema):
    target_user_id = fields.Int(required=True)
    liked = fields.Bool(required=True)

class UsersListSchema(Schema):
    page = fields.Int(dump_only=True)
    per_page = fields.Int(dump_only=True)
    pages = fields.Int(dump_only=True)
    total = fields.Int(dump_only=True)
    users = fields.List(fields.Nested(UserViewSchema()), dump_only=True)

class UsersProfileListSchema(Schema):
    page = fields.Int(dump_only=True)
    per_page = fields.Int(dump_only=True)
    pages = fields.Int(dump_only=True)
    total = fields.Int(dump_only=True)
    profiles = fields.List(fields.Nested(ProfileViewSchema()), dump_only=True)

class PaginationSchema(Schema):
    page = fields.Int(required=True)
    page_size = fields.Int(required=True)

class SearchPrefSchema(Schema):
    show_liked = fields.Bool(required=True)
    sort_on = fields.Str(required=True)
    sort_order = fields.Str(required=True)
    page = fields.Int(required=True)
    page_size = fields.Int(required=True)