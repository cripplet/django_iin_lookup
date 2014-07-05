import requests

from django.test import TestCase
from models import IINInfo

class TestIINInfo(TestCase):
	def test_iin(self):
		self.assertEqual(IINInfo.objects.count(), 0)
		info = IINInfo.fetch_iin(iin='546116')
		self.assertEqual(IINInfo.objects.count(), 1)
		self.assertEqual(info.type, 'D')
