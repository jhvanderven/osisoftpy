import pprint
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from osisoftpy.api import API
from osisoftpy.dataarchive import DataArchive, DataArchives

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

prettyprint = pprint.PrettyPrinter(indent=4)

dev = 'https://api.osisoft.dstcontrols.local/piwebapi/'
prod = 'https://dev.dstcontrols.com/piwebapi/'
eecs = 'https://sbb03.eecs.berkeley.edu/piwebapi/'

# kerberos authentication example:
# api = API(url=prod, verifyssl=True, authtype='kerberos')

# pi_server = api.get_pi_server('megatron.dstcontrols.local')

# pi_points = api.get_pi_points('name:sinusoid or name:cdt158', count=5)

# basic authentication example:
api = API(url=eecs, verifyssl=True, authtype='basic', username='albertxu',
          password='Welcome2pi')

pi_server = api.get_data_archive_server('sbb03.eecs.berkeley.edu')
prettyprint.pprint(pi_server.name)
print(pi_server.name)

query = 'name:sinusoid or name:cdt158'
query = '*'
points = api.get_points(query=query, count=600,
                        scope='pi:{}'.format(pi_server.name))
#
# pi_servers = api.get_pi_servers()
#
# if pi_servers.__len__() > 0:
#
#     print('There are ' + pi_servers.__len__().__str__() + ' PI servers:')
#
#     for pi_server in pi_servers:
#         print('Server: {0}, WebID: {1}'.format(pi_server.name, pi_server.webid))
#
#
# print(pi_points)

# print(api)
#
# print (api.url)
#
# print(api.get_piservers())


# api.test_connection()

# bannoffee = DataArchiveServer('Bannoffee')
# print(bannoffee)
# print(bannoffee.name)


# help(pi_servers)

# # print api.getDataArchiveServer('dev.dstcontrols.com')
# print "{0} {1}".format('hello', 'world!')
#
# dir('a string')
#
#
# class Animal(object):
#     """Animal class has a docstring, here!"""
#
#     def __init__(self, name):
#         self.name = name
#
#     def talk(self):
#         """Have the animal emit a sound."""
#         print '{0} makes a generic animal sound!'.format(self.name)
#
# bear = Animal('Bear')
# bear.talk()
# help(bear.talk)
