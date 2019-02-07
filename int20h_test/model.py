class PhotoInfo:
    def __init__(self, id, origin_url):
        self._id = id
        self._origin_url = origin_url

    @property
    def id(self):
        return self._id

    @property
    def origin_url(self):
        return self._origin_url

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, self.__class__):
            return False

        return self._id == other._id

    def __hash__(self):
        return hash(str(self._id))
