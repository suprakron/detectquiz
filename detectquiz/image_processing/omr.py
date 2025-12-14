import cv2
import numpy as np

def process_omr_image(file):
    """
    รับไฟล์ภาพนักเรียน ตรวจเครื่องหมาย OMR แล้วคืน dict ของคำตอบ
    """
    # อ่านภาพเป็น grayscale
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    file.seek(0)  # รีเซ็ต pointer ของไฟล์
    
    # ตัวอย่าง: ขั้นตอนง่ายๆ (คุณต้องปรับตามฟอร์มจริง)
    # threshold
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    
    # สมมติตรวจ 20 ข้อ
    answers = {}
    for i in range(1, 21):
        # ที่นี่คุณต้องใส่ logic ตรวจว่า mark อยู่ตำแหน่งไหน
        answers[str(i)] = "A"  # แค่ตัวอย่าง
    
    return answers

def compare_with_answer_key(student_answers, answer_key):
    """
    เปรียบเทียบคำตอบนักเรียนกับเฉลย
    คืนค่า dict: {"correct": int, "wrong": int, "result": {...}}
    """
    correct = 0
    wrong = 0
    result = {}
    for q, ans in answer_key.items():
        student_ans = student_answers.get(q)
        if student_ans == ans:
            correct += 1
            result[q] = True
        else:
            wrong += 1
            result[q] = False
    return {"correct": correct, "wrong": wrong, "result": result}
