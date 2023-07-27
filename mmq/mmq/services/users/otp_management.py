import random
import pyotp
import base64
from datetime import datetime
import time

class OtpManagement():

    def generateotp(self,email,counter):
        output_dict = {}
        # print(counter)
        # st = str(datetime.date(datetime.now())) + str(email)
        # key = base64.b32encode(st.encode())
        dt = datetime.now()
        # otp = pyotp.HOTP(key)
        # code = otp.at(counter)

        otp = pyotp.HOTP('base32secret3232')
        code = otp.at(counter)

        output_dict["code"] = code
        output_dict["otp_generated_time"] = dt
        print(output_dict)
        return output_dict


    def verifyotp(self,copyotpde,email,counter):
        print(type(counter))

        print(copyotpde)
        print(email)
        print(counter)
        print(self)

        # st = str(datetime.date(datetime.now())) + str(email)
        # key = base64.b32encode(st.encode())
        # otp = pyotp.HOTP(key)
        otp = pyotp.HOTP('base32secret3232')
        return otp.verify(copyotpde,counter)


    """  Time Base OTP """

    def generateTimeBasedOtp(self,email,counter):
        output_dict = {}
        dt = datetime.now()
        print("time",time.time())
        otp = pyotp.TOTP('base32secret3232',interval=60)
        otp.at(dt,60)
        
        otp.now()

        output_dict["code"] = otp.now()
        output_dict["generated_timestamp"] = dt
        # print(output_dict)
        return output_dict


    def verifyTimeBasedOtp(self,copyotpde,email,counter):
        # print(type(counter))
        # print(copyotpde)
        # print(email)
        # print(counter)
        # print(self)
        totp = pyotp.TOTP('base32secret3232')
        dt = datetime.now()
        # totp.now() # => '492039'

        print(totp.verify(copyotpde,dt,valid_window=1)) # => True
        time.sleep(61)
        return totp.verify(copyotpde,dt,valid_window=1) # => False

        
