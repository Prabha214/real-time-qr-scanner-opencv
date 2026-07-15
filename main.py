import cv2
import pyzbar.pyzbar as pyzbar
import time
import winsound


def play_beep():
    frequency = 2500  # Set the frequency in Hertz (Hz)
    duration = 400  # Set the duration in milliseconds (ms)
    winsound.Beep(frequency, duration)


def scan_qr_code(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    qr_codes = []

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        barcode_data = barcode.data.decode("utf-8")
        qr_codes.append({'data': barcode_data, 'bbox': (x, y, w, h)})
    return qr_codes


cap = cv2.VideoCapture(0)
last_scan_time = 0

while True:
    ret, frame = cap.read()
    detected_qr_codes = scan_qr_code(frame)

    if detected_qr_codes:
        current_time = time.time()

        if current_time - last_scan_time >= 2:
            last_scan_time = current_time

            for qr_code in detected_qr_codes:
                (x, y, w, h) = qr_code['bbox']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, qr_code['data'], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                play_beep()
                
                student_info = {}
                data_string = qr_code['data']
                data_lines = [line.strip() for line in data_string.splitlines() if line.strip()]
                for line in data_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        student_info[key.strip()] = value.strip()
                try:
                    print(student_info["NAME"])
                except KeyError:
                    print(qr_code['data'])
                break

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
