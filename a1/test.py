def list_output(channels):
    for chan_name, ch in channels.items():
        port = ch['port']
        current = len(ch['clients'])
        limit = ch['capacity']
        queue_len = len(ch['queue'])
        print(f"[Channel] {chan_name} {port} Capactiy: {current}/{limit} {queue_len}")

channels= {
  "general": {
    "port": 12345,
    "capacity": 5,
    "clients": {
      "alice": None
      ,
      "bob": None
    },
    "queue": []
  },
  "gaming": {
    "port": 12346,
    "capacity": 3,
    "clients": {
      "carol": None,
      "dave": None,
      "emma": None
    },
    "queue": [
      [
        "eve",
        None
      ]
    ]
  },
  "dev_team": {
    "port": 12347,
    "capacity": 8,
    "clients": {
      "frank": None
    },
    "queue": []
  }
}
def main():
    list_output(channels)

if __name__ == "__main__":
    main()