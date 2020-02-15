"""
    OVERALL CREDIT TO:
        t0mm0, Eldorado, VOINAGE, BSTRDMKR, tknorris, smokdpi, TheHighway

    resolveurl XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import re
from resolveurl.plugins.__resolve_generic__ import ResolveGeneric
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError
from resolveurl.plugins.lib import jsunpack

class DatoPornResolver(ResolveGeneric):
    name = "datoporn"
    domains = ['datoporn.com', 'dato.porn', 'datoporn.co']
    pattern = '(?://|\.)(datoporn\.com|dato\.porn|datoporn\.co)/(?:embed[/-])?([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA}
        html = self.net.http_GET(web_url, headers=headers).content
        try:
            packed = re.search('>(eval\(function\(p,a,c,k,e,d\).+)\s+', html)
            unpacked = jsunpack.unpack(packed.group(1))
            r = re.search('src:"([^"]+)"', unpacked)
            return r.group(1)
        except Exception as e:
            common.logger.log_debug(e)
            raise ResolverError("Video not found")

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/{media_id}')

    @classmethod
    def _is_enabled(cls):
        return True






