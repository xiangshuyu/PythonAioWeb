from ldap3 import Server, Connection, SUBTREE

ldap_host = 'localhost'
ldap_port = 389
ldap_admin_user = 'cn=admin,dc=www,dc=admin,dc=me'
ldap_admin_password = 'xiangshuyu'
ldap_base_search = 'dc=www,dc=admin,dc=me'


def ldap_auth(username, password):
    server = Server(host=ldap_host, port=ldap_port, use_ssl=False, get_info='ALL')
    # 这个首先看看你的admin能不能正常connect
    ldap_admin_connection = Connection(server, user=ldap_admin_user, password=ldap_admin_password, auto_bind='NONE',
                                       version=3, authentication='SIMPLE', client_strategy='SYNC', auto_referrals=True,
                                       check_names=True, read_only=False, lazy=False, raise_exceptions=False)
    # 连上以后必须bind才能有值
    ldap_admin_connection.bind()

    # 这个是为了查询你输入的用户名的入口搜索地址
    res = ldap_admin_connection.search(search_base=ldap_base_search,
                                       search_filter='(uid={})'.format(username),
                                       search_scope=SUBTREE,
                                       attributes=['cn', 'uid', 'userPassword'])  # 这里可能由你自己选择

    if res:
        entry = ldap_admin_connection.response[0]
        dn = entry['dn']
        attr_dict = entry['attributes']
        print(attr_dict)

        try:
            # 这个connect是通过你的用户名和密码还有上面搜到的入口搜索来查询的
            user_conn = Connection(server, user=dn, password=password, check_names=True, lazy=False, raise_exceptions=False)
            user_conn.bind()
            print(user_conn.result)
            # 正确-success 不正确-invalidCredentials
            if user_conn.result["description"] == "success":
                print("yes")
            elif user_conn.result["description"] == "invalidCredentials":
                print("invalidCredentials")
            else:
                raise RuntimeError("can't connect to ldap server")
        except Exception as e:
            print(e)


ldap_auth("stonker", "123456")
