from flask import Flask, request, render_template, url_for, session, flash, redirect,jsonify, Response
from otp import genotp
import bcrypt
from cmail import send_mail
from stoken import endata, dedata
import mysql.connector
import os
import re
mydb=mysql.connector.connect(user='root',host='localhost',password='srikanth',database='ecommee')
import razorpay
client = razorpay.Client(auth=("rzp_test_RL09zWiX8Ro8fO","dbg0Wc4x3V7PZgfGtlp5gFV6"))
import pdfkit
config=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
app=Flask(__name__)
app.secret_key='M@//e$h1405'
# welcome route
@app.route('/')
def home():
    return render_template('welcome.html')

#index page route
@app.route('/index')
def index():
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(item_id),item_name,item_description,price,quantity,category,item_image from items')
        all_itemsdata=cursor.fetchall()
        print(all_itemsdata)
    except Exception as e:
        print(f'error is {e}')
        flash('could fetch items data')
        return redirect(url_for('index'))
    else:
        return render_template('index.html',all_itemsdata=all_itemsdata)

#admin Signup
@app.route('/admincreate', methods=['GET', 'POST'])
def admincreate():
    if request.method == 'POST':
        print(request.form)
        adminname = request.form['username']
        adminemail = request.form['email']
        adminpassword = request.form['password']
        adminaddress = request.form['address']
        adminagree = request.form['agree']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(email) from admindata where email=%s',[adminemail])
            count_email=cursor.fetchone()
        except Exception as e:
            print(e)
            flash('Database connection lost')
            return redirect(url_for('admincreate'))
        else:
            if count_email[0]==0:
                gotp=genotp()
                admindata={'adminname':adminname,'adminemail':adminemail,'adminpassword':adminpassword,'adminaddress':adminaddress,'adminagree':adminagree,'adminotp':gotp}
                subject='Your OTP for Ecommerce App Verification'
                body=f'Hello {adminname}, your OTP for Ecommerce App is {gotp}'
                send_mail(adminemail,subject=subject,body=body)
                flash(f'OTP has been sent to {adminemail}')
                return redirect (url_for('adminotpverify',enadmin=endata(data=admindata)))
            elif count_email[0]==1:
                flash('Email already existed')
                return redirect(url_for('adminlogin'))
    return render_template('admincreate.html')

#OTP verify
@app.route('/adminnotverify/<enadmin>', methods=['GET', 'POST'])
def adminotpverify(enadmin):
    try:
        deadmin=dedata(enadmin)
    except Exception as e:
        print(e)
        flash('Couldnt verify OTP, Try Again')
        return redirect(url_for('admincreate'))
    except SignatureExpired as e:
        print(f'Token has Expired.Reason:{e}')
        flash('OTP Expired, Try Again')
        return redirect(url_for('admincreate'))
    else:
        if request.method == 'POST':
            given_otp=request.form['otp']
            if given_otp==deadmin['adminotp']:
                try:
                    hash_pwd=bcrypt.hashpw(deadmin['adminpassword'].encode('utf-8'),bcrypt.gensalt())
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into admindata(username,email,password,agreed,address) values (%s,%s,%s,%s,%s)',[deadmin['adminname'],deadmin['adminemail'],hash_pwd,deadmin['adminagree'],deadmin['adminaddress']])
                    mydb.commit()
                    cursor.close()
                except Exception as e:
                    print(e)
                    flash('Could not store your details')
                    return redirect(url_for('admincreate'))
                else:
                    flash('Details stored successfully')
                    return 'Login'
            else:
                flash('wrong otp')
                
    return render_template('adminotp.html')
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method=='POST':
        login_email=request.form['email']
        login_password=request.form['password'].encode('utf-8')
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(email) from admindata where email=%s',[login_email])
            count_email=cursor.fetchone()
        except Exception as e:
            print(e)
            flash ('Database connection lost while login')
            return redirect(url_for('adminlogin'))
        else:
            if count_email[0]==1:
                cursor.execute('select password from admindata where email=%s',[login_email])
                stored_password=cursor.fetchone()
                if bcrypt.checkpw(login_password,stored_password[0]):
                    session['admin']=login_email
                    return redirect(url_for('adminpanel'))
                else:
                    flash('password was wrong')
                    return redirect(url_for('adminlogin'))
            elif count_email[0]==0:
                flash('Email not found')
                return redirect(url_for('adminlogin'))
    return render_template('adminlogin.html')

#admin pannel
@app.route('/adminpanel')
def adminpanel():
    if session.get('admin'):
        return render_template('adminpanel.html')
    else:
        flash('Please login to access the dashboard')
        return redirect(url_for('adminlogin'))

#add item
@app.route('/additem',methods=['GET','POST'])
def additem():
    if session.get('admin'):
        if request.method=='POST':
            item_name=request.form['title']
            item_description=request.form['Description']
            item_price=request.form['price']
            item_quantity=request.form['quantity']
            item_category=request.form['category']
            item_imagedata=request.files['file']
            imagename=item_imagedata.filename
            print(imagename.split('.'))
            img_name=genotp()+'.'+imagename.split('.')[-1]
            print(img_name)
            filepath=os.path.abspath(__file__)
            print(filepath)
            dpath=os.path.dirname(filepath)
            print(dpath)
            static_path=os.path.join(dpath,'static')
            print(static_path)
            item_imagedata.save(os.path.join(static_path,img_name))
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select adminid from admindata where email=%s',[session.get ('admin')])
                admin_id=cursor.fetchone()
                if admin_id:
                    cursor.execute('insert into items(item_id,item_name,item_description,price,quantity,category,item_image,added_by) values(uuid_to_bin(uuid()),%s,%s,%s,%s,%s,%s,%s)',[item_name,item_description,item_price,item_quantity,item_category,img_name,admin_id[0]])
                    mydb.commit()
                    cursor.close()
                else:
                    flash('admindetails not found')
                    return redirect(url_for('additem'))
            except Exception as e:
                print(f'error is {e}')
                flash('couldnot store item  details')
                return redirect(url_for('additem'))
                
            else:
                flash('items detais added successfully')
                return redirect(url_for('additem'))
        return render_template('additem.html')
    else:
        flash('to add item plz login')
        return redirect(url_for('adminlogin'))
@app.route('/view_allitems')
def view_allitems():
    if session.get('admin'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select adminid from admindata where email=%s',[session.get('admin')])
            admin_id=cursor.fetchone()
            if admin_id:
                cursor.execute('select bin_to_uuid(item_id),item_name,item_description,price,quantity,category,item_image from items where added_by=%s',[admin_id[0]])
                all_itemsdata=cursor.fetchall()
                print(all_itemsdata)
            else:
                flash('admindetails not found')
                return redirect(url_for('additem'))
        except Exception as e:
            print(f'Error is {e}')
            flash('could fetch items data')
            return redirect(url_for('adminpanel'))
        else:
            return render_template('viewall_items.html',all_itemsdata=all_itemsdata)
    else:
        flash(f'to view all item plz login')
        return redirect(url_for('adminlogin'))    
         
#view single item
@app.route('/view_item/<itemid>')
def view_item(itemid):
    if session.get('admin'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select adminid from admindata where email=%s',[session.get('admin')])
            admin_id=cursor.fetchone()
            if admin_id:
                cursor.execute('select bin_to_uuid(item_id),item_name,item_description,price,quantity,category,item_image from items where item_id=uuid_to_bin(%s) and added_by=%s',[itemid,admin_id[0]])
                item_data=cursor.fetchone()
                print(item_data)
            else:
                flash('admin details not found')
                return redirect(url_for('adminpanel'))
        except Exception as e:
            print(f'error is {e}')
            flash('could not fetch item data')
            return redirect(url_for('adminpanel'))
        else:
            return render_template('view_item.html',item_data=item_data)
    else:
        flash(f'to view item pls login')
        return redirect(url_for('adminlogin'))
    
#delete item
@app.route('/delete_item/<itemid>')
def delete_item(itemid):
    if session.get('admin'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select adminid from admindata where email=%s',[session.get('admin')])
            admin_id=cursor.fetchone()
            if admin_id:
                cursor.execute('select item_image from items where item_id=uuid_to_bin(%s) and added_by=%s',[itemid,admin_id[0]])
                Stored_imagename=cursor.fetchone()
                if Stored_imagename:
                    filepath=os.path.abspath(_file_)
                    print(filepath)
                    dpath=os.path.dirname(filepath)
                    print(dpath)
                    static_path=os.path.join(dpath,'static')
                    print(static_path)
                    os.remove(os.path.join(static_path,Stored_imagename[0]))
                    cursor.execute('delete from items where item_id=uuid_to_bin(%s) and added_by=%s',[itemid,admin_id[0]])
                    mydb.commit()
                    cursor.close()
                else:
                    flash('could not find image')
                    return redirect(url_for('view_allitems'))
            else:
                flash('could not found admin details')
                return redirect(url_for('adminpanel'))
        except Exception as e:
            print(e)
            flash('could not delete image')
            return redirect(url_for('view_allitems'))
        else:
            flash('Item deleted successfully')
            return redirect(url_for('view_allitems'))
    else:
        flash('to delete please login first')
        return redirect(url_for('adminlogin'))
@app.route('/updateitem/<itemid>',methods=['GET','POST'])
def updateitem(itemid):
    if session.get('admin'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select adminid from admindata where email=%s',[session.get('admin')])
            admin_id=cursor.fetchone()
            if admin_id:
                cursor.execute('select bin_to_uuid(item_id),item_name,item_description,price,quantity,category,item_image from items where item_id=uuid_to_bin(%s) and added_by=%s',[itemid,admin_id[0]])
                item_data=cursor.fetchone()
                print(item_data)
            else:
                flash('admin details not found')
                return redirect(url_for('adminpanel'))
        except Exception as e:
            print(f'error is {e}')
            flash('could not fetch item data')
            return redirect(url_for('adminpanel'))
        if request.method=='POST':
            try:

                update_itemname=request.form['title']
                update_itemdesc=request.form['Description']
                update_itemquantity=request.form['quantity']
                update_itemprice=request.form['price']
                update_itemcategory=request.form['category']
                update_itemimage=request.files['file']
                print(request.form)
                print(update_itemimage)
                if update_itemimage.filename=='':
                    img_name=item_data[6]
                else:
                    img_name=genotp()+'.'+update_itemimage.filename.split('.')[-1]
                    filepath=os.path.abspath(__file__)
                    print(filepath)
                    dpath=os.path.dirname(filepath)
                    print(dpath)
                    static_path=os.path.join(dpath,'static')
                    print(static_path)
                    os.remove(os.path.join(static_path,item_data[6]))
                    update_itemimage.save(os.path.join(static_path,img_name))
                cursor.execute('update items set item_name=%s,item_description=%s,price=%s,quantity=%s,category=%s,item_image=%s where item_id=uuid_to_bin(%s) and added_by=%s',[update_itemname,update_itemdesc,update_itemprice,update_itemquantity,update_itemcategory,img_name,itemid,admin_id[0]])
                mydb.commit()
                cursor.close()
            except Exception as e:
                print(e)
                flash('couldnot upadate item details')
                return redirect(url_for('updateitem',itemid=itemid))
            else:
                flash('item updated successfully')
                return redirect(url_for ('view_item',itemid=itemid))


        return render_template('update_item.html',item_data=item_data)
    else:
        flash('To update an item pls login')
        return redirect(url_for('adminlogin'))
@app.route('/adminprofileupdate',methods=['GET','POST'])
def adminprofileupdate():
    if session.get('admin'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select * from admindata where email=%s',[session.get('admin')])
            stored_data=cursor.fetchone()
        except Exception as e:
            print(e)
            flash('could not fetch admin data')
            return redirect(url_for('adminpanel'))
        else:
            if request.method=='POST':
                try:
                    updated_username=request.form['adminname']
                    updated_address=request.form['address']
                    updated_phoneno=request.form['phone']
                    updated_profilepic=request.files['file']
                    print(updated_profilepic)
                    if updated_profilepic.filename=="":
                        display_img=stored_data[7]
                    else:
                        display_img=genotp()+'.'+updated_profilepic.filename.split('.')[-1]
                        filepath=os.path.abspath(__file__)
                        print(filepath)
                        dpath=os.path.dirname(filepath)
                        print(dpath)
                        static_path=os.path.join(dpath,'static')
                        print(static_path)
                        if stored_data[7]:
                            os.remove(os.path.join(static_path,stored_data[7]))
                        updated_profilepic.save(os.path.join(static_path,display_img))
                except Exception as e:
                    print(e)
                    flash('could not update profile')
                    return redirect(url_for('adminpanel'))
                else:
                    cursor.execute('update admindata set username=%s,address=%s,phone_no=%s,profile_img=%s where email=%s',[updated_username,updated_address,updated_phoneno,display_img,session.get('admin')])
                    mydb.commit()
                    cursor.close()
                    flash('profile updated successfully')
            return render_template('adminupdate.html',stored_data=stored_data)      
                   
    else:
        flash('to update profile pls login')
        return redirect(url_for('adminlogin'))


@app.route('/adminlogout')
def adminlogout():
    if session.get('admin'):
        session.pop('admin')
        return redirect(url_for('adminlogin'))
    else:
        flash('To logout please login first')
        return redirect(url_for('adminlogin'))


#user
#user register
@app.route('/usercreate', methods=['GET', 'POST'])
def usercreate():
    if request.method == 'POST':
        print(request.form)
        username = request.form['name']
        useremail = request.form['email']
        userpassword = request.form['password']
        useraddress = request.form['address']
        userphoneno = request.form['phone_no']
        usergender= request.form['usergender']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(useremail) from userdata where useremail=%s',[useremail])
            count_email=cursor.fetchone()
        except Exception as e:
            print(e)
            flash('Database connection lost')
            return redirect(url_for('usercreate'))
        else:
            if count_email[0]==0:
                gotp=genotp()
                userdata={'username':username,'useremail':useremail,'userpassword':userpassword,'useraddress':useraddress,'userphoneno':userphoneno, 'usergender':usergender,'userotp':gotp}
                subject='Your OTP for Ecommerce App Verification'
                body=f'Hello {username}, your OTP for Ecommerce App is {gotp}'
                send_mail(useremail,subject=subject,body=body)
                flash(f'OTP has been sent to {useremail}')
                return redirect (url_for('userotpverify',en_user=endata(data=userdata)))
            elif count_email[0]==1:
                flash('Email already existed')
                return redirect(url_for('userlogin'))
    return render_template('usersignup.html')

# user OTP verify
@app.route('/userotverify/<en_user>', methods=['GET', 'POST'])
def userotpverify(en_user):
    try:
        deuser=dedata(en_user)
    except Exception as e:
        print(e)
        flash('Couldnt verify OTP, Try Again')
        return redirect(url_for('usercreate'))
    except SignatureExpired as e:
        print(f'Token has Expired.Reason:{e}')
        flash('OTP Expired, Try Again')
        return redirect(url_for('usercreate'))
    else:
        if request.method == 'POST':
            given_otp=request.form['otp']
            if given_otp==deuser['userotp']:
                try:
                    hash_pwd=bcrypt.hashpw(deuser['userpassword'].encode('utf-8'),bcrypt.gensalt())
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into userdata(username,useremail,password,usergender,address, phone_no) values (%s,%s,%s,%s,%s,%s)',[deuser['username'],deuser['useremail'],hash_pwd,deuser['usergender'],deuser['useraddress'], deuser['userphoneno']])
                    mydb.commit()
                    cursor.close()
                except Exception as e:
                    print(e)
                    flash('Could not store your details')
                    return redirect(url_for('usercreate'))
                else:
                    flash('Details stored successfully')
                    return redirect(url_for('userlogin'))
            else:
                flash('Wrong OTP')
    return render_template('userotp.html')

#user login
@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if request.method=='POST':
        login_email=request.form['email']
        login_password=request.form['password'].encode('utf-8')
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(useremail) from userdata where useremail=%s',[login_email])
            count_email=cursor.fetchone()
        except Exception as e:
            print(e)
            flash ('Database connection lost while login')
            return redirect(url_for('userlogin'))
        else:
            if count_email[0]==1:
                cursor.execute('select password from userdata where useremail=%s',[login_email])
                stored_password=cursor.fetchone()
                if bcrypt.checkpw(login_password,stored_password[0]):
                    session['user']=login_email
                    if not session.get(login_email):
                        session[login_email]={}
                    return redirect(url_for('index'))
                else:
                    flash('password was wrong')
                    return redirect(url_for('userlogin'))
            elif count_email[0]==0:
                flash('Email not found')
                return redirect(url_for('userlogin'))
    return render_template('userlogin.html')
@app.route('/addcart/<itemid>')
def addcart(itemid):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select bin_to_uuid(item_id),item_name,item_description,price,quantity,category,item_image from items where item_id=uuid_to_bin(%s)',[itemid])
            itemdata=cursor.fetchone()
        except Exception as e:
            print(f'Error is {e}')
            flash('could not fetch data')
            return redirect(url_for('index'))
        else:
            print(session)
            if itemid not in session[session.get('user')]:
                session[session.get('user')][itemid]=[itemdata[1],itemdata[3],1,itemdata[5],itemdata[6]]
                session.modified=True
                print(session)
                flash(f'Item {itemdata[1]} added to cart')
                return redirect(url_for('index'))
            else:
                session[session.get('user')][itemid][2]+=1
                session.modified=True
                print(session)
                flash('Item already in cart')
                return redirect(url_for('index'))
    else:
        flash('To add items into cart pls login')
        return redirect(url_for('userlogin'))
    
#view cart
@app.route('/viewcart')
def viewcart():
    if session.get('user'):
        items=session[session.get('user')]
        if items:
            return render_template('cart.html',items=items)
        else:
            flash('No item added to cart')
            return render_template('cart.html',items=items)
    else:
        flash(f'please login to view cart items')
        return redirect(url_for('userlogin'))
@app.route('/removecartitem/<itemid>')
def removecartitem(itemid):
    if session.get('user'):
        if session[session.get('user')]:
            session[session.get('user')].pop(itemid)
            flash(f'{itemid} removed from cart')
            return redirect(url_for('viewcart'))
        else:
            flash('no items in cart to remove')
            return redirect(url_for('index'))
    else:
        flash('pls login to remove items from cart')
        return redirect(url_for('userlogin'))
@app.route('/category/<ctype>')
def category(ctype):
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(itemid),item_name,item_description,price,quantity,category,item_image from items where category=%s',[ctype])
        items_data=cursor.fetchall()
        print(items_data)
    except Exception as e:
        print(f'error is {e}')
        flash('could not fetch items data')
        return redirect(url_for('index'))
    else:
        return render_template('dashboard.html',items_data=items_data)
@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    if request.method=='POST':
        user_givenemail=request.form['email']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(useremail) from userdata where useremail=%s',[user_givenemail])
            count_email=cursor.fetchone()
        except Exception as e:
            print(e)
            flash('Database connection lost')
            return redirect(url_for('usercreate'))
        else:
            if count_email[0]==1:
                subject='Reset link for user password'
                body=f"use the given link for update password : {url_for('newpassword',id_user=endata(user_givenemail),_external=True)}"
                send_mail(to=user_givenemail,body=body,subject=subject)
                flash(f'Reset link has been sent to given mail {user_givenemail}')
                return redirect(url_for('forgotpassword'))
            elif count_email[0]==0:
                flash('please create account by sign up')
                return redirect(url_for('usercreate'))
    return render_template('forgotpassword.html')
@app.route('/newpassword/<id_user>',methods=['GET','PUT'])
def newpassword(id_user):
    try:
        user_email=dedata(id_user)
    except Exception as e:
        flash('Could not get the user email')
        return redirect(url_for('forgotpassword'))
    else:
        if request.method=='PUT':
            npassword=request.get_json()
            print(npassword['new_password'])
            cursor=mydb.cursor(buffered=True)
            hash_updatedpwd=bcrypt.hashpw(npassword['new_password'].encode('utf-8'),bcrypt.gensalt())
            print(hash_updatedpwd)
            cursor.execute('update userdata set password=%s where useremail=%s',[hash_updatedpwd,user_email])
            mydb.commit()
            cursor.close()
            flash('password updated')
            return jsonify({"message":"password updated successfully"})
    return render_template('newpassword.html',id_user=id_user)
#user logout
@app.route('/userlogout')
def userlogout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('userlogin'))
    else:
        flash('To logout please login first')
        return redirect(url_for('userlogin'))
@app.route('/pay/<itemid>',methods=['GET','POST'])
def pay(itemid):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select bin_to_uuid(item_id),item_name,item_description,price,quantity,category,item_image from items where item_id=uuid_to_bin(%s)',[itemid])
            item_data=cursor.fetchone()
        except Exception as e:
            print(f'error is {e}')
            flash('could fetch item data')
            return redirect(url_for('index'))
        else:
            if request.method=='POST':
                quantity=int(request.form['qyt'])
            price=item_data[3]*100
            amount=int(quantity * price)
            print(f'creating payment for item:{itemid} with total_amount{amount} name {item_data[1]}')
            order=client.order.create({
                "amount":amount,
                "currency":"INR",
                "receipt":"receipt#1",
                "payment_capture":"1"
            })
        print(f"order created:{order}")
        return render_template('pay.html',name=item_data[1],order=order,itemid=itemid,total_amount=amount,quantity=quantity)
    else:
        flash("plz login frist")
        return redirect(url_for('userlogin'))
@app.route('/success',methods=['POST'])
def success():
    if session.get('user'):
        payment_id=request.form['razorpay_payment_id']
        order_id=request.form['razorpay_order_id']
        signature=request.form['razorpay_signature']
        itemid=request.form['itemid']
        total_amount=request.form['total_price']
        quantity=request.form['qyt']
        item_name=request.form['name']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select bin_to_uuid(item_id),item_name,item_description,price,quantity,category,item_image from items where item_id=uuid_to_bin(%s)',[itemid])
            item_data=cursor.fetchone()
        except Exception as e:
            print(f'Error is {e}')
            flash('could not fetch data')
            return redirect(url_for('index'))
        else:
            params_dict={
                "razorpay_payment_id":payment_id,
                "razorpay_order_id":order_id,
                "razorpay_signature":signature

            }
            try:
                client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerifcationError:
                return 'Payment verification failed!',400
            else:
                cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
                user_id=cursor.fetchone()
                cursor.execute('insert into orders(order_id,item_id,item_name,quantity,item_image,total_amount,payment_by) values(%s,uuid_to_bin(%s),%s,%s,%s,%s,%s)',[order_id,itemid,item_name,quantity,item_data[6],total_amount,user_id[0]])
                mydb.commit()
                flash('order details registered successfully')
                return redirect(url_for('index'))
    else:
        flash('Please login first')
#my orders
@app.route('/myorders')
def myorders():
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
            user_id=cursor.fetchone()
            cursor.execute('select bin_to_uuid(item_id),order_id,item_name,quantity,item_image,total_amount from orders where payment_by=%s',[user_id[0]])
            orderlist=cursor.fetchall()
        except Exception as e:
            print(e)
            flash('could not fetch order details')
            return redirect(url_for('index'))
        else:
            if orderlist:
                return render_template('orders.html',orderlist=orderlist)
            else:
                flash('no orders placed')
                return redirect(url_for('index'))
    else:
        flash('Please login first')
        return redirect(url_for('userlogin'))

#get invoice
@app.route('/getinvoice/<orderid>.pdf')
def getinvoice(orderid):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid,username,useremail,usergender,address,phone_no from userdata where useremail=%s',[session.get('user')])
            user_data=cursor.fetchone()
            cursor.execute('select bin_to_uuid(item_id),order_id,item_name,quantity,item_image,total_amount from orders where payment_by=%s',[user_data[0]])
            order_data=cursor.fetchone()
            try:
                html=render_template('bill.html',order_data=order_data,user_data=user_data)
                pdf=pdfkit.from_string(html,False,configuration=config)
                response=Response(pdf,content_type='application/pdf')
                response.headers['content-Dispositon']='inline; filename=output.pdf'
                return response
            except Exception as e:
                print(e)
                flash('could not convert pdf')
                return redirect(url_for('myorders'))
        except Exception as e:
            print(e)
            flash('could not fetch order details')
            return redirect(url_for('index'))
    else:
        flash('Please login first')
        return redirect(url_for('userlogin'))
@app.route('/description/<itemid>')
def description(itemid):
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(item_id),item_name,item_description,price,quantity,category,item_image from items where item_id=uuid_to_bin(%s)',[itemid])
        desc_item=cursor.fetchone()
    except Exception as e:
        print(f'Error is {e}')
        flash('could fetch items data')
        return redirect(url_for('index'))
    else:
        return render_template('description.html',desc_item=desc_item)

# add reviews
@app.route('/addreview/<itemid>',methods=['GET','POST'])
def addreview(itemid):
    if session.get('user'):
        if request.method=='POST':
            review_title=request.form['title']
            review_text=request.form['review']
            review_rating=request.form['rate']
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
                user_id=cursor.fetchone()
                if user_id:
                    cursor.execute('insert into reviews(review_title,review_text,rating,item_id,user_id) values(%s,%s,%s,uuid_to_bin(%s),%s)',[review_title,review_text,review_rating,itemid,user_id[0]])
                    mydb.commit()
                    cursor.close()
                else:
                    flash('Could not fetch user details')
                    return redirect(url_for('description',itemid=itemid))
            except Exception as e:
                print(e)
                flash('could not fetch user details')
                return redirect(url_for('description',itemid=itemid))
            else:
                flash('Review added succesfully')
                return redirect(url_for('description',itemid=itemid))
        return render_template('review.html')
    else:
        flash('Please login first')
        return redirect(url_for('userlogin'))
#search 
@app.route('/user_search',methods=['GET','POST'])
def user_search():
    if request.method=='POST':
        sdata=request.form['search']
        strg=['A-Za-z0-9']
        pattern=re.compile(f'^{strg}',re.IGNORECASE)
        if re.match(pattern,sdata):
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select bin_to_uuid(item_id),item_name,item_description,price,quantity,category,item_image from items where item_name like %s or item_description like %s or price like %s or quantity like %s or category like %s or item_image like %s',['%'+sdata+'%','%'+sdata+'%','%'+sdata+'%','%'+sdata+'%','%'+sdata+'%','%'+sdata+'%'])
                search_result=cursor.fetchall()
            except Exception as e:
                print(e)
                flash('could fetch search result')
                return redirect(url_for('index'))
            else:
                return render_template('dashboard.html',items_data=search_result)
        else:
            flash('No search data given')
            return redirect(url_for('index'))
app.run(use_reloader=True, debug=True)  