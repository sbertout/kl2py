import unittest
import FabricEngine.Core as core
import BasicExtension as BE

class TestBE(unittest.TestCase):

	def test(self):
		# f = BE.Stuff() # this crashes KL !
		# self.assertEqual(f.getName(True), 'lulu')
		f = BE.Stuff('lulu')
		self.assertEqual(f.getName(True), 'lulu')
		self.assertEqual(f.getName(False), 'noname')
		self.assertEqual(f.isValid(), True)
		f = BE.Stuff('lala', False)
		self.assertEqual(f.getName(True), 'lala')
		self.assertEqual(f.getName(False), 'noname')
		self.assertEqual(f.isValid(), False)

if __name__ == '__main__':
    unittest.main()