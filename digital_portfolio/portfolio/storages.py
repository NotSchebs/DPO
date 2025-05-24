from cloudinary_storage.storage import MediaCloudinaryStorage

class RawMediaCloudinaryStorage(MediaCloudinaryStorage):
    def __init__(self, *args, **kwargs):
        kwargs['resource_type'] = 'raw'
        super().__init__(*args, **kwargs)
