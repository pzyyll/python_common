import svn.constants
import svn.common


class RemoteClient(svn.common.CommonClient):

    def __init__(self, url, *args, **kwargs):
        super(RemoteClient, self).__init__(
            url,
            svn.constants.LT_URL,
            *args, **kwargs)

    def checkout(self, path, revision=None, extra_args=None):
        cmd = []
        if revision is not None:
            cmd += ['-r', str(revision)]

        cmd += [self.url, path]
        if extra_args:
            cmd += extra_args
        
        self.run_command('checkout', cmd)

    def __repr__(self):
        return '<SVN(REMOTE) %s>' % self.url
