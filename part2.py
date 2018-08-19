# these should be the only imports you need
import sys
import sqlite3

# write your code here
# usage should be 
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>

conn = sqlite3.connect('Northwind_small.sqlite')
c = conn.cursor()

if sys.argv[1] == 'customers':
    print('{:5s}\t{}'.format('ID', 'Customer Name'))
    customers = []
    for row in c.execute('SELECT * FROM Customer'):
        customers.append((row[0], row[2]))
    customers = sorted(customers, key=lambda x: x[0])
    for c_id, c_name in customers:
        print('{}\t{}'.format(c_id, c_name))

elif sys.argv[1] == 'employees':
    print('{:5s}\t{}'.format('ID', 'Employee Name'))
    employees = []
    for row in c.execute('SELECT * FROM Employee'):
        employees.append((row[0], row[2], row[1]))
    employees = sorted(employees, key=lambda x: int(x[0]))
    for e_id, e_first, e_last in employees:
        print('{}\t{} {}'.format(e_id, e_first, e_last))

elif sys.argv[1] == 'orders' and sys.argv[2][:4].startswith('cust'):
    cust_id = sys.argv[2].split('=')[1]
    t = (cust_id,)
    c.execute("SELECT OrderDate FROM [Order] JOIN Customer ON [Order].CustomerId = Customer.id WHERE Customer.id = ?", t)
    customer_order_dates = []
    for row in c:
        customer_order_dates.append(row)
    print('Order Dates')
    for date in customer_order_dates:
        print(date[0])

elif sys.argv[1] == 'orders' and sys.argv[2].startswith('emp'):
    emp_lastname = sys.argv[2].split('=')[1]
    t = (emp_lastname,)
    c.execute("SELECT OrderDate FROM [Order] JOIN Employee ON [Order].EmployeeId = Employee.id WHERE Employee.LastName = ?", t)
    employee_order_dates = []
    for row in c:
        employee_order_dates.append(row)
    print('Order Dates')
    for date in employee_order_dates:
        print(date[0])