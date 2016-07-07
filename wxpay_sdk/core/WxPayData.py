# -*- coding:utf-8 -*-
import json
import hashlib
import xmltodict
from WxPayException import WxPayException
from WxPayConfig import WxPayConfig


class WxPayDataBase(object):
    """
    数据对象基础类，该类中定义数据类最基本的行为，包括：
    计算/设置/获取签名、输出xml格式的参数、从xml读取数据对象等
    @author minkedong
    """
    # _values = {}

    def __init__(self):
        self._values = {}


    def SetSign(self):
        """
        设置签名，详见签名生成算法
        @param string value 
        """
        sign = self.MakeSign()
        self._values['sign'] = sign
        return sign


    def GetSign(self):
        """
        获取签名，详见签名生成算法的值
        @return 值
        """
        return self._values.get('sign')


    def IsSignSet(self):
        """
        判断签名，详见签名生成算法是否存在
        @return true 或 false
        """
        return self._values.has_key('sign')


    def ToXml(self):
        """
        输出xml字符
        @throws WxPayException
        """
        if (not isinstance(self._values, dict)) or (self._values == {}):
            raise WxPayException(u'数组数据异常！')

        xml = '<xml>'
        for key, value in self._values.items():
            if isinstance(value, basestring):
                xml = '%s<%s><![CDATA[%s]]></%s>' % (xml, key, value, key, )
            else:
                xml = '%s<%s>%s</%s>' % (xml, key, value, key, )
        xml = '%s</xml>' % xml
        return xml


    def FromXml(self, xml):
        """
        将xml转为array
        @param string xml
        @throws WxPayException
        """
        if not xml:
            raise WxPayException(u'xml数据异常！')
        # 将XML转为dict(此处使用第三方库xmltodict)
        try:
            self._values = json.loads(json.dumps(xmltodict.parse(xml)['xml']))
        except Exception, e:
            self._values = {}
        
        return self._values

    
    def MakeSign(self):
        """
        生成签名
        @return 签名，本函数不覆盖sign成员变量，如要设置签名需要调用SetSign方法赋值
        """
        # 签名步骤一：按字典序排序参数
        params_str = self.ToUrlParams()
        # 签名步骤二：在string后加入KEY
        params_str = '%(params_str)s&key=%(partner_key)s' % {'params_str':params_str, 'partner_key':WxPayConfig._KEY}
        # 签名步骤三：MD5加密
        params_str = hashlib.md5(params_str.encode('utf-8')).hexdigest()
        # 签名步骤四：所有字符转为大写
        return params_str.upper()

    
    def ToUrlParams(self):
        """
        格式化参数格式化成url参数
        """
        ret = []
        for k in sorted(self._values.keys()):
            if (k != 'sign') and (k != '') and (self._values[k] is not None):
                ret.append('%s=%s' % (k, self._values[k]))

        sign_string = '&'.join(ret)
        return sign_string


    def GetValues(self):
        """
        获取设置的值
        """
        return self._values





class WxPayResults(WxPayDataBase):
    """
    接口调用结果类
    @author minkedong
    """

    def CheckSign(self):
        """
        检测签名
        """
        # fix异常
        if not self.IsSignSet():
            raise WxPayException(u'签名错误！')

        sign = self.MakeSign()
        if self.GetSign() == sign:
            return True
        raise WxPayException(u'签名错误！')

    
    def FromArray(self, array):
        """
        使用数组初始化
        @param array array
        """
        self._values = array
    

    @classmethod
    def InitFromArray(cls, array, noCheckSign = False):
        """
        * 使用数组初始化对象
        * @param array array
        * @param 是否检测签名 noCheckSign
        """
        obj = cls()
        obj.FromArray(array)
        if not noCheckSign:
            obj.CheckSign()
        return obj
    

    def SetData(self, key, value):
        """
        设置参数
        @param string key
        @param string value
        """
        self._values[key] = value


    @classmethod
    def Init(cls, xml):
        """
        将xml转为array
        @param string xml
        @throws WxPayException
        """
        obj = cls()
        obj.FromXml(xml)
        if obj._values.get('return_code') != 'SUCCESS': 
            return obj.GetValues()
        # 如果正确返回数据了，还要验证返回数据的正确性（通过返回的sign）
        obj.CheckSign()
        return obj.GetValues()





class WxPayNotifyReply(WxPayDataBase):
    """
    回调基础类
    @author minkedong
    """

    def SetReturn_code(self, return_code):
        """
        设置错误码 FAIL 或者 SUCCESS
        @param string
        """
        self._values['return_code'] = return_code
    

    def GetReturn_code(self):
        """
        获取错误码 FAIL 或者 SUCCESS
        @return string return_code
        """
        return self._values.get('return_code')

    
    def SetReturn_msg(self, return_msg):
        """
        设置错误信息
        @param string return_code
        """
        self._values['return_msg'] = return_msg
    
    
    def GetReturn_msg(self):
        """
        获取错误信息
        @return string
        """
        return self._values.get('return_msg')
    

    def SetData(self, key, value):
        """
        设置返回参数
        @param string key
        @param string value
        """
        self._values[key] = value






class WxPayUnifiedOrder(WxPayDataBase):
    """
    统一下单输入对象
    @author minkedong
    """
    
    def SetAppid(self, value):
        """
        设置微信分配的公众账号ID
        @param string value 
        """
        self._values['appid'] = value


    
    def GetAppid(self):
        """
        获取微信分配的公众账号ID的值
        @return 值
        """
        return self._values.get('appid')
    

    def IsAppidSet(self):
        """
        判断微信分配的公众账号ID是否存在
        @return true 或 false
        """
        return self._values.has_key('appid')


    def SetMch_id(self, value):
        """
        设置微信支付分配的商户号
        @param string value 
        """
        self._values['mch_id'] = value
    

    def GetMch_id(self):
        """
        获取微信支付分配的商户号的值
        @return 值
        """
        return self._values.get('mch_id')
    

    def IsMch_idSet(self):
        """
        判断微信支付分配的商户号是否存在
        @return true 或 false
        """
        return self._values.has_key('mch_id')


    def SetDevice_info(self, value):
        """
        设置微信支付分配的终端设备号，商户自定义
        @param string value 
        """
        self._values['device_info'] = value

    
    def GetDevice_info(self):
        """
        获取微信支付分配的终端设备号，商户自定义的值
        @return 值
        """
        return self._values.get('device_info')

    
    def IsDevice_infoSet(self):
        """
        判断微信支付分配的终端设备号，商户自定义是否存在
        @return true 或 false
        """
        return self._values.has_key('device_info')


    def SetNonce_str(self, value):
        """
        设置随机字符串，不长于32位。推荐随机数生成算法
        @param string value 
        """
        self._values['nonce_str'] = value

    
    def GetNonce_str(self):
        """
        获取随机字符串，不长于32位。推荐随机数生成算法的值
        @return 值
        """
        return self._values.get('nonce_str')

    
    def IsNonce_strSet(self):
        """
        判断随机字符串，不长于32位。推荐随机数生成算法是否存在
        @return true 或 false
        """
        return self._values.has_key('nonce_str')

    
    def SetBody(self, value):
        """
        设置商品或支付单简要描述
        @param string value 
        """
        self._values['body'] = value
    

    def GetBody(self):
        """
        获取商品或支付单简要描述的值
        @return 值
        """
        return self._values.get('body')

    
    def IsBodySet(self):
        """
        判断商品或支付单简要描述是否存在
        @return true 或 false
        """
        return self._values.has_key('body')


    def SetDetail(self, value):
        """
        设置商品名称明细列表
        @param string value 
        """
        self._values['detail'] = value

    
    def GetDetail(self):
        """
        获取商品名称明细列表的值
        @return 值
        """
        return self._values.get('detail')
    

    def IsDetailSet(self):
        """
        判断商品名称明细列表是否存在
        @return true 或 false
        """
        return self._values('detail')


    def SetAttach(self, value):
        """
        设置附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        @param string value 
        """
        self._values['attach'] = value
    

    def GetAttach(self):
        """
        获取附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据的值
        @return 值
        """
        return self._values.get('attach')

    
    def IsAttachSet(self):
        """
        判断附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据是否存在
        @return true 或 false
        """
        return self._values.has_key('attach')


    def SetOut_trade_no(self, value):
        """
        设置商户系统内部的订单号,32个字符内、可包含字母, 其他说明见商户订单号
        @param string value 
        """
        self._values['out_trade_no'] = value
    

    def GetOut_trade_no(self):
        """
        获取商户系统内部的订单号,32个字符内、可包含字母, 其他说明见商户订单号的值
        @return 值
        """
        return self._values.get('out_trade_no')

    
    def IsOut_trade_noSet(self):
        """
        判断商户系统内部的订单号,32个字符内、可包含字母, 其他说明见商户订单号是否存在
        @return true 或 false
        """
        return self._values.has_key('out_trade_no')


    def SetFee_type(self, value):
        """
        设置符合ISO 4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型
        @param string value 
        """
        self._values['fee_type'] = value

    
    def GetFee_type(self):
        """
        获取符合ISO 4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型的值
        @return 值
        """
        return self._values.get('fee_type')
    

    def IsFee_typeSet(self):
        """
        判断符合ISO 4217标准的三位字母代码，默认人民币：CNY，其他值列表详见货币类型是否存在
        @return true 或 false
        """
        return self._values.has_key('fee_type')

    
    def SetTotal_fee(self, value):
        """
        设置订单总金额，只能为整数，详见支付金额
        @param string value 
        """
        self._values['total_fee'] = value
    
    def GetTotal_fee(self):
        """
        获取订单总金额，只能为整数，详见支付金额的值
        @return 值
        """
        return self._values.get('total_fee')

    
    def IsTotal_feeSet(self):
        """
        判断订单总金额，只能为整数，详见支付金额是否存在
        @return true 或 false
        """
        return self._values.has_key('total_fee')


    def SetSpbill_create_ip(self, value):
        """
        设置APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP。
        @param string value 
        """
        self._values['spbill_create_ip'] = value
    

    def GetSpbill_create_ip(self):
        """
        获取APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP。的值
        @return 值
        """
        return self._values.get('spbill_create_ip')
    

    def IsSpbill_create_ipSet(self):
        """
        判断APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP。是否存在
        @return true 或 false
        """
        return self._values.has_key('spbill_create_ip')


    def SetTime_start(self, value):
        """
        设置订单生成时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010。其他详见时间规则
        @param string value 
        """
        self._values['time_start'] = value

    
    def GetTime_start(self):
        """
        获取订单生成时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010。其他详见时间规则的值
        @return 值
        """
        return self._values.get('time_start')

    
    def IsTime_startSet(self):
        """
        判断订单生成时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010。其他详见时间规则是否存在
        @return true 或 false
        """
        return self._values.has_key('time_start')


    def SetTime_expire(self, value):
        """
        设置订单失效时间，格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010。其他详见时间规则
        @param string value 
        """
        self._values['time_expire'] = value
    

    def GetTime_expire(self):
        """
        获取订单失效时间，格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010。其他详见时间规则的值
        @return 值
        """
        return self._values.get('time_expire')
    

    def IsTime_expireSet(self):
        """
        判断订单失效时间，格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010。其他详见时间规则是否存在
        @return true 或 false
        """
        return self._values.has_key('time_expire')


    def SetGoods_tag(self, value):
        """
        设置商品标记，代金券或立减优惠功能的参数，说明详见代金券或立减优惠
        @param string value 
        """
        self._values['goods_tag'] = value
    

    def GetGoods_tag(self):
        """
        获取商品标记，代金券或立减优惠功能的参数，说明详见代金券或立减优惠的值
        @return 值
        """
        return self._values.get('goods_tag')
    

    def IsGoods_tagSet(self):
        """
        判断商品标记，代金券或立减优惠功能的参数，说明详见代金券或立减优惠是否存在
        @return true 或 false
        """
        return self._values.has_key('goods_tag')


    def SetNotify_url(self, value):
        """
        设置接收微信支付异步通知回调地址
        @param string value 
        """
        self._values['notify_url'] = value
    

    def GetNotify_url(self):
        """
        获取接收微信支付异步通知回调地址的值
        @return 值
        """
        return self._values.get('notify_url')

    
    def IsNotify_urlSet(self):
        """
        判断接收微信支付异步通知回调地址是否存在
        @return true 或 false
        """
        return self._values.has_key('notify_url')


    def SetTrade_type(self, value):
        """
        设置取值如下：JSAPI，NATIVE，APP，详细说明见参数规定
        @param string value 
        """
        self._values['trade_type'] = value
    

    def GetTrade_type(self):
        """
        获取取值如下：JSAPI，NATIVE，APP，详细说明见参数规定的值
        @return 值
        """
        return self._values.get('trade_type')
    

    def IsTrade_typeSet(self):
        """
        判断取值如下：JSAPI，NATIVE，APP，详细说明见参数规定是否存在
        @return true 或 false
        """
        return self._values.has_key('trade_type')


    def SetProduct_id(self, value):
        """
        设置trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义。
        @param string value 
        """
        self._values['product_id'] = value

    
    def GetProduct_id(self):
        """
        获取trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义。的值
        @return 值
        """
        return self._values.get('product_id')

    
    def IsProduct_idSet(self):
        """
        判断trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义。是否存在
        @return true 或 false
        """
        return self._values.has_key('product_id')


    def SetOpenid(self, value):
        """
        设置trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识。下单前需要调用【网页授权获取用户信息】接口获取到用户的Openid。 
        @param string value 
        """
        self._values['openid'] = value

    
    def GetOpenid(self):
        """
        获取trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识。下单前需要调用【网页授权获取用户信息】接口获取到用户的Openid。 的值
        @return 值
        """
        return self._values.get('openid')
    
    def IsOpenidSet(self):
        """
        判断trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识。下单前需要调用【网页授权获取用户信息】接口获取到用户的Openid。 是否存在
        @return true 或 false
        """
        return self._values.has_key('openid')





class WxPayOrderQuery(WxPayDataBase):
    """
    订单查询输入对象
    @author minkedong
    """
    def SetAppid(self, value):
        """
        设置微信分配的公众账号ID
        @param string value 
        """
        self._values['appid'] = value


    
    def GetAppid(self):
        """
        获取微信分配的公众账号ID的值
        @return 值
        """
        return self._values.get('appid')


    def IsAppidSet(self):
        """
        判断微信分配的公众账号ID是否存在
        @return true 或 false
        """
        return self._values.has_key('appid')


    def SetMch_id(self, value):
        """
        设置微信支付分配的商户号
        @param string value 
        """
        self._values['mch_id'] = value


    def GetMch_id(self):
        """
        获取微信支付分配的商户号
        @return 值
        """
        return self._values.get('mch_id')


    def IsMch_idSet(self):
        """
        判断微信支付分配的商户号是否存在
        @return true 或 false
        """
        return self._values.has_key('mch_id')


    def SetTransaction_id(self, value):
        """
        设置微信的订单号，优先使用
        @param string value 
        """
        self._values['transaction_id'] = value


    def GetTransaction_id(self):
        """
        获取微信的订单号，优先使用
        @return 值
        """
        return self._values.get('transaction_id')


    def IsTransaction_idSet(self):
        """
        判断微信的订单号是否存在
        @return true 或 false
        """
        return self._values.has_key('transaction_id')


    def SetOut_trade_no(self, value):
        """
        设置商户系统内部的订单号，当没提供transaction_id时需要传这个
        @param string value 
        """
        self._values['out_trade_no'] = value


    def GetOut_trade_no(self):
        """
        获取商户系统内部的订单号，当没提供transaction_id时需要传这个
        @return 值
        """
        return self._values.get('out_trade_no')


    def IsOut_trade_noSet(self):
        """
        判断商户系统内部的订单号是否存在
        @return true 或 false
        """
        return self._values.has_key('out_trade_no')


    def SetNonce_str(self, value):
        """
        设置随机字符串，不长于32位。推荐随机数生成算法
        @param string value 
        """
        self._values['nonce_str'] = value


    def GetNonce_str(self):
        """
        获取随机字符串，不长于32位。推荐随机数生成算法
        @return 值
        """
        return self._values.get('nonce_str')


    def IsNonce_strSet(self):
        """
        判断随机字符串是否存在
        @return true 或 false
        """
        return self._values.has_key('nonce_str')




class WxPayOrderApp(WxPayDataBase):
    """
    APP调起支付输入对象
    @author minkedong
    """
    def SetAppid(self, value):
        """
        设置微信分配的公众账号ID
        @param string value 
        """
        self._values['appid'] = value


    
    def GetAppid(self):
        """
        获取微信分配的公众账号ID的值
        @return 值
        """
        return self._values.get('appid')


    def IsAppidSet(self):
        """
        判断微信分配的公众账号ID是否存在
        @return true 或 false
        """
        return self._values.has_key('appid')


    def SetMch_id(self, value):
        """
        设置微信支付分配的商户号
        @param string value 
        """
        self._values['partnerid'] = value


    def GetMch_id(self):
        """
        获取微信支付分配的商户号
        @return 值
        """
        return self._values.get('partnerid')


    def IsMch_idSet(self):
        """
        判断微信支付分配的商户号是否存在
        @return true 或 false
        """
        return self._values.has_key('partnerid')


    def SetPrepayid(self, value):
        """
        设置预支付交易会话ID
        @param string value
        """
        self._values['prepayid'] = value


    def GetPrepayid(self):
        """
        获取预支付交易会话ID
        @return 值
        """
        return self._values.get('prepayid')


    def IsPrepayidSet(self):
        """
        判断预支付交易会话ID是否存在
        @return true 或 false
        """
        return self._values.has_key('prepayid')


    def SetNoncestr(self, value):
        """
        设置随机字符串，不长于32位。推荐随机数生成算法
        @param string value 
        """
        self._values['noncestr'] = value


    def GetNoncestr(self):
        """
        获取随机字符串，不长于32位。推荐随机数生成算法
        @return 值
        """
        return self._values.get('noncestr')


    def IsNoncestrSet(self):
        """
        判断随机字符串是否存在
        @return true 或 false
        """
        return self._values.has_key('noncestr')


    def SetTimestamp(self, value):
        """
        设置时间戳
        @param string value 
        """
        self._values['timestamp'] = value


    def GetTimestamp(self):
        """
        获取时间戳
        @return 值
        """
        return self._values.get('timestamp')


    def IsTimestampSet(self):
        """
        判断时间戳是否存在
        @return true 或 false
        """
        return self._values.has_key('timestamp')


    def SetData(self, key, value):
        """
        设置一般参数
        @param string key 
        @param string value 
        """
        self._values[key] = value