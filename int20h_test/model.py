class PhotoInfo:
    def __init__(self, photo_id, origin_url, min_url, medium_url):
        self._id = photo_id
        self._origin_url = origin_url
        self._min_url = min_url
        self._medium_url = medium_url

    @property
    def id(self):
        return self._id

    @property
    def origin_url(self):
        return self._origin_url

    @property
    def min_url(self):
        return self._min_url

    @property
    def medium_url(self):
        return self._medium_url

    def __eq__(self, other):
        if other is None:
            return False

        if other is self:
            return True

        return self.id == other.id

    def __hash__(self):
        return hash(str(self._id))
