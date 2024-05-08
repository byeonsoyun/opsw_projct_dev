from flask import Flask, jsonify, request
import sqlite3
import datetime

app = Flask(__name__)

# SQLite 데이터베이스 연결
conn = sqlite3.connect('refrigerator.db')
cursor = conn.cursor()

# 음식 목록 추가 API
@app.route('/foods', methods=['POST'])
def add_food():
    data = request.get_json()
    name = data['name']
    category = data['category']
    purchase_date = data['purchase_date']
    expiration_date = data['expiration_date']
    refrigerator_id = data['refrigerator_id']
    
    # 유통기한 날짜 변환
    expiration_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d').date()
    
    # 음식을 데이터베이스에 추가
    cursor.execute("INSERT INTO foods (name, category, purchase_date, expiration_date, refrigerator_id) VALUES (?, ?, ?, ?, ?)", 
                   (name, category, purchase_date, expiration_date, refrigerator_id))
    conn.commit()
    
    return jsonify({'message': 'Food added successfully'}), 201

# 음식 목록 조회 API
@app.route('/foods', methods=['GET'])
def get_foods():
    refrigerator_id = request.args.get('refrigerator_id')
    
    # 해당 냉장고에 있는 음식 목록 조회
    cursor.execute("SELECT * FROM foods WHERE refrigerator_id = ?", (refrigerator_id,))
    foods = cursor.fetchall()
    
    food_list = []
    for food in foods:
        food_dict = {
            'id': food[0],
            'name': food[1],
            'category': food[2],
            'purchase_date': food[3],
            'expiration_date': food[4]
        }
        food_list.append(food_dict)
    
    return jsonify({'foods': food_list}), 200

# 유통기한 알림 API
@app.route('/expiration-alert', methods=['GET'])
def expiration_alert():
    today = datetime.date.today()
    
    # 오늘부터 3일 후까지의 유통기한이 끝나는 음식 목록 조회
    cursor.execute("SELECT * FROM foods WHERE expiration_date BETWEEN ? AND ?", (today, today + datetime.timedelta(days=3)))
    foods = cursor.fetchall()
    
    food_list = []
    for food in foods:
        food_dict = {
            'id': food[0],
            'name': food[1],
            'category': food[2],
            'purchase_date': food[3],
            'expiration_date': food[4]
        }
        food_list.append(food_dict)
    
    return jsonify({'foods': food_list}), 200

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
