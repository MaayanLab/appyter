from s3fs.core import S3FileSystem, sync_wrapper

class S3FileSystemEx(S3FileSystem):

    async def _info(self, path, bucket=None, key=None, refresh=False, version_id=None):
        if len(path) > 1024: raise FileNotFoundError
        return await super()._info(path, bucket=bucket, key=key, refresh=refresh, version_id=version_id)

    info = sync_wrapper(_info)

    async def _mkdir(self, path, acl=False, create_parents=True, **kwargs):
        '''
        Making a directory in an existing bucket always succeeds (even though s3 has no real
          directories): if it doesn't exist we add it to `dircache` so that it does, if it already
          exists as a directory nothing happens. Only an existing *file* at that path is an error.
          Otherwise (i.e. creating buckets) defer to s3fs.
        '''
        stripped = self._strip_protocol(path).rstrip("/")
        if stripped:
            bucket, key, _ = self.split_path(stripped)
            if key and await self._exists(bucket):
                try:
                    path_info = await self._info(stripped)
                except FileNotFoundError:
                    self.dircache[stripped] = []
                else:
                    if path_info['type'] == 'file':
                        raise FileExistsError(path)
                return
        return await super()._mkdir(path, acl=acl, create_parents=create_parents, **kwargs)

    mkdir = sync_wrapper(_mkdir)
