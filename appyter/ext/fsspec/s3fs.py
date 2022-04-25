from s3fs.core import S3FileSystem, buck_acls, ClientError, translate_boto_error, ParamValidationError, sync_wrapper

class S3FileSystemEx(S3FileSystem):
    async def _mkdir(self, path, acl="", create_parents=True, **kwargs):
        '''
        If we create an empty directory, we'll add it to `dircache`
        '''
        path = self._strip_protocol(path).rstrip("/")
        if not path:
            raise ValueError
        bucket, key, _ = self.split_path(path)
        if await self._exists(bucket):
            if not key:
                # requested to create bucket, but bucket already exist
                raise FileExistsError
            else:
              try:
                path_info = await self._info(path)
                if path_info['type'] == 'file':
                  raise FileExistsError
              except:
                self.dircache[path] = []
        elif not key or create_parents:
            if acl and acl not in buck_acls:
                raise ValueError("ACL not in %s", buck_acls)
            try:
                params = {"Bucket": bucket, "ACL": acl}
                region_name = kwargs.get("region_name", None) or self.client_kwargs.get(
                    "region_name", None
                )
                if region_name:
                    params["CreateBucketConfiguration"] = {
                        "LocationConstraint": region_name
                    }
                await self._call_s3("create_bucket", **params)
                self.invalidate_cache("")
                self.invalidate_cache(bucket)
            except ClientError as e:
                raise translate_boto_error(e)
            except ParamValidationError as e:
                raise ValueError("Bucket create failed %r: %s" % (bucket, e))
        else:
            # raises if bucket doesn't exist and doesn't get create flag.
            await self._ls(bucket)

    mkdir = sync_wrapper(_mkdir)