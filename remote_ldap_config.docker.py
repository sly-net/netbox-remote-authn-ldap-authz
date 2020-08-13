import importlib.util
import sys

try:
  spec = importlib.util.spec_from_file_location('remote_ldap_config', '/etc/netbox/config/remote_ldap_config.py')
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  sys.modules['netbox.remote_ldap_config'] = module
except:
  raise ImportError('')
