# Ported to IronPython from original .rb at 
# http://blog.tomasm.net/category/ironruby/page/2/

import clr, sys
clr.AddReference("Microsoft.Scripting")
from Microsoft.Scripting import *

class REPL :
	def __init__ (self) :
		self.currentlanguage = "py"
		self.runtime = Hosting.ScriptRuntime.CreateFromConfiguration()
		self.engine = self.runtime.GetEngineByFileExtension(self.currentlanguage)
		self.scope = self.engine.CreateScope()
	def run (self) :
		while (True) :
			scriptinput = raw_input("{0}> ".format(self.currentlanguage))
			if scriptinput == "" :
				sys.exit()
			if scriptinput[0] == "#" :
				self.execute_command(scriptinput[1:])
			else :
				self.execute_code(self.read_code(scriptinput))
	def read_code(self, firstline):
		code = firstline
		while (True) :
			interactivecode = self.engine.CreateScriptSourceFromString(code, SourceCodeKind.InteractiveCode)
			parseresult = interactivecode.GetCodeProperties()
			if parseresult ==  ScriptCodeParseResult.Complete or parseresult == ScriptCodeParseResult.Invalid :
				return interactivecode
			else :
				scriptinput = raw_input("{0}| ".format(self.currentlanguage))
				if scriptinput == "" :
					return interactivecode
				else :
					code = code + "\n" + scriptinput #add a newline to ensure separation between lines
	def execute_code(self, source):
		try:
			source.Execute(self.scope)
		except Exception, e:
			print "{0}".format(e)
	def execute_command(self, command):
		if command == 'exit' :
			sys.exit()
		elif command == 'ls' :
			self.display_languages()
		else :
			self.engine = self.switch_language(command)
	def display_languages (self) :
		for i in self.engine.Runtime.Setup.LanguageSetups:
			print '{0}'.format(i.DisplayName)
	def switch_language(self, name) :
		old_engine = self.engine
		try :
			new_engine = self.runtime.GetEngineByFileExtension(name)
			self.currentlanguage = name
		except :
			print "{0} is an unknown script engine file association".format(name)
			new_engine = old_engine
		return new_engine

r = REPL()
r.run()