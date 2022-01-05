# Category class that instantiates objects based on budget categories
class Category:
    def __init__(self, category, ledger=None):
        if ledger is None:  # instant variable ledger starts as an empty list
            self.ledger = []
        self.category = category  # budget category

    # print method of the object
    def __str__(self):

        # header is the budget category between asterisks with maximum of 30 characters
        asterisks = '******************************'
        asterisks = asterisks[:len(asterisks) - len(self.category)]
        if len(asterisks) % 2 == 0:
            header = asterisks[:len(asterisks) // 2] + self.category + asterisks[len(asterisks) // 2:]
        else:
            header = asterisks[:len(asterisks) // 2] + self.category + \
                     asterisks[len(asterisks) // 2 if len(asterisks) % 2 == 0 else ((len(asterisks) // 2) + 1):]
        printout = ''
        printout += header + '\n'

        # each subsequent line is a description for a transaction as well as the amount
        # description is left justified with max 23 characters
        # amount is right justified with max 7 characters
        total = 0
        for balance_change in self.ledger:
            description = balance_change.get('description')
            description = description[:23]
            amount = balance_change.get('amount')
            amount = float(amount)
            total += amount
            amount = '%.2f' % round(amount, 2)  # round to two decimals
            printout += f"{description : <23}{amount : >7}" + '\n'
        total = str(total)
        printout += 'Total: ' + total  # total is printed after all transactions
        return printout

    # deposit method which appends a dictionary with an amount and optional description to the object
    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    # withdraw method which appends a dictionary with a negative amount and optional description
    # returns False if not enough funds and True otherwise
    def withdraw(self, amount, description=''):
        if self.check_funds(amount) is False:
            return False
        else:
            self.ledger.append({'amount': -amount, 'description': description})
            return True

    # method which returns the current balance after taking into account all transactions
    def get_balance(self):
        balance = 0
        for balance_change in self.ledger:
            balance += balance_change.get('amount')
        return balance

    # transfer method which withdraws from current object and deposits to the destination object
    def transfer(self, amount, destination):
        if self.check_funds(amount) is False:
            return False
        else:
            self.withdraw(amount, 'Transfer to ' + destination.category)
            destination.deposit(amount, 'Transfer from ' + self.category)
            return True

    # check funds method which returns False if the amount is greater than the balance and True otherwise
    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True

# # returns a spend bar chart with percentages from each object in a list named 'categories'
def create_spend_chart(categories):
    percentages = get_percentages(categories)
    descriptions = get_descriptions(categories)
    my_print = show_descriptions(get_x_axis(get_chart(percentages), percentages), descriptions)
    return my_print


# returns a list of percentage spent in order of the 'categories' list
def get_percentages(categories):
    # creates a list of spending in order of the 'categories' list
    lst = []
    for category in categories:
        total = 0
        for balance_change in category.ledger:
            if balance_change.get('amount') < 0:
                total += -1 * balance_change.get('amount')
        lst.append(round(total, 2))

    # adds up dollars spent for each category to find total
    total = 0
    for category_total in lst:
        total += category_total

    # get percentages and append to a list in order of the 'categories' list
    percentages = []
    for category_total in lst:
        percentages.append(category_total / total * 100)
    return percentages


# returns a list of spending descriptions
def get_descriptions(categories):
    descriptions = []
    for cat in categories:  # go through each category in 'categories'
        for balance_change in cat.ledger:  # go through each transaction in a specific category
            if balance_change.get('amount') < 0:  # look for negative transactions
                descriptions.append(cat.category)  # append to a list
                break
    return descriptions


# returns the part of the chart above the x-axis
def get_chart(percentages):
    my_print = 'Percentage spent by category\n'  # header line
    y_axis = 100
    # while loop to account for 11 columns from 0-100 by 10
    while y_axis >= 0:

        # different spacings depending on y-axis number
        if y_axis == 100:
            my_print += str(y_axis) + '|'
        elif 0 < y_axis < 100:
            my_print += ' ' + str(y_axis) + '|'
        else:
            my_print += '  ' + str(y_axis) + '|'

        # get the max row count due to strict spacing requirements
        # for use in later part of this function
        x_axis = '    ' + '_'
        for percentage in percentages:
            x_axis += '___'
        row_count = len(x_axis) - 4

        current_line = ''
        # adds different bar ('o') or spacing depending on the category
        for percentage in range(0, len(percentages)):
            if percentage == 0:
                if percentages[percentage] >= y_axis:
                    current_line += ' o'
                else:
                    current_line += '  '
            elif 0 < percentage < len(percentages) - 1:
                if percentages[percentage] >= y_axis:
                    current_line += '  o'
                else:
                    current_line += '  '
            else:
                if percentages[percentage] >= y_axis:
                    current_line += '  o  '
                else:
                    current_line += '  '

        # compare current line with row_count to assess if more spaces are needed
        compare = len(current_line)
        while compare < row_count:
            current_line += ' '
            compare += 1

        # add string to my_print string
        my_print += current_line + '\n'
        y_axis -= 10
    return my_print

# return dash lines that represent the x-axis
def get_x_axis(my_print, percentages):
    x_axis = '    ' + '-'
    for percentage in percentages:
        x_axis += '---'
    my_print += x_axis
    my_print += '\n'
    return my_print

# return descriptions in a vertical line
def show_descriptions(my_print, descriptions):
    # find the description with the longest length
    max_description = 0
    for description in descriptions:
        if len(description) > max_description:
            max_description = len(description)

    # iterate through each letter and word index
    # use try and except IndexError as the program will go over the maximum index for certain words
    # spacing is also dependent on if it is the first word, a word in the middle or the last word
    for letter in range(0, max_description):
        for word in range(0, len(descriptions)):
            if word == 0 and word < len(descriptions):
                my_print += '     '
                try:
                    my_print += descriptions[word][letter]
                except IndexError:
                    my_print += ' '
            elif 0 < word < len(descriptions) - 1:
                my_print += '  '
                try:
                    my_print += descriptions[word][letter]
                except IndexError:
                    my_print += ' '
            else:
                my_print += '  '
                try:
                    my_print += descriptions[word][letter] + '  '
                except IndexError:
                    my_print += ' '
        if letter < max_description - 1:
            my_print += '\n'
    return my_print
