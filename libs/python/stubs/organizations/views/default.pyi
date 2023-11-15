from _typeshed import Incomplete
from organizations.models import Organization as Organization
from organizations.views.base import ViewFactory as ViewFactory
from organizations.views.mixins import AdminRequiredMixin as AdminRequiredMixin, MembershipRequiredMixin as MembershipRequiredMixin, OwnerRequiredMixin as OwnerRequiredMixin

bases: Incomplete

class OrganizationList(bases.OrganizationList): ...
class OrganizationCreate(bases.OrganizationCreate): ...
class OrganizationDetail(MembershipRequiredMixin, bases.OrganizationDetail): ...
class OrganizationUpdate(AdminRequiredMixin, bases.OrganizationUpdate): ...
class OrganizationDelete(OwnerRequiredMixin, bases.OrganizationDelete): ...
class OrganizationUserList(MembershipRequiredMixin, bases.OrganizationUserList): ...
class OrganizationUserDetail(AdminRequiredMixin, bases.OrganizationUserDetail): ...
class OrganizationUserUpdate(AdminRequiredMixin, bases.OrganizationUserUpdate): ...
class OrganizationUserCreate(AdminRequiredMixin, bases.OrganizationUserCreate): ...
class OrganizationUserRemind(AdminRequiredMixin, bases.OrganizationUserRemind): ...
class OrganizationUserDelete(AdminRequiredMixin, bases.OrganizationUserDelete): ...