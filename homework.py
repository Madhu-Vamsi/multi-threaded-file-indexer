#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations
from zipfile import ZipFile


class homework(Operations):

    def __init__(self, root):
        print"Allo! Allo! Welcome to my FileSystem!"
        #Some credits goes to this blog: https://www.stavros.io/posts/python-fuse-filesystem/#
        ZipFile(root, 'r').extractall("/tmp/zip/")
        self.root = "/tmp/zip"

    def complete_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def access(self, path, mode):
        full_path = self.complete_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def getattr(self, path, fh=None):
        full_path = self.complete_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self.complete_path(path)

        directories = ['.', '..']
        if os.path.isdir(full_path):
            directories.extend(os.listdir(full_path))
        for entry in directories:
            yield entry

    def statfs(self, path):
        full_path = self.complete_path(path)
        stat = os.statvfs(full_path)
        return dict((key, getattr(stat, key)) for key in ('f_bavail', 'f_bfree', 'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag', 'f_frsize', 'f_namemax'))

    def open(self, path, flags):
        full_path = self.complete_path(path)
        return os.open(full_path, flags)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

def main(mountpoint, root):
    FUSE(homework(root), mountpoint)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])