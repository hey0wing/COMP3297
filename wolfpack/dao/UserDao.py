from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from wolfpack.models import ProductOwner
from wolfpack.models import Developer
from wolfpack.models import ScrumMaster
from wolfpack.models import User

from . import ProjectDao

from wolfpack.Enum import UserRoleEnum


def getUserById(pid, role):
    if pid is None:
        return None
    if role == UserRoleEnum.PRODUCT_OWNER:
        return get_object_or_404(ProductOwner, id=pid)
    elif role == UserRoleEnum.SCRUM_MASTER:
        return get_object_or_404(ScrumMaster, id=pid)
    elif role == UserRoleEnum.DEVELOPER:
        return get_object_or_404(Developer, id=pid)
    else:
        raise Exception("user role doesn't exist in enum")


def getUserByOnlyId(pid):
    if pid is None:
        return None
    else:
        return get_object_or_404(User, id=pid)


def insert(name, role, projectId=None):
    if role == UserRoleEnum.PRODUCT_OWNER:
        user = ProductOwner(
            name=name,
            role=UserRoleEnum.PRODUCT_OWNER.value,
            projectId=ProjectDao.getProjectById(projectId)
        )
        user.save()
        return user.id
    elif role == UserRoleEnum.SCRUM_MASTER:
        user = ScrumMaster(
            name=name,
            role=UserRoleEnum.SCRUM_MASTER.value,
        )
        user.save()
        return user.id
    elif role == UserRoleEnum.DEVELOPER:
        user = Developer(
            name=name,
            role=UserRoleEnum.DEVELOPER.value,
            projectId=ProjectDao.getProjectById(projectId)
        )
        user.save()
        return user.id
    else:
        raise Exception("user type doesn't exist")


def deleteById(pid, role):
    user = getUserById(pid, role)
    user.delete()


def getUserProject(userId):
    pass


def updateById(pid, role, name=None, projectId=None):
    user = getUserById(pid, role)
    if name is not None:
        user.name = name

    if role is not None:
        user.role = role

    if projectId is not None:
        user.projectId = ProjectDao.getProjectById(projectId)

    user.save()


def getUserByRole(role):
    if role == UserRoleEnum.PRODUCT_OWNER:
        return ProductOwner.objects.all()
    elif role == UserRoleEnum.SCRUM_MASTER:
        return ScrumMaster.objects.all()
    elif role == UserRoleEnum.DEVELOPER:
        return Developer.objects.all()
    else:
        raise Exception("user role doesn't exist in enum")


def invite(pid, projectId):
    send_mail(
        'Invitation to project',
        'You are invited to this project.',
        'mail@wolfpack.com',
        ['receive@wolfpack.com'],  # getUserByOnlyId(pid).email
        fail_silently=False,
    )
    return


# this function will return developers with no project associated with
def getAvailableDevelopers():
    return Developer.objects.all().exclude(projectId__isnull=False)


def getUserByEmailAndPassword(email, password, role):
    user = None
    if role == UserRoleEnum.SCRUM_MASTER.value:
        try:
            user = ScrumMaster.objects.get(email=email, password=password)
        except ScrumMaster.DoesNotExist:
            pass
    elif role == UserRoleEnum.DEVELOPER.value:
        try:
            user = Developer.objects.get(email=email, password=password)
        except Developer.DoesNotExist:
            pass
    elif role == UserRoleEnum.PRODUCT_OWNER.value:
        try:
            user = ProductOwner.objects.get(email=email, password=password)
        except ProductOwner.DoesNotExist:
            pass
    else:
        raise Exception("cannot determine user role")

    return user
