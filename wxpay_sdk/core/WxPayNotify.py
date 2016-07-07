# -*- coding:utf-8 -*-
from WxPayData import WxPayNotifyReply
from WxPayApi import WxPayApi



class WxPayNotify(WxPayNotifyReply):
    """
    回调基础类
    @author minkedong
    """
    def Handle(self, xml, needSign = True):
        """
        回调入口
        @param bool needSign  是否需要签名输出
        """
        msg = {'msg':"OK"}
        # 当返回false的时候，表示notify中调用NotifyCallBack回调失败获取签名校验失败，此时直接回复失败
        result = WxPayApi.notify(xml, self.NotifyCallBack, msg)
        if not result:
            self.SetReturn_code("FAIL")
            self.SetReturn_msg(msg['msg'])
            return self._ReplyNotify(False)
        else:
            # 该分支在成功回调到NotifyCallBack方法，处理完成之后流程
            self.SetReturn_code("SUCCESS")
            self.SetReturn_msg("OK")

        return self._ReplyNotify(needSign)



    def NotifyProcess(self, data, msg):
        """
        回调方法入口，子类可重写该方法
        注意：
        1、微信回调超时时间为2s，建议用户使用异步处理流程，确认成功之后立刻回复微信服务器
        2、微信服务器在调用失败或者接到回包为非确认包的时候，会发起重试，需确保你的回调是可以重入
        @param array data 回调解释出的参数
        @param string msg 如果回调处理失败，可以将错误信息输出到该方法
        @return true回调出来完成不需要继续回调，false回调处理未完成需要继续回调
        """
        # TODO 用户基础该类之后需要重写该方法，成功的时候返回true，失败返回false
        return True
    
    
    def NotifyCallBack(self, data):
        """
        notify回调方法，该方法中需要赋值需要输出的参数,不可重写
        @param array data
        @return true回调出来完成不需要继续回调，false回调处理未完成需要继续回调
        """
        msg = {'msg':"OK"}
        result = self.NotifyProcess(data, msg)
        
        if result:
            self.SetReturn_code("SUCCESS")
            self.SetReturn_msg("OK")
        else:
            self.SetReturn_code("FAIL")
            self.SetReturn_msg(msg['msg'])

        return result
    
    
    def _ReplyNotify(self, needSign = True):
        """
        回复通知
        @param bool needSign 是否需要签名输出
        """
        # 如果需要签名
        if needSign and (self.GetReturn_code() == "SUCCESS"):
            self.SetSign()
        return WxPayApi.replyNotify(self.ToXml())