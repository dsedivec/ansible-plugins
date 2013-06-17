from ansible import errors

try:
    import passlib.hash as passlib_hash
except ImportError:
    passlib_hash = None


def hash(data, algorithm_name, **kwargs):
    if not passlib_hash:
        raise errors.AnsibleError(
            "passlib must be installed to use the hash filter")
    try:
        algorithm = getattr(passlib_hash, algorithm_name)
    except AttributeError:
        raise errors.AnsibleError(
            "passlib doesn't contain algorithm %r" % (algorithm_name,))
    return algorithm.encrypt(data, **kwargs)


class FilterModule (object):
    def filters(self):
        return {"hash": hash}
