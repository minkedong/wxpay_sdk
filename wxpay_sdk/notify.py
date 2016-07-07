# -*- coding:utf-8 -*-
from wxpay_sdk.core.WxPayApi import WxPayApi
from wxpay_sdk.core.WxPayNotify import WxPayNotify
from wxpay_sdk.core.WxPayData import WxPayOrderQuery



class PayNotifyCallBack(WxPayNotify):
    """
    支付回调实现类
    @author minkedong
    """

    def Queryorder(self, transaction_id):
        """
        查询订单
        """
        wxpayorderquery = WxPayOrderQuery()
        wxpayorderquery.SetTransaction_id(transaction_id)
        result = WxPayApi.orderQuery(wxpayorderquery)
        print 'query:%s' % result
        if (result.get('return_code') == 'SUCCESS') and (result.get('result_code') == 'SUCCESS'):
            return True

        return False
    
    
    def NotifyProcess(self, data, msg):
        """
        重写回调处理函数
        """
        print 'call back:%s' % data
        notfiyOutput = {}

        if not data.has_key('transaction_id'):
            msg['msg'] = u'输入参数不正确'
            return False

        # 查询订单，判断订单真实性
        if not self.Queryorder(data.get('transaction_id')):
            msg['msg'] = u'订单查询失败'
            return False

        return True
