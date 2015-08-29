import logging
import cPickle as pickle

from datetime import datetime
from beaker.container import NamespaceManager, Container
from beaker.synchronization import null_synchronizer
from beaker.util import SyncDict
from pyhs import Manager



log = logging.getLogger(__name__)


def parse_servers_for_hs(servers):
    entries = []
    for server in servers:
        host, port = server.split(':')
        entries.append(('inet', host, int(port)))

    return entries


class HandlerSocketMySQLNamespaceManager(NamespaceManager):
    
    clients = SyncDict()
    _pickle = True

    def __init__(self, namespace, read_servers=None, write_servers=None, 
            database=None, table=None, index=None, data_dir=None, skip_pickle=False, **kw):
        
        self.database = database
        self.table = table
        self.index = index

        NamespaceManager.__init__(self, namespace)

        data_key = "hs:%s" % (database)

        def _initiate_connections(read_servers, write_servers):
            read_servers = parse_servers_for_hs(read_servers)
            write_servers = parse_servers_for_hs(write_servers)
            hs = Manager(read_servers, write_servers)
            return hs

        self.hs = HandlerSocketMySQLNamespaceManager.clients.get(data_key,
                    _initiate_connections, read_servers, write_servers)

    
    def _format_key(self, key):
        key = self.namespace
        return key


    def get_creation_lock(self, key):
        return null_synchronizer()

    
    def do_remove(self):
        raise NotImplementedError('Method not supported')


    def __getitem__(self, key):
        key = self._format_key(key)
        result = None
        try:
            result = self.hs.find(self.database, self.table, '=', ['id', 'data'], [key], self.index, 1)
        except Exception as e:
            log.error("Failure {} trying to find key {}".format(e.message, key))
            raise

        data = result
        if result:
            #TODO document result data structure
            data = pickle.loads(result[0][1][1])
        return data

    
    def __contains__(self, key):
        key = self._format_key(key)
        result = self.__getitem__(key)
        return result

    
    def has_key(self, key):
        key = self._format_key(key)
        return key in self

    
    def set_value(self, key, value, expiretime=None):
        value = pickle.dumps(value)
        key = self._format_key(key)
        created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ekey = self.has_key(key)
        try:
            if not ekey:
                self.hs.insert(self.database, self.table, [('id', key),('data',value), ('created', created)])
            else:
                self.hs.update(self.database, self.table, '=', ['id', 'data'], [key], [key, value])
        except Exception as e:
            log.error("Failure {} while setting value for key {}".format(e.message, key))
            raise
    
    def __setitem__(self, key, value):
        key = self._format_key(key)
        self.set_value(key, value)

    
    def __delitem__(self, key):
        key = self._format_key(key)
        self.hs.delete(self.database, self.table, '=', ['id'], [key])

    
    def keys(self):
        raise NotImplementedError('Method not supported')


class HandlerSocketMySQLContainer(Container):

    namespace_class = HandlerSocketMySQLNamespaceManager


