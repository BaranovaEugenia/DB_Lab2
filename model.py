import psycopg2 as ps


class Model:
    def __init__(self):
        self.conn = None
        try:
            self.conn = ps.connect(
                dbname="coffee_shop",
                user='postgres',
                password="090902",
                host='127.0.0.1',
                port="5432",
            )
        except(Exception, ps.DatabaseError) as error:
            print("[INFO] Error while working with Postgresql", error)

    def request(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return True
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchall()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get_el(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchone()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def count(self, table_name: str):
        return self.get_el(f"select count(*) from public.\"{table_name}\"")

    def find(self, table_name: str, key_name: str, key_value: int):
        return self.get_el(f"select count(*) from public.\"{table_name}\" where {key_name}={key_value}")

    def max(self, table_name: str, key_name: str):
        return self.get_el(f"select max({key_name}) from public.\"{table_name}\"")

    def min(self, table_name: str, key_name: str):
        return self.get_el(f"select min({key_name}) from public.\"{table_name}\"")

    def print_category(self) -> None:
        return self.get(f"SELECT * FROM public.\"Category\"")

    def print_drink(self) -> None:
        return self.get(f"SELECT * FROM public.\"Drink\"")

    def print_drink_category(self) -> None:
        return self.get(f"SELECT * FROM public.\"Drink_category\"")

    def print_order(self) -> None:
        return self.get(f"SELECT * FROM public.\"Order\"")

    def delete_data(self, table_name: str, key_name: str, key_value) -> None:
        self.request(f"DELETE FROM public.\"{table_name}\" WHERE {key_name}={key_value};")

    def update_data_category(self, key_value: int, name: str) -> None:
        self.request(f"UPDATE public.\"Category\" SET name=\'{name}\' WHERE id={key_value};")

    def update_data_drink(self, key_value: int, name: str, price: int) -> None:
        self.request(f"UPDATE public.\"Drink\" SET name=\'{name}\', price=\'{price}\' WHERE id={key_value};")

    def update_data_drink_category(self, key_value: int, drink_id: int, category_id: int) -> None:
        self.request(f"UPDATE public.\"Drink_category\" SET drink_id=\'{drink_id}\', category_id=\'{category_id}\' "
                     f"WHERE id={key_value};")

    def update_data_order(self, key_value: int, drink_category_id: int, customer_name: str) -> None:
        self.request(f"UPDATE public.\"Order\" SET drink_category_id=\'{drink_category_id}\', "
                     f"customer_name=\'{customer_name}\' WHERE id={key_value};")

    def insert_data_category(self, key_value: int, name: str) -> None:
        self.request(f"insert into public.\"Category\" (id, name) "
                     f"VALUES ({key_value}, \'{name}\');")

    def insert_data_drink(self, key_value: int, name: str, price: int) -> None:
        self.request(f"insert into public.\"Drink\" (id, name, price) "
                     f"VALUES ({key_value}, \'{name}\', \'{price}\');")

    def insert_data_drink_category(self, key_value: int, drink_id: int, category_id: int) -> None:
        self.request(f"insert into public.\"Drink_category\" (id, drink_id, category_id) "
                     f"VALUES ({key_value}, \'{drink_id}\', \'{category_id}\');")

    def insert_data_order(self, key_value: int, drink_category_id: int, customer_name: str) -> None:
        self.request(f"insert into public.\"Order\" (id, drink_category_id, customer_name) "
                     f"VALUES ({key_value}, \'{drink_category_id}\', \'{customer_name}\');")

    def drink_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Drink\""
                         "select (SELECT MAX(id)+1 FROM public.\"Drink\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''), "
                         "FLOOR(RANDOM()*(100000-1)+1);")

    def order_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Order\" select (SELECT MAX(id)+1 FROM public.\"Order\"), "
                         "(SELECT id FROM public.\"Drink_category\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"Drink_category\")-1)))), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(15-5)+5):: integer)), '');")

    def category_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Category\""
                         "select (SELECT MAX(id)+1 FROM public.\"Category\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), '');")


    def drink_category_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Drink_category\" "
                         "select (SELECT (MAX(id)+1) FROM public.\"Drink_category\"), "
                         "(SELECT id FROM public.\"Drink\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"Drink\")-1)))), "
                         "(SELECT id FROM public.\"Category\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"Category\")-1))));")



    def search_data_two_tables(self, table1_name: str, table2_name: str, table1_key, table2_key,
                               search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" "
                        f"where {search}")

    def search_data_three_tables(self, table1_name: str, table2_name: str, table3_name: str,
                                 table1_key, table2_key, table3_key, table13_key,
                                 search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" inner join public.\"{table3_name}\" as three "
                        f"on three.\"{table3_key}\"=one.\"{table13_key}\""
                        f"where {search}")

    def search_data_all_tables(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                               table1_key, table2_key, table3_key, table13_key,
                               table4_key, table24_key,
                               search: str):
        return self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                        f"on one.\"{table1_key}\"=two.\"{table2_key}\" inner join public.\"{table3_name}\" as three "
                        f"on three.\"{table3_key}\"=one.\"{table13_key}\" inner join public.\"{table4_name}\" as four "
                        f"on four.\"{table4_key}\"=two.\"{table24_key}\""
                        f"where {search}")
