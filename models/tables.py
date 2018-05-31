# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime


def get_user_email():
    return auth.user.email if auth.user else None


db.define_table('profiles',
                Field('user_obj', 'reference auth_user', default=auth.user_id),
                Field('height', 'float'),
                Field('weight', 'float'),
                Field('active_plan'), #current plan
                Field('followed_plans'), #array of plans followed by user
                Field('my_plans')  # the array of plans created by user
                )

db.define_table('fitness_plans',
                Field('schedule'), #array of 'days' to hold the fitness schedule
                Field('goals', 'text'), #creator's intention on creating the plan
                Field('results', 'text'),  # expected results from plan
                Field('feedback'),  # journal of progress and results from plan
                Field('is_archived', 'boolean')  # whether or not the creator is still editing the plan
                )

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
