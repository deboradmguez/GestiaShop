import sys, os, tempfile

class SingleInstance:
    def __init__(self, name=""):
        self.name = name
        self.lockfile = os.path.normpath(tempfile.gettempdir() + '/' + self.name + '.lock')
        self.fp = None

    def already_running(self):
        try:
            if sys.platform == 'win32':
                self.fp = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            else:
                # En otros sistemas, usamos un enfoque de archivo de bloqueo
                import fcntl
                self.fp = open(self.lockfile, 'w')
                fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return False
        except (IOError, ImportError):
            return True

    def release(self):
        if self.fp:
            if sys.platform == 'win32':
                os.close(self.fp)
                os.remove(self.lockfile)
            else:
                import fcntl
                fcntl.lockf(self.fp, fcntl.LOCK_UN)
                self.fp.close()
                os.remove(self.lockfile)
            self.fp = None

    def __del__(self):
        self.release()