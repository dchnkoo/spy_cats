from urllib.parse import urlparse


class URLPath:
    
    def __init__(self, path: str, *, prefix: str = "", domain: str = "") -> None:
        if not path.startswith("/"):
            raise ValueError(f"Path should start with '/'. Your path => {path}")
        
        if not prefix.startswith("/"):
            raise ValueError(f"Prefix should start with '/'. Your prefix => {prefix}")
        
        if domain.endswith("/"):
            raise ValueError(f"Domain should not end with '/'.")

        self.path = path
        self.prefix = prefix
        self.domain = domain

    @property
    def tag(self):
        return self.prefix.removeprefix("/").title()

    @property
    def path_with_prefix(self):
        return self.prefix + self.path
    
    @property
    def full_path(self):
        return self.domain + self.path_with_prefix
    
    @property
    def parsed_url(self):
        return urlparse(self.full_path)
    
    def __str__(self) -> str:
        return f"URLPath({self.path})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __add__(self, other: str) -> "URLPath":
        if not isinstance(other, str):
            raise ValueError(f"Add value should be str! Your value is {type(other)}")

        return URLPath(self.path + other, prefix=self.prefix, domain=self.domain)

class URLs:

    def __init_subclass__(cls, prefix: str = "", domain: str = "") -> None:
        cls.prefix = prefix
        cls.domain = domain
        for attr, t in cls.__annotations__.items():
            if t is URLPath and isinstance((value := getattr(cls, attr)), str):
                setattr(cls, attr, URLPath(value, prefix=prefix, domain=domain))
    