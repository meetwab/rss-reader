"""
Main application entry point and application controller.
"""

import sys
from .ui import UserInterface


class RssApp:
    """RSS 应用主控制器，协调各个组件"""
    
    def __init__(self):
        self.ui = UserInterface()
    
    def run(self):
        """运行应用程序主循环"""
        while True:
            self.ui.show_main_menu()
            choice = self.ui.get_user_input("请选择操作（输入数字）：")
            
            if choice == "1":
                self._handle_add_subscription()
            elif choice == "2":
                self._handle_view_subscriptions()
            elif choice == "0":
                print("感谢使用，再见！")
                sys.exit(0)
            else:
                print("无效的选择，请输入 1、2 或 0。")
    
    def _handle_add_subscription(self):
        """处理添加订阅"""
        url = self.ui.get_user_input("请输入 RSS 订阅链接：")
        self.ui.subscription_manager.add_subscription(url)
    
    def _handle_view_subscriptions(self):
        """处理查看订阅"""
        self.ui.handle_subscriptions_view()


def main():
    """程序入口点"""
    app = RssApp()
    app.run()


if __name__ == "__main__":
    main()
