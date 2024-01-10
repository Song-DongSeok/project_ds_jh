from flask import Flask, render_template, request, redirect
from cs50 import SQL
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = Flask(__name__)

db = SQL("sqlite:///orders.db")


@app.route('/',  methods=["GET", "POST"])
def home():
    return render_template('index.html')


@app.route('/drinkorder.html', methods=["GET", "POST"])
def drinkorder():
    return render_template('drinkorder.html')


@app.route('/checkout',  methods=["GET", "POST"])
def checkout():
    if request.method == 'POST':
        order_time = request.form.get('timestamp')
        st_id = request.form.get("studentId")
        
        AM = request.form.get("아메리카노")
        LA = request.form.get("라떼")
        CH = request.form.get("차이티")
        PR = request.form.get("프라프치노")
        SM = request.form.get("스무디")
        AD = request.form.get("에이드")
        
        duration = 3*int(AM) + 6*int(LA) + 9*int(CH) + 6*int(PR) + 9*int(SM) + 3*int(AD)

        db.execute("INSERT INTO orders (order_time, st_id, AM, LA, CH, PR, SM, AD, order_remain, order_duration) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   order_time, st_id, AM, LA, CH, PR, SM, AD, duration, duration)

        return redirect("/")

    
'''
@app.route('/scheduling',  methods=["GET", "POST"])
def scheduling():
    order = db.execute("SELECT * FROM orders")
    schedul = "FIFO"
    
    while order:
        # 30초동안 "FIFO" 반환
        time.sleep(30)
        schedul = "FIFO"

        # 15초동안 "SJF" 반환
        time.sleep(15)
        schedul = "SJF"
        
    return redirect("/")
'''

@app.route('/status.html',  methods=["GET", "POST"])
def status():
    return render_template('status.html')


@app.route('/check_status',  methods=["GET", "POST"])
def check_status():
    if request.method == 'POST':
        st_id = request.form.get('employeeNumber')
        db_st_id = db.execute("SELECT * FROM orders WHERE st_id = ?", st_id)
        db_all = db.execute("SELECT * FROM orders")

        if st_id == "manager":
            return render_template("manager.html", db_all=db_all)
        elif (len(st_id) == 5) and db_st_id:
            return render_template("myorder.html", st_id=st_id, db_st_id=db_st_id)
        else:
            error_message = "입력하신 교번이 잘못되었거나 주문을 찾을 수 없습니다."
            return render_template("status.html", error_message=error_message)


@app.route('/myorder.html', methods=['GET', 'POST'])
def myorder():
    return render_template('myorder.html')


@app.route('/manager.html', methods=['GET', 'POST'])
def manager():
    return render_template('manager.html')


################APScheduler를 사용한 백그라운드 음료 제작 스케줄링##################
sec = 0
def scheduling():
    global sec
    if 0 <= (sec // 45) and (sec // 45) < 30:
        FIFO()
    else:
        SJF()
    
    sec += 1

def making_drink(drink):
    if drink == "AM":
        time.sleep(3)
        
    elif drink == "LA":
        time.sleep(6)
        
    elif drink == "CH":
        time.sleep(9)
        
    elif drink == "PR":
        time.sleep(6)
        
    elif drink == "SM":
        time.sleep(9)
        
    elif drink == "AD":
        time.sleep(3)
        

def FIFO():
    orders = db.execute("SELECT * FROM orders")
    print("Scheduled task executed!")

def SJF():
    order = db.execute("SELECT * FROM orders")
    print("Scheduled task executed!")

# APScheduler 설정
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(scheduling, 'interval', seconds=1)

scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
