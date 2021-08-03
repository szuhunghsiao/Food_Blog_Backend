# Food_Blog_Backend
## Basic info in the database
The ingredients, serves, and measure will be automatically enter in the database.
The user can add more meals serves time, ingredients list, and measure units manually into the code.

## User input recipes
To enter the recipes, enter the following code
```
> python blog.py database.db
```
The database.db is required argument for this program to store data.
Example after executed the program
```
Pass the empty recipe name to exit.
Recipe name: > Milkshake
Recipe description: > Blend all ingredients and put in the fridge.
1) breakfast 2) brunch 3) lunch 4)supper
When the dish can be served: > 1 3 4
Input quantity of ingredient <press enter to stop>: > 500 ml milk
Input quantity of ingredient <press enter to stop>: > 1 cup strawberry
Input quantity of ingredient <press enter to stop>: > 1 tbsp sugar
Input quantity of ingredient <press enter to stop>: >
```
This will store the recipe "Milkshake" to the database and the description will be store in the same table.
The serving meal time will be store in another table.

## User searching recipes
There will be two more arguments need to be enter for searching the recipe
Example execute command
```
> python blog.py database.db --ingredients="sugar,milk" --meals="breakfast,brunch"
```
This line will search the ingredients and meals that match the database and will output the recipe name.
