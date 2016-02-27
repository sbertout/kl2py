import unittest
import FabricEngine.Core as core
import AnotherBasicExtension as ABE

class TestABE(unittest.TestCase):

	def test(self):
		f = ABE.Foo(123)
		self.assertEqual(f.getId(), 123)
		f.setId(456)
		self.assertEqual(f.getId(), 456)

if __name__ == '__main__':
    unittest.main()