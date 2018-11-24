db = None

# *DEFAULT CATEGORIES*, keep last
default_categories = [
  {
    "name": "Income",
    "category_rules": {
      "creditAmount": {
        "mode": "STRICT",
        "rules": [
          [
            ">",
            0
          ]
        ]
      },
      "description": {
        "mode": "STRICT",
        "rules": [
          [
            "!~",
            "$NAME"
          ]
        ]
      }
    },
    "className": "cat-income",
    "id": "income"
  },
  {
    "name": "Main Income",
    "category_rules": {
      "creditAmount": {
        "rules": [
          [
            ">",
            0
          ]
        ]
      },
      "description": {
        "rules": [
          [
            "!~",
            "$NAME"
          ]
        ]
      }
    },
    "className": "cat-income",
    "id": "main-income",
    "txn_month_modifier": 1
  },
  {
    "name": "Expenditure",
    "category_rules": {
      "debitAmount": {
        "rules": [
          [
            ">",
            0
          ]
        ]
      },
      "description": {
        "rules": [
          [
            "!~",
            "$NAME"
          ]
        ]
      }
    },
    "className": "cat-exp",
    "id": "exp"
  },
  {
    "name": "Refunds",
    "category_rules": {
      "type": {
        "rules": [
          [
            "=",
            "DEB"
          ]
        ]
      },
      "creditAmount": {
        "rules": [
          [
            ">",
            0
          ]
        ]
      }
    },
    "className": "class-refunds",
    "id": "refunds"
  },
  {
    "name": "Direct Debits",
    "category_rules": {
      "type": {
        "rules": [
          [
            "=",
            "DD"
          ]
        ]
      }
    },
    "className": "cat-dd",
    "id": "direct-debits"
  },
  {
    "name": "Standing Orders",
    "category_rules": {
      "type": {
        "rules": [
          [
            "=",
            "SO"
          ]
        ]
      }
    },
    "className": "cat-so",
    "id": "standing-orders"
  },
  {
    "name": "Cash Withdrawals",
    "category_rules": {
      "type": {
        "rules": [
          [
            "=",
            "CPT"
          ]
        ]
      }
    },
    "className": "cat-cpt",
    "id": "cpt"
  },
  {
    "name": "Personal Bank Transfers",
    "category_rules": {
      "description": {
        "rules": [
          [
            "=~",
            "$NAME"
          ]
        ]
      }
    },
    "className": "cat-tfr-pers",
    "id": "tfr-pers"
  },
  {
    "name": "Source: HSBC",
    "category_rules": {
      "source": {
        "rules": [
          [
            "=",
            "HSBC"
          ]
        ]
      }
    },
    "className": "cat-hsbc",
    "id": "hsbc"
  },
  {
    "name": "Source: FairFX Corp",
    "category_rules": {
      "source": {
        "rules": [
          [
            "=",
            "FairFX Corp"
          ]
        ]
      }
    },
    "className": "cat-ffxcorp",
    "id": "ffxcorp"
  },
  {
    "name": "Source: Midata",
    "category_rules": {
      "source": {
        "rules": [
          [
            "=",
            "Midata"
          ]
        ]
      }
    },
    "className": "cat-midata",
    "id": "midata"
  },
  {
    "name": "Source: RBS",
    "category_rules": {
      "source": {
        "rules": [
          [
            "=",
            "RBS"
          ]
        ]
      }
    },
    "className": "cat-rbs",
    "id": "rbs"
  },
  {
    "name": "Source: LLoyds",
    "category_rules": {
      "debitAmount": {
        "rules": [
          [
            ">",
            0
          ]
        ]
      },
      "source": {
        "rules": [
          [
            "=",
            "Lloyds"
          ]
        ]
      }
    },
    "className": "cat-lloyds",
    "id": "lloyds"
  }
]
