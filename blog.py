import sqlite3
import argparse


class SqliteData:

    def __init__(self):
        self.conn = sqlite3.connect('food_blog.db')
        self.cur = self.conn.cursor()

    def create_table(self):
        try:
            self.cur.execute('PRAGMA foreign_keys = ON;')
            self.cur.execute('''CREATE TABLE meals (
                                    meal_id INT PRIMARY KEY,
                                    meal_name TEXT NOT NULL UNIQUE)''')
            self.cur.execute('''CREATE TABLE ingredients (
                                    ingredient_id INT PRIMARY KEY,
                                    ingredient_name TEXT NOT NULL UNIQUE)''')
            self.cur.execute('''CREATE TABLE measures (
                                    measure_id INT PRIMARY KEY,
                                    measure_name TEXT UNIQUE)''')
            self.cur.execute('''CREATE TABLE recipes (
                                    recipe_id INT PRIMARY KEY,
                                    recipe_name TEXT NOT NULL,
                                    recipe_description TEXT)''')
            self.cur.execute('''CREATE TABLE serve (
                                    serve_id INT PRIMARY KEY,
                                    meal_id INT NOT NULL,
                                    recipe_id INT NOT NULL,
                                    FOREIGN KEY(meal_id) REFERENCES meals(meal_id),
                                    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id))''')
            self.cur.execute('''CREATE TABLE quantity (
                                    quantity_id INT PRIMARY KEY,
                                    quantity INT NOT NULL,
                                    recipe_id INT NOT NULL,
                                    measure_id INT NOT NULL,
                                    ingredient_id INT NOT NULL,
                                    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
                                    FOREIGN KEY (measure_id) REFERENCES measures(measure_id),
                                    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id))''')
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)

    def insert_table(self, t_name, t_id, t_value):
        try:
            self.cur.execute(f'INSERT INTO {t_name} VALUES (?, ?)', (t_id, str(t_value)))
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)

    def insert_table2(self, t_name, t_id, t_value, t_value2):
        try:
            self.cur.execute(f'INSERT INTO {t_name} VALUES (?, ?, ?)', (t_id, str(t_value), str(t_value2)))
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)

    def insert_table3(self, t_name, t_id, t_value, t_value2, t_value3, t_value4):
        try:
            self.cur.execute(f'INSERT INTO {t_name} VALUES (?, ?, ?, ?, ?)',
                             (t_id, t_value, t_value2, t_value3, t_value4))
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)

    def load_table(self, t_name):
        try:
            self.cur.execute(f'SELECT * FROM {t_name}')
            records = self.cur.fetchall()
            return records
        except sqlite3.Error as error:
            print(error)


def ing_input():
    ing_amount = input('Input quantity of ingredient <press enter to stop>: ')
    if len(ing_amount):
        ing_amount = ing_amount.split(' ')
        if len(ing_amount) == 3:
            return int(ing_amount[0]), ing_amount[1], ing_amount[2]
        elif len(ing_amount) == 2:
            return int(ing_amount[0]), 'NULL', ing_amount[1]
    else:
        return 0, 'NULL', 'NULL'


parser = argparse.ArgumentParser()
parser.add_argument('database')
parser.add_argument('--ingredients')
parser.add_argument('--meals')
args = parser.parse_args()

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

test = SqliteData()
if not args.ingredients:
    test.create_table()
    for key, value in data.items():
        for i in range(len(value)):
            test.insert_table(key, i + 1, value[i])
    exit_status = False
    recipes_data = test.load_table('recipes')
    num_recipes = len(recipes_data)
    num_serve = 0
    num_quantity = 0
    measures = test.load_table('measures')
    measure_list = [measures[i][1] for i in range(len(measures))]
    ingredients = test.load_table('ingredients')
    ing_list = [ingredients[i][1] for i in range(len(ingredients))]
    print('Pass the empty recipe name to exit')
    while not exit_status:
        name = input('Recipe name:')
        if len(name) == 0:
            exit_status = True
        else:
            num_recipes += 1
            description = input('Recipe description')
            test.insert_table2('recipes', num_recipes, name, description)
            print('1) breakfast 2) brunch 3) lunch 4) supper')
            serve_time = input('When the dish can be served: ').split(' ')
            for i in serve_time:
                num_serve += 1
                test.insert_table2('serve', num_serve, int(i), num_recipes)
            get_ing = True
            while get_ing:
                ing_n, ing_m, ing_i = ing_input()
                if ing_n == 0:
                    get_ing = False
                m_str = [i for i in measure_list if ing_m in i]
                print(len(m_str))
                i_str = [j for j in ing_list if ing_i in j]
                if (len(m_str) == 1 or len(m_str) == 8) and len(i_str) == 1:
                    print('ADDING TO LIST')
                    num_quantity += 1
                    m_id = measure_list.index(m_str[0]) + 1
                    i_id = ing_list.index(i_str[0]) + 1
                    test.insert_table3('quantity', num_quantity, ing_n, num_recipes, m_id, i_id)
                elif len(m_str) == 0 and len(i_str) == 1:
                    print('Adding to List')
                    num_quantity += 1
                    m_id = 8
                    i_id = ing_list.index(i_str[0]) + 1
                    test.insert_table3('quantity', num_quantity, ing_n, num_recipes, m_id, i_id)
                else:
                    print('The measure is not conclusive!')
    test.conn.close()
else:
    quantity_id = test.load_table('quantity')
    ingredient_dict = {t[1]: t[0] for t in test.load_table('ingredients')}
    meal_dict = {t[1]: t[0] for t in test.load_table('meals')}
    recipes_dict = {t[1]: t[0] for t in test.load_table('recipes')}
    com_ingredient = args.ingredients.split(',')
    for i in com_ingredient:
        if i not in data['ingredients']:
            print('There are no such recipes in the database')
            test.conn.close()
            exit()
    com_ingredient_id = [str(ingredient_dict[i]) for i in com_ingredient]
    com_meal = args.meals.split(',')
    com_meal_id = [str(meal_dict[i]) for i in com_meal]
    combine_list1 = []
    combine_list2 = []
    select_recipe_id = []
    select_recipe = []
    for i in com_meal_id:
        test.cur.execute('''SELECT recipe_id FROM serve WHERE meal_id IN (?)''', (i,))
        combine_list1.append(test.cur.fetchall())
    print(combine_list1)
    test_list1 = [i for j in combine_list1 for i in j]
    print(test_list1)
    for j in com_ingredient_id:
        test.cur.execute('''SELECT recipe_id FROM quantity WHERE ingredient_id IN (?)''', (j,))
        combine_list2.append(test.cur.fetchall())
    print(combine_list2)
    for k in test_list1:
        check = 0
        for i in range(len(combine_list2)):
            if k in combine_list2[i]:
                check += 1
            else:
                break
            if check == len(combine_list2):
                select_recipe_id.append(str(k[0]))
    testing = ','.join(select_recipe_id)
    #print(testing)
    test.cur.execute(f'SELECT recipe_name FROM recipes WHERE recipe_id IN ({testing})')
    print(test.cur.fetchall())
    test.conn.close()
