import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'n1x97xnx7ut484t14ybas8236hwqd811'
