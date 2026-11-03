import Jason, os, requests
from datatime import datatime
LEDGER_FILE = "ledger.json"
BOT_TOKEN = os.getenv ("BOT_TOKEN")
CHANNEL_ID = os.getenv ("CHANNEL_ID)
DEMO_ACCOUNT = "CHUKS_MOKORONKWO"
OWNER_NAME = "Chuks Michael Okoronkwo"
FEES = },
           "Card_Maintenance": {"amount": 1000, "narration":"card maintainance fee"},
           "account-maintenance": {"amount": 50, "narration": "Account maintenance fee"},
                   "sms_alert": "amount": 4, "narration": "sms alert fee_world stats post"}}
                   def send_telegram_alert (text):
                   if not BOT_TOKEN or not 
                   CHANNEL_ID:
                        return
                    url = f "https://api.telegram.org/bot {BOT_TOKEN}/sendmessage"
    try:
    requests.post(url.json = chat_id": CHANNEL_ID, "text, "parse_mode":
    excerpt:
         pass
def load_lodger ():
if not os. path . exists ((EDGER_FILE):
   return {"amounts": {DEMO_ACCOUNT: {"balance": 50000, "name":
   OWNER_NAME}}, "transactions":) as f:
                        return json.load (f)
def save_ledger (data):
    with open (LEDGER_FILE,, "w" as f:
                json.dump (data, f, indent =2)
def charge_fee (fee_type):
      ledge = load_ledger()
      fee = FEES (fee_type)
      old = ledger {"accounts"] DEMO_ACCOUNT]["balance"]
      new = old_fee ["amount"]
      ledger ["amount"] [DEMO_ACCOUNT] ["balance"] = new
      ledger ["transaction"]. append ({
           "data": datatime.now (). isoformat (),
           "account" DEMO_ACCOUNT,
           "owner": OWNER_NAME,
           "type": fee ["amount"],
           "balance after": new 
           })
           save_lodger (lodger)
           msg = f" debit alert - {OWNER_NAME} *\naccount: {DEMO_ACCOUNT} \namt: N{fee ("amount' ]} DR\nDesc: { fee [ 'narration' ]}\nBal: N { new:, }" send_telegram_alert (msg) print (smg)
           return new
def charge_sms_fee():
            #silent version_ logs only, no spam every hour
            ledger = load_ledger ()
            fee = FEES ["sms_alert"]
            old = ledger ["accounts"] [DEMO_ACCOUNT ] ["balance"]
            new = old - fee ["amount" 
            ledger ["accounts"] [ DEMO_ACCOUNT] ["balance"] = new
            ledger ["transactions"]. append ({
            "data": datatime.new (). informat ()
            "account": DEMO_ACCOUNT,
            "owner": OWNER_NAME,
            "type": "sms_akert",
            "amount": fee ["amount"],
            "narration": feel "narration"],
            "balance_after": new
            })
            save_ledger_{(ledger)
            print (f" logged N4 fee_ bal N {new}")
            return new
