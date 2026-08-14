# -*- coding: utf-8 -*-

# ============================
# Google Sheets
# ============================

import time
import serial
import json
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
	"https://www.googleapis.com/auth/spreadsheets",
	"https://www.googleapis.com/auth/drive"
]


CREDS = Credentials.from_service_account_file(
	r"D:\A CiRA Database\Database\credentials.json",
	scopes=SCOPES
)


gc = gspread.authorize(CREDS)

sheet = gc.open("LicensePlateDatabase").worksheet("Database")
log_sheet = gc.open("LicensePlateDatabase").worksheet("Log")


# ============================
# Arduino
# ============================

try:
    arduino = serial.Serial("COM3", 9600, timeout=1)
    time.sleep(2)
    ARDUINO_CONNECTED = True
    print("[ARDUINO] Connected")
except Exception:
    arduino = None
    ARDUINO_CONNECTED = False
    print("[ARDUINO] Not connected - Simulation Mode")


# ============================
# ป้องกัน Log ซ้ำ
# ============================

# ป้องกันการประมวลผลซ้ำด้วย OCR State
# ไม่จำเป็นต้องใช้ Cooldown แล้ว


# ============================
# OCR State
# ============================

STATE_FILE = r"D:\A CiRA Database\Database\ocr_state.json"

STABLE_TIME = 1.5


# ============================
# ฟังก์ชัน State
# ============================

def load_state():

	if not os.path.exists(STATE_FILE):

		return {
			"plate": "",
			"province": "",
			"since": 0,
			"processed": False
		}


	try:

		with open(
			STATE_FILE,
			"r",
			encoding="utf-8"
		) as f:

			return json.load(f)


	except Exception:

		return {
			"plate": "",
			"province": "",
			"since": 0,
			"processed": False
		}


def save_state(state):

	try:

		with open(
			STATE_FILE,
			"w",
			encoding="utf-8"
		) as f:

			json.dump(
				state,
				f,
				ensure_ascii=False
			)

	except Exception as e:

		print("State Error:", e)


# ============================
# ฟังก์ชันเรียงตำแหน่ง
# ============================

def myFunc(e):
	return e["x"]


# ============================
# ตัวอักษรทะเบียน
# ============================

alphabes_dict = {

	"0": "0",
	"1": "1",
	"2": "2",
	"3": "3",
	"4": "4",
	"5": "5",
	"6": "6",
	"7": "7",
	"8": "8",
	"9": "9",

	"t1": "ก",
	"t2": "ข",
	"t3": "ฃ",
	"t4": "ค",
	"t5": "ฅ",
	"t6": "ฆ",
	"t7": "ง",
	"t8": "จ",
	"t9": "ฉ",
	"t10": "ช",
	"t11": "ซ",
	"t12": "ฌ",
	"t13": "ญ",
	"t14": "ฎ",
	"t15": "ฏ",
	"t16": "ฐ",
	"t17": "ฑ",
	"t18": "ฒ",
	"t19": "ณ",
	"t20": "ด",
	"t21": "ต",
	"t22": "ถ",
	"t23": "ท",
	"t24": "ธ",
	"t25": "น",
	"t26": "บ",
	"t27": "ป",
	"t28": "ผ",
	"t29": "ฝ",
	"t30": "พ",
	"t31": "ฟ",
	"t32": "ภ",
	"t33": "ม",
	"t34": "ย",
	"t35": "ร",
	"t36": "ล",
	"t37": "ว",
	"t38": "ศ",
	"t39": "ษ",
	"t40": "ส",
	"t41": "ห",
	"t42": "ฬ",
	"t43": "อ",
	"t44": "ฮ"
}


# ============================
# จังหวัด P1-P77
# ============================

province_dict = {

	"P1": "กระบี่",
	"P2": "กรุงเทพมหานคร",
	"P3": "กาญจนบุรี",
	"P4": "กาฬสินธุ์",
	"P5": "กำแพงเพชร",
	"P6": "ขอนแก่น",
	"P7": "จันทบุรี",
	"P8": "ฉะเชิงเทรา",
	"P9": "ชลบุรี",
	"P10": "ชัยนาท",
	"P11": "ชัยภูมิ",
	"P12": "ชุมพร",
	"P13": "เชียงราย",
	"P14": "เชียงใหม่",
	"P15": "ตรัง",
	"P16": "ตราด",
	"P17": "ตาก",
	"P18": "นครนายก",
	"P19": "นครปฐม",
	"P20": "นครพนม",
	"P21": "นครราชสีมา",
	"P22": "นครศรีธรรมราช",
	"P23": "นครสวรรค์",
	"P24": "นนทบุรี",
	"P25": "นราธิวาส",
	"P26": "น่าน",
	"P27": "บึงกาฬ",
	"P28": "บุรีรัมย์",
	"P29": "ปทุมธานี",
	"P30": "ประจวบคีรีขันธ์",
	"P31": "ปราจีนบุรี",
	"P32": "ปัตตานี",
	"P33": "พระนครศรีอยุธยา",
	"P34": "พะเยา",
	"P35": "พังงา",
	"P36": "พัทลุง",
	"P37": "พิจิตร",
	"P38": "พิษณุโลก",
	"P39": "เพชรบุรี",
	"P40": "เพชรบูรณ์",
	"P41": "แพร่",
	"P42": "ภูเก็ต",
	"P43": "มหาสารคาม",
	"P44": "มุกดาหาร",
	"P45": "แม่ฮ่องสอน",
	"P46": "ยโสธร",
	"P47": "ยะลา",
	"P48": "ร้อยเอ็ด",
	"P49": "ระนอง",
	"P50": "ระยอง",
	"P51": "ราชบุรี",
	"P52": "ลพบุรี",
	"P53": "ลำปาง",
	"P54": "ลำพูน",
	"P55": "เลย",
	"P56": "ศรีสะเกษ",
	"P57": "สกลนคร",
	"P58": "สงขลา",
	"P59": "สตูล",
	"P60": "สมุทรปราการ",
	"P61": "สมุทรสงคราม",
	"P62": "สมุทรสาคร",
	"P63": "สระแก้ว",
	"P64": "สระบุรี",
	"P65": "สิงห์บุรี",
	"P66": "สุโขทัย",
	"P67": "สุพรรณบุรี",
	"P68": "สุราษฎร์ธานี",
	"P69": "สุรินทร์",
	"P70": "หนองคาย",
	"P71": "หนองบัวลำภู",
	"P72": "อ่างทอง",
	"P73": "อำนาจเจริญ",
	"P74": "อุดรธานี",
	"P75": "อุตรดิตถ์",
	"P76": "อุทัยธานี",
	"P77": "อุบลราชธานี"
}


# ============================
# อ่าน Payload
# ============================

detects = payload["DeepD_D"]["detects"]


# ============================================================
# กรณี "ไม่พบป้ายทะเบียน"
# ============================================================

if not detects or detects[0]["name"] != "licenseplate":

	# รีเซ็ต State
	state = {
		"plate": "",
		"province": "",
		"since": 0,
		"processed": False
	}

	save_state(state)


	payload["license"] = ""
	payload["province"] = ""
	payload["member"] = "-"
	payload["status"] = "NO PLATE"

	payload["label"] = (
		"ทะเบียน : -\n"
		"จังหวัด : -\n"
		"สมาชิก : -\n"
		"สถานะ : NO PLATE"
	)


# ============================================================
# กรณีพบป้ายทะเบียน
# ============================================================

else:

	objects = detects[0]["objects"]

	plate_objects = []

	province = ""


	# ============================
	# แยกตัวอักษรกับจังหวัด
	# ============================

	for obj in objects:

		name = obj["name"]


		# จังหวัด
		if name.startswith("P"):

			province = province_dict.get(
				name,
				name
			)


		else:

			# T1 -> t1
			if name.startswith("T"):

				obj["name"] = name.lower()

			plate_objects.append(obj)


	# ============================
	# เรียงซ้าย -> ขวา
	# ============================

	plate_objects.sort(
		key=myFunc
	)


	# ============================
	# สร้างทะเบียน
	# ============================

	license_plate = ""


	for obj in plate_objects:

		name = obj["name"]

		if name in alphabes_dict:

			license_plate += alphabes_dict[name]


	# ============================
	# ใส่กลับ Payload
	# ============================

	payload["license"] = license_plate
	payload["province"] = province

	payload["license_full"] = (
		f"{license_plate} {province}"
	)


	# ============================
	# โหลด State
	# ============================

	state = load_state()

	current_time = time.time()


	# ============================
	# ตรวจว่าค่า OCR เปลี่ยนหรือไม่
	# ============================

	if (
		state["plate"] != license_plate
		or
		state["province"] != province
	):

		# ค่าเปลี่ยน → เริ่มจับเวลาใหม่

		state["plate"] = license_plate
		state["province"] = province
		state["since"] = current_time
		state["processed"] = False

		save_state(state)


	# ============================
	# คำนวณเวลาที่ค่าเดิมค้าง
	# ============================

	elapsed = (
		current_time - state["since"]
	)


	# ========================================================
	# ยังไม่ครบ 3 วินาที
	# ========================================================

	if elapsed < STABLE_TIME:

		payload["member"] = "-"
		payload["status"] = "CHECKING"

		payload["label"] = (
			"ทะเบียน : {}\n"
			"จังหวัด : {}\n"
			"สมาชิก : -\n"
			"สถานะ : CHECKING"
		).format(
			license_plate,
			province
		)


	# ========================================================
	# ครบ 3 วินาทีแล้ว แต่ยังไม่เคยประมวลผล
	# ========================================================

	elif not state["processed"]:

		member = "-"
		status = "NOT FOUND"


		# ============================
		# ค้นหา Google Sheets
		# ============================

		try:

			for row in sheet.get_all_records():

				if (
					str(row["Plate"]).strip()
					== license_plate
					and
					str(row["Province"]).strip()
					== province
				):

					member = str(
						row.get(
							"Member",
							"-"
						)
					)

					status = "FOUND"

					break


		except Exception as e:

			print(
				"Google Sheets Error:",
				e
			)

			member = "-"
			status = "SHEET ERROR"


		# ====================================================
		# FOUND
		# ====================================================

		if status == "FOUND":

			try:

				# สั่ง Arduino เปิดไม้กั้น
				arduino.write(
					b"OPEN\n"
				)


				print(
					"========== BARRIER OPEN =========="
				)


				# บันทึก Log
				log_sheet.append_row([
					datetime.now().strftime(
						"%Y-%m-%d %H:%M:%S"
					),
					license_plate,
					province,
					member,
					"OPEN",
					"FOUND"
				])


			except Exception as e:

				print(
					"Arduino / Log Error:",
					e
				)


		# ====================================================
		# NOT FOUND
		# ====================================================

		elif status == "NOT FOUND":

			try:

				log_sheet.append_row([
					datetime.now().strftime(
						"%Y-%m-%d %H:%M:%S"
					),
					license_plate,
					province,
					"-",
					"-",
					"NOT FOUND"
				])


			except Exception as e:

				print(
					"Log Error:",
					e
				)


		# ====================================================
		# ทำเครื่องหมายว่า Process แล้ว
		# ====================================================

		state["processed"] = True

		save_state(state)


		# ============================
		# Label
		# ============================

		payload["member"] = member
		payload["status"] = status

		payload["label"] = (
			"ทะเบียน : {}\n"
			"จังหวัด : {}\n"
			"สมาชิก : {}\n"
			"สถานะ : {}"
		).format(
			license_plate,
			province,
			member,
			status
		)


	# ========================================================
	# ครบ 3 วินาทีและประมวลผลไปแล้ว
	# ========================================================

	else:

		# ไม่เช็ก Google Sheets
		# ไม่สั่ง Arduino
		# ไม่เขียน Log ซ้ำ

		payload["member"] = "-"
		payload["status"] = "READY"

		payload["label"] = (
			"ทะเบียน : {}\n"
			"จังหวัด : {}\n"
			"สมาชิก : -\n"
			"สถานะ : READY"
		).format(
			license_plate,
			province
		)


# ============================
# แสดงผล
# ============================

print(
	payload["label"]
)