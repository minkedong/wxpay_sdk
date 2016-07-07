# -*- coding:utf-8 -*-
from wxpay_sdk.core.WxPayApi import WxPayApi


class AppPay(object):
    """
    app支付实现类
    @author minkedong
    """
    def GetPayUrl(self, paydataobj):
        """
        生成直接支付url，支付url有效期为2小时
        @param UnifiedOrderInput paydataobj
        """
        if paydataobj.GetTrade_type() == 'APP':
            result = WxPayApi.unifiedOrder(paydataobj)
            return result


    def GetAppUrl(self, paydataobj):
        """
        生成APP端支付的url
        """
        result = WxPayApi.getAppUrl(paydataobj)
        return result
