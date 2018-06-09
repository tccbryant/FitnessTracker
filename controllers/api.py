import tempfile

# Cloud-safe of uuid, so that many cloned servers do not all use the same uuids.
from gluon.utils import web2py_uuid

# Here go your api methods.

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
        feedback=request.vars.feedback
    )

    return response.json(dict(plan=plan))

#getallusers

#getuser(id)
