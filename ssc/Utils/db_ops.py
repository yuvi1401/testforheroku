import psycopg2
import aiopg


from ssc.dbconfig import dsn


async def get_user_id(username):
    connection = None
    try:
        pool = await aiopg.create_pool(dsn)
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                get_user_id_sql = "select user_id from users where username=%s"
                await cursor.execute(get_user_id_sql, (username,))
                user_id = await cursor.fetchone()
    except (Exception, psycopg2.Error) as error:
        print("psycopg2 error: ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            if (user_id is None):
                return -1
            else:
                return user_id[0]
        else:
            return -1


async def is_user_admin(user_id, workspace_id):
    connection = None
    try:
        pool = await aiopg.create_pool(dsn)
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                is_user_admin_sql = "select * from workspace_users where user_id=%s " \
                            "and workspace_id=%s and is_admin=True"
                await cursor.execute(is_user_admin_sql, (user_id, workspace_id))
                count = cursor.rowcount
                # print(count)
    except (Exception, psycopg2.Error) as error:
        print("psycopg2 error: ", error)
        count = 0
    finally:
        if (connection):
            cursor.close()
            connection.close()
            return count
        else:
            return 0


async def get_workspace_id(workspace):
    connection = None

    try:
        pool = await aiopg.create_pool(dsn)
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                get_workspace_id_sql = "select workspace_id from workspaces where name=%s"
                await cursor.execute(get_workspace_id_sql, (workspace,))
                workspace_id = await cursor.fetchone()


    except (Exception, psycopg2.Error) as error:
        print("psycopg2 error: ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            if (workspace_id is None):
                return -1
            else:
                return workspace_id[0]
        else:
            return -1


# import psycopg2
# from ssc.dbconfig import user, password, database
#
# def get_user_id(username):
#     try:
#         connection = psycopg2.connect(
#             user=user,
#             password=password,
#             database=database)
#         cursor = connection.cursor()
#
#         get_user_id_sql = "select user_id from users where username=%s"
#
#         cursor.execute(get_user_id_sql, (username,))
#         user_id = cursor.fetchone()
#
#         if (user_id is None):
#             return -1
#
#     except (Exception, psycopg2.Error) as error:
#         print("Error while connecting to PostgreSQL", error)
#     finally:
#         if (connection):
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")
#
#     return user_id[0]
#
#
# def is_user_admin(user_id, workspace_id):
#     try:
#         connection = psycopg2.connect(
#             user=user,
#             password=password,
#             database=database)
#         cursor = connection.cursor()
#
#         is_user_admin_sql = "select * from workspace_users where user_id=%s " \
#                             "and workspace_id=%s and is_admin=True"
#
#         cursor.execute(is_user_admin_sql, (user_id, workspace_id))
#         count = cursor.rowcount
#
#
#     except (Exception, psycopg2.Error) as error:
#         print("Error while connecting to PostgreSQL", error)
#     finally:
#         if (connection):
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")
#
#     return count
#
#
# def get_workspace_id(workspace):
#     try:
#         connection = psycopg2.connect(
#             user=user,
#             password=password,
#             database=database)
#         cursor = connection.cursor()
#
#         get_workspace_id_sql = "select workspace_id from workspaces where name=%s"
#
#         cursor.execute(get_workspace_id_sql, (workspace,))
#         workspace_id = cursor.fetchone()
#
#         if (workspace_id is None):
#             return -1
#
#     except (Exception, psycopg2.Error) as error:
#         print("Error while connecting to PostgreSQL", error)
#     finally:
#         if (connection):
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")
#
#     return workspace_id[0]
#
#
#
