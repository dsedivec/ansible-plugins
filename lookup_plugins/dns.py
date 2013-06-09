import socket

from ansible import utils, errors


class LookupModule (object):
    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)
        if isinstance(terms, basestring):
            terms = [terms]
        ret = []
        for term in terms:
            try:
                ret.append(socket.gethostbyname(term))
            except socket.error, ex:
                raise errors.AnsibleError("exception resolving %r" % (term,),
                                          ex)
        return ret
