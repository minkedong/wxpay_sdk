# -*- coding:utf-8 -*-
import xmltodict
from wxpay_sdk.core.WxPayConfig import WxPayConfig
from wxpay_sdk.core.WxPayData import WxPayUnifiedOrder, WxPayOrderApp
from wxpay_sdk.WxPayNativePay import NativePay
from wxpay_sdk.WxPayAppPay import AppPay
from wxpay_sdk.core.WxPayException import WxPayException
from wxpay_sdk.notify import PayNotifyCallBack


__all__ = ['WxPayBasic']



class WxPayBasic(object):

    def __init__(self, conf=None):
        if conf is None:
            raise WxPayException(u'缺少商家支付配置')
        try:
            WxPayConfig._APPID = conf.get('wechatpay_appid')
            WxPayConfig._MCHID = conf.get('wechatpay_mchid')
            WxPayConfig._KEY = conf.get('wechatpay_key')
            WxPayConfig._APPSECRET = conf.get('wechatpay_appsecret')
        except Exception, e:
            raise WxPayException(u'商家参数配置错误')
        


    def _unifiedorder_get_result(self, out_trade_no, body, total_fee, notify_url, trade_type, product_id, attach='',\
            time_start='', time_expire='', goods_tag=''):
        """
        统一下单基础函数
        """
        wxpayunifiedorder = WxPayUnifiedOrder()
        wxpayunifiedorder.SetOut_trade_no(out_trade_no)
        wxpayunifiedorder.SetBody(body)
        wxpayunifiedorder.SetTotal_fee(total_fee)
        wxpayunifiedorder.SetNotify_url(notify_url)
        wxpayunifiedorder.SetTrade_type(trade_type)
        wxpayunifiedorder.SetProduct_id(product_id)
        if goods_tag:
            wxpayunifiedorder.SetGoods_tag(goods_tag)
        if attach:
            wxpayunifiedorder.SetAttach(attach)
        if time_start:
            wxpayunifiedorder.SetTime_start(time_start)
        if time_expire:
            wxpayunifiedorder.SetTime_expire(time_expire)

        if trade_type == 'NATIVE':
            nativepay = NativePay()
        elif trade_type == 'APP':
            nativepay = AppPay()
        else:
            raise WxPayException(u'暂未实现此支付类型')

        result = nativepay.GetPayUrl(wxpayunifiedorder)

        if result.get('return_code') == 'SUCCESS':
            if result.get('result_code') == 'SUCCESS':
                print result
                return result
            else:
                raise WxPayException(result.get('err_code_des'))
        elif result.get('return_code') == 'FAIL':
            raise WxPayException(result.get('return_msg'))
        else:
            raise WxPayException(u'请求出错，错误码:error')


    def unifiedorder2_get_code_url(self, out_trade_no, body, total_fee, notify_url, trade_type, product_id, attach='',\
            time_start='', time_expire='', goods_tag=''):
        """
        扫码支付 模式二
        
        流程：
        1、调用统一下单，取得code_url，生成二维码
        2、用户扫描二维码，进行支付
        3、支付完成之后，微信服务器会通知支付成功
        4、在支付成功通知中需要查单确认是否真正支付成功（见：notify.py）
        
        """
        result = self._unifiedorder_get_result(out_trade_no, body, total_fee, notify_url, trade_type, product_id, attach,\
            time_start, time_expire, goods_tag)
        return result.get('code_url')


    def unifiedorder_get_app_url(self, out_trade_no, body, total_fee, notify_url, trade_type, product_id, attach='',\
            time_start='', time_expire='', goods_tag=''):
        result = self._unifiedorder_get_result(out_trade_no, body, total_fee, notify_url, trade_type, product_id, attach,\
            time_start, time_expire, goods_tag)

        wxpayorderapp = WxPayOrderApp()
        wxpayorderapp.SetPrepayid(result.get('prepay_id'))

        apppay = AppPay()
        return apppay.GetAppUrl(wxpayorderapp)
        



    def wxpay_callback(self, xml, needSign=False):
        """
        ##### 支付回调:签名验证，订单查询验证 #####
        返回提交给微信的标准xml字符串
        开发者需完成商户自身订单后续流程
        """
        notify = PayNotifyCallBack()
        res_xml = notify.Handle(xml, needSign)

        return res_xml




if __name__ == '__main__':
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
        'wechatpay_appid': 'xxxxxxxxx',  # 必填,微信分配的公众账号ID
        'wechatpay_key': 'xxxxxxxxxxx',  # 必填,appid 密钥
        'wechatpay_mchid': 'xxxxxxxxx',  # 必填,微信支付分配的商户号
        'wechatpay_appsecret': 'xxxxxxxxxxxxx',
    }
    wxpay = WxPayBasic(conf=wechatpay_qrcode_config)
    code_url = wxpay.unifiedorder2_get_code_url(**params)

    # 后续处理把code_url做成二维码供用户扫码支付
    # .........



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
        'wechatpay_appid': 'xxxxxxxxx',  # 必填,微信分配的公众账号ID
        'wechatpay_key': 'xxxxxxxxx',  # 必填,appid 密钥
        'wechatpay_mchid': 'xxxxxxxxx',  # 必填,微信支付分配的商户号
        'wechatpay_appsecret': 'xxxxxxxxx',
    }
    wxpay = WxPayBasic(conf=wechatpay_qrcode_config)
    app_result = wxpay.unifiedorder_get_app_url(**params)

    # 后续处理把app_result传递给app客户端，由客户端sdk使用此参数发起请求即可
    # ..........




    ####################################
    # ３支付回调定义 （注意：扫码支付&&app支付，使用的是不同config）#
    # (以django的views为例)
    ####################################
    # @csrf_exempt
    # def wechat_pay_callback(request, *args, **kwargs):
    #     req_xml_str = request.body

    #     # 回调处理：签名验证，订单查询验证
    #     # 返回验证结果（可作为直接返回给微信的xml）
    #     wechatpay_qrcode_config = {
    #         'wechatpay_appid': 'xxxxxxxxx',  # 必填,微信分配的公众账号ID
    #         'wechatpay_key': 'xxxxxxxxx',  # 必填,appid 密钥
    #         'wechatpay_mchid': 'xxxxxxxxx',  # 必填,微信支付分配的商户号
    #         'wechatpay_appsecret': 'xxxxxxxxx',
    #     }
    #     # wechatpay_qrcode_config = {
    #     #     'wechatpay_appid': 'xxxxxxxxx',  # 必填,微信分配的公众账号ID
    #     #     'wechatpay_key': 'xxxxxxxxx',  # 必填,appid 密钥
    #     #     'wechatpay_mchid': 'xxxxxxxxx',  # 必填,微信支付分配的商户号
    #     #     'wechatpay_appsecret': 'xxxxxxxxx',
    #     # }
    #     wxpay = WxPayBasic(conf=wechatpay_qrcode_config)
    #     res_xml_str = wxpay.wxpay_callback(req_xml_str)

    #     res_xml_dict = xmltodict.parse(res_xml_str)
    #     if res_xml_dict['xml']['return_code'] == 'SUCCESS':
    #         # 处理商户订单逻辑
    #         req_xml_dict = xmltodict.parse(req_xml_str)
    #         total_fee = req_xml_dict['xml']['total_fee']
    #         out_trade_no = req_xml_dict['xml']['out_trade_no']
    #         ............
    #     else:
    #         print 'wxpay callback error'

    #     return HttpResponse(res_xml_str, content_type='text/xml')