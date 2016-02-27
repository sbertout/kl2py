import os, sys, unittest, json
import FabricEngine.Core as core

class KLCodeFunctionArgument:
	def __init__(self, p):
		self.name = p['name']
		self.type = p['typeUserName']
		self.usage = p['usage'] # in out io

class KLCodeFunction:
	def __init__(self, el):
		self.name = el['name']
		self.arguments = []
		for p in el['params']:
			print ' - found param', p['name'], 'type=', p['typeUserName'], 'usage=', p['usage']
			self.arguments.append(KLCodeFunctionArgument(p))
		self.returnType = None if 'returnType' not in el else el['returnType']
	def getArgsDoc(self):
		argsNames = ''
		addComma = False
		for arg in self.arguments:
			argsNames += (', ' if addComma else '') + arg.type + ' ' + arg.name
			addComma = True
		return argsNames		
	def getArgs(self):
		argsNames = ''
		argsTypes = ''
		addComma = False
		for arg in self.arguments:
			argsNames += (', ' if addComma else '') + arg.name #+ ', ' if addComma else ' '
			argsTypes += arg.type + ' '
			addComma = True
		return argsNames, argsTypes
	# def generatePYConstructor(self, f, extensionName): # A VIRER !
	# 	argsNames, argsTypes = self.getArgs()
	# 	f.write('\tdef __init__(self%s):#%s\n' % ((', ' if argsNames != '' else '') + argsNames, argsTypes))
	# 	f.write('\t\tc = core.createClient()\n') # todo use singleton!!!
	# 	f.write('\t\tc.loadExtension("%s")\n' % extensionName) # todo use singleton!!!
	# 	f.write('\t\tself.klObj = self.c.RT.types.%s(%s)\n' % (self.name, argsNames)) # todo use singleton!!!
	def generatePYMethod(self, f):
		if self.name.startswith('_'): return
		argsNames, argsTypes = self.getArgs()
		# f.write('\tdef %s(self%s):#%s\n' % (self.name, (', ' if argsNames != '' else '') + argsNames, 'None' if argsTypes == '' else argsTypes))
		f.write('\tdef %s(self%s): #%s\n' % (self.name, (', ' if argsNames != '' else '') + argsNames, self.getArgsDoc()))
		returnCode = "" if self.returnType == None else 'return '
		returnCodeDoc = "" if self.returnType == None else self.returnType
		getSimpleType = "" if self.returnType == None else '.getSimpleType()'
		fuck = "''" if self.returnType == None else ("'%s'" % returnCodeDoc)
		if len(self.arguments) > 0: fuck = fuck +', '
		f.write('\t\t%sself.klObj.%s(%s%s)%s #%s\n' % (returnCode, self.name, fuck, argsNames, getSimpleType, returnCodeDoc))


class KLCodeObject:
	def __init__(self, name):
		self.name = name
		self.constructors = []
		self.methods = []
	def addConstructor(self, el):
		self.constructors.append(KLCodeFunction(el))
	def addMethod(self, el):
		self.methods.append(KLCodeFunction(el))
	def generatePYClass(self, location, extensionName):
		f = open(location + '/' + self.name + '.py', 'w')
		f.write('import FabricEngine.Core as core\n')
		f.write('class %s:\n' % self.name)
		constructorOptions = []
		for constructor in self.constructors:
			# constructor.generatePYConstructor(f, extensionName)
			constructorOptions.append(constructor.getArgsDoc())
		
		f.write('\tdef __init__(self, *args): #%s\n' % (constructorOptions))
		f.write('\t\tc = core.createClient()\n') # todo use singleton!!!
		f.write('\t\tc.loadExtension("%s")\n' % extensionName) # todo use singleton!!!
		f.write('\t\tself.klObj = c.RT.types.%s(*args)\n' % (self.name)) # todo use singleton!!!
		
		for method in self.methods:
			method.generatePYMethod(f)
		f.close()
		

class KLCodeExtension:
	def __init__(self, name):
		self.name = name
		self.objects = {}
		self.functions = []
	def addObject(self, el):
		objectName = el['name']
		if objectName in self.objects: return
		print '*** adding', objectName
		self.objects[objectName] = KLCodeObject(objectName)
	def getObject(self, objectName):
		print 'searching for ', objectName
		if objectName not in self.objects: 
			# print 'printing.....'
			# for o in  self.objects:
			# 	print o
			return None
		return self.objects[objectName]
	def addFunction(self, el):
		functionName = el['name']
		if functionName in self.objects: # we found a constructor!
			object = self.objects[functionName]
			object.addConstructor(el)
		else:
			# print 'FREEEE FUNCTION !!', functionName
			self.functions.append(KLCodeFunction(el))
	def generatePYModule(self, location):
		# extension.generatePYModule(location)
		print self.name
		print os.path.exists(location)
		if os.path.exists(location):
			os.rmdir(location)
		# print os.dir.exist(location)
		# print os.dir.exist(location)
		# print os.dir.exist(location)
		# print os.dir.exist(location)
		os.makedirs(location + '/' + self.name)
		f = open(location + '/' + self.name + '/__init__.py', 'w')
		# f.write('from . import uri\n')
		# f.write('from . import _functions\n')
		for objectName in self.objects:
			f.write('from %s import %s\n' % (objectName, objectName))
			self.objects[objectName].generatePYClass(location + '/' + self.name, self.name)
		f.write('\n')
		f.close()

class KLCodeStack:
	def __init__(self, extensionName, includeRequires):
		self.extensionName = extensionName
		self.includeRequires = includeRequires
		self.extensions = {}
		self.c = core.createClient()
		self.ast = self.c.getKLJSONAST('AST.kl', "require %s; operator entry() {}" % extensionName, True)
		self.data = json.loads(self.ast.getStringCString())['ast']
		self.parseData()
	def __addExtension(self, extensionName):
		if extensionName in self.extensions: return
		if self.includeRequires is False and extensionName != self.extensionName: return
		print '*** adding', extensionName
		self.extensions[extensionName] = KLCodeExtension(extensionName)
	def __getExtension(self, extensionName):
		if extensionName not in self.extensions: return None
		if self.includeRequires is False and extensionName != self.extensionName: return None
		print '*** getting', extensionName
		return self.extensions[extensionName]
	def parseData(self):
		# print 'parseData for KLCodeStack with sourceCode=', self.sourceCode, ' includeRequires=', self.includeRequires
		for elementList in self.data:
			# print type(elementList)
			if type(elementList) == list:
				self.parseList(elementList)
			# elif type(elementList) == dict:
			# 	self.parseDict(elementList)
			else:
				print 'WTF ? ******************** found ' + str(type(elementList))
			print '  '		
	# def parseDict(self, d):
	# 	for el in d:
	# 		print 'type = dict 2'
	# 		print type(el)
	# 		print el
	# 		# print '...'
	# 		# print d[el]
	# 		if el == 'requires':
	# 			# print len(d[el])
	# 			# self.extensions.append(KLCodeExtension(d[el][0]['name']))
	# 			self.__addExtension(d[el][0]['name']) # should not be needed at the end..
	# 		else:
	# 			print 'WTF x ? ******************** not yet suported ' + str(el)
	# 			print d[el]
	# 			print type(d[el])


	def parseList(self, l):
		for el in l: # todo rename l el etc..
			# print 'type = list 1'
			# print type(el)
			if type(el) == dict:
				# self.parseDict(el)
				# print ' &&&&&&&&&&&&&&&&&&&&&&&&&&&'
				# print el.keys()

				if 'owningExtName' in el:
					self.__addExtension(el['owningExtName'])

				if el['type'] == 'ASTObjectDecl' or el['type'] == 'ASTStructDecl':
					# print 'found Object', el['name'], 'from', el['owningExtName']
					extension = self.__getExtension(el['owningExtName'])
					if extension: extension.addObject(el)

				elif el['type'] == 'MethodOpImpl':
					# print el
					print 'found Method', el['name'], 'from', el['owningExtName'], 'on', el['thisType']
					# print  ' - params=', el['params'][0]['name'] #, 'type=', el['params']['typeUserName']
					# print el['params']
					# print len(el['params'])
					# print type(el['params'])
					for p in el['params']:
						print ' - found param', p['name'], 'type=', p['typeUserName'], 'usage=', p['usage']
					if 'returnType' in el:
						print ' - found returnType=', el['returnType']
					else:
						print ' - no return type'
					extension = self.__getExtension(el['owningExtName'])
					if extension:
						print el
						object = extension.getObject(el['thisType'])
						if object == None:
							print ' - error cannot process: ', el
							print ' certainly a method on an alias :('
						else:
							object.addMethod(el)

				elif el['type'] == 'Function':
					# print 'found Function', el['name'], 'from', el['owningExtName']
					# # print  ' - params=', el['params']['name'], 'type=', el['params']['typeUserName']
					# # print el
					# for p in el['params']:
					# 	print ' - found param', p['name'], 'type=', p['typeUserName'], 'usage=', p['usage']
					# if 'returnType' in el:
					# 	print ' - found returnType=', el['returnType']
					# else:
					# 	print ' - no return type'
					extension = self.__getExtension(el['owningExtName'])
					if extension: extension.addFunction(el)


				else:
					print el['type']

				# if 'owningExtName' in el:
				# 	# self.extensions.append(KLCodeExtension(el['owningExtName']))
				# 	self.__addExtension(el['owningExtName'])
				# print el.keys()
				# print el
				# print el['name']
			else:
				print 'WTF y ? ******************** not yet suported ' + str(el)
			# print '---'

	def generatePYModules(self, location):
		for extensionName  in self.extensions:
			extension = self.extensions[extensionName]
			extension.generatePYModule(location)
			# print extension.name
			# os.makedirs(location + '/' + extensionName)
			# f = open(location + '/' + extensionName + '/__init__.py', 'w')
			# f.write('from . import uri\n')
			# f.write('from . import _functions\n')
			# f.write('\n')
			# f.close()



