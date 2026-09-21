# Orchestrator Saga - Rika Cinema Deal System

## Giới thiệu
Bài tập này minh họa việc triển khai mô hình **Orchestration-based Saga Pattern** kết hợp với **Spring State Machine** giả lập bằng Python để điều phối giao dịch giữa các microservice: `order-service`, `payment-service`, và `cinema-service`.

## Các chức năng đã làm
1. **Quản lý trạng thái tập trung (Orchestrator)**: Theo dõi luồng từ `PENDING` đến `SUCCESS` hoặc `CANCELLED` mà không vi phạm lỗi God Service.
2. **Bộ giáp dữ liệu (Data Armor)**:
   - **Giao dịch bù (Compensating Transaction)**: Tự động hoàn tiền (`refundPayment`) khi gặp lỗi đặt ghế.
   - **Khóa ngữ nghĩa (Semantic Lock)**: Đảm bảo trạng thái ghế được giữ tạm thời thay vì trừ thẳng.
   - **Tính lũy đẳng (Idempotency)**: Chặn đứng request trùng lặp dựa trên `idempotencyKey`.

## Hướng dẫn chạy chương trình
Cài đặt Python và chạy file `main.py`:
```bash
python main.py
```