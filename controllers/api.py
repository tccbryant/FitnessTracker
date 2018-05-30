import tempfile

# Cloud-safe of uuid, so that many cloned servers do not all use the same uuids.
from gluon.utils import web2py_uuid

# Here go your api methods.


def get_images():
    user_images = []
    rows = db().select(db.user_images.ALL)

    for r in rows:
        if str(r.created_by) == str(request.vars.user_id):
            i = dict(
                id=r.id,
                created_by=r.created_by,
                created_on=r.created_on,
                image_url=r.image_url
            )
            user_images.append(i)

    return response.json(dict(user_images=user_images))


def get_users():
    if auth.is_logged_in():
        users = []
        rows = db(db.auth_user.id > 0).select()

        u = dict(
            id=auth.user.id,
            first_name=auth.user.first_name,
            last_name=auth.user.last_name
        )
        users.append(u)

        for r in rows:
            if r.id != auth.user.id:
                u = dict(
                    id=r.id,
                    first_name=r.first_name,
                    last_name=r.last_name
                )
                users.append(u)

        return response.json(dict(users=users))


@auth.requires_signature()
def add_image():
    db.user_images.insert(
        image_url=request.vars.image_url
    )


def get_self_id():
    if auth.is_logged_in():
        return response.json(dict(id=auth.user.id))
    else:
        return response.json(dict(id=-1))

#getallusers

#getuser(id)
