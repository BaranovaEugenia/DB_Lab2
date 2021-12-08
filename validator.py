class Validator:
    def __init__(self):
        self.error = ''
        self.er_flag = False

    def check_table_name(self, arg: str):
        if arg in ['Category', 'Drink', 'Drink_category', 'Order']:
            return arg
        else:
            self.er_flag = True
            self.error = f'table {arg} does not exist in the database'
            print(self.error)
            return False

    def check_pkey_value(self, arg: str, min_val: int, max_val: int):
        try:
            value = int(arg)
        except ValueError:
            self.er_flag = True
            self.error = f'{arg} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if min_val <= value <= max_val:
                return value
            else:
                self.er_flag = True
                self.error = f'{arg} is not existing primary key value'
                print(self.error)
                return 0

    def check_pk_name(self, table_name: str, key_name: str):
        if table_name == 'Category' and key_name == 'id' \
                or table_name == 'Drink' and key_name == 'id' \
                or table_name == 'Drink_category' and key_name == 'id' \
                or table_name == 'Order' and key_name == 'id':
            return key_name
        else:
            self.er_flag = True
            self.error = f'key {key_name} is not a primary key of table {table_name}'
            print(self.error)
            return False

    def check_pk(self, val, count):
        try:
            value = int(val)
        except ValueError:
            self.er_flag = True
            self.error = f'{val} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if count and not count == (0,):
                return value
            else:
                return 0

    def check_key_names(self, table_name: str, key: str):
        if table_name == 'Category' and key in ['id', 'name']:
            return True
        elif table_name == 'Drink' and key in ['id', 'name', 'price']:
            return True
        elif table_name == 'Drink_category' and key in ['id', 'drink_id', 'category_id']:
            return True
        elif table_name == 'Order' and key in ['id', 'drink_category_id ', 'customer_name']:
            return True
        else:
            self.er_flag = True
            self.error = f'{key} is not correct name for {table_name} table'
            print(self.error)
            return False

    def check_possible_keys(self, table_name: str, key: str, val):
        if table_name == 'Category':
            if key in ['id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['name']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Category table'
                print(self.error)
                return False
        elif table_name == 'Drink':
            if key in ['id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'name':
                return True
            elif key == 'price':
                try:
                    value = float(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct price value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Drink table'
                print(self.error)
                return False
        elif table_name == 'Drink_category':
            if key in ['id', 'drink_id', 'category_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Product table'
                print(self.error)
                return False
        elif table_name == 'Order':
            if key in ['id', 'drink_category_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['customer_name']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Order table'
                print(self.error)
                return False