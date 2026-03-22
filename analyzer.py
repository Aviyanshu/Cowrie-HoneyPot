import pandas as pd
import json
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class Analyzer:
    def __init__(self, data):
        self.data = data

    def analyze(self):
        print("Inside Analyse()")
    
        df = pd.read_csv(self.data, names=["src_ip", "username", "password"])
        
        # Count the number of source IPs attempts
        df_password_used = df['password'].value_counts().sort_values(ascending=False)
        print("Most used passwords:")
        print(df_password_used.head(10))

        # Source IPs with the most login attempts
        df_src_ip_attempts = df['src_ip'].value_counts().sort_values(ascending=False)
        print("\nSource IPs with the most login attempts:")
        print(df_src_ip_attempts.head(10))

        # Username and password combinations
        df_user_pass = df.groupby(['username', 'password']).size().reset_index(name='count')
        df_user_pass = df_user_pass.sort_values(by='count', ascending=False)
        print("\nMost common username and password combinations:")
        print(df_user_pass.head(10))

analyze = Analyzer("cowrie.csv")
analyze.analyze()