from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.registry.interfaces import IRegistry
from zope import component
from collective.googlemaps import interfaces
import urllib

BASE = "://maps.googleapis.com/maps/api/js?"
SCRIPT = """<script type="text/javascript" src="%s"></script>"""
ASYNC_SCRIPT = """
<script type="text/javascript">
function googlemapsAsync() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "%s";
  document.body.appendChild(script);
}

$(function() {
   googlemapsAsync();
});
</script>
"""

class JavascriptViewlet(common.ViewletBase):
    """Integrate the google maps javascript tag"""
    def __init__(self, context, request, view, manager=None):
        super(JavascriptViewlet, self).__init__(context, request, view,
                                                manager=manager)
        self._param = None
        self._lang = None

    def index(self):
        if 'callback' in self.param():
            return ASYNC_SCRIPT%(self.src())
        return SCRIPT%(self.src())
    
    def protocol(self):
        #TODO: get it from self.request
        return 'http'
    
    def param(self):
        if self._param is None:
            config = self.configuration()
            param = {}
            param['v'] = config.version
            param['language'] = self.language()
            param['sensor'] = 'false'
            if config.sensor:
                param['sensor'] = 'true'
            param['libraries'] = ','.join(config.libraries)
            if config.callback:
                param['callback'] = config.callback
            self._param = urllib.urlencode(param)
        return self._param

    def configuration(self):
        registry = component.queryUtility(IRegistry)
        return registry.forInterface(interfaces.JavascriptLoadingConfiguration)
    
    def src(self):
        protocol = self.protocol()
        param = self.param()
        return protocol + BASE + param

    def language(self):
        if self._lang is None:
            state = component.getMultiAdapter((self.context, self.request),
                                              name=u'plone_portal_state')
            self._lang = state.language()
        return self._lang
    
