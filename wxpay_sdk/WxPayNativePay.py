# -*- coding:utf-8 -*-
from wxpay_sdk.core.WxPayApi import WxPayApi


class NativePay(object):
    """
    native支付实现类
    @author minkedong
    """
    def GetPayUrl(self, paydataobj):
        """
        生成直接支付url，支付url有效期为2小时,模式二
        @param UnifiedOrderInput paydataobj
        """
        if paydataobj.GetTrade_type() == 'NATIVE':
            result = WxPayApi.unifiedOrder(paydataobj)
            return result
