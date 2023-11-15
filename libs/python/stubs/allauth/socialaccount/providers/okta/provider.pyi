from _typeshed import Incomplete
from allauth.account.models import EmailAddress as EmailAddress
from allauth.socialaccount.providers.base import ProviderAccount as ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider as OAuth2Provider

class OktaAccount(ProviderAccount):
    def to_str(self): ...

class OktaProvider(OAuth2Provider):
    id: str
    name: str
    account_class = OktaAccount
    def get_default_scope(self): ...
    def extract_uid(self, data): ...
    def extract_extra_data(self, data): ...
    def extract_email_addresses(self, data): ...
    def extract_common_fields(self, data): ...

provider_classes: Incomplete