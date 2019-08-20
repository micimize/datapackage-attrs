

from datetime import datetime


@attr.s(auto_attribs=True)
class Simple:
    """A simple tableschema
    """
    id: int
    title: t.Optional[str] = None
    timestamp: t.Optional[datetime] = None
