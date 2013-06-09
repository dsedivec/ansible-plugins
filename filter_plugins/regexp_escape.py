import re


class FilterModule (object):
    def filters(self):
        return {"regexp_escape": re.escape}
