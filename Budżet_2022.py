# Program Budżet 2022 - Prototyp

from BTCInput import *
import pickle

#sheets = []

class Sheet:
    """
    Zeszyt na konkretny miesiąc.
    """

    def __init__(self, month_name):
        self.month_name = month_name
        self.__incomes = 0
        self.__expenses = 0
        self.__balance = 0
        self.__dictionary = {}

    def __str__(self):

        template = """
Miesiąc: {0}
Przychody: {1}
Wydatki: {2}
Bilans: {3}
"""

        return template.format(self.month_name, self.__incomes, self.__expenses,
                               self.__balance)

    def add_to_dict(self, dictionary_of_expenses):
        self.__dictionary.update(dictionary_of_expenses)

    def get_dictionary(self):
        return self.__dictionary

    def get_incomes(self):
        """
        Pobiera wysokość wpływów
        """
        return self.__incomes

    def add_incomes(self, incomes_value):
        self.__incomes = self.__incomes + incomes_value
        return

    def get_expenses(self):
        """
        Pobiera wysokość wydatków
        """
        return self.__expenses

    def add_expenses(self, expenses_value):
        self.__expenses = expenses_value

    def get_balance(self):
        """
        Pobiera bilans
        """
        return self.__balance

    def add_balance(self, balance_value):
        self.__balance = balance_value
        return


def new_sheet():
    """
    Czyta nową pozycję w budżecie i ją zapisuje
    """

    print('\nStwórz nowe rozliczenie\n')
    # tworzę obiekt klasy Sheet i dodaję do listy sheets
    month_name = read_text('Wprowadź nazwę miesiąca: ')
    try:
        sheet = Sheet(month_name = month_name)
    except Exception as e:
        print('Dodanie nowego rozliczenia nie powiodło się:', e)
    sheets.append(sheet)
    
    search_month_name = month_name
    edit_billing(search_month_name)
    add_to_dictionary(search_month_name)
    
def edit_billing(search_month_name):
    # dodaję wpływy do obiektu
    sheet = find_sheet(search_month_name)

    if sheet != None:
        # program odnalazł miesiąc rozliczeniowy
        # wyświetla wpływy, wydatki i bilans
        print('\nNazwa miesiąca: ', sheet.month_name)
        print('Wpływy: ', sheet.get_incomes())
        print('Wydatki: ', sheet.get_expenses())
        # wprowadzam aktualne wydatki i wpływy
        incomes_value = read_float('\nDodaj przychód: ')
        try:
            # przekazuję wartości zmiennych do obiektu klasy Month
            sheet.add_incomes(incomes_value)
            balance_value = sheet.get_incomes() - sheet.get_expenses()
            sheet.add_balance(balance_value)
            #sheet.add_balance(balance_value)
            print('\nWpływy w miesiącu: ', sheet.get_incomes())
            print('Wydatki w miesiącu: ', sheet.get_expenses())
            print('Bilans miesiąca: ', sheet.get_balance())
        except:
            print('\nNie udało się:', e)
    else:
        print('\nWprowadzony miesiąc rozliczeniowy nie istnieje')
    
def add_to_dictionary(search_month_name):
 # dodaję listę wydatków
    sheet = find_sheet(search_month_name)

    if sheet != None:
        # program odnalazł miesiąc rozliczeniowy
        # wyświetla nazwę miesiąca
        print('\nWprowadź wydatki dla miesiąca ', sheet.month_name)
        # wprowadzam aktualne wydatki
        i = read_int("Ile wydatków chcesz wprowadzić: ")
        dictionary_of_expenses = sheet.get_dictionary()
        for count in range(1, i+1):
            exp_name = input('Nazwa: ')
            exp_value = read_float('Kwota: ')
            # sprawdzam czy dany klucz już istnieje
            # jeśli tak - nadpisuję jego wartość
            if exp_name in dictionary_of_expenses:
                dictionary_of_expenses[exp_name] = dictionary_of_expenses[exp_name] + exp_value
            else:
                #jeśli klucz nie istnieję, tworzę tymczasowy słownik i dodaję do głównego
                little_dict = {exp_name:exp_value}
                # nadpisuję główny słównik
                dictionary_of_expenses.update(little_dict)
        try:
            # przekazuję wartości do słownika obiektu
            sheet.add_to_dict(dictionary_of_expenses)
            print('Dodanie listy wydatków powiodło się')
        except:
            print('\nNie udało się:', e)
        try:
            expenses_value = sum(dictionary_of_expenses.values())
            sheet.add_expenses(expenses_value)
            print('Dodanie sumy wydatków powiodło się')
        except:
            print('Dodanie sumy wydatków nie powiodło się')
        try:
            balance_value = sheet.get_incomes() - sheet.get_expenses()
            sheet.add_balance(balance_value)
        except:
            print('Obliczenie bilansu nie powiodło się')
    else:
        print('\nWprowadzony miesiąc rozliczeniowy nie istnieje')
    
        
def find_sheet(search_month_name):
    # funkcja odpowiadająca za wyszukanie odpowiedniego zeszytu
    # na podstawie nazwy miesięcy
    search_month_name = search_month_name.strip()
    search_month_name = search_month_name.lower()
    # dla zeszytu spośród zeszytów (lista sheets)
    for sheet in sheets:
        month_name = sheet.month_name
        month_name = month_name.strip()
        month_name = month_name.lower()
        #  jeśli znajdzie miesiąc o odpowiedniej nazwie zwróci jego wart.
        if month_name.startswith(search_month_name):
            return sheet
    return None

def display_sheet(search_month_name):
    # po wprowadzeniu nazwy przypisuje do zmiennej sheet
    # odnaleziony obiekt
    sheet = find_sheet(search_month_name)
    if sheet != None:
        print(64 * '-')
        print(sheet)
        print('Lista wydatków')
        for key, value in sheet.get_dictionary().items():
            print(key,':',value)
        print(64 * '-')
    else:
        print('\nBrak wyszukiwanego miesiąca')

def save(filename):

    with open(filename, 'wb') as out_file:
        pickle.dump(sheets, out_file)

def load(filename):

    global sheets
    with open(filename, 'rb') as input_file:
        sheets = pickle.load(input_file)


def find_billing():
    """
    Znajduje rozliczenie i wyświetla menu edycji
    """
    print('\nZnajdź rozliczenie\n')
    search_month_name = read_text('\nWprowadź nazwę miesiąca: ')
    sheet = find_sheet(search_month_name)
    if sheet != None:
        prompt = """Wybierz działanie

1. Dodaj przychód
2. Dodaj wydatki
3. Wyświetl raport
4. Wróć do menu głównego

Wprowadź polecenie: """
        while(True):
            command = read_int_ranged(prompt, 1, 5)
            if command == 1:
                edit_billing(search_month_name)
            elif command == 2:
                add_to_dictionary(search_month_name)
            elif command == 3:
                display_sheet(search_month_name)
            elif command == 4:
                break
                
                

def main_menu():
    prompt = """Aplikacja Budżet 2022

1. Stwórz nowy okres rozliczeniowy
2. Znajdź okres rozliczeniowy
3. Wyjście

Wprowadź polecenie: """

    while(True):
        command = read_int_ranged(prompt, 1, 3)
        if command == 1:
            new_sheet()
        elif command == 2:
            find_billing()
        elif command == 3:
            save(filename)
            break


filename = 'sheets.pickle'
try:
    load(filename)
except:
    print('Nie znaleziono rozliczeń')
    sheets = []
    
main_menu()

    



