from packages.order_management.Order import Order
from packages.order_management.SoldOutMonitor import SoldOutMonitor


# info = {
#     'userId': 'ote1111',
#     'mealNum': 2,
#     'resTime': '18:00',
#     'address': 'test',
#     'paymentInfo': 'testPay',
#     'dinnerInfo': {
#         'dinnerId': 'end01',
#         'dinnerName': 'English Dinner',
#         'dinnerStyle': 'Simple',
#         'options': [
#             {
#                 'menuId': 'st01',
#                 'detail': 'extra',
#             }
#         ]
#     }
# }

S =SoldOutMonitor()
print(S.getOrderedNum())