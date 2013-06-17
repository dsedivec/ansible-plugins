# Copyright 2013 Dale Sedivec
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
