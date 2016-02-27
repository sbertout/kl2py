import FabricEngine.Core as core
class MyOBJ:
	def __init__(self, *args): #[]
		c = core.createClient()
		c.loadExtension("BasicExtension")
		self.klObj = c.RT.types.MyOBJ(*args)
