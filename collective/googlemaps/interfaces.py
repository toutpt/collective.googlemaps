from zope import interface
from zope import schema

class IGoogleMapsLayer(interface.Interface):
    """Browser layer"""

class JavascriptLoadingConfiguration(interface.Interface):
    
    sensor = schema.Bool(title=u"Sensor",
                         default=False)
    
    libraries = schema.List(title=u"Libraries",
                            value_type=schema.ASCIILine(title=u"Library"),
                            default=['googleearth'])

    version = schema.ASCIILine(title=u"Version",
                         default="3.4")

    callback = schema.ASCIILine(title=u"Callback",
                                description=u"Make the javascript load async and use this callback function",
                                required=False)
