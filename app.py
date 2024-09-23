from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import mysql.connector
import random
import re
from pythainlp.tokenize import word_tokenize
from pythainlp.tag import pos_tag

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from flask import send_file
from datetime import datetime

import io

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'  # ใช้ secret key สำหรับการเข้ารหัส session

host = "localhost"
user = "root"
password = ""
db = "mathprob"
db2 = "word"

@app.route('/about')
def about():
    return render_template('about.html')

# ฟังก์ชันสำหรับสุ่มส่วนของประโยคจากตาราง part4add
def get_random_word_from_part4add():
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db2)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM part4add")
        words = mycursor.fetchall()

        if words:
            selected_word = random.choice(words)
            return selected_word['part4']
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()

# ฟังก์ชันสำหรับสุ่มส่วนของประโยคจากตาราง part4minus
def get_random_word_from_part4minus():
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db2)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM part4minus")
        words = mycursor.fetchall()

        if words:
            selected_word = random.choice(words)
            return selected_word['part4']
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()

# ฟังก์ชันสำหรับสุ่มส่วนของประโยคจากตาราง part4multiply
def get_random_word_from_part4multiply():
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db2)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM part4multiply")
        words = mycursor.fetchall()

        if words:
            selected_word = random.choice(words)
            return selected_word['part4']
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()

# ฟังก์ชันสำหรับสุ่มส่วนของประโยคจากตาราง part4divide
def get_random_word_from_part4divide():
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db2)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM part4divide")
        words = mycursor.fetchall()

        if words:
            selected_word = random.choice(words)
            return selected_word['part4']
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()

# ฟังก์ชันสุ่มประเภท
def get_random_type():
    types = ["object", "fruit", "vehicle", "animal", "plant", "food"]
    random_type = random.choice(types)
    print(f"สุ่มประเภท: {random_type}")  # ตรวจสอบผลลัพธ์ประเภทที่สุ่มได้
    return random_type

# แยกสัญลักษณ์ทางคณิตศาสตร์
def extractmathsym(sentence):
    pattern = re.compile(r'\d+')
    matches = pattern.findall(sentence)
    return matches

# ตัดคำและแยกชนิดคำ
def processmathprob(problem):
    tokens = word_tokenize(problem, engine='newmm')
    pos_tags = pos_tag(tokens, engine='perceptron', corpus='orchid_ud')
    nouns = [word for word, pos in pos_tags if pos.startswith('N')]
    verbs = [word for word, pos in pos_tags if pos.startswith('V')]
    math_symbols = extractmathsym(problem)
    return nouns, verbs, math_symbols

# ฟังก์ชันสำหรับสุ่มคำนามจาก database 2
def get_random_noun_from_db2():
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db2)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM word_nouns1")
        words = mycursor.fetchall()

        if words:
            selected_word = random.choice(words)
            return selected_word['nouns']
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()

# แยกส่วนประโยค
def split_sentence(sentence):
    parts = re.split(r'(\s+)', sentence)
    parts = [part for part in parts if part.strip()]
    return parts

# ฟังก์ชันสุ่มโจทย์จากตารางที่ผู้ใช้กรอกประโยคสัญลักษณ์เข้ามา
def get_random_problem_from_db(symbol_sentence, problem_type):
    try:
        # ตรวจสอบว่าสัญลักษณ์เป็นการบวก, ลบ, คูณ หรือ หาร
        if '-' in symbol_sentence:
            db_table = 'mathprob_minus'
        elif '*' in symbol_sentence:
            db_table = 'mathprob_multiply'
        elif '/' in symbol_sentence:
            db_table = 'mathprob_divide'
        else:
            db_table = 'mathprob'

        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(f"SELECT * FROM {db_table} WHERE type = %s", (problem_type,))
        problems = mycursor.fetchall()

        if problems:
            return random.choice(problems)
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()

# ฟังก์ชันดึงข้อมูลจากคอลัมน์ problem ในตาราง edit_o
def get_fruit_problems():
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database=db2)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT problem FROM edit_o")
        fruits = mycursor.fetchall()
        return [fruit['problem'] for fruit in fruits]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()

# ฟังก์ชันสุ่มตัวเลข
def generate_random_number_by_digits(digit_type):
    if digit_type == "หน่วย":
        return random.randint(1, 9)
    elif digit_type == "สิบ":
        return random.randint(10, 99)
    elif digit_type == "ร้อย":
        return random.randint(100, 999)
    elif digit_type == "พัน":
        return random.randint(1000, 9999)
    return 0

# ฟังก์ชันสุ่มโจทย์จากการเลือกสัญลักษณ์พร้อมกับการสุ่มจาก part4
def generate_problem_with_random_numbers_and_part4(math_symbol, digit_choice, problem_type):
    # เคลียร์ข้อมูลหน่วยก่อนสร้างโจทย์ใหม่
    session['units'] = []  # ลบข้อมูลหน่วยที่เก็บอยู่เดิม

    num1 = generate_random_number_by_digits(digit_choice)
    num2 = generate_random_number_by_digits(digit_choice)
    symsentence = f"{num1} {math_symbol} {num2}"

    try:
        selected_problem = get_random_problem_from_db(symsentence, problem_type)
        if selected_problem:
            original_problem = selected_problem['problem']
            # แทนที่ตัวเลขในโจทย์ด้วยตัวเลขสุ่มที่ได้
            numbers_in_problem = re.findall(r'\d+', original_problem)
            for old_num, new_num in zip(numbers_in_problem, [str(num1), str(num2)]):
                original_problem = original_problem.replace(old_num, new_num, 1)

            # แยกประโยคและแทนที่คำส่วนที่ 3 ด้วยคำจาก part4
            parts = split_sentence(original_problem)
            if len(parts) > 3:
                if '-' in symsentence:
                    new_word = get_random_word_from_part4minus()
                elif '*' in symsentence:
                    new_word = get_random_word_from_part4multiply()
                elif '/' in symsentence:
                    new_word = get_random_word_from_part4divide()
                else:
                    new_word = get_random_word_from_part4add()

                if new_word:
                    parts[3] = new_word  # แทนที่ส่วนที่ 3 ด้วยคำที่สุ่มจาก part4
                original_problem = ' '.join(parts)

            # คำนวณคำตอบ
            answer = None
            numbers_and_symbols = extractmathsym(original_problem)
            if '+' in symsentence:
                nums = [int(num) for num in numbers_and_symbols]
                answer = sum(nums)
            elif '-' in symsentence:
                nums = [int(num) for num in numbers_and_symbols]
                answer = nums[0] - sum(nums[1:])
            elif '*' in symsentence:
                nums = [int(num) for num in numbers_and_symbols]
                answer = 1
                for num in nums:
                    answer *= num
            elif '/' in symsentence:
                nums = [int(num) for num in numbers_and_symbols]
                answer = nums[0]
                for num in nums[1:]:
                    if num != 0:
                        answer /= num
                    else:
                        answer = 'ไม่สามารถหารด้วยศูนย์ได้'
                        break

            # เก็บคำตอบและหน่วยลงใน session
            if answer is not None:
                answers = session.get('answers', [])
                answers.append(answer)
                session['answers'] = answers

            # ดึงคำสุดท้ายของประโยคมาเป็นหน่วย
            tokenized_problem = word_tokenize(original_problem, engine='newmm')
            if '?' in tokenized_problem:
                question_mark_index = tokenized_problem.index('?')
                if question_mark_index > 0:
                    units = session.get('units', [])
                    units.append(tokenized_problem[question_mark_index - 1])  # เก็บคำสุดท้ายก่อนเครื่องหมาย '?' เป็นหน่วย
                    session['units'] = units
            else:
                units = session.get('units', [])
                units.append(tokenized_problem[-1])  # เก็บคำสุดท้ายของโจทย์เป็นหน่วย
                session['units'] = units

            return original_problem
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/', methods=['POST', 'GET'])
def index():
    original_problem = None
    updated_problems = session.get('updated_problems', [])  # ดึงข้อมูลโจทย์ที่สร้างไว้ก่อนหน้านี้จาก session
    answers = session.get('answers', [])  # ดึงข้อมูลคำตอบที่มีอยู่ก่อนจาก session
    units = session.get('units', [])  # ดึงข้อมูลหน่วยที่มีอยู่ก่อนจาก session
    error = None
    symsentences = ""
    problem_type = ""
    math_symbol = ""
    digit_choice = ""
    problem_count = 1  # ค่าเริ่มต้นคือ 1 ข้อ

    if request.method == 'POST':
        form = request.form

        # กรณีการสร้างโจทย์จากการสุ่มตัวเลขและสัญลักษณ์
        if 'math_symbol' in form and 'digit_choice' in form and 'noun_category' in form and 'problem_count' in form:
            math_symbol = form['math_symbol']
            digit_choice = form['digit_choice']
            problem_type = form['noun_category']
            problem_count = int(form['problem_count'])  # รับจำนวนข้อที่ผู้ใช้เลือก

            if problem_type == "random":
                problem_type = get_random_type()

            # สร้างโจทย์จากการสุ่มตัวเลขและสัญลักษณ์ที่เลือก และวนลูปตามจำนวนที่ผู้ใช้เลือก
            for _ in range(problem_count):
                generated_problem = generate_problem_with_random_numbers_and_part4(math_symbol, digit_choice, problem_type)
                if generated_problem:
                    updated_problems.append(generated_problem)

                    # คำนวณคำตอบตามสัญลักษณ์ที่สุ่มมา
                    answer = None  # ตั้งค่าเริ่มต้นของตัวแปร answer
                    numbers_and_symbols = extractmathsym(generated_problem)
                    
                    # ตรวจสอบประเภทของสัญลักษณ์ทางคณิตศาสตร์และคำนวณ
                    if '+' in generated_problem:
                        nums = [int(num) for num in numbers_and_symbols]
                        answer = sum(nums)
                    elif '-' in generated_problem:
                        nums = [int(num) for num in numbers_and_symbols]
                        answer = nums[0] - sum(nums[1:])
                    elif '*' in generated_problem:
                        nums = [int(num) for num in numbers_and_symbols]
                        answer = 1
                        for num in nums:
                            answer *= num
                    elif '/' in generated_problem:
                        nums = [int(num) for num in numbers_and_symbols]
                        answer = nums[0]
                        for num in nums[1:]:
                            if num != 0:
                                answer /= num
                            else:
                                answer = 'ไม่สามารถหารด้วยศูนย์ได้'
                                break
                    
                    # บันทึกคำตอบลงในลิสต์ answers
                    if answer is not None:
                        answers.append(answer)

                    # ดึงคำสุดท้ายจากโจทย์มาใช้เป็นหน่วยของคำตอบ
                    tokenized_problem = word_tokenize(generated_problem, engine='newmm')
                    if '?' in tokenized_problem:
                        question_mark_index = tokenized_problem.index('?')
                        if question_mark_index > 0:
                            units.append(tokenized_problem[question_mark_index - 1])
                        else:
                            units.append('')
                    else:
                        units.append(tokenized_problem[-1])
                else:
                    error = "ไม่พบโจทย์ในฐานข้อมูล"
                    break  # ถ้าเกิดข้อผิดพลาดให้หยุดการสุ่มโจทย์

        # กรณีการกรอกประโยคสัญลักษณ์
        elif 'symsen' in form and 'noun_category' in form:
            symsentences = form['symsen']  # รับประโยคสัญลักษณ์หลายๆ ประโยค
            problem_type = form['noun_category']  # ประเภทของคำนาม

            # ถ้าผู้ใช้เลือก "สุ่ม" ให้สุ่มประเภทจากที่เหลือ
            if problem_type == "random":
                problem_type = get_random_type()
                print(f"ประเภทหลังจากสุ่ม: {problem_type}")  # ตรวจสอบผลลัพธ์ประเภทที่สุ่มได้

            # แยกหลายประโยคที่ผู้ใช้กรอกเข้ามาด้วยเครื่องหมายจุลภาค (,)
            sentence_list = symsentences.split(',')

            for symsentence in sentence_list:
                symsentence = symsentence.strip()
                print("Original Sentence: ", symsentence)

                if re.match(r'^[\d\s\+\-\*\/\=\(\)]+$', symsentence):
                    numbers_and_symbols = extractmathsym(symsentence)
                    print("ตัวเลขและสัญลักษณ์: ", numbers_and_symbols)

                    try:
                        selected_problem = get_random_problem_from_db(symsentence, problem_type)
                        if selected_problem:
                            original_problem = selected_problem['problem']
                            print("Selected Problem: ", original_problem)

                            numbers_in_problem = extractmathsym(original_problem)
                            for old_num, new_num in zip(numbers_in_problem, numbers_and_symbols):
                                original_problem = original_problem.replace(old_num, new_num, 1)

                            print("Updated Problem: ", original_problem)

                            # กำหนดค่าเริ่มต้นให้กับตัวแปร answer
                            answer = None
                            
                            # ดึงคำสุดท้ายจากโจทย์มาใช้เป็นหน่วยของคำตอบ
                            tokenized_problem = word_tokenize(original_problem, engine='newmm')
                            if '?' in tokenized_problem:
                                question_mark_index = tokenized_problem.index('?')
                                if question_mark_index > 0:
                                    units.append(tokenized_problem[question_mark_index - 1])
                                else:
                                    units.append('')
                            else:
                                units.append(tokenized_problem[-1])

                            # คำนวณคำตอบตามสัญลักษณ์ที่ผู้ใช้ป้อน
                            if '+' in symsentence:
                                nums = [int(num) for num in numbers_and_symbols]
                                answer = sum(nums)
                            elif '-' in symsentence:
                                nums = [int(num) for num in numbers_and_symbols]
                                answer = nums[0] - sum(nums[1:])
                            elif '*' in symsentence:
                                nums = [int(num) for num in numbers_and_symbols]
                                answer = 1
                                for num in nums:
                                    answer *= num
                            elif '/' in symsentence:
                                nums = [int(num) for num in numbers_and_symbols]
                                answer = nums[0]
                                for num in nums[1:]:
                                    if num != 0:
                                        answer /= num
                                    else:
                                        answer = 'ไม่สามารถหารด้วยศูนย์ได้'
                                        break

                            # เก็บคำตอบลงในลิสต์ (เฉพาะเมื่อ answer ถูกกำหนดค่าแล้ว)
                            if answer is not None:
                                answers.append(answer)
                            updated_problems.append(original_problem)
                        else:
                            error = "ไม่พบโจทย์ในฐานข้อมูล"
                    except mysql.connector.Error as err:
                        error = str(err)
                    finally:
                        if 'mycursor' in locals():
                            mycursor.close()  # type: ignore
                        if 'mydb' in locals():
                            mydb.close()  # type: ignore
                else:
                    error = "เราต้องการแค่ประโยคสัญลักษณ์ทางคณิตศาสตร์"

        session['updated_problems'] = updated_problems
        session['answers'] = answers  # เก็บคำตอบลง session
        session['units'] = units  # เก็บหน่วยลง session

        # ตรวจสอบค่าของ answers และ units
        print(f"Answers: {answers}")
        print(f"Units: {units}")

    return render_template('index.html',
        updated_problems=updated_problems,
        answers=answers,
        units=units,
        error=error,
        symsentences=symsentences,
        problem_type=problem_type,
        math_symbol=math_symbol,
        digit_choice=digit_choice,
        problem_count=problem_count)

@app.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        problem_to_edit = request.form.get('problem_to_edit')
        edited_problem = request.form.get('edited_problem')
        new_fruit = request.form.get('fruit_problem_select')
        replace_word = request.form.get('replace_word_select')
        target_word = request.form.get('target_word_select')

        fruit_problems = get_fruit_problems()  # ดึงข้อมูลจากคอลัมน์ problem ในตาราง edit_o

        if problem_to_edit and edited_problem:
            updated_problems = session.get('updated_problems', [])
            try:
                index = updated_problems.index(problem_to_edit)
                updated_problems[index] = edited_problem

                # ตรวจสอบและแทนที่คำว่า "ผล" หรือ "ลูก" ที่ผู้ใช้เลือก
                if target_word and target_word in edited_problem:
                    edited_problem = edited_problem.replace(target_word, replace_word, 1)
                    updated_problems[index] = edited_problem

                # แทนที่คำนามด้วยชนิดผลไม้ที่เลือก
                nouns, verbs, _ = processmathprob(edited_problem)
                if nouns:
                    first_noun = nouns[1] if len(nouns) > 1 else nouns[0]
                    edited_problem = edited_problem.replace(first_noun, new_fruit, 1)
                    updated_problems[index] = edited_problem

                session['updated_problems'] = updated_problems
            except ValueError:
                return f"Error: '{problem_to_edit}' not found in the list", 400

            return redirect(url_for('index'))

        return render_template('edit.html', problem=problem_to_edit, fruit_problems=fruit_problems)
    else:
        problem_to_edit = request.args.get('problem')
        fruit_problems = get_fruit_problems()
        return render_template('edit.html', problem=problem_to_edit, fruit_problems=fruit_problems)

@app.route('/delete', methods=['POST'])
def delete():
    problem_to_delete = request.form.get('problem_to_delete')
    updated_problems = session.get('updated_problems', [])
    answers = session.get('answers', [])
    units = session.get('units', [])
    
    if problem_to_delete and problem_to_delete in updated_problems:
        # ค้นหาดัชนีของโจทย์ที่ต้องการลบ
        index_to_delete = updated_problems.index(problem_to_delete)
        
        # ตรวจสอบว่าดัชนีนี้อยู่ในขอบเขตของลิสต์
        if index_to_delete < len(updated_problems):
            updated_problems.pop(index_to_delete)
        
        if index_to_delete < len(answers):
            answers.pop(index_to_delete)
        
        if index_to_delete < len(units):
            units.pop(index_to_delete)

        # บันทึกค่าใหม่ลงใน session
        session['updated_problems'] = updated_problems
        session['answers'] = answers
        session['units'] = units

    return redirect(url_for('index'))


@app.route('/clear_all', methods=['POST'])
def clear_all():
    # ลบข้อมูลทั้งหมดใน session
    session['updated_problems'] = []  # กำหนดเป็นลิสต์ว่าง
    session['answers'] = []  # กำหนดเป็นลิสต์ว่าง
    session['units'] = []  # กำหนดเป็นลิสต์ว่าง
    
    return redirect(url_for('index'))


# การบันทึกโจทย์
@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    updated_problems = session.get('updated_problems', [])
    
    # ตรวจสอบว่าโจทย์ไม่ว่างเปล่า
    if not updated_problems:
        return "No problems to download", 400
    
    # สร้างไฟล์ PDF ใน memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # เพิ่มการลงทะเบียนฟอนต์ภาษาไทย
    pdfmetrics.registerFont(TTFont('THSarabun', 'THSarabunNew.ttf'))
    
    # ตั้งค่าฟอนต์ภาษาไทยและขนาดฟอนต์
    text_object = c.beginText(50, 750)
    text_object.setFont("THSarabun", 16)
    
    # วาด "ชื่อ", "นามสกุล", "เลขที่", "วันที่" ในบรรทัดเดียวกัน
    text_object.textLine(f"ชื่อ: ____________  นามสกุล: ____________  เลขที่: ______        วันที่: ____________")
    c.drawText(text_object)
    
    # ขยับ "คะแนน" ไปทางขวาสุด
    c.setFont("THSarabun", 16)
    c.drawRightString(580, 750, "คะแนน: ______")  # ขยับคะแนนไปมุมขวาสุด

    # วาดข้อความ "Math Problem Generator" ตรงกลางของหน้า
    c.setFont("THSarabun", 20)  # ตั้งขนาดฟอนต์ใหญ่ขึ้นสำหรับหัวข้อ
    c.drawCentredString(300, 720, "Math Problem Generator")  # ข้อความตรงกลางที่พิกัด y = 720

    # เริ่มต้นตำแหน่ง y สำหรับโจทย์
    text_object = c.beginText(50, 680)  # เริ่มที่ตำแหน่งล่างลงมาจาก "Math Problem Generator"
    text_object.setFont("THSarabun", 16)
    
    for i, problem in enumerate(updated_problems, 1):
        text_object.textLine(f"{i}) {problem}")
        text_object.moveCursor(0, 10)  # ลดระยะห่างระหว่างโจทย์กับบรรทัดคำว่า "ตอบ" ให้เหลือเพียง 10
        text_object.textLine("ตอบ: .....................................................................................")  # เพิ่มบรรทัดคำว่า "ตอบ" ใต้โจทย์
        text_object.moveCursor(0, 5)  # ลดระยะห่างระหว่างโจทย์แต่ละข้อ
        
        # ตรวจสอบว่าถ้าตำแหน่ง y ต่ำเกินไป จะขึ้นหน้าใหม่
        if text_object.getY() < 100:  # กำหนดจุดที่ควรเริ่มหน้ากระดาษใหม่
            c.drawText(text_object)  # วาดข้อความบนหน้ากระดาษ
            c.showPage()  # ขึ้นหน้ากระดาษใหม่
            text_object = c.beginText(50, 750)  # ตั้งตำแหน่ง y ใหม่สำหรับหน้าใหม่
            text_object.setFont("THSarabun", 16)
    
    c.drawText(text_object)
    
    # เพิ่มเลขหน้าที่มุมล่างขวา
    for page_num in range(1, c.getPageNumber() + 1):
        c.setFont("THSarabun", 12)
        c.drawRightString(580, 20, f"Page {page_num}")
    
    c.save()
    
    # ส่งไฟล์ PDF กลับให้ผู้ใช้
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="math_problems.pdf", mimetype='application/pdf')



if __name__ == "__main__":
    app.run(debug=True)





































