import datetime
import locale

locale.setlocale(locale.LC_TIME, "de_DE.utf8")

start_date = datetime.datetime.now()
number_of_days = int(input("How many days shall be generated? "))

date_list = [(start_date + datetime.timedelta(days=day)
              ).strftime("%a. %d.%m.%Y, %d.%m.%Y") for day in range(number_of_days)]

print()
for date in date_list:
    print(date)
print("\nREMEMBER TO CHECK FOR DAYS OF / SUNDAYS")
