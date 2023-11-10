import time
from pymongo import MongoClient


def connect_mongodb():
    try:
        connection_uri = "mongodb://SP_DBA_SA_ACCOUNT:!Q%40W#E$R%25T6y7u8i9o0p" \
                         "@13.52.144.222:48017/?authSource=admin"
        mongo_client = MongoClient(connection_uri)
        testDb = mongo_client.tquens_test_db

        global isaac_table
        isaac_table = testDb.isaac

        return isaac_table

    except Exception as e:
        print(e)
        print("Issue ::: connect_mongodb")


# def main():
#     connect_mongodb()
#     inserObject = {
#         "title": "123123",
#         "price": "123123"
#     }

#     isaac_table.insert_one(inserObject)
#     all_data = list(isaac_table.find({}))
#     for data in all_data:
#         try:
#             print(data)
#             # time.sleep(3)
#         except Exception as e:
#             print(e)

#     print("done !!!")


# if __name__ == '__main__':
#     start_time = time.time()
#     done_flag = None
#     while done_flag is None:
#         try:
#             main()
#             done_flag = True
#         except Exception as e:
#             print(e)
#     print("--- Execution Time : %s seconds ---" % (time.time() - start_time))
