# Day 11 - Guardrails, HITL và Responsible AI

Repository này bao gồm:

- phần lab Day 11 đã hoàn thiện trong `src/`
- pipeline Assignment 11 theo hướng production trong `src/production/pipeline.py`
- các artifact phục vụ chấm điểm trong `artifacts/assignment/`
- báo cáo cá nhân cuối cùng trong `reports/Mai_Tan_Thanh_Assignment11_Report.md`

## Nội Dung Đã Triển Khai

### Các TODO của lab

Toàn bộ TODO của Day 11 đã được hoàn thành trong các file:

- `src/attacks/attacks.py`
- `src/guardrails/input_guardrails.py`
- `src/guardrails/output_guardrails.py`
- `src/guardrails/nemo_guardrails.py`
- `src/testing/testing.py`
- `src/hitl/hitl.py`

Những module này bao phủ các nội dung:

- thiết kế adversarial prompts
- AI-generated red teaming
- phát hiện prompt injection bằng regex
- topic filtering
- input/output guardrail plugins
- redaction đầu ra
- LLM-as-Judge
- security testing trước/sau khi có guardrails
- HITL confidence routing

### Pipeline Assignment 11

Lời giải chính cho assignment được cài đặt tại:

- `src/production/pipeline.py`

Pipeline này gồm các lớp:

1. `Rate Limiter`
2. `Input Guardrails`
3. `Session Anomaly Detector` như lớp bảo vệ bonus thứ sáu
4. `Output Guardrails`
5. `LLM-as-Judge`
6. `Audit Log`
7. `Monitoring & Alerts`

## Kết Quả Cuối Cùng

Khi chạy assignment pipeline bằng:

```bash
python src/main.py --part 5
```

thu được các kết quả:

- Safe queries: `5/5` passed
- Attack queries: `7/7` blocked
- Rate limiting: `10` allowed, `5` blocked
- Edge cases: `5/5` blocked
- Bonus anomaly demo: `4/4` blocked
- Audit log: `36` entries

## Cấu Trúc Repository

```text
Day-11-Guardrails-HITL-Responsible-AI-main/
|-- artifacts/
|   `-- assignment/
|       |-- audit_log.json
|       |-- output_redaction_demo.json
|       `-- results_summary.json
|-- notebooks/
|-- reports/
|   `-- Mai_Tan_Thanh_Assignment11_Report.md
|-- src/
|   |-- agents/
|   |-- attacks/
|   |-- core/
|   |-- guardrails/
|   |-- hitl/
|   |-- production/
|   |-- testing/
|   `-- main.py
|-- assignment11_defense_pipeline.md
|-- requirements.txt
|-- requirements-nemo.txt
`-- README.md
```

## Cài Đặt

### Dependency chính

```bash
pip install -r requirements.txt
```

### Hỗ trợ NeMo Guardrails

NeMo là dependency tùy chọn trong repo này. Nếu muốn chạy `Part 2C` tại local:

```bash
pip install -r requirements-nemo.txt
```

Cấu hình NeMo trong `src/guardrails/nemo_guardrails.py` đã được cập nhật để dùng backend:

- `google_genai`

Bạn có thể thử riêng `TODO 9` bằng:

```bash
python src/guardrails/nemo_guardrails.py
```

Trên Windows, việc cài `nemoguardrails` có thể cần:

- Microsoft Visual C++ Build Tools

vì dependency `annoy` phải build native extension.

### API key

Đặt Gemini API key trước khi chạy các phần có model-backed inference:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

Trên Windows PowerShell:

```powershell
$env:GOOGLE_API_KEY="your-api-key-here"
```

Lưu ý: repo này cũng hỗ trợ đọc key từ file `.env` cục bộ cho mục đích chạy local.

## Cách Chạy

Từ thư mục gốc của project:

```bash
cd src
python main.py --part 1    # Attacks
python main.py --part 2    # Guardrails
python main.py --part 3    # Testing pipeline
python main.py --part 4    # HITL design
python main.py --part 5    # Assignment 11 production pipeline
```

Bạn cũng có thể chạy assignment pipeline trực tiếp:

```bash
python src/production/pipeline.py
```

## Các File Output Quan Trọng

Các artifact chính phục vụ chấm điểm gồm:

- `artifacts/assignment/audit_log.json`
- `artifacts/assignment/results_summary.json`
- `artifacts/assignment/output_redaction_demo.json`
- `reports/Mai_Tan_Thanh_Assignment11_Report.md`

## Ghi Chú

- Lệnh mặc định `python src/main.py` giữ hành vi gốc của lab và chạy `Part 1-4`.
- Luồng nộp assignment chính là `python src/main.py --part 5`.
- NeMo là tùy chọn vì assignment cho phép lời giải `Pure Python`.
- `TODO 9` có thể chạy riêng tại local bằng `python src/guardrails/nemo_guardrails.py` sau khi đã cài `requirements-nemo.txt`.

## Tham Khảo

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [AI Safety Fundamentals](https://aisafetyfundamentals.com/)
