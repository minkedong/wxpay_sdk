# -*- coding:utf-8 -*-
import codecs
import os
import sys

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()



NAME = "wxpay_sdk"

# PACKAGES = ['wxpay_sdk']
PACKAGES = find_packages()

REQUIRES = ['requests', 'xmltodict']

DESCRIPTION = "this is a package for weixin pay"


KEYWORDS = "wxpay_sdk weixin wechat wechatpay wechatsdk"

AUTHOR = "minkedong"

AUTHOR_EMAIL = "minkedong89@126.com"

URL = "https://git.oschina.net/minkedong/wxpay_sdk"

VERSION = "0.0.3"

LICENSE = "Free"

LONG_DESCRIPTION = """
wxpay_sdk

微信支付（暂时实现了扫码支付、app支付、回调辅助函数）

由于工作中暂时只用到了这些，按照微信支付官方SDK的PHP版本，实现了python版本，后面如果有时间会继续实现其他类型支付，
有用到微信支付的童鞋，可以方便的使用之！！！


安装：
pip install wxpay_sdk

使用：
####################################
# １．扫码支付　模式二 #
####################################

params = {

    'body': u'Ipad mini  16G  白色', # 商品或支付单简要描述,例如：Ipad mini  16G  白色
    
    'out_trade_no': '9001231230956', # 商户系统内部的订单号,32个字符内、可包含字母
    
    'total_fee': 2, # 订单总金额，单位为分
    
    'product_id': '1116', # 商品ID
    
    'notify_url': 'http://145657w88r.iok.la/weixin/pay_callback/',
    
    'trade_type':'NATIVE',
    
}


wechatpay_qrcode_config = {

    'wechatpay_appid': 'wx26f047e3c34a3983',  # 必填,微信分配的公众账号ID
    
    'wechatpay_key': '0E5F25355D845D48751D9581586BD3B7',  # 必填,appid 密钥
    
    'wechatpay_mchid': '1266915501',  # 必填,微信支付分配的商户号
    
    'wechatpay_appsecret': 'b71c0ab291e895f5f37172f4c7eb8ece',
    
}

wxpay = WxPayBasic(conf=wechatpay_qrcode_config)

code_url = wxpay.unifiedorder2_get_code_url(**params)

后续处理把code_url做成二维码供用户扫码支付
.........



####################################
# ２．app支付 #
####################################

params = {

    'body': u'Ipad mini  16G  白色', # 商品或支付单简要描述,例如：Ipad mini  16G  白色
    
    'out_trade_no': '9401231230956', # 商户系统内部的订单号,32个字符内、可包含字母
    
    'total_fee': 2, # 订单总金额，单位为分
    
    'product_id': '2116', # 商品ID
    
    'notify_url': 'http://145657w88r.iok.la/weixin/pay_callback/',
    
    'trade_type':'APP',
    
}

wechatpay_qrcode_config = {

    'wechatpay_appid': 'wx6db274a7ba941254',  # 必填,微信分配的公众账号ID
    
    'wechatpay_key': '45151BB392D80732D0BFF09EFFFA907D',  # 必填,appid 密钥
    
    'wechatpay_mchid': '1267906201',  # 必填,微信支付分配的商户号
    
    'wechatpay_appsecret': '4706d1cf5865d513d7a4a601d0c36539',
    
}

wxpay = WxPayBasic(conf=wechatpay_qrcode_config)

app_result = wxpay.unifiedorder_get_app_url(**params)

后续处理把app_result传递给app客户端，由客户端sdk使用此参数发起请求即可
..........




####################################
# ３支付回调定义 （注意：扫码支付&&app支付，使用的是不同config）#
# (以django的views为例)
####################################

@csrf_exempt

def wechat_pay_callback(request, *args, **kwargs):

    req_xml_str = request.body

    # 回调处理：签名验证，订单查询验证
    # 返回验证结果（可作为直接返回给微信的xml）
    wechatpay_qrcode_config = {
        'wechatpay_appid': 'wx26f047e3c34a3983',  # 必填,微信分配的公众账号ID
        'wechatpay_key': '0E5F25355D845D48751D9581586BD3B7',  # 必填,appid 密钥
        'wechatpay_mchid': '1266915501',  # 必填,微信支付分配的商户号
        'wechatpay_appsecret': 'b71c0ab291e895f5f37172f4c7eb8ece',
    }
    # wechatpay_qrcode_config = {
    #     'wechatpay_appid': 'wx6db274a7ba941254',  # 必填,微信分配的公众账号ID
    #     'wechatpay_key': '45151BB392D80732D0BFF09EFFFA907D',  # 必填,appid 密钥
    #     'wechatpay_mchid': '1267906201',  # 必填,微信支付分配的商户号
    #     'wechatpay_appsecret': '4706d1cf5865d513d7a4a601d0c36539',
    # }
    wxpay = WxPayBasic(conf=wechatpay_qrcode_config)
    res_xml_str = wxpay.wxpay_callback(req_xml_str)

    res_xml_dict = xmltodict.parse(res_xml_str)
    if res_xml_dict['xml']['return_code'] == 'SUCCESS':
        # 处理商户订单逻辑
        req_xml_dict = xmltodict.parse(req_xml_str)
        total_fee = req_xml_dict['xml']['total_fee']
        out_trade_no = req_xml_dict['xml']['out_trade_no']
        ............
    else:
        print 'wxpay callback error'

    return HttpResponse(res_xml_str, content_type='text/xml')
"""


setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    install_requires = REQUIRES,
    include_package_data=True,
    zip_safe=True,
)