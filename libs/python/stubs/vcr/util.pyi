from _typeshed import Incomplete
from collections.abc import MutableMapping

class CaseInsensitiveDict(MutableMapping):
    def __init__(self, data: Incomplete | None = ..., **kwargs) -> None: ...
    def __setitem__(self, key, value) -> None: ...
    def __getitem__(self, key): ...
    def __delitem__(self, key) -> None: ...
    def __iter__(self): ...
    def __len__(self) -> int: ...
    def lower_items(self): ...
    def __eq__(self, other): ...
    def copy(self): ...

def partition_dict(predicate, dictionary): ...
def compose(*functions): ...
def read_body(request): ...
def auto_decorate(decorator, predicate=...): ...