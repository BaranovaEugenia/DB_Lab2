import psycopg2
from psycopg2 import Error
import model
import view
import time


class Controller:
    def __init__(self):
        self.v = view.View()
        self.m = model.Model()

    def print(self, table_name):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'Drink':
                self.v.print_drink(self.m.print_drink())
            elif t_name == 'Category':
                self.v.print_category(self.m.print_category())
            elif t_name == 'Drink_category':
                self.v.print_drink_category(self.m.print_drink_category())
            elif t_name == 'Order':
                self.v.print_order(self.m.print_order())

    def delete(self, table_name, key_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        k_name = self.v.valid.check_pk_name(table_name, key_name)
        if t_name and k_name:
            count = self.m.find(t_name, k_name, value)
            k_val = self.v.valid.check_pk(value, count)
            if k_val:
                if t_name == 'Drink' or t_name == 'Category':
                    if t_name == 'Drink':
                        count_d_c = self.m.find('Drink_category', 'drink_id', value)[0]
                    if t_name == 'Category':
                        count_d_c = self.m.find('Drink_category', 'category_id', value)[0]
                    if count_d_c:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'Drink_category':
                    count_o = self.m.find('Order', k_name, value)[0]
                    if count_o:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data(table_name, key_name, k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()

    def update_order(self, key: str, drink_category_id: str, customer_name: str):
        if self.v.valid.check_possible_keys('Order', 'id', key):
            count_o = self.m.find('Order', 'id', int(key))
            o_val = self.v.valid.check_pk(key, count_o)
        if self.v.valid.check_possible_keys('Drink_category', 'id', drink_category_id):
            count_d_c = self.m.find('Drink_category', 'id', int(drink_category_id))
            d_c_val = self.v.valid.check_pk(drink_category_id, count_d_c)

        if o_val and d_c_val and customer_name:
            try:
                self.m.update_data_order(o_val, d_c_val, customer_name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_drink_category(self, key: str, drink_id: str, category_id: str):
        if self.v.valid.check_possible_keys('Drink_category', 'id', key):
            count_d_c = self.m.find('Drink_category', 'id', int(key))
            d_c_val = self.v.valid.check_pk(key, count_d_c)
        if self.v.valid.check_possible_keys('Drink', 'id', drink_id):
            count_d = self.m.find('Drink', 'id', int(drink_id))
            d_val = self.v.valid.check_pk(drink_id, count_d)
        if self.v.valid.check_possible_keys('Category', 'id', category_id):
            count_c = self.m.find('Category', 'id', int(category_id))
            c_val = self.v.valid.check_pk(category_id, count_c)

        if d_c_val and d_val and c_val:
            try:
                self.m.update_data_drink_category(d_c_val, d_val, c_val,)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_drink(self, key: str, name: str, price: int):
        if self.v.valid.check_possible_keys('Drink', 'id', key):
            count_d = self.m.find('Drink', 'id', int(key))
            d_val = self.v.valid.check_pk(key, count_d)

        if d_val and name and price:
            try:
                self.m.update_data_drink(d_val, name, price)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_category(self, key: str, name: str):
        if self.v.valid.check_possible_keys('Category', 'id', key):
            count_c = self.m.find('Category', 'id', int(key))
            c_val = self.v.valid.check_pk(key, count_c)

        if c_val and name:
            try:
                self.m.update_data_category(c_val, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def insert_order(self, key: str, drink_category_id: str, customer_name: str):
        if self.v.valid.check_possible_keys('Order', 'id', key):
            count_o = self.m.find('Order', 'id', int(key))
        if self.v.valid.check_possible_keys('Drink_category', 'id', drink_category_id):
            count_d_c = self.m.find('Drink_category', 'id', int(drink_category_id))
            d_c_val = self.v.valid.check_pk(drink_category_id, count_d_c)

        if (not count_o or count_o == (0,)) and d_c_val and customer_name:
            try:
                self.m.insert_data_order(int(key), d_c_val, customer_name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_drink_category(self, key: str, drink_id: str, category_id: str):
        if self.v.valid.check_possible_keys('Drink_category', 'id', key):
            count_d_c = self.m.find('Drink_category', 'id', int(key))
        if self.v.valid.check_possible_keys('Drink', 'id', drink_id):
            count_d = self.m.find('Drink', 'id', int(drink_id))
            d_val = self.v.valid.check_pk(drink_id, count_d)
        if self.v.valid.check_possible_keys('Category', 'id', category_id):
            count_c = self.m.find('Category', 'id', int(category_id))
            c_val = self.v.valid.check_pk(category_id, count_c)

        if (not count_d_c or count_d_c == (0,)) and d_val and c_val:
            try:
                self.m.insert_data_drink_category(int(key), d_val, c_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_drink(self, key: str, name: str, price: int):
        if self.v.valid.check_possible_keys('Drink', 'id', key):
            count_d = self.m.find('Drink', 'id', int(key))

        if (not count_d or count_d == (0,)) and name and price:
            try:
                self.m.insert_data_drink(int(key), name, price)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_category(self, key: str, name: str):
        if self.v.valid.check_possible_keys('Category', 'id', key):
            count_c = self.m.find('Category', 'id', int(key))

        if (not count_c or count_c == (0,)) and name:
            try:
                self.m.insert_data_category(int(key), name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def generate(self, table_name: str, n: int):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'Order':
                self.m.order_data_generator(n)
            elif t_name == 'Drink_category':
                self.m.drink_category_data_generator(n)
            elif t_name == 'Drink':
                self.m.drink_data_generator(n)
            elif t_name == 'Category':
                self.m.category_data_generator(n)

    def search_two(self, table1_name: str, table2_name: str, table1_key: str, table2_key: str, search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and t2_n \
                and self.v.valid.check_key_names(t2_n, table2_key):
            start_time = time.time()
            result = self.m.search_data_two_tables(table1_name, table2_name, table1_key, table2_key,
                                                   search)
            self.v.print_time(start_time)

            self.v.print_search(result)

    def search_three(self, table1_name: str, table2_name: str, table3_name: str,
                     table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                     search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key):
            start_time = time.time()
            result = self.m.search_data_three_tables(table1_name, table2_name, table3_name,
                                                     table1_key, table2_key, table3_key, table13_key,
                                                     search)
            self.v.print_time(start_time)
            self.v.print_search(result)

    def search_four(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                    table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                    table4_key: str, table24_key: str,
                    search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        t4_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and self.v.valid.check_key_names(t2_n, table24_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key) \
                and t4_n and self.v.valid.check_key_names(t4_n, table4_key) \
                and self.v.valid.check_key_names(t4_n, table24_key):

            start_time = time.time()
            result = self.m.search_data_all_tables(table1_name, table2_name, table3_name, table4_name,
                                                   table1_key, table2_key, table3_key, table13_key,
                                                   table4_key, table24_key,
                                                   search)
            self.v.print_time(start_time)
            self.v.print_search(result)
