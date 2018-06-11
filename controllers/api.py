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
            if p.active_plan is None:
                goals = "No active plan."
                cur_plan = None
            else:
                goals = p.active_plan.goals
                cur_plan = p.active_plan.id
            profile = dict(
                height=p.height,
                weight=p.weight,
                goals=goals,
                cur_plan=cur_plan
            )

    if profile is None:
        newp = db.profiles.insert(
            user_id=auth.user.id
        )
        profile = dict(
            height=newp.height,
            weight=newp.weight,
            goals="No active plan.",
            cur_plan=None
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
    followed.append(request.vars.plan_id)

    profile.update_record(
        followed_plans=followed
    )

    print(profile.followed_plans)

def unfollow_plan():
    profile = db(db.profiles.user_id == auth.user.id).select().first()
    profile.followed_plans.remove(request.vars.plan_id)

def get_followed_plans():
    profile = db(db.profiles.user_id == auth.user.id).select().first()
    followed_plans = []
    for plans in profile.followed_plans:
        plan = db(db.fitness_plans.owner_id == plans).select().first()
        print(plan)
        p = dict(
            plan_id=plans,
            title=plan.title,
            goals=plan.goals
        )
        followed_plans.append(p)
    return response.json(dict(followed_plans=followed_plans))

#getallusers

#getuser(id)
