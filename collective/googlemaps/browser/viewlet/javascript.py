from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.registry.interfaces import IRegistry
from zope import component
from collective.googlemaps import interfaces
import urllib

BASE = "://maps.googleapis.com/maps/api/js?"

ASYNC_SCRIPT = """
function googlemapsAsync() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "%s";
  document.body.appendChild(script);
}

$(function() {
   googlemapsAsync();
});
"""

class JavascriptViewlet(common.ViewletBase):
    """Integrate the google maps javascript tag"""
    def __init__(self, context, request, view, manager=None):
        super(JavascriptViewlet, self).__init__(context, request, view,
                                                manager=manager)
        self._param = None

    def index(self):
        if 'callback' in self.param():
            return ViewPageTemplateFile('javascript_async.pt')(self)
        return ViewPageTemplateFile('javascript.pt')(self)
    
    def protocol(self):
        #TODO: get it from self.request
        return 'http'
    
    def param(self):
        if self._param is None:
            config = self.configuration()
            param = {}
            param['v'] = config.version
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

    def async(self):
        return ASYNC_SCRIPT%(self.src())
