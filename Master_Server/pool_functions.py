import sqlite3
from server_functions import receive_data, send_data

database = 'crypto_database.db'
database_timeout = 10
PoolVersion = 0.1

def PoolList_NO_SEND()
    with sqlite3.connect(database, timeout=database_timeout) as conn:
        c2 = conn.cursor()
        c2.execute('''CREATE TABLE IF NOT EXISTS PoolList(identifier TEXT, name TEXT, ip TEXT, port TEXT, Status TEXT, hidden TEXT)''')

        c2.execute("SELECT name, ip, port, Status FROM PoolList WHERE hidden != 'ok'")
        info = c2.fetchall()
        info = (str(info)).replace('\n', '')

        return info

def PoolList(connection)
    send_data(data=PoolList_NO_SEND(), connection=connection)



class Pool_Function_class:

    def __init__(connection):
        self.poolID = None
        self.connection = connection

    def login(self):
        data = receive_data(connection=self.connection)

        try:
            info = str(data[1])

            info = ast.literal_eval(info)
            poolHost = info['host']
            poolPort = info['port']
            poolVersion_sent = info['version']
            poolID = info['identifier']
        except IndexError:
            send_data(data="NO,Not enough data", connection=self.connection)
            break

        if str(poolVersion_sent) == str(PoolVersion):
            with sqlite3.connect(database, timeout=database_timeout) as conn:
                c2 = conn.cursor()
                c2.execute('''CREATE TABLE IF NOT EXISTS PoolList(identifier TEXT, name TEXT, ip TEXT, port TEXT, Status TEXT, hidden TEXT)''')

                c2.execute("SELECT COUNT(identifier) FROM PoolList WHERE identifier = ?", (poolID,))
                if (c2.fetchall()[0][0]) == 0:
                    send_data(data="NO,Identifier not found", connection=self.connection)

                    break

                c2.execute("UPDATE PoolList SET ip = ?, port = ?, Status = ? WHERE identifier = ?",(poolHost, poolPort, "True", poolID))

                conn.commit()

                send_data(data="LoginOK", connection=self.connection)
        else:
            send_data(data="LoginFailed", connection=self.connection)


################################## Pool Login ####################################


            ################################## Pool add Node ####################################
            elif str(data[0]) == "PoolLoginAdd":
                try:
                    password = str(data[1])
                    info = str(data[2])
                except IndexError:
                    c.send(bytes("NO,Not enough data", encoding='utf8'))
                    break
                print("Debug 1")
                try:
                    info = ast.literal_eval(info)
                    poolName = info['name']
                    poolHost = info['host']
                    poolPort = info['port']
                    poolID = info['identifier']
                    poolHidden = info['hidden']
                except Exception as e:
                    print(e)
                    c.send(bytes(f"NO,Error: {e}", encoding='utf8'))
                    break
                print("Debug 2")

                if password == PoolPassword:
                    print("Debug 3")
                    with sqlite3.connect(database, timeout=database_timeout) as conn:
                        c2 = conn.cursor()
                        print("Debug 4")
                        c2.execute('''CREATE TABLE IF NOT EXISTS PoolList(identifier TEXT, name TEXT, ip TEXT, port TEXT, Status TEXT, hidden TEXT)''')
                        c2.execute("SELECT COUNT(identifier) FROM PoolList WHERE identifier = ?", (poolID,))
                        if (c2.fetchall()[0][0]) == 0:
                            c2.execute("INSERT INTO PoolList(identifier, name, ip, port, Status, hidden) VALUES(?, ?, ?, ?, ?, ?)",(poolID, poolName, poolHost, poolPort, "False", poolHidden))

                            conn.commit()
                            c.send(bytes("LoginOK", encoding='utf8'))

                        else:
                            c.send(bytes("NO,Identifier not found", encoding='utf8'))
                            break
                else:
                    c.send(bytes("NO,Password Incorrect", encoding='utf8'))


            ################################## Pool remove Node ####################################
            elif str(data[0]) == "PoolLoginRemove":
                try:
                    password = str(data[1])
                    info = str(data[2])
                except IndexError:
                    c.send(bytes("NO,Not enough data", encoding='utf8'))
                    break

                try:
                    info = ast.literal_eval(info)
                    poolID = info['identifier']
                except Exception as e:
                    print(e)
                    c.send(bytes(f"NO,Error: {e}", encoding='utf8'))
                    break

                if password == PoolPassword:
                    with sqlite3.connect(database, timeout=database_timeout) as conn:
                        c2 = conn.cursor()
                        c2.execute('''CREATE TABLE IF NOT EXISTS PoolList(identifier TEXT, name TEXT, ip TEXT, port TEXT, Status TEXT, hidden TEXT)''')
                        c2.execute("SELECT COUNT(identifier) FROM PoolList WHERE identifier = ?", (poolID,))
                        if (c2.fetchall()[0][0]) != 0:
                            c2.execute('''DELETE FROM PoolList WHERE identifier=?''',(poolID,))

                            conn.commit()
                            c.send(bytes("DeletedOK", encoding='utf8'))

                        else:
                            c.send(bytes("NO,Identifier not found", encoding='utf8'))
                            break
                else:
                    c.send(bytes("NO,Password Incorrect", encoding='utf8'))



            ################################## Pool Sync ####################################
            elif str(data[0]) == "PoolSync" and str(poolID) != "":
                try:
                    info = str(data[1])
                except IndexError:
                    c.send(bytes("NO,Not enough data", encoding='utf8'))
                    break

                try:
                    info = ast.literal_eval(info)
                    rewards = info['rewards']
                    blocks_to_add = int(info['blocks']['blockIncrease'])
                except Exception as e:
                    print(e)
                    c.send(bytes(f"NO,Error: {e}", encoding='utf8'))
                    break

                # ============

                blocks += blocks_to_add

                with sqlite3.connect(database, timeout=database_timeout) as conn:
                    datab = conn.cursor()
                    for user in rewards.keys():
                        datab.execute("UPDATE Users set balance = balance + ?  where username = ?", (float(rewards[user]), user))
                    conn.commit()

                # ============
                data_send = {"totalBlocks": blocks,
                            "diffIncrease": diff_incrase_per}

                data_send = (str(data_send)).replace("\'", "\"")

                c.send(bytes(f"SyncOK,{data_send}", encoding='utf8'))



            ################################## Pool Logout ####################################
            elif str(data[0]) == "PoolLogout":
                try:
                    poolID = str(data[1])
                except IndexError:
                    c.send(bytes("NO,Not enough data", encoding='utf8'))
                    break


                with sqlite3.connect(database, timeout=database_timeout) as conn:
                    c2 = conn.cursor()
                    c2.execute('''CREATE TABLE IF NOT EXISTS PoolList(identifier TEXT, name TEXT, ip TEXT, port TEXT, Status TEXT, hidden TEXT)''')

                    c2.execute("SELECT COUNT(identifier) FROM PoolList WHERE identifier = ?", (poolID,))
                    if (c2.fetchall()[0][0]) == 0:
                        c.send(bytes("NO,Identifier not found", encoding='utf8'))
                        break

                    c2.execute("UPDATE PoolList SET Status = ? WHERE identifier = ?",("False", poolID))

                    conn.commit()

                    c.send(bytes("LogoutOK", encoding='utf8'))








