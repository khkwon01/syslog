# -*- coding: utf-8 -*-


from azure.identity import ClientSecretCredential
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.privatedns import PrivateDnsManagementClient

class AzureMysql:

    __o_auth = None
    __o_mysql = None


    def __init__(self, v_config):
        self.__o_Config = v_config

        self.s_tenant = self.__o_Config['env']['tenant']
        self.s_qa_sub = self.__o_Config['env']['qa_subscr_id']
        self.s_prd_sub = self.__o_Config['env']['prd_subscr_id']
        self.s_clientid = self.__o_Config['app']['client']
        self.s_passwd = self.__o_Config['app']['passwd']

        self.__o_auth = ClientSecretCredential(tenant_id=self.s_tenant,
                                               client_id=self.s_clientid,
                                               client_secret=self.s_passwd)


    def get_db(self, v_env):
        o_servers = None
        s_subscr = None

        if v_env == 'qa':
           s_subscr = self.s_qa_sub
        else:
           s_subscr = self.s_prd_sub


        self.__o_mysql = MySQLManagementClient(self.__o_auth, s_subscr)
        o_servers = self.__o_mysql.servers.list()


        return o_servers


class AzureDns:
    __o_auth = None
    __o_dns = None


    def __init__(self, v_config):
        self.__o_Config = v_config

        self.s_tenant = self.__o_Config['env']['tenant']
        self.s_qa_sub = self.__o_Config['env']['qa_subscr_id']
        self.s_prd_sub = self.__o_Config['env']['prd_subscr_id']
        self.s_clientid = self.__o_Config['app']['client']
        self.s_passwd = self.__o_Config['app']['passwd']
        self.s_qa_rg = self.__o_Config['env']['qa_resource']
        self.s_prd_rg = self.__o_Config['env']['prd_resource']

        self.__o_auth = ClientSecretCredential(tenant_id=self.s_tenant,
                                               client_id=self.s_clientid,
                                               client_secret=self.s_passwd)

    def get_dns_mysql(self, v_env, v_server):
        o_prvdns = None
        s_subscr = None
        s_res = None
        s_link = "privatelink.mysql.database.azure.com"

        if v_env == 'qa' :
           s_subscr = self.s_qa_sub
           s_res = self.s_qa_rg
        else:
           s_subscr = self.s_prd_sub
           s_res = self.s_prd_rg

        self.__o_dns = PrivateDnsManagementClient(self.__o_auth, s_subscr)
        o_prvdns = self.__o_dns.record_sets.list(s_res, s_link, recordsetnamesuffix=v_server)
        o_prvdns = list(o_prvdns)


        return (o_prvdns[0].fqdn, o_prvdns[0].a_records[0].ipv4_address)