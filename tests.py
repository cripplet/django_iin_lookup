import requests

from django.test import TestCase
from models import IINInfo

class TestIINInfo(TestCase):
	def test_iin(self):
		self.assertEqual(IINInfo.objects.count(), 0)
		info = IINInfo.objects.fetch_iin(iin='546116')
		self.assertEqual(IINInfo.objects.count(), 1)
		self.assertEqual(info.bin, '546116')
		self.assertEqual(info.iin, info.bin)
		self.assertEqual(info.card_brand, 'MASTERCARD')
		self.assertEqual(info.card_type, 'D')
		info = IINInfo.objects.fetch_iin(iin='546116')
		self.assertEqual(info.card_brand, 'MASTERCARD')
		self.assertEqual(info.card_type, 'D')
		info = IINInfo.objects.fetch_iin(iin='601100')
		self.assertEqual(IINInfo.objects.count(), 2)
		self.assertEqual(info.card_brand, 'DISCOVER')
		self.assertEqual(info.card_type, 'C')
		self.assertRaises(ValueError, IINInfo.objects.fetch_iin, 5)
		self.assertRaises(ValueError, IINInfo.objects.fetch_iin, '5')
		self.assertRaises(ValueError, IINInfo.objects.fetch_iin, '5461160')
		self.assertRaises(ValueError, IINInfo.objects.fetch_iin, '546116a')
		self.assertEqual(IINInfo.objects.count(), 2)
