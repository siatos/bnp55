import calendar
from datetime import date
import string

def get_date():
   """ Get year, month and day of the protein when discovered
       Checks whether year is a leap year or not
       Returns: year month day
   """
   prompt = "Enter year for protein: "
   while True:
       try:
           year = int(input(prompt))
           if  1900 < year <= 2024:
               print("You entered: {}".format(year))
               if calendar.isleap(year):
                   print("Year: {} is a leap year".format(year))
               break
           else:
               print("year entry should be 1900<entry<2024 ")
       except ValueError:
           print("Please enter a valid integer > 1900 ")

   prompt = "Enter month: "
   while True:
       # in_month = int(input(prompt))
       in_month = input(prompt)  #accept inputs like 0n
       print(in_month)
       if len(in_month) == 0:
           print("Nothing entered, assuming default 1")
           month = 1
           break
       else:
           try:
               month = int(in_month.lstrip("0")) #remove reduntant 0n
               if  1 <= month <= 12:
                   print("You entered: {}".format(month))
                   break
               else:
                   print("month entry shoulnd be in [1, 12] ")
           except ValueError:
               print("Please enter a valid integer > 1 ")
   days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
   if calendar.isleap(year):
       days[1] = 29   # February is at pos 1 since position starts from 0
   prompt = "Enter day: "
   while True:
       in_day = input(prompt)
       if len(in_day) == 0:
           print("Nothing entered, assuming default 1")
           day = 1
           break
       else:
           try:
               day = int(in_day.lstrip("0"))
               if 0 < day <= days[month-1]:
                   print("You entered: {}".format(day))
                   break
               else:
                   print("Day entry should be in [1, {}]".format(str(days[month-1])))
           except ValueError:
               print("Please enter a valid integer > 1 ")

   return year, month, day



if __name__ == '__main__':
   while True:
       protein = input("Enter name for protein ")
       if len(protein) != 0:
           print("protein is : " + protein)
           break
       else:
           print("Enter some name ")

   print("get date")
   year, month, day = get_date()
   print("Year: {} Month: {} Day: {}".format(year, month, day))

   start_date = date(year, month, day)
   end_date = date(2022, 12, 31)
   hours = ((end_date - start_date).days)*24
   if hours > 0:
       print("protein {} is known for {} hrs before end of 2022".format(protein, hours))
   else:
       print("protein {} has been known for {} hrs after end of 2022".format(protein, abs(hours)))

