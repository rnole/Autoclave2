import wx
import unittest
from AutoclaveGestion import AutoclaveGestion

class TestMainFrame(unittest.TestCase):

	def setUp(self):
		app = wx.PySimpleApp()
		self.myframe = AutoclaveGestion.MainFrame()		

	def tearDown(self):
		self.myframe.Destroy()

	def test_CheckBoxes(self):
		self.myframe.productionCheckbox.SetValue(True)
		self.myframe.OnProductionCheckbox(None)
		self.assertEqual(self.myframe.frameModel.productionCheckbox_value, True)
		self.assertEqual(self.myframe.frameModel.qualityCheckbox_enabled, False)

		self.myframe.qualityCheckbox.SetValue(True)
		self.myframe.OnQualityCheckbox(None)
		self.assertEqual(self.myframe.frameModel.qualityCheckbox_value, True)
		self.assertEqual(self.myframe.frameModel.productionCheckbox_enabled, False)

if __name__ == '__main__':
	unittest.main()

