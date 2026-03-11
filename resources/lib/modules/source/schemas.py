class PlaybackRequest:
    def __init__(
        self,
        media_type: str,
        content_id: str,
        title: str,
    ):
        self.media_type = media_type
        self.content_id = content_id
        self.title = title
