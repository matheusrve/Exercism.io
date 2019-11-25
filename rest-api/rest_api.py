import json

class RestAPI:
    def __init__(self, database=None):
      self.database = database

    def get(self, url, payload=None):
      if url == "/users":
        if payload is None:
          return json.dumps(self.database)
        else:
          users = []
          for user in self.database["users"]:
            if user["name"] in json.loads(payload)["users"]:
              users.append(user)
          print(users)
          return json.dumps({"users": sorted(users, key=lambda x: x["name"])}) 

    def post(self, url, payload=None):

      if url == "/add":
        if payload is None:
          raise Exception("No user")
        else:
          user = {"name": json.loads(payload)["user"], "owes": {}, "owed_by": {}, "balance": 0.0}
          self.database["users"].append(user)
          return json.dumps(user)

      if url == "/iou":

        if payload is None:
          raise Exception("No payload")

        else:
          payload = json.loads(payload)
          lender_name = payload["lender"]
          borrower_name = payload["borrower"]
          lender = list(filter(lambda x: x["name"] == lender_name, self.database["users"]))[0]
          borrower = list(filter(lambda x: x["name"] == borrower_name, self.database["users"]))[0]
          self.database["users"].remove(lender)
          self.database["users"].remove(borrower)
          lender_owed_by = payload["amount"] + lender["owed_by"].get(borrower_name, 0) - lender["owes"].get(borrower_name, 0)

          if lender_owed_by > 0:
            lender["owed_by"][borrower_name] = lender_owed_by
            lender["owes"].pop(borrower_name, None)
            borrower["owes"][lender_name] = lender_owed_by
            borrower["owed_by"].pop(lender_name, None)

          elif lender_owed_by < 0:
            lender["owes"][borrower_name] = abs(lender_owed_by)
            lender["owed_by"].pop(borrower_name, None)
            borrower["owed_by"][lender_name] = abs(lender_owed_by)
            borrower["owes"].pop(lender_name, None)

          else:
            lender["owed_by"].pop(borrower_name, None)
            lender["owes"].pop(borrower_name, None)
            borrower["owes"].pop(lender_name, None)
            borrower["owed_by"].pop(lender_name, None)

          borrower["balance"] -= payload["amount"]
          lender["balance"] += payload["amount"]
          users = {"users": sorted([lender, borrower], key=lambda x: x["name"])}
          self.database["users"] += [lender, borrower]

          return json.dumps(users)