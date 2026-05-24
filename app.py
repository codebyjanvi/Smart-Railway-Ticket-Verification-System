from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3, random, base64, os, uuid
import qrcode
import face_recognition
from datetime import timedelta
from pyngrok import ngrok, conf

# ---------------- APP ----------------
app = Flask(__name__)
app.secret_key = "supersecretkey"
app.permanent_session_lifetime = timedelta(minutes=10)

# ---------------- NGROK ----------------
ngrok.set_auth_token("3CoTEQbIBktlMxsye2AggO5CzQv_2tNUGDs5Z3KSzthYUsgar")

public_url = ngrok.connect(5000).public_url
print("🔗 Public URL:", public_url)

# ---------------- PAYMENT STATUS ----------------
payment_status = {
    "paid": False
}

# ---------------- PAYMENT SUCCESS ----------------
@app.route("/payment_success")
def payment_success():

    payment_status["paid"] = True

    return """
    <html>
    <body style="
        font-family:Segoe UI;
        background:#111827;
        color:white;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
        flex-direction:column;
    ">

    <h1>✅ Payment Successful</h1>
    <h2>Ticket Booking Activated</h2>

    </body>
    </html>
    """

# ---------------- CHECK PAYMENT ----------------

@app.route("/check_payment")
def check_payment():

    return jsonify(payment_status)
app.permanent_session_lifetime = timedelta(minutes=10)

os.makedirs("static/temp", exist_ok=True)
os.makedirs("static/faces", exist_ok=True)
os.makedirs("static/qr", exist_ok=True)

# ---------------- TRAIN DATA ----------------
train_data = {
    "Bangalore-Mumbai": {"AC": 1500, "Sleeper": 800},
    "Bangalore-Delhi": {"AC": 2500, "Sleeper": 1200},
    
    # 🔵 SOUTH INDIA
    "Bangalore-Chennai": {"AC": 1200, "Sleeper": 600},
    "Bangalore-Hyderabad": {"AC": 1400, "Sleeper": 700},
    "Chennai-Hyderabad": {"AC": 1500, "Sleeper": 800},
    "Chennai-Kochi": {"AC": 1000, "Sleeper": 500},
    "Bangalore-Kochi": {"AC": 1100, "Sleeper": 550},
    "Hyderabad-Kochi": {"AC": 1800, "Sleeper": 900},

    # 🔵 WEST INDIA
    "Mumbai-Pune": {"AC": 800, "Sleeper": 400},
    "Mumbai-Goa": {"AC": 1200, "Sleeper": 600},
    "Mumbai-Ahmedabad": {"AC": 1400, "Sleeper": 700},
    "Pune-Goa": {"AC": 900, "Sleeper": 450},
    "Ahmedabad-Jaipur": {"AC": 1600, "Sleeper": 800},

    # 🔵 NORTH INDIA
    "Delhi-Jaipur": {"AC": 900, "Sleeper": 450},
    "Delhi-Amritsar": {"AC": 1300, "Sleeper": 650},
    "Delhi-Lucknow": {"AC": 1200, "Sleeper": 600},
    "Delhi-Chandigarh": {"AC": 800, "Sleeper": 400},
    "Delhi-Varanasi": {"AC": 1500, "Sleeper": 750},

    # 🔵 EAST INDIA
    "Kolkata-Patna": {"AC": 1100, "Sleeper": 550},
    "Kolkata-Bhubaneswar": {"AC": 1000, "Sleeper": 500},
    "Patna-Varanasi": {"AC": 700, "Sleeper": 350},
    "Kolkata-Guwahati": {"AC": 1800, "Sleeper": 900},

    # 🔵 CENTRAL INDIA
    "Bhopal-Indore": {"AC": 600, "Sleeper": 300},
    "Bhopal-Nagpur": {"AC": 900, "Sleeper": 450},
    "Nagpur-Hyderabad": {"AC": 1100, "Sleeper": 550},
    "Indore-Mumbai": {"AC": 1300, "Sleeper": 650},

    # 🔵 LONG DISTANCE (MAJOR ROUTES)
    "Bangalore-Mumbai": {"AC": 1500, "Sleeper": 800},
    "Bangalore-Delhi": {"AC": 2500, "Sleeper": 1200},
    "Mumbai-Delhi": {"AC": 2200, "Sleeper": 1100},
    "Chennai-Delhi": {"AC": 2600, "Sleeper": 1300},
    "Kolkata-Delhi": {"AC": 2400, "Sleeper": 1200},
    "Mumbai-Kolkata": {"AC": 2600, "Sleeper": 1300},

    # 🔵 TOURISM ROUTES
    "Delhi-Agra": {"AC": 700, "Sleeper": 350},
    "Jaipur-Udaipur": {"AC": 900, "Sleeper": 450},
    "Goa-Mangalore": {"AC": 800, "Sleeper": 400},
    "Kochi-Trivandrum": {"AC": 600, "Sleeper": 300},

}
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        ticket_id TEXT,
        name TEXT,
        phone TEXT,
        source TEXT,
        destination TEXT,
        date TEXT,
        seat TEXT,
        bogie TEXT,
        pnr TEXT,
        is_used INTEGER,
        face_image TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()
# ---------------- DB ----------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    # 🔥 SAFETY CHECK (AUTO CREATE TABLE IF MISSING)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS tickets(
                   ticket_id TEXT,
                   name TEXT,
                   phone TEXT,
                   source TEXT,
                   destination TEXT,
                   date TEXT,
                   seat TEXT,
                   bogie TEXT,
                   pnr TEXT,
                   is_used INTEGER,
                   is_fraud INTEGER DEFAULT 0,
                   face_image TEXT
                   )
                   """)
    conn.commit()

    return conn

# ---------------- INIT USERS ----------------
def init_users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("SELECT * FROM users WHERE username='tte'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users VALUES ('tte','123','tte')")

    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users VALUES ('admin','123','admin')")

    conn.commit()
    conn.close()

init_users()
init_db() 
# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/book')
def book():
    return render_template("book.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/upi_pay/<amount>')
def upi_pay(amount):
    return render_template("upi_pay.html", amount=amount)
# ---------------- PRICE API (FIXED) ----------------
@app.route('/get_price', methods=['POST'])
def get_price():
    data = request.get_json()

    source = data['source'].strip().title()
    destination = data['destination'].strip().title()

    route = source + "-" + destination

    if route in train_data:
        info = train_data[route]
        return jsonify({
            "price": info[data['seat']],
            "train": "Superfast Express",
            "time": "10:00 AM"
        })

    return jsonify({"error": "Route not found"})
@app.route('/generate_payment_qr', methods=['POST'])
def generate_payment_qr():
    payment_status["paid"] = False
    data = request.get_json()

    print("BOOKING DATA:", data)

    # SAFETY CHECK
    if not data:
        return jsonify({
            "error": "No booking data received"
        }), 400

    source = data.get("source", "").strip().title()
    destination = data.get("destination", "").strip().title()
    seat = data.get("seat", "Sleeper")

    route = source + "-" + destination

    print("ROUTE:", route)

    # ---------------- PRICE ----------------
    if route in train_data:

        if seat in train_data[route]:
            base = train_data[route][seat]
        else:
            base = 500

    else:
        base = 500

    platform = 20
    gst = round(base * 0.05)

    total = base + platform + gst

    # ---------------- REAL UPI LINK ----------------
    # DEMO PAYMENT PAGE LINK
    upi_link = f"{public_url}/upi_pay/{total}"

    print("UPI LINK:", upi_link)

    # ---------------- QR GENERATE ----------------
    filename = f"{uuid.uuid4().hex}.png"

    qr_path = f"static/qr/{filename}"

    qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5
    )

    qr.add_data(upi_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img.save(qr_path)

    return jsonify({
        "base": base,
        "platform": platform,
        "gst": gst,
        "total": total,
        "qr": "/" + qr_path
    })
# ---------------- LOGIN ----------------
@app.route('/login_user', methods=['POST'])
def login_user():
    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (data['username'], data['password']))
    user = cursor.fetchone()

    if user:
        session['role'] = user['role']
        session['username'] = user['username']

        if user['role'] == 'admin':
            return jsonify({"redirect": "/admin"})
        elif user['role'] == 'tte':
            return jsonify({"redirect": "/tte_dashboard"})
        else:
            return jsonify({"redirect": "/book"})

    return jsonify({"error": "Invalid login"})

# ---------------- TTE DASHBOARD ----------------
@app.route('/tte_dashboard')
def tte_dashboard():
    if session.get('role') != 'tte':
        return "❌ Access Denied"
    return render_template("tte_dashboard.html")



@app.route('/scan/<ticket_id>')
def scan_ticket(ticket_id):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # CHECK TICKET EXISTS
    cursor.execute(
        "SELECT * FROM tickets WHERE ticket_id=?",
        (ticket_id,)
    )

    ticket = cursor.fetchone()

    if ticket:

        # STORE VERIFIED DATA
        cursor.execute("""
            INSERT INTO verified_tickets
            (
                ticket_id,
                name,
                phone,
                source,
                destination,
                date,
                seat,
                bogie,
                pnr,
                face_image,
                verified_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            ticket["ticket_id"],
            ticket["name"],
            ticket["phone"],
            ticket["source"],
            ticket["destination"],
            ticket["date"],
            ticket["seat"],
            ticket["bogie"],
            ticket["pnr"],
            ticket["face_image"]
        ))

        conn.commit()
        conn.close()

        return render_template(
            "scan_result.html",
            valid=True,
            ticket_id=ticket_id
        )

    conn.close()

    return render_template(
        "scan_result.html",
        valid=False
    )


@app.route('/details/<ticket_id>')
def passenger_details(ticket_id):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tickets WHERE ticket_id=?",
        (ticket_id,)
    )

    ticket = cursor.fetchone()

    conn.close()

    if not ticket:
        return "Ticket Not Found"

    return render_template(
        "ticket_details.html",
        ticket=ticket
    )
# ---------------- SELECT BOGIE ----------------
@app.route('/select_bogie', methods=['POST'])
def select_bogie():
    if session.get('role') != 'tte':
        return "❌ Access Denied"

    data = request.get_json()
    session['bogie'] = data.get("bogie")

    return jsonify({"redirect": "/verify"})

# ---------------- VERIFY PAGE ----------------
@app.route('/verify')
def verify():
    if session.get('role') != 'tte':
        return "❌ Access Denied"
    return render_template("verify.html")

# ---------------- TICKET PAGE FIX ----------------
@app.route('/ticket/<ticket_id>')
def ticket(ticket_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
    ticket = cursor.fetchone()

    conn.close()

    return render_template("ticket.html", ticket=ticket)

# ---------------- VERIFY TICKET ----------------
@app.route('/verify_ticket', methods=['POST'])
def verify_ticket():
    data = request.get_json()

    ticket_id = data.get("ticket")
    face_data = data.get("face")

    # ---------- SAVE FACE ----------
    temp_file = None
    if face_data:
        try:
            img = face_data.split(",")[1]
            temp_file = f"static/faces/temp_{uuid.uuid4().hex}.jpg"
            with open(temp_file, "wb") as f:
                f.write(base64.b64decode(img))
        except:
            return jsonify({"status": "error", "message": "Face capture failed"})

    # ---------- DB ----------
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tickets 
        WHERE ticket_id=? AND bogie=?
    """, (ticket_id, session.get("bogie")))

    ticket = cursor.fetchone()

    if not ticket:
        return jsonify({"status": "invalid", "fine": 500})

    # ---------- FACE MATCH ----------
    try:
        known_path = "static/faces/" + str(ticket["face_image"])
        known = face_recognition.load_image_file(known_path)

        if not temp_file:
            return jsonify({"status": "fraud", "message": "No face provided", "fine": 1000})

        unknown = face_recognition.load_image_file(temp_file)

        known_enc = face_recognition.face_encodings(known)
        unknown_enc = face_recognition.face_encodings(unknown)

        if not known_enc or not unknown_enc:
            cursor.execute("UPDATE tickets SET is_fraud=1 WHERE ticket_id=?", (ticket_id,))
            conn.commit()
            return jsonify({
                "status": "fraud",
                "message": "Face not detected",
                "fine": 1000
            })

        # ---------- MATCH ----------
        distance = face_recognition.face_distance([known_enc[0]], unknown_enc[0])[0]
        confidence = round((1 - distance) * 100, 2)

        print("Confidence:", confidence)

        # 🔥 KEY FIX: STRICT MATCH
        if confidence >= 65:
            match = True
        else:
            match = False

    except Exception as e:
        print("Face error:", e)
        return jsonify({
            "status": "fraud",
            "message": "Face processing error",
            "fine": 1000
        })

    # ---------- FRAUD ----------
    if not match:
        cursor.execute("UPDATE tickets SET is_fraud=1 WHERE ticket_id=?", (ticket_id,))
        conn.commit()

        return jsonify({
            "status": "fraud",
            "message": f"Face mismatch ({confidence}%)",
            "fine": 2000
        })

    # ---------- ALREADY USED ----------
    if ticket["is_used"] == 1:
        cursor.execute("UPDATE tickets SET is_fraud=1 WHERE ticket_id=?", (ticket_id,))
        conn.commit()

        return jsonify({
            "status": "fraud",
            "message": "Ticket already used",
            "fine": 1000
        })

    # ---------- SUCCESS ----------
    cursor.execute("UPDATE tickets SET is_used=1 WHERE ticket_id=?", (ticket_id,))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "valid",
        "name": ticket["name"],
        "seat": ticket["seat"],
        "bogie": ticket["bogie"],
        "confidence": confidence
    })

@app.route('/verify/<ticket_id>')
def verify_qr(ticket_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
    ticket = cursor.fetchone()

    conn.close()

    if not ticket:
        return "❌ Invalid Ticket"

    return render_template("ticket.html", ticket=ticket)

# ---------------- BOOK TICKET ----------------
# ---------------- BOOK TICKET ----------------

@app.route('/book_ticket', methods=['POST'])
def book_ticket():

    data = request.get_json()

    name = data.get('name')
    phone = data.get('phone')
    source = data.get('source')
    destination = data.get('destination')
    date = data.get('date')
    seat = data.get('seat')
    face = data.get('face')

    ticket_id = str(uuid.uuid4())[:8]

    pnr = str(random.randint(1000000000, 9999999999))

    conn = get_db()

    cursor = conn.cursor()

    # ---------------- AUTO BOGIE ----------------

    if seat == "AC":
        bogie = "A1"
    else:
        bogie = "S1"

    # ---------------- SAVE IMAGE ----------------

    face_file = None

    if face:

        img = face.split(",")[1]

        face_file = f"{ticket_id}.jpg"

        with open(f"static/faces/{face_file}", "wb") as f:

            f.write(base64.b64decode(img))

    # ---------------- INSERT ----------------

    cursor.execute("""

    INSERT INTO tickets(

        ticket_id,
        name,
        phone,
        source,
        destination,
        date,
        seat,
        bogie,
        pnr,
        face_image

    )

    VALUES (?,?,?,?,?,?,?,?,?,?)

    """, (

        ticket_id,
        name,
        phone,
        source,
        destination,
        date,
        seat,
        bogie,
        pnr,
        face_file

    ))

    conn.commit()

    conn.close()

    # ---------------- QR ----------------

    qr_data = f"{public_url}/scan/{ticket_id}"

    qrcode.make(qr_data).save(
        f"static/qr/{ticket_id}.png"
    )

    return jsonify({

        "ticket_id": ticket_id

    })

@app.route('/bogie_stats')
def bogie_stats():
    conn = get_db()
    cursor = conn.cursor()

    bogies = ["A1", "A2", "S1", "S2", "S3"]
    stats = {}

    for b in bogies:
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE bogie=?", (b,))
        stats[b] = cursor.fetchone()[0]

    conn.close()
    return jsonify(stats)
# ---------------- PNR CHECK ----------------
@app.route('/check_pnr', methods=['POST'])
def check_pnr():
    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE pnr=?", (data['pnr'],))
    ticket = cursor.fetchone()

    conn.close()

    if not ticket:
        return jsonify({"error": "Not found"})

    return jsonify(dict(ticket))

# ---------------- PAYMENT PAGE ----------------
@app.route('/payment')
def payment():
    return render_template("payment.html")
# ---------------- CANCEL PAGE ----------------
@app.route('/cancel')
def cancel():
    return render_template("cancel.html")
@app.route('/face_verify')
def face_verify():
    if session.get('role') != 'tte':
        return "❌ Access Denied"
    return render_template("face_verify.html")
# ---------------- ADMIN FIX ----------------
@app.route('/admin')
def admin():

    conn = get_db()

    cursor = conn.cursor()

    # TOTAL TICKETS
    cursor.execute("SELECT COUNT(*) FROM tickets")
    total = cursor.fetchone()[0]

    # VERIFIED TICKETS
    cursor.execute("SELECT COUNT(*) FROM verified_tickets")
    verified = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        total=total,
        verified=verified
    )

# ---------------- CANCEL TICKET ----------------
# ---------------- CANCEL TICKET ----------------
@app.route('/cancel_ticket', methods=['POST'])
def cancel_ticket():

    data = request.get_json()

    value = data.get("ticket")

    if not value:

        return jsonify({
            "message":"❌ Enter Ticket ID or PNR"
        })

    conn = get_db()

    cursor = conn.cursor()

    # FIND TICKET
    cursor.execute("""

    SELECT * FROM tickets

    WHERE ticket_id=? OR pnr=?

    """, (value, value))

    ticket = cursor.fetchone()

    if not ticket:

        conn.close()

        return jsonify({
            "message":"❌ Ticket Not Found"
        })

    # DELETE
    cursor.execute("""

    DELETE FROM tickets

    WHERE ticket_id=? OR pnr=?

    """, (value, value))

    conn.commit()

    conn.close()

    return jsonify({
        "message":"✅ Ticket Cancelled Successfully"
    })
# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
@app.route('/pnr')
def pnr():
    return render_template("pnr.html")
@app.route('/result')
def result():
    return render_template("result.html")


@app.route("/verify_face", methods=["POST"])
def verify_face():
    try:
        data = request.get_json()

        known_img_data = data.get("known_image")
        unknown_img_data = data.get("unknown_image")

        if not known_img_data or not unknown_img_data:
            return jsonify({
                "status": "error",
                "message": "Images not provided"
            })

        # decode images
        known_img_bytes = base64.b64decode(known_img_data.split(",")[1])
        unknown_img_bytes = base64.b64decode(unknown_img_data.split(",")[1])

        known_path = "static/temp/known.jpg"
        unknown_path = "static/temp/unknown.jpg"

        with open(known_path, "wb") as f:
            f.write(known_img_bytes)

        with open(unknown_path, "wb") as f:
            f.write(unknown_img_bytes)

        known_image = face_recognition.load_image_file(known_path)
        unknown_image = face_recognition.load_image_file(unknown_path)

        known_enc = face_recognition.face_encodings(known_image)
        unknown_enc = face_recognition.face_encodings(unknown_image)

        if len(known_enc) == 0 or len(unknown_enc) == 0:
            return jsonify({
                "status": "fail",
                "message": "Face not detected"
            })

        distance = face_recognition.face_distance([known_enc[0]], unknown_enc[0])[0]
        confidence = round((1 - distance) * 100, 2)

        if confidence >= 60:
            return jsonify({
                "status": "success",
                "confidence": confidence
            })
        else:
            return jsonify({
                "status": "fail",
                "confidence": confidence
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=False) 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)