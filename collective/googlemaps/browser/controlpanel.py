from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from collective.googlemaps.interfaces import JavascriptLoadingConfiguration
from plone.z3cform import layout

class JavascriptPanelForm(RegistryEditForm):
    schema = JavascriptLoadingConfiguration

JavascriptControlPanelView = layout.wrap_form(JavascriptPanelForm,
                                              ControlPanelFormWrapper)
JavascriptControlPanelView.label = u"GoogleMaps Javascript settings"
