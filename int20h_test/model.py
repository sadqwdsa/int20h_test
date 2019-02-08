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

        if other is self:
            return True

        return self.id == other.id

    def __hash__(self):
        return hash(str(self._id))
