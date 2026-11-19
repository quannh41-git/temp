---
category: "alpha_test_catalog"
updated: "2026-11-18"
language: "vi"
source: "knowledge.md and linked research records"
---

# Danh sách alpha và cấu hình nên thử trên WorldQuant BRAIN

## 1. Phạm vi và cách dùng

Danh sách cụ thể hóa các công thức, họ tín hiệu và thí nghiệm trong [bản tổng hợp kiến thức](knowledge.md). Bao gồm mẫu lịch sử, giả thuyết mới và đối chứng cần thiết; không phải xuất toàn bộ 1.669 hồ sơ field thành 1.669 alpha độc lập. Các vùng thất bại đã biết không được đưa vào hàng đợi ưu tiên chỉ để tăng số lượng.

**Chưa có biểu thức nào trong tài liệu này được chạy lại hoặc submit trong phiên làm việc này.** “Lịch sử” là bằng chứng trong kho, không phải bảo đảm đạt kiểm tra hiện tại. “Đề xuất” và “đối chứng” chưa được xác nhận có alpha. Phải kiểm tra quyền truy cập field/operator, kiểu dữ liệu, đơn vị và kết quả chính thức trên tài khoản của bạn.

Mỗi mục có một expression đầy đủ và một mã config. Dùng toàn bộ settings của mã đó; không tự thay field/cửa sổ mà giữ nguyên kết luận lịch sử. Chạy riêng từng biểu thức, không nối các khối thành một chương trình.

## 2. Cấu hình dùng chung

Các JSON dưới đây là **settings cho lần mô phỏng đề xuất**, không phải payload API hoàn chỉnh; nếu dùng API còn cần bọc đúng simulation type và expression theo API hiện tại. Các nguồn thường chỉ ghi universe, neutralization và decay, không đủ để tái lập chính xác mọi settings lịch sử. Delay, truncation và các tùy chọn còn lại ở đây là lựa chọn nghiên cứu minh bạch, không khẳng định nguồn cũ dùng đúng tất cả giá trị này.

### F6: baseline fundamental, sự kiện, interaction

```json
{
  "instrumentType": "EQUITY",
  "region": "USA",
  "universe": "TOP3000",
  "delay": 1,
  "decay": 6,
  "neutralization": "SUBINDUSTRY",
  "truncation": 0.08,
  "pasteurization": "ON",
  "unitHandling": "VERIFY",
  "nanHandling": "OFF",
  "language": "FASTEXPR",
  "visualization": false
}
```

### I10: IV spread, market neutralization

```json
{
  "instrumentType": "EQUITY",
  "region": "USA",
  "universe": "TOP3000",
  "delay": 1,
  "decay": 10,
  "neutralization": "MARKET",
  "truncation": 0.08,
  "pasteurization": "ON",
  "unitHandling": "VERIFY",
  "nanHandling": "OFF",
  "language": "FASTEXPR",
  "visualization": false
}
```

### M6: không leverage, kiểm tra MARKET

```json
{
  "instrumentType": "EQUITY",
  "region": "USA",
  "universe": "TOP3000",
  "delay": 1,
  "decay": 6,
  "neutralization": "MARKET",
  "truncation": 0.08,
  "pasteurization": "ON",
  "unitHandling": "VERIFY",
  "nanHandling": "OFF",
  "language": "FASTEXPR",
  "visualization": false
}
```

**Quy tắc chung:**

- `decay` trong config khác cửa sổ `ts_decay_linear` trong expression; giữ nguyên cả hai khi so sánh đối chứng.
- Chọn cùng khoảng dữ liệu nghiên cứu cho các phép so sánh. Lưu ngày bắt đầu/kết thúc thực tế BRAIN trả về; không để các lần chạy có mẫu khác nhau mà coi là cùng điều kiện.
- Dành giai đoạn theo thời gian chưa dùng để chọn công thức cho xác nhận nếu nền tảng cho phép. Nếu không có holdout sạch, ghi rõ và theo dõi forward; re-run cùng mẫu không phải ngoài mẫu.
- `nanHandling=OFF` để không mặc nhiên biến thiếu dữ liệu thành 0. Không thay bằng ON nhằm làm đẹp chỉ số mà không kiểm tra semantics.
- Nếu `unitHandling=VERIFY` báo lỗi, xem lại field/đơn vị và operator; không tắt kiểm tra để che lỗi.
- Không thêm backfill, winsorize hoặc đổi universe hàng loạt trước khi có chẩn đoán. Các settings có thể phụ thuộc quyền tài khoản và phiên bản nền tảng.

## 3. Mẫu lịch sử và baseline để tái lập

### R01. Leverage đơn lẻ

Config: `F6`. Loại: baseline lịch sử. Ưu tiên: đối chứng cho họ leverage.

```text
rank(-1 * equity / assets)
```

Nguồn: [leverage premium](patterns/leverage-premium.md). Kiểm tra tài sản bằng 0, equity âm và concentration. Không chuyển sang MARKET để so Sharpe mà không ghi đây là một thí nghiệm khác.

### R02. Leverage + deferred-revenue leg

Config: `F6`. Loại: mẫu lịch sử. Ưu tiên: cao nếu book chưa chứa họ leverage.

```text
rank(-1 * equity / assets) + rank(fnd6_drlt / close)
```

Nguồn: [leverage premium](patterns/leverage-premium.md). Từng có biến thể qua checks; hiện phải kiểm tra lại sub-universe và self-corr. Không diễn giải mọi `F / close` là value yield nếu F là tổng tiền.

### R03. ITCI level chuẩn hóa giá

Config: `F6`. Loại: baseline lịch sử. Ưu tiên: đối chứng cho event-magnitude.

```text
rank(fnd6_itci / close)
```

Nguồn: [hồ sơ itci](factor_profiles/fnd6_itci.md). Field được mô tả là Investment Tax Credit (Income Account), không phải tồn kho. Hồ sơ có cảnh báo LOW_SUB_UNIVERSE_SHARPE; dùng để đo mức cải thiện của các biến đổi sau, không mặc định là ứng viên submit.

### R04. Event ITCI 3 ngày + leverage + drlt

Config: `F6`. Loại: mẫu lịch sử. Ưu tiên: cao để tái lập, thấp nếu book đã bão hòa họ này.

```text
rank(abs(ts_delta(fnd6_itci / close, 3))) + rank(-1 * equity / assets) + rank(fnd6_drlt / close)
```

Nguồn: [event-magnitude](patterns/event-magnitude-abs-ts-delta.md); đại diện lịch sử `0m8GV1Pp`, S=2.64, F=2.77. Không gán số liệu này cho lần chạy mới trước khi có kết quả.

### R05. Analyst netprofit tích lũy 22 ngày

Config: `F6`. Loại: cấu trúc lịch sử. Ưu tiên: chỉ chạy sau khi hiểu mã flag.

```text
ts_decay_linear(zscore(ts_sum(anl4_netprofit_flag, 22)), 3)
```

Nguồn: [accumulated revision](patterns/zscore-accumulated-revision.md). Flag có thể là forecast type, không phải mức nâng/hạ dự báo. Đừng diễn giải tổng các mã như số lần analyst tăng dự báo nếu chưa xác minh mã hóa và tần suất lặp trạng thái.

### R06. IV call-put 270 ngày, smoothed zscore

Config: `I10`. Loại: mẫu lịch sử. Ưu tiên: cao nếu quyền dữ liệu cho phép và book chưa có họ IV.

```text
ts_decay_linear(zscore(ts_mean(implied_volatility_call_270 - implied_volatility_put_270, 22)), 10)
```

Nguồn: [IV smoothing](patterns/iv-spread-zscore-tsmean.md); đại diện lịch sử `vRm07LP3`, S=1.82, F=2.35. Phải kiểm tra coverage options và self-corr mới, không suy ra tenor khác là độc lập.

### R07. Buzz-reversal đơn lẻ

Config: `F6`. Loại: baseline của thành phần lịch sử. Ưu tiên: đối chứng trước khi thêm buzz vào blend.

```text
rank(ts_mean(scl12_buzz, 5) * (-1 * returns))
```

Nguồn: [blend template](patterns/blend-template.md). Là attention kết hợp đảo chiều giá, không phải attention level thuần túy. Xem turnover và chi phí.

### R08. Hai anchor, bỏ leverage, nhân đôi ivaco và buzz

Config: `F6`. Loại: mẫu lịch sử. Ưu tiên: cao để nghiên cứu đóng góp từng thành phần.

```text
ts_decay_linear(rank(fnd6_cld2 / close) + rank(fnd6_fopo / close) + 2 * rank(fnd6_ivaco / close) + 2 * rank(ts_mean(scl12_buzz, 10) * (-1 * returns)), 5)
```

Nguồn: [leverage-free fresh anchor](patterns/leverage-free-fresh-anchor-decorrelation.md); đại diện lịch sử `aknmG1M6`, S=2.29, F=2.26, self-corr chính thức 0.6181. Đây đã là mẫu có trong kho, không phải khám phá mới của tài liệu này.

### R09. Event ITCI 5 ngày + leverage + drlt

Config: `F6`. Loại: biến thể lịch sử. Ưu tiên: sau R04, chỉ để xem độ nhạy cửa sổ.

```text
rank(abs(ts_delta(fnd6_itci / close, 5))) + rank(-1 * equity / assets) + rank(fnd6_drlt / close)
```

Nguồn: [event-magnitude](patterns/event-magnitude-abs-ts-delta.md). Không coi R04 và R09 là hai nguồn alpha độc lập để submit cùng lúc.

### R10. Event ITCI 5 ngày + leverage + ivaco

Config: `F6`. Loại: biến thể lịch sử. Ưu tiên: so sánh vai trò stabilizer với R09.

```text
rank(abs(ts_delta(fnd6_itci / close, 5))) + rank(-1 * equity / assets) + rank(fnd6_ivaco / close)
```

Nguồn: [event-magnitude](patterns/event-magnitude-abs-ts-delta.md). Đổi stabilizer chưa bảo đảm giảm tương quan hoặc qua sub-universe.

### R11. Analyst netprofit tích lũy, smoothing 5 ngày

Config: `F6`. Loại: biến thể cửa sổ của template lịch sử. Ưu tiên: sau R05.

```text
ts_decay_linear(zscore(ts_sum(anl4_netprofit_flag, 22)), 5)
```

Nguồn: [accumulated revision](patterns/zscore-accumulated-revision.md). Giữ platform decay 6; chỉ đổi cửa sổ smoothing từ 3 sang 5. Không gán S/F của R05 cho biến thể này.

### R12. Product ivaco x intraday x bvps flag

Config: `F6`. Loại: expression lịch sử đã đối chiếu trực tiếp. Ưu tiên: sau khi hiểu semantics của flag.

```text
ts_decay_linear(rank(fnd6_ivaco / close) * rank(open / close - 1) * rank(anl4_bvps_flag), 5)
```

Nguồn: [candidate JjpzQAze](opportunities/submit-jjpzqaze.md); S=2.30, F=2.05, self-corr=0.6813 trong ghi chép. Đây là biến thể `bvps_flag`; không nhầm với N13 dùng `ptpr_flag`.

### R13. Additive acdo + intraday + ptpr + itci

Config: `F6`. Loại: tổ hợp lịch sử trong template additive. Ưu tiên: cao nếu book chưa chứa họ intraday-fundamental.

```text
ts_decay_linear(rank(fnd6_acdo / close) + rank(open / close - 1) + rank(anl4_ptpr_flag) + rank(fnd6_itci / close), 5)
```

Nguồn: [fundamental-intraday blend](patterns/overnight-gap-fundamental-blend.md). Tên pattern gốc có chữ overnight, nhưng thành phần ở đây là `open / close - 1` trong cùng ngày dữ liệu.

### R14. Additive acdo + intraday + netdebt + itci

Config: `F6`. Loại: biến thể lịch sử của R13. Ưu tiên: chỉ chạy như đối chứng flag, không kỳ vọng độc lập với R13.

```text
ts_decay_linear(rank(fnd6_acdo / close) + rank(open / close - 1) + rank(anl4_netdebt_flag) + rank(fnd6_itci / close), 5)
```

Nguồn: [fundamental-intraday blend](patterns/overnight-gap-fundamental-blend.md). Chọn đại diện sau khi so sánh độ bền; không chỉ chọn Sharpe cao nhất ở một mẫu.

### R15. IV/event/breadth có volatility gate

Config: `F6`. Loại: expression lịch sử đã đối chiếu trực tiếp. Ưu tiên: có điều kiện; dùng khi muốn nghiên cứu LOW_SUB_UNIVERSE_SHARPE và stateful gating.

```text
trade_when(ts_std_dev(returns, 20) > 0.02, ts_decay_linear(rank(ts_mean(implied_volatility_call_270 - implied_volatility_put_270, 10)) + rank(fnd6_itci / close) + rank(fnd6_acdo) + rank(anl4_netdebt_flag) + rank(ts_mean(scl12_buzz, 5)) + rank(open / close - 1), 5), ts_std_dev(returns, 20) < 0.01)
```

Nguồn: [candidate 0m7lnAEr](opportunities/submit-0m7lnaer.md); S=2.08, F=2.01, self-corr=0.5480 trong ghi chép. Expression cố ý giữ `rank(fnd6_acdo)`, không tự đổi thành `/ close`. Cần so với D02; kiểm tra tuổi vị thế, NaN, ưu tiên entry/exit. Không tự chuyển config sang I10 chỉ vì công thức có IV.

### R16. Liability fair-value event + FFO + intraday + sales count

Config: `F6`. Loại: expression lịch sử đã đối chiếu trực tiếp. Ưu tiên: có điều kiện; nghiên cứu densifier khi đã đo đủ main effects.

```text
ts_decay_linear(rank(abs(ts_delta(fn_liab_fair_val_a / close, 3))) + rank(-1 * equity / assets) + rank(anl4_ffo_flag) + rank(fnd6_ivaco / close) + rank(fnd6_drlt / close) + rank(open / close - 1) + rank(sales_estimate_count_quarterly), 5)
```

Nguồn: [candidate N1rY5ZJg](opportunities/submit-n1ry5zjg.md); S=2.23, F=2.20, self-corr=0.6638 trong ghi chép. Anchor là `fn_liab_fair_val_a`, không phải một field FFO. `anl4_ffo_flag` là thành phần riêng. So với D03, D04 và D06 trước khi quy hiệu quả cho sales count.

### R17. MSA event không leverage, MARKET neutralization

Config: `M6`. Loại: expression lịch sử. Ưu tiên: có điều kiện nếu muốn thử escape khỏi shared leverage.

```text
ts_decay_linear(rank(abs(ts_delta(fnd6_newqv1300_msaq / close, 3))) + rank(fnd6_ivaco / close) + rank(fnd6_drlt / close) + rank(anl4_ffo_flag) + rank(ts_mean(scl12_buzz, 10) * (-1 * returns)), 5)
```

Nguồn: [market-neutral escape](patterns/market-neutral-event-magnitude-escape.md); đại diện `O0Z6NE0b`, S=2.10, F=2.02. Giá trị corr 0.528 được nguồn ghi là local lúc khám phá, không được đổi tên thành số đo check chính thức. Nguồn sau đó ghi alpha ACTIVE. Vẫn cần xác minh ý nghĩa anchor và check lại cho book hiện tại.

### R18. Preferred-stock event không leverage

Config: `F6`. Loại: expression lịch sử đã đối chiếu trực tiếp. Ưu tiên: sau kiểm tra tương quan bộ stabilizer.

```text
ts_decay_linear(rank(abs(ts_delta(fnd6_pstkrv / close, 3))) + rank(fnd6_ivaco / close) + rank(fnd6_drlt / close) + rank(anl4_fcf_flag) + rank(ts_mean(scl12_buzz, 10) * (-1 * returns)), 5)
```

Nguồn: [candidate N1rlJ7mq](opportunities/submit-n1rlj7mq.md); S=2.32, F=2.07, self-corr=0.6903 trong ghi chép. Biên tương quan lịch sử rất mỏng; bỏ leverage không bảo đảm mọi anchor đều qua.

### R19. Tax event TXW + leverage + ivaco + drlt + buzz

Config: `F6`. Loại: tổ hợp lịch sử. Ưu tiên: thấp với book đã có họ này; dùng để hiểu vì sao level yếu vẫn có thể hữu ích trong blend.

```text
ts_decay_linear(rank(abs(ts_delta(fnd6_txw / close, 3))) + rank(-1 * equity / assets) + rank(fnd6_ivaco / close) + rank(fnd6_drlt / close) + rank(ts_mean(scl12_buzz, 5) * (-1 * returns)), 5)
```

Nguồn: [event-magnitude buzz boost](patterns/event-magnitude-buzz-boost.md); S=2.63, F=2.68 cho đại diện lịch sử `WjGVJ7bN`. Không mặc định self-corr hiện tại còn PASS, nhất là khi full stack có leverage đã bị các ghi chép sau đánh dấu bão hòa.

### R20. Tax-loss event TLCF + cùng bộ stabilizer

Config: `F6`. Loại: tổ hợp lịch sử. Ưu tiên: đối chứng theo field cho R19, không phải family độc lập.

```text
ts_decay_linear(rank(abs(ts_delta(fnd6_tlcf / close, 3))) + rank(-1 * equity / assets) + rank(fnd6_ivaco / close) + rank(fnd6_drlt / close) + rank(ts_mean(scl12_buzz, 5) * (-1 * returns)), 5)
```

Nguồn: [event-magnitude buzz boost](patterns/event-magnitude-buzz-boost.md). Đánh giá ablation trước khi kết luận phần cải thiện đến từ anchor thay vì stabilizer chung.

### R21. Analyst EPSR tích lũy

Config: `F6`. Loại: biến thể template lịch sử với smoothing đề xuất 3 ngày. Ưu tiên: thấp; đối chứng sau R05 và xác minh flag.

```text
ts_decay_linear(zscore(ts_sum(anl4_epsr_flag, 22)), 3)
```

Nguồn: [accumulated revision](patterns/zscore-accumulated-revision.md). Các biến thể EPSR trong nguồn yếu hơn netprofit; không có lý do ưu tiên chỉ vì tên field gợi ý earnings revision.

### R22. Analyst CAPEX tích lũy

Config: `F6`. Loại: biến thể template lịch sử với smoothing đề xuất 3 ngày. Ưu tiên: thấp; chỉ khi có giả thuyết riêng về CAPEX.

```text
ts_decay_linear(zscore(ts_sum(anl4_capex_flag, 22)), 3)
```

Nguồn: [accumulated revision](patterns/zscore-accumulated-revision.md). Không gán hiệu quả netprofit cho CAPEX; kiểm tra semantics của mã flag riêng.

### R23. Analyst FCF tích lũy

Config: `F6`. Loại: biến thể template lịch sử với smoothing đề xuất 3 ngày. Ưu tiên: thấp; đối chứng, không phải ứng viên mạnh đã xác nhận.

```text
ts_decay_linear(zscore(ts_sum(anl4_fcf_flag, 22)), 3)
```

Nguồn: [accumulated revision](patterns/zscore-accumulated-revision.md). FCF đơn lẻ trong template này từng yếu; vai trò của flag trong R18 không chứng minh nó mạnh khi đứng một mình.

## 4. Đề xuất nghiên cứu và đối chứng cơ chế

Các N-ID dưới đây là biểu thức cụ thể hóa mục 8 của [bản tổng hợp](knowledge.md). Không gắn Sharpe dự kiến. Cặp dấu đối nhau dùng để kiểm tra hướng và tính nhất quán pipeline, không tính là hai nguồn thông tin độc lập. Negation được đặt trong `rank` và giữ nguyên wrapper để giảm sai khác không cần thiết.

### N01. Event magnitude của tỷ số ITCI/giá

Config: `F6`. Loại: baseline tách thành phần từ R04. Ưu tiên: nhóm chạy đầu tiên.

```text
rank(abs(ts_delta(fnd6_itci / close, 3)))
```

Đây là anchor chưa thêm stabilizer, không phải R04 đầy đủ.

### N02. Đối hướng N01

Config: `F6`. Loại: đối chứng hướng. Ưu tiên: cùng đợt N01 nếu chưa biết chiều.

```text
rank(-1 * abs(ts_delta(fnd6_itci / close, 3)))
```

Không giả định kết quả hai hướng đều dương hoặc tạo đa dạng hóa thực sự.

### N03. Chỉ biến động kế toán, magnitude

Config: `F6`. Loại: giả thuyết phân rã. Ưu tiên: cao.

```text
rank(abs(ts_delta(fnd6_itci, 3) / close))
```

Loại thành phần thay đổi tỷ số chỉ vì mẫu số giá. Vẫn cần kiểm soát đơn vị, quy mô và dữ liệu kế toán được restate.

### N04. Đối hướng N03

Config: `F6`. Loại: đối chứng hướng. Ưu tiên: cùng đợt N03.

```text
rank(-1 * abs(ts_delta(fnd6_itci, 3) / close))
```

Kiểm tra xem sự kiện lớn được thưởng hay bị phạt trong dữ liệu nghiên cứu.

### N05. Chỉ thành phần biến động mẫu số giá

Config: `F6`. Loại: giả thuyết phân rã. Ưu tiên: cao.

```text
rank(abs(ts_delay(fnd6_itci, 3) * (1 / close - 1 / ts_delay(close, 3))))
```

So với N01 và N03 để xác định tín hiệu gốc có thực sự đến từ cập nhật kế toán không. Đẳng thức phân rã chỉ đúng trước `abs` và `rank`.

### N06. Đối hướng N05

Config: `F6`. Loại: đối chứng hướng. Ưu tiên: cùng đợt N05.

```text
rank(-1 * abs(ts_delay(fnd6_itci, 3) * (1 / close - 1 / ts_delay(close, 3))))
```

Nếu N05/N06 giải thích phần lớn PnL của N01, phải xem lại câu chuyện underreaction với sự kiện kế toán.

### N07. Biến động kế toán có dấu

Config: `F6`. Loại: đối chứng cho phép `abs`. Ưu tiên: cao.

```text
rank(ts_delta(fnd6_itci, 3) / close)
```

Kiểm tra hướng tăng và giảm khác nhau, không xóa dấu ngay từ đầu.

### N08. Đối hướng N07

Config: `F6`. Loại: đối chứng hướng. Ưu tiên: cùng đợt N07.

```text
rank(-1 * ts_delta(fnd6_itci, 3) / close)
```

N03/N04 đo magnitude, N07/N08 đo hướng; chúng trả lời hai câu hỏi khác nhau.

### N09. Main effect A: ivaco có smoothing

Config: `F6`. Loại: đối chứng main effect. Ưu tiên: chạy cùng N10-N12 và N17.

```text
ts_decay_linear(rank(fnd6_ivaco / close), 5)
```

Không dùng kết quả một ivaco baseline khác universe hoặc smoothing để thay thế.

### N10. Main effects cộng: ivaco + intraday

Config: `F6`. Loại: baseline additive. Ưu tiên: cao trong nhóm interaction.

```text
ts_decay_linear(rank(fnd6_ivaco / close) + rank(open / close - 1), 5)
```

Main effect B tương ứng là N17. Giữ config F6 cho cả nhóm.

### N11. Centered-rank interaction

Config: `F6`. Loại: giả thuyết interaction. Ưu tiên: cao.

```text
ts_decay_linear((rank(fnd6_ivaco / close) - 0.5) * (rank(open / close - 1) - 0.5), 5)
```

Cả hai thành phần cùng thấp cũng cho tích dương. Chỉ dùng nếu cơ chế phù hợp, không diễn giải đây là bộ lọc chỉ chọn cả hai cùng cao. So với N09, N10 và N17.

### N12. Product rank không centered

Config: `F6`. Loại: đối chứng interaction. Ưu tiên: sau N11.

```text
ts_decay_linear(rank(fnd6_ivaco / close) * rank(open / close - 1), 5)
```

So N11 để phân biệt tác động của main effects và cấu trúc tích; kiểm tra concentration.

### N13. Product ba chiều với ptpr flag

Config: `F6`. Loại: ví dụ cụ thể trong bản tổng hợp, chưa xác minh hiệu quả của đúng tổ hợp. Ưu tiên: sau N09-N12, chỉ khi hiểu flag.

```text
ts_decay_linear(rank(fnd6_ivaco / close) * rank(open / close - 1) * rank(anl4_ptpr_flag), 5)
```

Không sử dụng S=2.30/F=2.05 của R12 làm số liệu cho N13. R12 dùng `bvps_flag` và là một expression khác.

### N14. EPS consensus thay đổi 22 ngày

Config: `F6`. Loại: đề xuất nghiên cứu, có điều kiện dữ liệu. Ưu tiên: sau khi xử lý fiscal rollover.

```text
ts_decay_linear(rank(ts_delta(anl4_afv4_eps_mean, 22) / close), 5)
```

Nguồn ngữ nghĩa: [EPS mean](factor_profiles/anl4_afv4_eps_mean.md). Cần cùng kỳ dự báo; chỉ kéo cửa sổ lên 22 chưa đủ biến delta thành earnings surprise.

### N15. Đối hướng EPS consensus change

Config: `F6`. Loại: đối chứng hướng cho N14. Ưu tiên: chỉ khi N14 đủ điều kiện dữ liệu.

```text
ts_decay_linear(rank(-1 * ts_delta(anl4_afv4_eps_mean, 22) / close), 5)
```

Giữ nguyên thông tin khả dụng, fiscal period và cùng khoảng đánh giá với N14.

### N16. EPS consensus level làm baseline

Config: `F6`. Loại: đối chứng mức cho N14/N15. Ưu tiên: không chạy riêng để tìm ứng viên nếu không có giả thuyết khác.

```text
ts_decay_linear(rank(anl4_afv4_eps_mean / close), 5)
```

Tách thay đổi kỳ vọng khỏi earnings-yield-like level; EPS phải có đơn vị nhất quán với giá. Profile lịch sử của các biến đổi mức đơn giản không mạnh.

### N17. Intraday inverse-return có smoothing

Config: `F6`. Loại: main effect B và baseline cơ chế. Ưu tiên: cao.

```text
ts_decay_linear(rank(open / close - 1), 5)
```

Với Delay 1, đây là thông tin của ngày dữ liệu trước quyết định; không phải chiến lược dùng close hôm nay để giao dịch open cùng ngày.

### N18. Đối hướng intraday

Config: `F6`. Loại: đối chứng hướng. Ưu tiên: cùng đợt N17.

```text
ts_decay_linear(rank(-1 * (open / close - 1)), 5)
```

Đối hướng cùng đại lượng với N17, không thay bằng `close / open - 1` vì hai đại lượng không là âm chính xác của nhau.

### N19. Overnight gap đúng định nghĩa giá trước đó

Config: `F6`. Loại: baseline để phân biệt cơ chế. Ưu tiên: cao.

```text
ts_decay_linear(rank(open / ts_delay(close, 1) - 1), 5)
```

Dùng giá điều chỉnh nhất quán. Đây là overnight gap trên chuỗi ngày dữ liệu; với Delay 1 không mặc định giao dịch tại chính open tạo ra gap đó.

### N20. Đối hướng overnight gap

Config: `F6`. Loại: đối chứng hướng. Ưu tiên: cùng đợt N19.

```text
ts_decay_linear(rank(-1 * (open / ts_delay(close, 1) - 1)), 5)
```

So N17-N20 để biết họ blend gốc dựa vào intraday reversal hay thông tin ngoài giờ. Chưa thêm fundamental khi chưa hiểu baseline.

### N21. Anchor cld2 đơn lẻ

Config: `F6`. Loại: ablation cho R08. Ưu tiên: cùng đợt N22-N28.

```text
ts_decay_linear(rank(fnd6_cld2 / close), 5)
```

Nguồn ngữ nghĩa: [cld2](factor_profiles/fnd6_cld2.md), capitalized leases due in second year. Profile standalone yếu; mục đích là đo đóng góp, không hứa hẹn submit độc lập.

### N22. Anchor fopo đơn lẻ

Config: `F6`. Loại: ablation cho R08. Ưu tiên: cùng N21.

```text
ts_decay_linear(rank(fnd6_fopo / close), 5)
```

Nguồn ngữ nghĩa: [fopo](factor_profiles/fnd6_fopo.md), Funds from Operations - Other. Không tự gọi đây là free cash flow hoặc cash balance.

### N23. Chỉ hai anchor cld2 + fopo

Config: `F6`. Loại: ablation bỏ shared stabilizer của R08. Ưu tiên: nhóm đo đóng góp anchor.

```text
ts_decay_linear(rank(fnd6_cld2 / close) + rank(fnd6_fopo / close), 5)
```

So N21/N22 và N24, không chỉ so với R08 để kết luận hai anchor độc lập.

### N24. Chỉ shared stabilizers ivaco + buzz

Config: `F6`. Loại: đối chứng R08 bỏ toàn bộ anchor. Ưu tiên: bắt buộc nếu đánh giá R08.

```text
ts_decay_linear(2 * rank(fnd6_ivaco / close) + 2 * rank(ts_mean(scl12_buzz, 10) * (-1 * returns)), 5)
```

Nếu N24 gần như giữ nguyên PnL của R08 thì hai anchor có ít đóng góp biên trong cấu hình này.

### N25. R08 bỏ cld2

Config: `F6`. Loại: leave-one-out ablation. Ưu tiên: chỉ sau R08/N24.

```text
ts_decay_linear(rank(fnd6_fopo / close) + 2 * rank(fnd6_ivaco / close) + 2 * rank(ts_mean(scl12_buzz, 10) * (-1 * returns)), 5)
```

Đo đóng góp riêng của cld2; không tối ưu lại trọng số khi chạy phép so sánh này.

### N26. R08 bỏ fopo

Config: `F6`. Loại: leave-one-out ablation. Ưu tiên: chỉ sau R08/N24.

```text
ts_decay_linear(rank(fnd6_cld2 / close) + 2 * rank(fnd6_ivaco / close) + 2 * rank(ts_mean(scl12_buzz, 10) * (-1 * returns)), 5)
```

Đo đóng góp riêng của fopo, không gán việc giảm Sharpe tự động cho quan hệ nhân quả.

### N27. R08 bỏ ivaco

Config: `F6`. Loại: leave-one-out ablation. Ưu tiên: chẩn đoán vai trò stabilizer.

```text
ts_decay_linear(rank(fnd6_cld2 / close) + rank(fnd6_fopo / close) + 2 * rank(ts_mean(scl12_buzz, 10) * (-1 * returns)), 5)
```

Nếu chất lượng giảm, xem cả coverage, trọng số và tương quan; không chỉ kết luận “ivaco luôn bắt buộc”.

### N28. R08 bỏ buzz-reversal

Config: `F6`. Loại: leave-one-out ablation. Ưu tiên: chẩn đoán tín hiệu reversal.

```text
ts_decay_linear(rank(fnd6_cld2 / close) + rank(fnd6_fopo / close) + 2 * rank(fnd6_ivaco / close), 5)
```

Nếu R08 hơn N28 chủ yếu nhờ reversal, cần đo corr với book giá-volume hiện có trước khi gọi đây là alpha cơ bản mới.

## 5. Đối chứng có điều kiện, không phải hàng đợi ưu tiên

Chỉ chạy D-ID khi cần trả lời câu hỏi tương ứng. Chúng có thể yếu hoặc từng trượt gate; không dành quota tái khai thác nếu không có lý do nghiên cứu mới.

### D01. ITCI event + leverage, bỏ drlt

Config: `F6`. Loại: đối chứng âm cho R04. Ưu tiên: chỉ để kiểm tra vai trò sub-universe stabilizer.

```text
rank(abs(ts_delta(fnd6_itci / close, 3))) + rank(-1 * equity / assets)
```

[Pattern event](patterns/event-magnitude-abs-ts-delta.md) ghi nhận biến thể hai thành phần trượt sub-universe. Không tối ưu thêm nhiều cửa sổ chỉ vì headline Sharpe đẹp.

### D02. R15 bỏ volatility gate

Config: `F6`. Loại: baseline bắt buộc trước khi quy hiệu quả cho gate.

```text
ts_decay_linear(rank(ts_mean(implied_volatility_call_270 - implied_volatility_put_270, 10)) + rank(fnd6_itci / close) + rank(fnd6_acdo) + rank(anl4_netdebt_flag) + rank(ts_mean(scl12_buzz, 5)) + rank(open / close - 1), 5)
```

So R15 về sub-universe, turnover, active positions, tuổi vị thế và kết quả theo regime. Gate có thể chỉ giữ vị thế cũ; giảm turnover không tự chứng minh tín hiệu tốt hơn.

### D03. R16 bỏ sales count

Config: `F6`. Loại: đối chứng coverage densifier.

```text
ts_decay_linear(rank(abs(ts_delta(fn_liab_fair_val_a / close, 3))) + rank(-1 * equity / assets) + rank(anl4_ffo_flag) + rank(fnd6_ivaco / close) + rank(fnd6_drlt / close) + rank(open / close - 1), 5)
```

Theo [candidate sales densify](opportunities/submit-n1ry5zjg.md), một biến thể OC-only từng self-corr FAIL. Không gán check cũ cho lần chạy này; so trực tiếp cùng mẫu với R16.

### D04. R16 bỏ cả intraday và sales count

Config: `F6`. Loại: baseline trước khi thêm hai thành phần dày dữ liệu.

```text
ts_decay_linear(rank(abs(ts_delta(fn_liab_fair_val_a / close, 3))) + rank(-1 * equity / assets) + rank(anl4_ffo_flag) + rank(fnd6_ivaco / close) + rank(fnd6_drlt / close), 5)
```

So D04 -> D03 -> R16. Không quy toàn bộ cải thiện R16 so D04 cho riêng sales count.

### D05. Analyst tích lũy nhưng dùng rank

Config: `F6`. Loại: đối chứng chuẩn hóa cho R05.

```text
ts_decay_linear(rank(ts_sum(anl4_netprofit_flag, 22)), 3)
```

Giữ nguyên tổng 22 ngày và smoothing 3 ngày để chỉ kiểm tra rank so với zscore. Vẫn cần hiểu flag; đối chứng thống kê không sửa được ngữ nghĩa sai.

### D06. Sales-estimate-count đơn lẻ

Config: `F6`. Loại: main effect đối chứng cho R16.

```text
ts_decay_linear(rank(sales_estimate_count_quarterly), 5)
```

Nguồn: [sales-count profile](factor_profiles/sales_estimate_count_quarterly.md). Số ước lượng không phải mức kỳ vọng doanh thu. Đo size/liquidity exposure trước khi gọi đây là thông tin analyst mới.

## 6. Thứ tự chạy và giới hạn ngân sách

Danh mục có **57 biểu thức riêng**: 23 mục R, 28 mục N và 6 mục D. Đây là menu nghiên cứu, không phải yêu cầu chạy hết trong một phiên hoặc một lời khẳng định có 57 alpha có lãi.

### Đợt A: tìm hiểu cơ chế mới, tối đa 24 mô phỏng

| Giai đoạn | ID/config | Số lượt tối đa | Quyết định cần có |
|---|---|---|---|
| Phân rã sự kiện | N01-N08, tất cả F6 | 8 | Thay đổi kế toán hay giá ở mẫu số mang tín hiệu? |
| Main effects và interaction | N09-N12 và N17, tất cả F6 | 5 | Interaction có giá trị hơn tổng/main effects không? |
| Tách intraday/overnight | N18-N20, tất cả F6; tái dùng N17 | 3 | Cơ chế và chiều nào còn hợp lý? |
| Chẩn đoán nhánh còn sống | Tối đa 4 ID phù hợp chưa chạy hoặc thay một tham số có lý do | 4 | Lỗi cấu trúc có cách sửa hợp lý không? |
| Xác nhận | Tối đa 4 cấu hình đã chọn, trên phần xác nhận nếu hỗ trợ | 4 | Hiệu quả có bền ngoài phần chọn mô hình không? |

N17 được dùng trong hai phép so sánh nhưng chỉ mô phỏng một lần với cùng settings/mẫu. Nếu chưa có baseline lịch sử, có thể thay một số lượt bằng R02, R04, R06 hoặc R08 theo mục tiêu; không cộng vô hạn vào ngân sách. Các cặp dấu và ablation không tự được tính là structural novelty.

### Đợt B: tái lập các mẫu mạnh trong kho

Với book còn ít alpha, bắt đầu bằng R02/F6, R04/F6, R06/I10 và R08/F6. Sau đó cân nhắc R12/F6, R13/F6, R17/M6 hoặc R18/F6 tùy dữ liệu và phần tương quan còn trống. R05/F6 chỉ nên thêm sau khi xác minh flag.

R15 và R16 có nhiều thành phần, nên để sau khi hiểu baseline. R19/R20 chia sẻ full leverage stack và có nguy cơ bão hòa cao; không ưu tiên chỉ vì Sharpe lịch sử đẹp. R21-R23 là template đối chứng yếu hơn, không phải hàng đợi submit tự động.

### Đợt C: kiểm tra tính mới của hai anchor

Chạy R08 và N21-N28 cùng F6 để đo đóng góp. Có thể bắt đầu bằng R08, N23 và N24 rồi chỉ mở rộng leave-one-out khi kết quả còn đáng nghiên cứu. Đây là một đợt riêng; không cần trộn toàn bộ với đợt A.

Không xuất expression hồi quy residual thành công thức giả khi chưa có operator/dữ liệu phù hợp. Hướng residualization trong bản tổng hợp cần quy trình ước lượng quá khứ và kiểm định sau đó; không có một biểu thức FASTEXPR cố định đáng tin để tự điền nếu chưa thiết kế bước này.

## 7. Điều kiện dừng và cách lưu kết quả

Mỗi lần chạy lưu: ID tài liệu, expression thực tế, toàn bộ settings, khoảng dữ liệu, BRAIN alpha ID, S/F/T, returns, drawdown, coverage, số vị thế, concentration, sub-universe, correlation period và mọi check bắt buộc. Bất kỳ thay đổi config nào đều tạo một lần thử khác và phải ghi lại.

Dừng nhánh nếu field sai ngữ nghĩa/không đủ coverage, concentration không có cách sửa hợp lý, chỉ số phụ thuộc một giai đoạn, hoặc bỏ anchor không làm giảm đóng góp. Không “cứu” mọi công thức bằng cùng leverage/ivaco/buzz rồi gọi đó là alpha độc lập.

Trước khi submit, dùng [checklist trong bản tổng hợp](knowledge.md), kiểm tra tương quan với book hiện tại và đợi kết quả chính thức hoàn tất. PENDING/timeout không phải PASS; S/F lịch sử và grade trong kho không phải chứng nhận đủ điều kiện cho tài khoản hiện tại. Chưa có kiểm định mới thì tất cả mục ở đây vẫn là công thức để nghiên cứu, không phải khuyến nghị giao dịch tiền thật.
