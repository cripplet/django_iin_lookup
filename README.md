django_iin_lookup
=================

IIN / BIN lookup for credit and debit cards

GET request wrapper for http://binlist.net, with DB acting as a caching backend to avoid duplicate GET requests.

Installation Requirements
----

* python-requests
* Django (add to INSTALLED_APPS in Django settings file)

```
./manage.py syncdb
```

Example
----

```
from django_iin_lookup import IINInfo
info = IINInfo.objects.fetch_iin(iin='123456')
```

Fields are specified by http://binlist.net, but guarantee

* `iin`, `bin`
* `card_brand' (i.e. VISA, DISCOVER, MASTERCARD)
* `card_sub_brand`
* `card_type` (i.e. CREDIT, DEBIT)
* `card_category` (e.g. STANDARD, PREMIUM)
