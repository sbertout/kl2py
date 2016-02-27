import os, sys, unittest, json
import FabricEngine.Core as core
# from mpc.kl.tessa.uri import *
from kl2py import *

class TestKLCodeStack(unittest.TestCase):

	def testFindRequires1(self):
		self.klcs = KLCodeStack('BasicExtension', False)
		self.assertEqual(self.klcs.extensions.keys(), ['BasicExtension'])
		self.__testBasicExtension()

	def testFindRequires2(self):
		self.klcs = KLCodeStack('BasicExtension', True)
		self.assertEqual(self.klcs.extensions.keys(), ['AnotherBasicExtension', 'BasicExtension'])
		self.__testBasicExtension()
		self.__testAnotherBasicExtension()
		self.klcs.generatePYModules('./tests/py')

	# def __testFEUnitTest(self):
	# 	self.klcs = KLCodeStack('FEUnitTest', False) # todo give 'BasicExtension' instead 
	# 	self.assertEqual(self.klcs.extensions.keys(), ['FEUnitTest'])
	# 	self.klcs.generatePYModules('./')		

	# def __testAlembicWrapper(self):
	# 	self.klcs = KLCodeStack('AlembicWrapper', False) # todo give 'BasicExtension' instead 
	# 	self.assertEqual(self.klcs.extensions.keys(), ['AlembicWrapper'])
	# 	self.klcs.generatePYModules('./')		

	# def __testMath(self):
	# 	self.klcs = KLCodeStack('Math', False) # todo give 'BasicExtension' instead 
	# 	self.assertEqual(self.klcs.extensions.keys(), ['Math'])
	# 	self.klcs.generatePYModules('./')	

	# def __testXXX(self):
	# 	self.klcs = KLCodeStack('Containers', False) # todo give 'BasicExtension' instead 
	# 	# self.assertEqual(self.klcs.extensions.keys(), ['Util'])
	# 	self.klcs.generatePYModules('./')		

	# def __testFindRequires2(self):
	# 	self.klcs = KLCodeStack('BasicExtension', True) # todo give 'BasicExtension' instead 
	# 	self.assertEqual(self.klcs.extensions.keys(), ['AnotherBasicExtension', 'BasicExtension'])
	# 	self.__testAnotherBasicExtension()
	# 	self.__testBasicExtension()
	# 	# self.klcs.generatePYModules('./')
	# 	# self.klcs.generatePYModules('./gen')
		
	def __testAnotherBasicExtension(self):
		# test AnotherBasicExtension
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects.keys(), ['Foo'])
		# test AnotherBasicExtension.Foo
		self.assertEqual(len(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].constructors), 2)
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].constructors[0].name, 'Foo')
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].constructors[0].returnType, None)
		self.assertEqual(len(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].constructors[0].arguments), 0)
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].constructors[1].name, 'Foo')
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].constructors[1].returnType, None)
		self.assertEqual(len(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].constructors[1].arguments), 1)
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].constructors[1].arguments[0].name, 'id')
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].constructors[1].arguments[0].type, 'Integer')
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].constructors[1].arguments[0].usage, 'in')
		self.assertEqual(len(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].methods), 2)
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].methods[0].name, 'getId')
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].methods[0].returnType, 'Integer')
		self.assertEqual(len(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].methods[0].arguments), 0)
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].methods[1].name, 'setId')
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].methods[1].returnType, None)
		self.assertEqual(len(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].methods[1].arguments), 1)
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].methods[1].arguments[0].name, 'id')
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].methods[1].arguments[0].type, 'Integer')
		self.assertEqual(self.klcs.extensions['AnotherBasicExtension'].objects['Foo'].methods[1].arguments[0].usage, 'in')

		# test AnotherBasicExtension.functions
		self.assertEqual(len(self.klcs.extensions['AnotherBasicExtension'].functions), 0)
		
	def __testBasicExtension(self):
		# test BasicExtension
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects.keys(), ['MyOBJ', 'Stuff', 'MyStruct'])
		# test BasicExtension.MyOBJ
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['MyOBJ'].constructors), 0)
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['MyOBJ'].methods), 0)
		# test BasicExtension.Stuff
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors), 3)
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[0].name, 'Stuff')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[0].returnType, None)
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[0].arguments), 0)
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[1].name, 'Stuff')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[1].returnType, None)
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[1].arguments), 1)
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[1].arguments[0].name, 'name')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[1].arguments[0].type, 'String')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[1].arguments[0].usage, 'in')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[2].name, 'Stuff')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[2].returnType, None)
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[2].arguments), 2)
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[2].arguments[0].name, 'name')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[2].arguments[0].type, 'String')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[2].arguments[0].usage, 'in')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[2].arguments[1].name, 'valid')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[2].arguments[1].type, 'Boolean')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].constructors[2].arguments[1].usage, 'in')
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['Stuff'].methods), 2)
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].methods[0].name, 'isValid')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].methods[0].returnType, 'Boolean')
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['Stuff'].methods[0].arguments), 0)
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].methods[1].name, 'getName')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].methods[1].returnType, 'String')
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['Stuff'].methods[1].arguments), 1)
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].methods[1].arguments[0].name, 'b')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].methods[1].arguments[0].type, 'Boolean')
		self.assertEqual(self.klcs.extensions['BasicExtension'].objects['Stuff'].methods[1].arguments[0].usage, 'in')
		# test BasicExtension.MyStruct
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['MyStruct'].constructors), 0)
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].objects['MyStruct'].methods), 0)
		# test BasicExtension.functions
		self.assertEqual(len(self.klcs.extensions['BasicExtension'].functions), 1)
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].name, 'floatingFunction')
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].returnType, 'String')
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].arguments[0].name, 's')
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].arguments[0].type, 'String')
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].arguments[0].usage, 'in')
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].arguments[1].name, 'b')
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].arguments[1].type, 'Boolean')
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].arguments[1].usage, 'io')
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].arguments[2].name, 'i')
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].arguments[2].type, 'Integer')
		self.assertEqual(self.klcs.extensions['BasicExtension'].functions[0].arguments[2].usage, 'out')



	def __test_URI(self):
		c = core.createClient() # todo use singleton
		# c.loadExtension('Math') # todo use extension manager to load extensions only once
		c.loadExtension('BasicExtension') # todo use extension manager to load extensions only once
		# ast = c.getKLJSONAST('AST.kl', "require Math; operator entry() {}", True)
		# data = json.loads(ast.getStringCString())['ast']
		# # print data 
		# for elementList in data:
		# 	print elementList
		# 	type = elementList['type']
		# 	print type

		sourceCode = "require BasicExtension; operator entry() {}"
		ast = c.getKLJSONAST('AST.kl', sourceCode, True)
		data = json.loads(ast.getStringCString())['ast']

		klObjects = {}
		# elementList = data[0]
		# print elementList
		for elementList in data:
			if type(elementList) == list:
				for el in elementList:
					print 'type = list 1'
					print el
					print '---'
					# print elementList[el]
			elif type(elementList) == dict:
				for el in elementList:
					print 'type = dict 2'
					print el
					print '...'
					print elementList[el]
			else:
				print '******************** found ' + str(type(elementList))
			print '  '
		    # type = elementList['type']
		    # print type

		# self.uri = self.c.RT.types.URI(strUri)

		# uri = URI('assetversion:MPC.rnd_dev.build.charBee:CharacterPkg.beeAvA:anim.13')
		# self.assertEqual(uri.facility(), 'MPC')
		# self.assertEqual(uri.job(), 'rnd_dev')
		# self.assertEqual(uri.scene(), 'build')
		# self.assertEqual(uri.shot(), 'charBee')
		# self.assertEqual(uri.assetType(), 'CharacterPkg')
		# self.assertEqual(uri.name(), 'beeAvA')
		# self.assertEqual(uri.stream(), 'anim')
		# self.assertEqual(uri.version(), 13)

if __name__ == '__main__':
    unittest.main()
