# -*- coding:utf-8 -*-
import string
import time
import random
import requests
from WxPayException import WxPayException
from WxPayConfig import WxPayConfig
from WxPayData import WxPayResults



class WxPayApi(object):
    """
    接口访问类，包含所有微信支付API列表的封装，类中方法为class方法，
    每个接口有默认超时时间（除提交被扫支付为10s，上报超时时间为1s外，其他均为6s）
    @author minkedong
    """

    @classmethod
    def unifiedOrder(cls, inputObj, timeOut=6):
        """
        统一下单，WxPayUnifiedOrder中out_trade_no、body、total_fee、trade_type必填
        appid、mchid、spbill_create_ip、nonce_str不需要填入
        @param WxPayUnifiedOrder inputObj
        @param int timeOut
        @throws WxPayException
        @return 成功时返回，其他抛异常
        """
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        # 检测必填参数
        if not inputObj.IsOut_trade_noSet():
            raise WxPayException(u'缺少统一支付接口必填参数out_trade_no！')
        elif not inputObj.IsBodySet():
            raise WxPayException(u'缺少统一支付接口必填参数body！')
        elif not inputObj.IsTotal_feeSet():
            raise WxPayException(u'缺少统一支付接口必填参数total_fee！')
        elif not inputObj.IsTrade_typeSet():
            raise WxPayException(u'缺少统一支付接口必填参数trade_type！')

        # 关联参数
        if inputObj.GetTrade_type() == 'JSAPI' and (not inputObj.IsOpenidSet()):
            raise WxPayException(u'统一支付接口中，缺少必填参数openid！trade_type为JSAPI时，openid为必填参数！')
        if inputObj.GetTrade_type() == 'NATIVE' and (not inputObj.IsProduct_idSet()):
            raise WxPayException(u'统一支付接口中，缺少必填参数product_id！trade_type为JSAPI时，product_id为必填参数！')

        # 异步通知url未设置，则使用配置文件中的url
        if not inputObj.IsNotify_urlSet():
            inputObj.SetNotify_url(WxPayConfig._NOTIFY_URL)

        inputObj.SetAppid(WxPayConfig._APPID)# 公众账号ID
        inputObj.SetMch_id(WxPayConfig._MCHID)# 商户号
        inputObj.SetSpbill_create_ip('127.0.0.1')# 终端ip    
        inputObj.SetNonce_str(cls.getNonceStr())# 随机字符串
        
        # 签名
        inputObj.SetSign()
        xml = inputObj.ToXml()
        
        # startTimeStamp = cls.getMillisecond()# 请求开始时间
        response = cls.postXmlCurl(xml, url, False, timeOut)
        result = WxPayResults.Init(response)
        # cls.reportCostTime(url, startTimeStamp, result)# 上报请求花费时间
        
        return result


    @classmethod
    def getNonceStr(cls, length=32):
        """
        产生随机字符串，不长于32位
        @param int length
        @return 产生的随机字符串
        """
        pstr = '%s%s' % (string.ascii_letters, string.digits, )
        pwd = []
        for i in xrange(length):
            pwd.append(random.choice(pstr))
        nonce_str = ''.join(pwd)
        return nonce_str


    @classmethod
    def postXmlCurl(cls, xml, url, useCert = False, second = 30):
        """
        以post方式提交xml到对应的接口url
        
        @param string xml  需要post的xml数据
        @param string url  url
        @param bool useCert 是否需要证书，默认不需要
        @param int second   url执行超时时间，默认30s
        @throws WxPayException
        """
        kwargs_post = {
            'url': url,
            'headers':{'content-type': 'text/xml'},
            'data': xml.encode('utf-8'),
            'timeout': second
        }
        try:
            res = requests.post(**kwargs_post)
            if res.status_code == requests.codes.ok:
                return res.content
            else:
                raise WxPayException(u'请求出错，错误码:error')
        except requests.exceptions.Timeout, e:
            raise WxPayException(u'请求超时')
        except Exception, e:
            raise WxPayException(u'请求出错，错误码:error')



    @classmethod
    def notify(cls, xml, callback, msg):
        """
        支付结果通用通知
        @param function callback
        直接回调函数使用方法: notify(you_function)
        回调类成员函数方法:notify(array(this, you_function))
        callback  原型为：function function_name(data){}
        """
        # 获取通知的数据
        # xml = GLOBALS['HTTP_RAW_POST_DATA']

        # 如果返回成功则验证签名
        try:
            result = WxPayResults.Init(xml)
        except Exception, e:
            msg['msg'] = e.message
            return False
        
        return callback(result)


    @classmethod
    def replyNotify(cls, xml):
        """
        直接输出xml
        @param string xml
        """
        return xml


    @classmethod
    def orderQuery(cls, inputObj, timeOut = 6):
        """
        查询订单，WxPayOrderQuery中out_trade_no、transaction_id至少填一个
        appid、mchid、spbill_create_ip、nonce_str不需要填入
        @param WxPayOrderQuery inputObj
        @param int timeOut
        @throws WxPayException
        @return 成功时返回，其他抛异常
        
        """
        url = "https://api.mch.weixin.qq.com/pay/orderquery"
        # 检测必填参数
        if ( not inputObj.IsOut_trade_noSet()) and (not inputObj.IsTransaction_idSet()):
            raise WxPayException(u'订单查询接口中，out_trade_no、transaction_id至少填一个！')

        inputObj.SetAppid(WxPayConfig._APPID) # 公众账号ID
        inputObj.SetMch_id(WxPayConfig._MCHID) # 商户号
        inputObj.SetNonce_str(cls.getNonceStr()) # 随机字符串
        
        inputObj.SetSign() # 签名
        xml = inputObj.ToXml()
        
        # startTimeStamp = cls.getMillisecond() # 请求开始时间
        response = cls.postXmlCurl(xml, url, False, timeOut)
        result = WxPayResults.Init(response)
        # cls.reportCostTime(url, startTimeStamp, result) # 上报请求花费时间
        
        return result


    @classmethod
    def getAppUrl(cls, inputObj):
        """
        生成APP端支付的url
        """
        inputObj.SetAppid(WxPayConfig._APPID) # 应用ID
        inputObj.SetMch_id(WxPayConfig._MCHID) # 商户号
        inputObj.SetData('package', 'Sign=WXPay') 
        inputObj.SetNoncestr(cls.getNonceStr()) # 随机字符串
        inputObj.SetTimestamp(str(int(time.time()))) # 时间戳
        inputObj.SetSign() # 签名
        return inputObj.GetValues()
