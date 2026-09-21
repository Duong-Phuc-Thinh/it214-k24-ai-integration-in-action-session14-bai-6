import uuid
import time

class PaymentService:
    def __init__(self):
        self.transactions = set()

    def process_payment(self, idempotency_key, amount):
        if idempotency_key in self.transactions:
            print(f"[PAYMENT_SERVICE] Duplicate request detected for key: {idempotency_key}. Ignored.")
            return True
        print(f"[PAYMENT_SERVICE] Trừ tiền thành công {amount}đ. Key: {idempotency_key}")
        self.transactions.add(idempotency_key)
        return True

    def refund_payment(self, amount):
        print(f"[PAYMENT_SERVICE] Giao dịch bù: Đang hoàn tiền {amount}đ... (Refund Success)")
        return True

class CinemaService:
    def __init__(self, fail_seat=False):
        self.fail_seat = fail_seat

    def reserve_seat(self, seat_id):
        if self.fail_seat:
            print(f"[CINEMA_SERVICE] LỖI: Ghế {seat_id} đã có người đặt!")
            return False
        print(f"[CINEMA_SERVICE] Đặt ghế {seat_id} thành công! Khóa ngữ nghĩa từ AVAILABLE sang RESERVED.")
        return True

class OrderOrchestrator:
    def __init__(self, payment_service, cinema_service):
        self.payment_service = payment_service
        self.cinema_service = cinema_service
        self.state = "PENDING"

    def execute_saga(self, payload):
        order_id = payload["orderId"]
        amount = payload["amount"]
        seat_id = payload["seatId"]
        idempotency_key = payload["idempotencyKey"]

        print(f"--- BẮT ĐẦU SAGA CHO ĐƠN HÀNG: {order_id} ---")
        
        # 1. PENDING -> PAYING
        self.state = "PAYING"
        print(f"[ORCHESTRATOR] State Change: PENDING -> PAYING")
        payment_success = self.payment_service.process_payment(idempotency_key, amount)
        
        if not payment_success:
            self.state = "CANCELLED"
            print(f"[ORCHESTRATOR] Thanh toán thất bại. State Change -> CANCELLED")
            return self.state

        # 2. PAYING -> PAID
        self.state = "PAID"
        print(f"[ORCHESTRATOR] State Change: PAYING -> PAID")

        # 3. PAID -> RESERVING
        self.state = "RESERVING"
        print(f"[ORCHESTRATOR] State Change: PAID -> RESERVING")
        seat_success = self.cinema_service.reserve_seat(seat_id)

        if seat_success:
            self.state = "SUCCESS"
            print(f"[ORCHESTRATOR] State Change: RESERVING -> SUCCESS")
            print(f"[SYSTEM] Trạng thái cuối: ORDER_SUCCESS. Giao dịch hoàn tất.")
        else:
            self.state = "CANCELLED"
            print(f"[ORCHESTRATOR] Phát hiện lỗi ghế. Transition to CANCELLED.")
            self.payment_service.refund_payment(amount)
            print(f"[SYSTEM] Trạng thái cuối: ORDER_CANCELLED. Dữ liệu nhất quán.")

        return self.state

if __name__ == " == "__main__":
    payload = {
        "orderId": "RIKA_DEAL_001",
        "amount": 150000,
        "seatId": "A12",
        "idempotencyKey": "uuid-999-order"
    }

    print("=== KỊCH BẢN 1: HAPPY PATH ===")
    ps = PaymentService()
    cs = CinemaService(fail_seat=False)
    orch = OrderOrchestrator(ps, cs)
    orch.execute_saga(payload)

    print("\n=== KỊCH BẢN 2: FALLBACK FLOW (HẾT GHẾ) ===")
    ps2 = PaymentService()
    cs2 = CinemaService(fail_seat=True)
    orch2 = OrderOrchestrator(ps2, cs2)
    orch2.execute_saga(payload)
