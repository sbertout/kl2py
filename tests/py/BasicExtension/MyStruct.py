import FabricEngine.Core as core
class MyStruct:
	def __init__(self, *args): #[]
		c = core.createClient()
		c.loadExtension("BasicExtension")
		self.klObj = c.RT.types.MyStruct(*args)
