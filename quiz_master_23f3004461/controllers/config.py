# admin credentials
class AdminCredentials:
    __admin_username = "23f3004461@ds.study.iitm.ac.in"  
    __admin_password = "23f3004461"   

    @classmethod
    def get_username(cls):
        return cls.__admin_username

    @classmethod
    def get_password(cls):
        return cls.__admin_password

