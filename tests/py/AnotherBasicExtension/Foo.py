import FabricEngine.Core as core
class Foo:
	def __init__(self, *args): #['', u'Integer id']
		c = core.createClient()
		c.loadExtension("AnotherBasicExtension")
		self.klObj = c.RT.types.Foo(*args)
	def getId(self): #
		return self.klObj.getId('Integer').getSimpleType() #Integer
	def setId(self, id): #Integer id
		self.klObj.setId('', id) #
