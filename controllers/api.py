import tempfile

# Cloud-safe of uuid, so that many cloned servers do not all use the same uuids.
from gluon.utils import web2py_uuid

# Here go your api methods.
def log_in():
    if auth.is_logged_in():
        return response.json(dict(logged_in = True))
    else:
        return response.json(dict(logged_in = False))



def get_profile():
    profiles = db().select(db.profiles.ALL)
    profile = None

    print auth.user.id

    for p in profiles:
        if int(p.user_id) == int(auth.user.id):
            profile = dict(
                height=p.height,
                weight=p.weight
            )

    if profile is None:
        newp = db.profiles.insert(
            user_id=auth.user.id
        )
        profile = dict(
            height=newp.height,
            weight=newp.weight
        )

    return response.json(dict(profile=profile))


def edit_profile():
    profiles = db().select(db.profiles.ALL)

    print(request.vars.height)

    for p in profiles:
        if int(p.user_id) == int(auth.user.id):
            p.update_record(
                height=request.vars.height,
                weight=request.vars.weight
            )


def add_plan():
    plan = db.fitness_plans.insert(
        owner_id=auth.user.id,
        title=request.vars.title,
        goals=request.vars.goals,
        results=request.vars.results,
        feedback=request.vars.feedback,
        Sunday=request.vars.Sunday,
        Monday=request.vars.Monday,
        Tuesday=request.vars.Tuesday,
        Wednesday=request.vars.Wednesday,
        Thursday=request.vars.Thursday,
        Friday=request.vars.Friday,
        Saturday=request.vars.Saturday
    )

    return response.json(dict(plan=plan))


def get_my_plans():
    plans = db(db.fitness_plans.owner_id == auth.user.id).select()
    my_plans = []

    for plan in plans:
        p = dict(
            id=plan.id,
            title=plan.title,
            goals=plan.goals
        )
        my_plans.append(p)

    return response.json(dict(my_plans=my_plans))


def delete_plan():
    db(db.fitness_plans.id == request.vars.plan_id).delete()


def view_plan():
    plan = db(db.fitness_plans.id == request.vars.plan_id).select().first()
    user = db(db.auth_user.id == plan.owner_id).select().first()

    open_plan = dict(
        first_name=user.first_name,
        last_name=user.last_name,
        id=plan.id,
        title=plan.title,
        goals=plan.goals,
        results=plan.results,
        Sunday=plan.Sunday,
        Monday=plan.Monday,
        Tuesday=plan.Tuesday,
        Wednesday=plan.Wednesday,
        Thursday=plan.Thursday,
        Friday=plan.Friday,
        Saturday=plan.Saturday
    )

    return response.json(dict(open_plan=open_plan))


def browse():
    profile = db(db.profiles.user_id == auth.user.id).select().first()
    plans = db().select(db.fitness_plans.ALL)
    browse_plans = []

    print(profile)

    for plan in plans:
        is_followed = False
        if profile.followed_plans.count(plan.id) > 0:
            is_followed = True
        user = db(db.auth_user.id == plan.owner_id).select().first()
        
        p = dict(
            first_name=user.first_name,
            last_name=user.last_name,
            title=plan.title,
            goals=plan.goals,
            id=plan.id,
            is_followed=is_followed
        )
        browse_plans.append(p)

    return response.json(dict(browse_plans=browse_plans))


def follow_plan():
    profile = db(db.profiles.user_id == auth.user.id).select().first()
    followed = profile.followed_plans
    followed.append(int(request.vars.plan_id))

    profile.update_record(
        followed_plans=followed
    )

    print(profile.followed_plans)

def unfollow_plan():
    profile = db(db.profiles.user_id == auth.user.id).select().first()
    followed = profile.followed_plans
    followed.remove(int(request.vars.plan_id))
    
    profile.update_record(
        followed_plans=followed
    )

def get_followed_plans():
    profile = db(db.profiles.user_id == auth.user.id).select().first()
    followed_plans = []
    for plans in profile.followed_plans:
        plan = db(db.fitness_plans.id == plans).select().first()
        p = dict(
            plan_id=plans,
            title=plan.title,
            goals=plan.goals
        )
        followed_plans.append(p)
    return response.json(dict(followed_plans=followed_plans))


def edit_plan():
    plan = db(db.fitness_plans.id == request.vars.plan_id).select().first()

    plan.update_record(
        title=request.vars.title,
        goals=request.vars.goals,
        results=request.vars.results,
        Sunday=request.vars.Sunday,
        Monday=request.vars.Monday,
        Tuesday=request.vars.Tuesday,
        Wednesday=request.vars.Wednesday,
        Thursday=request.vars.Thursday,
        Friday=request.vars.Friday,
        Saturday=request.vars.Saturday
    )

def set_current_plan():
    profile = db(db.profiles.user_id == auth.user.id).select().first()
    profile.update_record(active_plan = request.vars.plan_id)

def get_current_plan():
    profile = db(db.profiles.user_id == auth.user.id).select().first()
    if profile.active_plan is not None:
        cur_plan = db(db.fitness_plans.id == profile.active_plan).select().first()
        plan = dict(
            id = cur_plan.id,
            goals = cur_plan.goals
        )
    else:
        plan = dict(
            id = -1,
            goals = "No active plan. Try following or adding a plan to set an active plan."
        )
    return response.json(dict(plan = plan))


#getallusers

#getuser(id)
