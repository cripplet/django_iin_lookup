import requests
from django.db import models, transaction

class IINInfoManager(models.Manager):
	class RateLimitExceeded(Exception):
		pass

	def fetch_iin(self, iin):
		try:
			return(super(IINInfoManager, self).get_queryset().get(iin=iin))
		except IINInfo.DoesNotExist:
			self.fetch_iin_query(iin)
			return(super(IINInfoManager, self).get_queryset().get(iin=iin))

	@transaction.atomic
	#iin is a string literal of length six
	def fetch_iin_query(self, iin=None):
		if not (isinstance(iin, str) and len(iin) == 6):
			raise IINInfo.DoesNotExist

		r = requests.get('http://www.binlist.net/json/' % iin)

		if r.status_code == 404:
			raise IINInfo.DoesNotExist
		if r.status_code == 403:
			raise IINInfoManager.RateLimitExceeded
		resp = r.json()
		iin_info = {}
		iin_info['iin'] = resp['bin']
		iin_info['card_brand'] = resp['brand'][0:127]
		iin_info['card_sub_brand'] = resp['sub_brand'][0:127]
		iin_info['card_type'] = 'C' if resp['type'] == 'CREDIT' else 'D'
		iin_info['card_category'] = resp['card_category'][0:127]
		iin_info['country_code'] = resp['country_code']
		iin_info['country_name'] = resp['country_name'][0:255]
		iin_info['bank_name'] = resp['bank'][0:255]

		IINInfo(**iin_info).save()
		

class IINInfo(models.Model):
	class DoesNotExist(Exception):
		pass

	objects = IINInfoManager()

	iin = models.CharField(max_length=6, help_text='First six digits of a credit / debit card number', primary_key=True)
	card_brand = models.CharField(max_length=127, db_index=True, help_text='e.g. VISA, MASTERCARD')
	card_sub_brand = models.CharField(max_length=127)
	card_type = models.CharField(max_length=1, choices=(('C', 'Credit'), ('D', 'Debit')), help_text='Card default type, oneof Credit / Debit', db_index=True)
	card_category = models.CharField(max_length=127)
	country_code = models.CharField(max_length=2, help_text='Country code, as per ISO3166-1 alpha2 designation', db_index=True)
	country_name = models.CharField(max_length=255, help_text='Fully qualified country name')
	bank_name = models.CharField(max_length=255, help_text='Issuing banking institution name')
