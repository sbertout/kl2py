import FabricEngine.Core as core
class Stuff:
	def __init__(self, *args): #['', u'String name', u'String name, Boolean valid']
		c = core.createClient()
		c.loadExtension("BasicExtension")
		self.klObj = c.RT.types.Stuff(*args)
	def isValid(self): #
		return self.klObj.isValid('Boolean').getSimpleType() #Boolean
	def getName(self, b): #Boolean b
		return self.klObj.getName('String', b).getSimpleType() #String
