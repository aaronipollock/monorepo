from allauth.socialaccount import providers as providers
from allauth.socialaccount.providers.base import ProviderAccount as ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider as OAuth2Provider

class CleverAccount(ProviderAccount):
    def get_avatar_url(self) -> None: ...
    def to_str(self): ...

class CleverProvider(OAuth2Provider):
    id: str
    name: str
    account_class = CleverAccount
    def extract_uid(self, data): ...
    def get_user_type(self, data): ...
    def extract_common_fields(self, data): ...
    def get_default_scope(self): ...