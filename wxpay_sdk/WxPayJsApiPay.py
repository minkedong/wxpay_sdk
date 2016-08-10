# -*- coding:utf-8 -*-
import time
import json
from wxpay_sdk.core.WxPayException import WxPayException
from wxpay_sdk.core.WxPayData import WxPayJsApiPay
from wxpay_sdk.core.WxPayApi import WxPayApi


class JsApiPay(object):
    """
    /**
     * 
     * JSAPI支付实现类
     * 该类实现了从微信公众平台获取code、通过code获取openid和access_token、
     * 生成jsapi支付js接口所需的参数、生成获取共享收货地址所需的参数
     * 
     * 该类是微信支付提供的样例程序，商户可根据自己的需求修改，或者使用lib中的api自行开发
     * 
     * @author minkedong
     *
     */
    """

    def GetPayUrl(self, paydataobj):
        """
        生成直接支付url，支付url有效期为2小时
        @param UnifiedOrderInput paydataobj
        """
        if paydataobj.GetTrade_type() == 'JSAPI':
            result = WxPayApi.unifiedOrder(paydataobj)
            return result

    def GetJsApiParameters(self, unifiedorderresult):
        """
        /**
         * 
         * 获取jsapi支付的参数
         * @param array unifiedorderresult 统一支付接口返回的数据
         * @throws WxPayException
         * 
         * @return json数据，可直接填入js函数作为参数
         */
        """
        if not (unifiedorderresult.has_key('appid') and unifiedorderresult.has_key('prepay_id') and unifiedorderresult.get('prepay_id')):
            raise WxPayException(u'参数错误')
        jsapi = WxPayJsApiPay()
        jsapi.SetAppid(unifiedorderresult.get('appid'))
        jsapi.SetTimeStamp(str(int(time.time())))
        jsapi.SetNonceStr(WxPayApi.getNonceStr())
        jsapi.SetPackage("prepay_id=%s" % unifiedorderresult.get('prepay_id'))
        jsapi.SetSignType("MD5")
        jsapi.SetPaySign(jsapi.MakeSign())
        return jsapi.GetValues()
