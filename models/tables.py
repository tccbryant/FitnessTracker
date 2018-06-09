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


db.define_table('schedule_day',
                Field('title', 'text'),
                Field('workouts', 'text'),
                Field('meals', 'text'),
                Field('misc', 'text'))


db.define_table('fitness_plans',
                Field('schedule', 'list:reference schedule_day'), #array of 'days' to hold the fitness schedule
                Field('title', 'text'),
                Field('goals', 'text', default=""), #creator's intention on creating the plan
                Field('results', 'text'),  # expected results from plan
                Field('feedback', 'text'),  # journal of progress and results from plan
                Field('is_archived', 'boolean')  # whether or not the creator is still editing the plan
                )


db.define_table('profiles',
                Field('user_id'),
                Field('height', 'float', default=0),
                Field('weight', 'float', default=0),
                Field('active_plan', 'reference fitness_plans'), #current plan
                Field('followed_plans', 'list:reference fitness_plans'), #array of plans followed by user
                Field('my_plans', 'list:reference fitness_plans')  # the array of plans created by user
                )


# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
