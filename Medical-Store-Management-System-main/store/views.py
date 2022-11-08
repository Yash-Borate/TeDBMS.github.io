from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import datetime

import mysql.connector

try:
	conn = mysql.connector.connect(host="localhost", user="username", password="password", database='your_database', auth_plugin='mysql_native_password')
	print("Connected to MySQL Database")
except:
	print("Can't Connect to MySQL Database")

cur = conn.cursor()


def info(request):
	return render(request, 'store/info.html')


def index(request):
	try:
		params = []
		query = "SELECT COUNT(emp_id) FROM employee"
		cur.execute(query)
		count_of_employee = int(cur.fetchall()[0][0])
		params.append(count_of_employee)

		query = "SELECT exp_date from stock"
		cur.execute(query)
		result = cur.fetchall()
		count = 0

		for date in result:
			days = (date[0] - datetime.date.today()).days
			if days <= 30:
				count = count + 1
		params.append(count)

		query = "select distinct(med_name) from medicine natural join stock;"
		cur.execute(query)
		res = cur.fetchall()
		params.append(res)

		d = datetime.date.today()
		full_date = str(d.year) + '-' +str(d.month) + '-' + str(d.day)
		query=f"select sum(price) from bill where bill_date = '{full_date}'"
		cur.execute(query)
		res = cur.fetchall()
		params.append(res[0][0])
		
		return render(request, 'store/index.html', {'params': params})

	except Exception as e:
		print(e)
		return render(request, 'store/index.html', {'params': [0,0]})


def bill_all(request):
	query = 'select * from bill order by bill_date desc;'
	try:
		cur.execute(query)
		records = cur.fetchall()
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect('store:store-home')
	return render(request, 'store/bill_all.html', {'records':records})


# BILL
def bill_register(request):

	if request.method=='POST':
		value = []
		customername = request.POST.getlist('name')[0]
		medname = request.POST.getlist('medicine')
		qua = request.POST.getlist('quantity')
		d = datetime.date.today()
		full_date = str(d.year) + '-' +str(d.month) + '-' + str(d.day)
		try:
			for i in range(len(medname)):
				query = f"select sum(curr_quantity) from medicine natural join stock where med_name='{medname[i]}' group by med_name;"
				cur.execute(query)
				data = cur.fetchone()[0]
				if data < int(qua[i]):
					messages.error(request, f"Sorry, Required Quantity Of   \"{medname[i]}\"   Not Available !")
					return redirect('store:store-home') 	

			for name in request.POST.getlist('medicine'):
				query=f"SELECT med_price FROM medicine where med_name=\'{name}\'"
				cur.execute(query)
				res = cur.fetchall()
				value.append(res[0][0])
			
			count = 0
			for q in request.POST.getlist('quantity'):
				value[count] *= int(q)
				count = count + 1
			
			for i in range(len(value)):
				query=f"INSERT INTO bill (cust_name, med_name, quantity, price, bill_date) VALUES (\'{customername}\', \'{medname[i]}\', {qua[i]}, {value[i]}, '{full_date}')"
				cur.execute(query)
				conn.commit()
				
				query_2 = f"select * from stock where med_id in (select med_id from medicine where med_name='{medname[i]}') and curr_quantity > 0 order by exp_date;"
				cur.execute(query_2)
				records = cur.fetchall()
				quantities = []
				item_quantity = int(qua[i])
				
				for record in records:
					quantities.append([record[0],record[8]])

				total_quantity = 0
				
				for i in quantities:
					total_quantity += i[1]
				
				if item_quantity > total_quantity:
					messages.error(request, "Not Sufficient Quantity")
					return redirect('store:store-home')
				
				for i in quantities:
					if item_quantity > i[1]:
						item_quantity = item_quantity - i[1]
						i[1] = 0
					else:
						i[1] = i[1] - item_quantity
				
				for i in quantities:
					query = f"update stock set curr_quantity = {i[1]} where stock_id = {i[0]};"
					cur.execute(query)
					conn.commit()

			messages.success(request, "Bill Generated Successfully !")
				
			return redirect("store:store-home")
		except Exception as e:
			print("**\n",e,"\n**")
			messages.error(request, "Some Error Occurred !")
			return redirect('store:store-home')


	return render(request, 'store/index.html')


# STAFF
def staff_register(request):

	if request.method == 'POST':
		name = request.POST['firstname'] + " " + request.POST['lastname']
		gender = request.POST['gender']
		age = int(request.POST['age'])
		salary = int(request.POST['salary'])
		# Write in database
		query = f"insert into employee (emp_name, emp_gender, emp_age, emp_salary) values ('{name}','{gender}',{age},{salary});"
		try:
			cur.execute(query)
			conn.commit()
		except:
			messages.error(request,"Some Error Occured !")
			return redirect('store:staff-all')

		messages.success(request, 'Record Saved Successfully !')
		return redirect('store:staff-all')
	else:
		pass
	return render(request, 'store/staff_form.html')


def staff_all(request):

	cur.execute('select * from employee;')
	records = cur.fetchall()
	return render(request, 'store/staff_all.html', {'records':records})


def staff_delete(request, pk):

	try:
		query = f'delete from employee where emp_id={pk}'
		cur.execute(query)
		conn.commit()
		messages.success(request, "Record Deleted Successfully !")
	except:
		messages.error(request, "Can't Delete Record !")
	return redirect('store:staff-all')


def staff_update(request, pk):
	
	query = f'select * from employee where emp_id={pk}'
	try:
		cur.execute(query)
		val = cur.fetchone()
	except:
		messages.error(request, "Can't Update Record !")
		return redirect('store:staff-all')
	emp={
		'emp_id':val[0],
		'fname':val[1].split()[0],
		'lname':val[1].split()[1],
		'gender':val[2],
		'age':val[3],
		'salary':val[4]
	}
	if request.method == 'POST':
		emp_id = request.POST['emp_id'] 
		name = request.POST['firstname'] + " " + request.POST['lastname']
		gender = request.POST['gender']
		age = int(request.POST['age'])
		salary = int(request.POST['salary'])
		query = f"update employee set emp_name = '{name}', emp_gender = '{gender}', emp_age = {age}, emp_salary = {salary} where emp_id = {emp_id};"	
		cur.execute(query)
		conn.commit()
		messages.success(request, "Record Updated Successfully !")
		return redirect('store:staff-all')

	return render(request, 'store/staff_update.html',{'emp':emp})

# STOCK
def stock_register(request):
	try:
		medicines = []
		suppliers = []
		query = 'select med_name from medicine order by med_name'
		cur.execute(query)
		med_items = cur.fetchall()
		for item in med_items:
			medicines.append(item[0])
		
		query = 'select supplier_name from supplier order by supplier_name'
		cur.execute(query)
		supp_items = cur.fetchall()
		for item in supp_items:
			suppliers.append(item[0])
		
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect('store:stock-register')

	if request.method=='POST':
		medname = request.POST['name']
		quantity = request.POST['quantity']
		price = request.POST['price']
		supplier = request.POST['supplier']
		mfg_date = request.POST['mfg_date']
		exp_date = request.POST['exp_date']
		d = datetime.date.today()
		arr_date = str(d.year) + '-' +str(d.month) + '-' + str(d.day)
		try:
			query = f"SELECT med_id FROM medicine WHERE med_name=\'{medname}\'"
			cur.execute(query)
			medid = cur.fetchall()[0][0]
		except:
			messages.error(request, "Medicine Not Registered ! Please Register First From /register/medicine .")
			return redirect("store:stock-all")
			
		try:
			query = f"SELECT supplier_id FROM supplier WHERE supplier_name=\'{supplier}\'"
			cur.execute(query)
			supid=cur.fetchall()[0][0]
		except:
			messages.error(request, "Supplier Not Registered ! Please Register First From /register/supplier .")
			return redirect("store:supplier-register")
						
		query = f"INSERT INTO stock (quantity, price, mfg_date, exp_date, stock_arrival_date, supplier_id, med_id, curr_quantity) VALUES ({quantity}, {price}, \'{mfg_date}\', \'{exp_date}\', \'{arr_date}\', {supid}, {medid}, {quantity})"
		cur.execute(query)
		conn.commit()
		messages.success(request, "Record Registered Successfully !")
		return redirect("store:stock-all")
	else:
		return render(request, 'store/stock_form.html', {'medicines':medicines, 'suppliers':suppliers})


def stock_med_sort(request):
	query = 'select med_name, sum(quantity),sum(curr_quantity) from stock natural join medicine group by med_id order by med_name;'
	try:
		cur.execute(query)
		records = cur.fetchall()
	except:
		messages.error(request, "Some Error Occurred!")
		return redirect('store:stock-all')

	return render(request, 'store/stock_med_sort.html', {'records':records})


def stock_all(request):
	try:
		cur.execute('select stock_id, quantity, price, mfg_date, exp_date, stock_arrival_date, med_name, supplier_name, curr_quantity from stock natural join medicine natural join supplier order by exp_date;')
		records = cur.fetchall()
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect('store:stock-all')
	
	return render(request, 'store/stock_all.html', {'records':records})


# SUPPLIER
def supplier_register(request):

	if request.method == 'POST':
		suppliername = request.POST["supname"]
		city = request.POST["city"]			
		pincode = request.POST["pincode"]
		query = f"INSERT INTO supplier (supplier_name, supplier_city, city_pincode) VALUES ('{suppliername}', '{city}', {pincode});"
		print(query)
		try:
			cur.execute(query)
			conn.commit()
			messages.success(request, "Record Saved Successfully !")
			return redirect('store:supplier-all')
		except:
			messages.error(request, "Some Error Occurred !")
			return redirect('store:supplier-all')
			
	else:
		return render(request, 'store/supplier_form.html')


def supplier_all(request):
	query = 'select * from supplier;'
	try:
		cur.execute(query)
		records = cur.fetchall()
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect('store:supplier-all')
	
	return render(request, 'store/supplier_all.html', {'records':records})


def supplier_delete(request, pk):
	query = f'delete from supplier where supplier_id = {pk};'
	try:
		cur.execute(query)
		conn.commit()
	except:
		messages.error(request, "Can't Delete Record !")
		return redirect('store:supplier-all')
	
	return redirect('store:supplier-all')


def supplier_update(request, pk):
	query = f'select * from supplier where supplier_id={pk}'
	#print(query)
	try:
		cur.execute(query)
		supplier = cur.fetchone()
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect('store:supplier-all')
	#print(supplier)
	if request.method == 'POST':
		supplier_id = request.POST['supplier_id']
		suppliername = request.POST["supname"]
		city = request.POST["city"]			
		pincode = request.POST["pincode"]
		query = f"update supplier set supplier_name = '{suppliername}', supplier_city = '{city}', city_pincode = {pincode} where supplier_id = {supplier_id};"

		try:
			cur.execute(query)
			conn.commit()
			messages.success(request, "Record Updated Successfully !")
			return redirect('store:supplier-all')
		except:
			messages.error(request, "Some Error Occurred !")
			return redirect('store:supplier-all')

	return render(request, 'store/supplier_update.html', {'supplier':supplier})

# MEDICINE
def medicine_register(request):
	if request.method=='POST':
		name = request.POST["medname"]
		price = request.POST["medprice"]
		query = f"INSERT INTO medicine (med_name, med_price) VALUES ('{name}', {price});"
		print("**\n",query,"**\n")
		try:
			cur.execute(query)
			conn.commit()
			messages.success(request, "Record Saved Successfully !")
			return redirect('store:medicine-all')
			
		except :
			messages.error(request, "Some Error Occurred !")
			return redirect('store:medicine-all')

	else:
		return render(request, 'store/medicine_form.html')


def medicine_all(request):
	query = 'select * from medicine;'
	try:
		cur.execute(query)
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect("store:medicine-all")
	
	records = cur.fetchall()

	return render(request, 'store/medicine_all.html', {'records':records})


def medicine_delete(request, pk):
	query = f'delete from medicine where med_id = {pk}'
	try:
		cur.execute(query)
		conn.commit()
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect("store:medicine-all")
	messages.success(request,"Record Saved Successfully !")
	return redirect('store:medicine-all')


def medicine_update(request, pk):
	query = f'select * from medicine where med_id = {pk}'
	try:
		cur.execute(query)
		med = cur.fetchone()
	except:
		messages.error(request, "Some Error Occurred !")
		return redirect('store:medicine-all')

	if request.method == 'POST':
		name = request.POST['medname']
		price = request.POST['medprice']
		try:
			query = f"update medicine set med_name = '{name}', med_price = {price} where med_id = {pk};"
			print(query)
			cur.execute(query)
			conn.commit()
			messages.success(request, 'Record Successfully Updated !')
			return redirect('store:medicine-all')
		except:
			messages.error(request, 'Some Error Occurred !')
			return redirect('store:medicine-all')

	return render(request, 'store/medicine_update.html', {'med':med})
