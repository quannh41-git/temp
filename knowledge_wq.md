---
category: "synthesis"
updated: "2026-11-18"
scope: "WorldQuant BRAIN alpha research from local knowledge archive"
language: "vi"
---

# Phương pháp nghiên cứu alpha cho WorldQuant BRAIN

## 1. Phạm vi và cách đọc

Tài liệu này tổng hợp kinh nghiệm trong workspace thành một quy trình tạo alpha mới. Mục tiêu không phải tìm một công thức có Sharpe cao nhất trong quá khứ, mà tìm tín hiệu có cơ chế kinh tế hợp lý, dữ liệu phù hợp, chất lượng kiểm định đủ tốt và đóng góp khác biệt cho danh mục.

**Giới hạn bằng chứng:** đây là kho nghiên cứu lịch sử, không phải kết quả backtest mới. Ngày tổng hợp không phải ngày xác nhận lại các ứng viên. Các trạng thái ACTIVE, EXCELLENT, SPECTACULAR và những ngưỡng được nhắc đến là ghi nhận của dự án tại thời điểm nghiên cứu; không phải cam kết về tài khoản BRAIN hiện tại. Hạ tầng hàng đợi và tài khoản của dự án gốc đã ngừng hoạt động theo phần giới thiệu trong tài liệu gốc của repository.

Phân biệt ba cấp độ:

- **Đã quan sát:** có ghi chép thử nghiệm cụ thể trong kho; vẫn có thể phụ thuộc thời kỳ, universe và cấu hình.
- **Suy luận nghiên cứu:** giải thích hợp lý từ kết quả, chưa chứng minh quan hệ nhân quả.
- **Đề xuất mới:** giả thuyết để kiểm định, không được xem là alpha đã đạt chuẩn.

### Bản đồ nguồn

| Thư mục | Vai trò | Cách sử dụng |
|---|---|---|
| `patterns/` | Các phép biến đổi và tổ hợp từng có hiệu quả | Hiểu điều kiện thành công, không sao chép mù quáng |
| `rules/` | Ràng buộc và bài học vận hành | Chặn lỗi trước khi tiêu tốn lượt mô phỏng |
| `dead_zones/` | Dataset, họ tín hiệu hoặc template đã thất bại/bão hòa | Chỉ mở lại khi có giả thuyết thay đổi điều kiện thất bại |
| `factor_profiles/` | Hồ sơ theo field, gồm cả kết quả không tốt | Chọn dữ liệu và kiểm tra mức độ đã được khai thác |
| `opportunities/` | Hướng nghiên cứu và ứng viên lịch sử | Kiểm tra ngày, trạng thái và tương quan hiện tại trước khi dùng |
| `reviews/` | Tổng kết, loại trùng và cập nhật nhận thức | Ưu tiên kết luận mới có bằng chứng hơn ghi chú cũ mâu thuẫn |

## 2. Kết luận cốt lõi từ workspace

### 2.1. Khác biệt về công thức chưa chắc khác biệt về lợi nhuận

Đổi field, cửa sổ hoặc decay có thể tạo biểu thức mới nhưng vẫn giữ cùng cơ chế và PnL. [Quy tắc novelty](rules/novelty-required.md) phân biệt đổi lá của cây toán tử với thay đổi cấu trúc cây; yêu cầu lịch sử là dành ít nhất 50% ngân sách phiên cho cấu trúc mới.

Đây là quy tắc phân bổ nghiên cứu của dự án, không phải quy định BRAIN. Một cấu trúc mới cũng có thể vô dụng: các template correlation động, gating và signal-to-noise đã có nhiều thất bại trong kho. Tính mới phải đi cùng lý do kinh tế và kiểm định.

### 2.2. Tín hiệu phải khớp với bản chất dữ liệu

[Review tổng hợp](reviews/20260614-draft-pr-distillation.md) ghi nhận ba ví dụ quan trọng:

- Cờ điều chỉnh dự báo thưa nên được thử theo tích lũy `zscore(ts_sum(flag, 22))`, thay vì chỉ `rank(flag)` trên rất nhiều giá trị bằng 0.
- `rank(abs(ts_delta(fnd6_itci / close, 3)))` từng tạo họ event-magnitude có chất lượng; không suy rộng sang mọi field cơ bản. Lời giải thích về tồn kho trong pattern gốc mâu thuẫn với hồ sơ field: `itci` được mô tả là Investment Tax Credit (Income Account), không phải tồn kho. Xem mục 3 trước khi diễn giải cơ chế.
- `ts_zscore` trên dữ liệu fundamental2 thưa từng tạo chỉ số tổng hợp rất đẹp nhưng không qua kiểm tra tập trung trọng số.

Bài học: phải hiểu field đo gì, cập nhật khi nào, thiếu dữ liệu ra sao và phép biến đổi đang đo mức độ, thay đổi hay sự kiện.

### 2.3. Khả năng submit là bài toán nhiều điều kiện

Sharpe cao không đủ nếu fitness thấp, turnover cao, vị thế tập trung hoặc tự tương quan quá lớn. [Ghi nhận về self-correlation](rules/self-corr-threshold.md) của dự án mô tả ngưỡng 0.70 và ngoại lệ Sharpe premium 1.10 lần. Đây là quan sát lịch sử, không thay thế kết quả kiểm tra trên nền tảng hiện tại.

Kiểm tra PnL correlation cục bộ chỉ dùng để sàng lọc. Kết quả check chính thức của BRAIN đối với đúng candidate và đúng danh mục tại thời điểm đánh giá mới là căn cứ quyết định.

### 2.4. Mẫu thành công là điểm xuất phát, không phải danh sách để tái khai thác vô hạn

Kho đã có nhiều biến thể của value cơ bản, IV spread, analyst flags và các thành phần ổn định. Khi chúng đã hiện diện trong danh mục, tiếp tục cộng cùng thành phần có thể nâng chỉ số nhưng tiêu hết khoảng trống tương quan.

Vì vậy, thứ tự tiếp cận nên là: **cơ chế mới hoặc tương tác có lý do -> dữ liệu phù hợp -> phép biến đổi -> kiểm định độc lập -> kiểm tra đóng góp danh mục**. Không bắt đầu bằng việc ghép ngẫu nhiên các toán tử.

## 3. Kiểm toán dữ liệu trước khi tìm công thức

### 3.1. Quy mô kho và giới hạn của bản tổng hợp

Tại ngày tổng hợp, thư mục có 1.669 hồ sơ field, 29 patterns, 28 dead zones, 18 rules, 44 opportunities và 1 review, không tính tài liệu này. Đây là số tệp hiện diện, không phải số alpha độc lập hoặc số phiên đã kiểm chứng.

Bản tổng hợp đối chiếu trực tiếp các nguồn then chốt và một số hồ sơ đại diện, không tái chạy toàn bộ thí nghiệm hoặc kiểm toán từng hồ sơ. Nhiều bảng có dữ liệu 2019-2023; chúng không chứng minh tính hiệu quả trong năm 2026 hay ngoài mẫu.

### 3.2. Hợp đồng dữ liệu cho mỗi field

Trước khi mô phỏng, cần ghi được:

| Câu hỏi | Vì sao quan trọng |
|---|---|
| Field đo đại lượng gì? | Không suy ra ý nghĩa kinh tế chỉ từ tên viết tắt |
| Là số đo liên tục, số đếm, mã phân loại hay cờ sự kiện? | Không cộng/trừ một mã phân loại như thể nó là lợi nhuận hoặc số lần revision |
| Dữ liệu là MATRIX hay VECTOR? | VECTOR cần phép tổng hợp phù hợp trong danh sách operator được cấp quyền |
| Đơn vị: tổng tiền, tiền/cổ phiếu, tỷ lệ hay số lượng? | Tránh tỷ số không có ý nghĩa và lỗi kiểm tra đơn vị |
| Tần suất cập nhật thực tế là gì? | Fundamental báo cáo quý không tạo ra thông tin mới mỗi ngày |
| Giá trị được biết vào thời điểm nào? | Phải dùng thời điểm công bố/khả dụng, không dùng ngày kết thúc kỳ kế toán |
| Coverage, tỷ lệ NaN/0 và độ cũ thế nào? | Phân biệt không có dữ liệu với giá trị thực bằng 0 |
| Có restatement, fiscal rollover, stock split hay đổi đơn vị không? | Những thay đổi này có thể giả dạng sự kiện kinh tế |
| Đã có field tương đương hoặc cùng redundancy cluster chưa? | Tránh nghiên cứu lại cùng tín hiệu dưới tên khác |

Không dùng `ts_backfill` hoặc `group_backfill` như cách sửa mọi thiếu hụt. Backfill thời gian có thể giữ thông tin quá cũ; backfill theo nhóm tạo giá trị ước lượng, không phải báo cáo thật của công ty. Tuyệt đối không backfill từ tương lai.

### 3.3. Bốn điểm dễ diễn giải sai trong chính kho này

**`fnd6_itci` không được mặc định là tồn kho.** [Hồ sơ itci](factor_profiles/fnd6_itci.md) ghi Investment Tax Credit (Income Account), trong khi [pattern event-magnitude](patterns/event-magnitude-abs-ts-delta.md) kể câu chuyện inventory. Kết quả mô phỏng và lời giải thích là hai loại bằng chứng khác nhau. Phải kiểm tra mô tả chính thức trên BRAIN trước khi xây giả thuyết về thuế đầu tư; không kế thừa câu chuyện tồn kho.

**Flag không tự động là hướng điều chỉnh dự báo.** [Hồ sơ netprofit flag](factor_profiles/anl4_netprofit_flag.md) mô tả “forecast type (revision/new/...)”. Vì vậy, `ts_sum(flag, 22)` có kết quả lịch sử tốt không đồng nghĩa đã đo được 22 ngày nâng/hạ dự báo. Nếu là mã phân loại, phải hiểu và ánh xạ đúng mã; nếu là trạng thái được lặp lại hàng ngày, tổng theo ngày không phải số sự kiện độc lập.

**`open / close - 1` không phải gap qua đêm.** Khi cùng chỉ số ngày, nó so sánh giá mở cửa với đóng cửa trong ngày. Gap qua đêm thông thường là `open / ts_delay(close, 1) - 1`. Hai công thức không được đổi tên hoặc thay thế cho nhau khi trích kết quả lịch sử. Với Delay 1, giá trị ở ngày dữ liệu t phục vụ quyết định sau đó; không giả định có thể giao dịch tại chính giá mở cửa t bằng close t.

**Chia tổng đại lượng kế toán cho giá cổ phiếu chưa chắc là value yield.** Nếu `F` là tổng tiền của doanh nghiệp, `F / close` còn lẫn số cổ phiếu/quy mô; mẫu số kinh tế thường cần vốn hóa hoặc đại lượng quy mô phù hợp. Nếu `F` là tiền/cổ phiếu, chia cho giá mới gần với yield. Không tự áp `/ close` cho số lượng analyst, mã tiền tệ hoặc lãi suất.

## 4. Các họ ý tưởng đã có bằng chứng

Trong mục này, S = Sharpe, F = fitness, T = turnover. Các số là ghi nhận lịch sử của đúng biến thể trong nguồn; không phải kết quả mới. Grade là nhãn của pipeline, không thay thế submission checks của BRAIN.

### 4.1. Mức cơ bản và leverage trong ngành

```text
rank(-1 * equity / assets) + rank(fnd6_drlt / close)
```

[Leverage premium](patterns/leverage-premium.md) ghi nhận leverage đơn lẻ S khoảng 1.55, phối hợp `drlt` đạt S khoảng 1.87 và qua checks tại thời điểm đó. Cơ chế được đề xuất là phần bù rủi ro đòn bẩy trong cùng ngành; đây không phải bằng chứng rằng nợ cao gây lợi nhuận cao.

SUBINDUSTRY hiệu quả hơn MARKET trong thí nghiệm này; MARKET làm S của thành phần leverage giảm từ 1.55 xuống 0.72. Điều đó cảnh báo tín hiệu nhạy với cách so sánh ngang ngành và rủi ro còn sót lại.

**Cách dùng:** làm baseline hoặc đối chứng loại bỏ thành phần. Không coi leverage là thành phần bắt buộc cho mọi alpha mới vì nó đã trở thành nguồn tương quan chung lớn trong danh mục lịch sử.

### 4.2. Event-magnitude: đo độ lớn thay đổi, không đo hướng

```text
rank(abs(ts_delta(fnd6_itci / close, 3)))
+ rank(-1 * equity / assets)
+ rank(fnd6_drlt / close)
```

[Nguồn event-magnitude](patterns/event-magnitude-abs-ts-delta.md) ghi nhận `0m8GV1Pp`: S=2.64, F=2.77, self-corr=0.549 PASS; cấu hình USA TOP3000, SUBINDUSTRY, platform decay 6. Bỏ stabilizer từng làm biến thể hai thành phần trượt sub-universe dù chỉ số tổng thể tốt.

**Điểm cần học:** thay đổi phép biểu diễn có thể quan trọng hơn thay field. Nhưng `abs` xóa dấu kinh tế; phải thử biến đổi có dấu để biết liệu biến động tăng và giảm có thật sự cùng dự báo lợi nhuận hay không. Mẫu này còn trộn thay đổi field với thay đổi giá ở mẫu số, cần phân rã ở mục 8.1.

Nhận định sớm “chỉ itci tốt” không còn bao quát toàn bộ kho: [ghi chép sparse guidance](dead_zones/family-sparse-analyst-guidance-untested-fields.md) sau đó ghi nhận đột phá event-magnitude ở `fnd6_txw`/`fnd6_txdbca`. Điều đó không làm mọi field trở thành ứng viên tốt.

### 4.3. Tích lũy analyst flags và lựa chọn chuẩn hóa

```text
ts_decay_linear(zscore(ts_sum(anl4_netprofit_flag, 22)), 3)
```

[Pattern tích lũy](patterns/zscore-accumulated-revision.md) ghi nhận S=1.72, F=2.21, self-corr=0.593 cho biến thể netprofit; trong so sánh cùng bối cảnh, đổi `rank` sang `zscore` nâng S từ -0.72 lên 1.71. Các chênh lệch nhỏ là những biến thể được nguồn mô tả, không phải một lần chạy duy nhất.

**Giải thích thống kê:** rank có nhiều giá trị đồng hạng khi dữ liệu chủ yếu bằng 0; zscore giữ thông tin về khoảng cách số học. Tuy nhiên zscore cũng nhạy với ngoại lệ và không sửa sai ngữ nghĩa mã phân loại. Không suy diễn rằng rank luôn sai hoặc mọi flag đều phải dùng zscore.

**Cách phát triển:** xác minh loại flag; so sánh với thay đổi forecast liên tục của cùng kỳ dự báo; kiểm soát việc chuyển năm tài chính và thay đổi thành phần analyst.

### 4.4. IV call-put spread và smoothing

```text
ts_decay_linear(
	zscore(ts_mean(implied_volatility_call_270 - implied_volatility_put_270, 22)),
	10
)
```

[Pattern IV](patterns/iv-spread-zscore-tsmean.md) ghi nhận `vRm07LP3`: S=1.82, F=2.35, self-corr=0.309, USA TOP3000, MARKET, platform decay 10. Cơ chế giả định là thông tin/risk premium trong chênh lệch IV call-put; không mặc định nó là chênh lệch kỳ vọng lợi nhuận thuần túy.

**Điểm cần học:** phép chuẩn hóa và neutralization có thể giúp độ phủ/trọng số, nhưng không miễn kiểm tra concentration. Thay tenor 270 thành 90 hay 60 không tự tạo cơ chế độc lập; nhiều họ IV đã bão hòa trong danh mục.

Pattern sớm cảnh báo blend fundamentals thất bại, nhưng [review sau đó](reviews/20260614-draft-pr-distillation.md) ghi nhận hybrid thành công. Vì vậy, lời cấm chỉ phản ánh biến thể/cấu hình đã thử, không phải định luật về IV-fundamental.

### 4.5. Attention kết hợp đảo chiều

```text
rank(ts_mean(scl12_buzz, 5) * (-1 * returns))
```

Đây là thành phần xuất hiện trong [blend template](patterns/blend-template.md) và [mẫu bỏ leverage](patterns/leverage-free-fresh-anchor-decorrelation.md). Giả thuyết: biến động giá gần đây ở cổ phiếu được chú ý mạnh dễ đảo chiều ngắn hạn. Đây là tín hiệu giá-hành vi, không phải thông tin cơ bản mới.

Quan trọng: `rank(mean(buzz) * (-returns))` khác `rank(mean(buzz)) * rank(-returns)`. Không thay công thức mà giữ nguyên kết luận. [Buzz level nhân event-magnitude](dead_zones/template-buzz-level-event-magnitude-product.md) từng yếu trong hai thử nghiệm; attention level không thay thế được thành phần reversal.

### 4.6. Tương tác nhân so với cộng

```text
ts_decay_linear(
	rank(fnd6_ivaco / close)
	* rank(open / close - 1)
	* rank(anl4_ptpr_flag),
	5
)
```

Đây là ví dụ điền field vào [template product-interaction](patterns/product-interaction-blend.md), **không gắn số liệu của một alpha ID cho tổ hợp minh họa này**. Nguồn ghi nhận biến thể dùng `ivaco` đạt S=2.30, F=2.05, self-corr=0.681; thay bằng `acdo` đạt S=2.28 nhưng self-corr=0.822 và bị chặn.

Tổng có thể cho phép một thành phần mạnh bù thành phần yếu; tích của các rank không âm thiên về nhóm đồng thời xếp hạng cao. Tuy nhiên tích không bảo đảm các tín hiệu “đồng thuận hướng” theo nghĩa long/short sau neutralization. Tích của nhiều rank cũng có thể làm tập trung vị thế.

**Cách dùng:** so sánh cộng, nhân và tương tác rank đã trừ 0.5 trong cùng cấu hình; đo trọng số và PnL thực tế, không kết luận từ hình dạng toán tử.

### 4.7. Đổi chế độ và loại bỏ thành phần chung

Hai hướng đã có bằng chứng nhưng không được dùng như thuốc chữa chung:

| Hướng | Bằng chứng | Rủi ro |
|---|---|---|
| Volatility gate | [Một blend](patterns/volatility-gate-fixes-sub-universe.md) được sửa lỗi sub-universe: S=2.08, F=2.01, self-corr khoảng 0.548 | Ngưỡng vol tuyệt đối phụ thuộc universe; có thể chỉ chọn lại giai đoạn tốt |
| Bỏ leverage và thay anchor | [Hai anchor cld2 + fopo](patterns/leverage-free-fresh-anchor-decorrelation.md), giữ 2x ivaco + 2x buzz-reversal: S=2.29, F=2.26, check chính thức 0.6181 | Không còn mới với book đã chứa chính alpha này; vẫn chia sẻ các thành phần mạnh |
| Thêm coverage count | [Sales-count densifier](patterns/sales-count-densifier-decorrelates-oc.md): một biến thể từ corr 0.725 FAIL xuống 0.664 PASS, F=2.20 | Có thể đang thêm size/liquidity exposure chứ không sửa cơ chế gốc |

`trade_when(entry, signal, exit)` có trạng thái: cập nhật tín hiệu khi điều kiện entry đúng, đóng khi exit đúng, còn lại thường giữ vị thế theo semantics của operator. Nó không tương đương `entry * signal`. Cần kiểm tra thứ tự ưu tiên entry/exit và xử lý NaN trong tài liệu operator hiện tại.

### 4.8. Kết luận về kiến trúc alpha trong kho

Nhiều công thức có dạng: **anchor cơ bản/sự kiện + thành phần leverage hoặc coverage + reversal/analyst + smoothing**. Các thành phần có vai trò khác nhau, nhưng đó chỉ là cách phân tích; không phải lúc nào cũng cần đủ bốn.

Nếu một anchor mới chỉ đạt chuẩn sau khi thêm nhiều thành phần quen thuộc, hãy hỏi: **alpha mới có thực sự đến từ anchor, hay phần lớn PnL đang được tái sử dụng từ các alpha cũ?** Câu trả lời cần thử nghiệm loại bỏ từng thành phần, không chỉ xem Sharpe của tổng.

## 5. Những hướng nên tránh và điều kiện mở lại

| Vùng rủi ro | Bằng chứng trong kho | Chỉ mở lại khi |
|---|---|---|
| `ts_zscore` trên fundamental2 thưa | [22 biểu thức](dead_zones/fundamental2-sparse-ts-zscore.md); raw anchor S=4.10, F=10.75 nhưng concentration 0.50 so với limit 0.10 trong lần kiểm tra đó | Có cơ chế độ phủ mới và kiểm tra concentration trước khi tối ưu Sharpe |
| Delta/std của fundamental chậm | [Hai thí nghiệm](dead_zones/template-signal-to-noise-ratio.md) S gần 0/âm, T khoảng 36-44% | Dữ liệu dày hơn hoặc định nghĩa surprise khác, không chỉ đổi cửa sổ |
| Fundamental nhân dấu momentum giá/volume | [Năm biến thể](dead_zones/template-directional-gating-sign-delta.md) S âm, T khoảng 31-61% | Có cơ chế phù hợp tần suất và đối chứng cho chi phí đảo vị thế |
| Tỷ số fundamental tùy ý | [Bốn tỷ số](dead_zones/template-inter-field-ratio.md), S tốt nhất 0.26 | Tỷ số có ý nghĩa kế toán/kinh tế, mẫu số an toàn, không phải ghép field ngẫu nhiên |
| Full stabilizer stack có leverage | [Quy tắc sửa ngày 2026-07-19](rules/stabilizer-stack-block-generalizes-beyond-pstkrv.md): có trường hợp corr khoảng 0.77-0.93 | Bỏ/giảm nguồn tương quan chung và chứng minh phần PnL riêng của anchor |
| Chỉ đổi analyst flag hoặc IV tenor | Nhiều biến thể có thể có PnL gần giống nhau | Cơ chế, thời điểm hoặc exposure khác thực sự, có check mới |
| Nhãn “untested” trong hồ sơ cũ | Một số profile chưa phản ánh pattern thử sau đó | Đối chiếu profile với pattern, dead zone và ngày cập nhật |

Dead zone là bằng chứng âm trong một miền điều kiện, không phải chứng minh bất khả thi. Số mẫu 2-5 quá ít để tuyên bố mọi dataset hoặc mọi biến thể đã hết alpha.

## 6. Đọc có phê phán: tương quan, đảo dấu và bằng chứng thống kê

### 6.1. Đảo dấu phải được kiểm định, nhưng không tạo thông tin từ hư không

[Rule về negation](rules/no-negated-duplicates.md) và [phân tích direction](patterns/direction-diversification.md) ghi nhận các lần chạy hai hướng có kết quả không đối xứng. Điều này đáng điều tra, nhưng cách giải thích “neutralization tự tạo chiều độc lập” chưa được chứng minh trong các tài liệu đã đọc.

Trong trường hợp cùng tập cổ phiếu hợp lệ và rank chuẩn, xấp xỉ có:

$$
\operatorname{rank}(-x)=1-\operatorname{rank}(x).
$$

Sau khi loại thành phần hằng số bằng neutralization tuyến tính, hai tín hiệu sẽ đối dấu. Nếu mọi bước dựng vị thế và chi phí đều đối xứng, lợi nhuận gộp cũng đối dấu. Neutralization tuyến tính riêng nó không phá vỡ điều đó.

Vì vậy, khi hai hướng đều có Sharpe dương, cần so sánh alpha ID, ngày chạy, cửa sổ dữ liệu, universe, expression, NaN handling, neutralization, truncation, chi phí và phiên bản dữ liệu. Truncation đối xứng cũng không tự giải thích mọi bất đối xứng. Không so “best positive” với “best negative” ở hai template/universe khác nhau rồi quy hết chênh lệch cho dấu.

Thêm đúng bản sao `-X` vào ma trận dữ liệu không tăng hạng tuyến tính. Các thống kê PCA trong nguồn có thể phản ánh thay đổi tập mẫu, cách chọn best variant hoặc điều kiện chạy; không đủ để hứa rằng negation luôn tạo “5 lần số chiều alpha”. Tương quan âm mạnh cũng không đồng nghĩa độc lập; dùng cả corr có dấu và trị tuyệt đối khi chẩn đoán trùng thông tin.

### 6.2. PnL correlation, signal correlation và check chính thức là ba thứ khác nhau

- **Signal/weight correlation:** hai công thức có tạo cùng thứ hạng/vị thế không?
- **PnL correlation:** lợi nhuận theo ngày có cùng biến động không? Cần cùng lịch, cùng thời gian và đủ số quan sát giao nhau.
- **BRAIN correlation checks:** kết quả theo định nghĩa và tập đối chiếu của nền tảng; không suy ra đầy đủ từ hai đại lượng trên.

[Nguồn local-vs-BRAIN](rules/self-corr-pnl-gap.md) quan sát một nhóm IV có hệ số chênh 1.45-1.59 lần, nhưng [mẫu bỏ leverage](patterns/leverage-free-fresh-anchor-decorrelation.md) có local và check gần như trùng nhau. Không coi 1.6 là hệ số hiệu chỉnh phổ quát; chưa có bằng chứng xác nhận thuật toán nội bộ BRAIN là weight-level như nguồn suy đoán.

Mốc local khoảng 0.44 khi chia sẻ field chỉ là buffer bảo thủ trong kinh nghiệm cũ. Quyết định cuối cùng phải dựa trên check đã hoàn tất; PENDING, timeout hoặc chưa có chuỗi PnL không phải PASS. Production correlation, nếu tài khoản có check đó, phải được xem riêng với self-correlation.

### 6.3. Sharpe của blend PnL không phải Sharpe của biểu thức blend

[Factor merge screen](opportunities/factor-merge-candidates.md) và [theme blend screen](opportunities/theme-blend-candidates.md) đã tự ghi rõ đây là ước lượng. Với hai chuỗi lợi nhuận được ghép tuyến tính:

$$
\mu_p=w_A\mu_A+w_B\mu_B,\qquad
\sigma_p^2=w_A^2\sigma_A^2+w_B^2\sigma_B^2+2w_Aw_B\rho_{AB}\sigma_A\sigma_B.
$$

Tương quan thấp có thể cải thiện Sharpe danh mục, nhưng `rank(A) + rank(B)` sau neutralization, truncation và smoothing không nhất thiết tái tạo chuỗi PnL đó. Hơn nữa, cùng trọng số tín hiệu khác cùng trọng số vốn hoặc cùng rủi ro.

Không sử dụng Sharpe screen, nhãn all-weather hoặc toàn bộ các năm dương như bằng chứng ngoài mẫu. Việc chọn biểu thức tốt nhất từ hàng nghìn phép thử đã tạo selection bias đáng kể.

## 7. Quy trình tạo alpha mới trên BRAIN

### Bước 1. Chốt bài toán và cấu hình trước khi nhìn kết quả

Xác định mục tiêu: học một cơ chế, tìm một ứng viên đủ chuẩn, hay tăng đóng góp danh mục. Với người mới, nên bắt đầu từ một family dễ giải thích và baseline đơn giản; chưa cần tối ưu theo book bão hòa của tác giả gốc, vì book của bạn có thể hoàn toàn khác.

Lưu một cấu hình cố định: instrument, region, universe, language, delay, neutralization, decay, truncation, pasteurization, unit/NaN handling, ngày bắt đầu/kết thúc và giai đoạn kiểm định. Chỉ đổi một nhóm yếu tố khi có lý do.

**Baseline gợi ý cho phiên đầu:** equity USA, TOP3000, Fast Expression, Delay 1, SUBINDUSTRY, platform decay 6, truncation 0.08, nếu tài khoản hỗ trợ. Đây là điểm khởi đầu tái lập một số mẫu trong kho, không phải cấu hình tối ưu chung. Lưu rõ các tùy chọn còn lại thay vì dựa vào mặc định giao diện. Mẫu IV ở mục 4.4 dùng cấu hình khác và phải được tái lập riêng.

Độ dài `ts_decay_linear` trong biểu thức khác platform decay; cùng dùng cả hai có thể làm tín hiệu trễ nhiều hơn dự kiến.

### Bước 2. Viết giả thuyết có thể bị bác bỏ

Mẫu một câu: “Vì [cơ chế], cổ phiếu có [đặc tính đo được] tại thời điểm thông tin khả dụng sẽ có [hướng lợi nhuận] trong [horizon], đặc biệt trong [điều kiện], sau khi kiểm soát [rủi ro].”

Ví dụ nghiên cứu, chưa kiểm định: “Thay đổi khoản thuế đầu tư có thông tin dự báo khác phần biến động giá trong tỷ số thuế/giá; nếu đúng, thành phần thay đổi kế toán phải còn giá trị sau khi loại proxy đảo chiều giá.”

Ghi trước kết quả nào khiến bạn bỏ giả thuyết. Nếu tín hiệu biến mất khi bỏ price denominator, câu chuyện sự kiện kế toán phải được xem lại, dù biểu thức gốc còn có thể có giá trị như tín hiệu giá.

### Bước 3. Chọn field, không chọn theo Sharpe cao nhất đơn thuần

Đọc profile, đơn vị, coverage, tần suất, concentration và sub-universe; sau đó tra pattern/dead zone mới hơn. Ưu tiên cơ chế khác với book của chính bạn, không chỉ dataset khác tên.

[Các redundancy clusters](opportunities/factor-themes-redundancy.md) giúp giảm trùng lặp, nhưng hai field khác cluster không được bảo đảm độc lập. Cluster lịch sử không đại diện cho tương quan hiện tại hay quan hệ nhân quả.

Không đưa field mang mã định danh/tiền tệ vào alpha chỉ vì screen có Sharpe cao. Chúng có thể đang proxy quốc gia, dữ liệu thiếu hoặc cách nhà cung cấp mã hóa.

### Bước 4. Tạo họ biểu thức nhỏ, có đối chứng

Mỗi giả thuyết bắt đầu bằng 2-4 biến thể có chủ đích: mức, thay đổi có dấu, magnitude hoặc một interaction có lý do. Không nhân toàn bộ field x window x decay x neutralization thành một lưới lớn.

Một tập ablation hữu ích với anchor A và thành phần B:

| Biến thể | Câu hỏi |
|---|---|
| A | Anchor có tín hiệu riêng không? |
| B | Thành phần phụ tự nó mạnh đến đâu? |
| A + B | Tổng có cải thiện ổn định không? |
| A * B hoặc tương tác centered-rank | Có quan hệ điều kiện vượt quá tổng không? |
| Blend đầy đủ bỏ A | Alpha có còn gần như nguyên vẹn khi bỏ ý tưởng mới? |

Giữ cùng thang đo khi so sánh. Không đọc hệ số `2 * rank(...)` như gấp đôi mức rủi ro thực tế sau pipeline dựng trọng số.

### Bước 5. Mô phỏng và sàng lọc lỗi cấu trúc trước

Trong BRAIN: xác nhận field/operator được cấp quyền, nhập expression, lưu settings, chạy simulation, lưu alpha ID và toàn bộ kết quả. Những biểu thức mẫu trong tài liệu chưa được parser hoặc simulator BRAIN hiện tại xác nhận.

Thứ tự sàng lọc nên là: dữ liệu/đơn vị hợp lệ -> độ phủ và concentration -> turnover/fitness -> Sharpe và drawdown -> sub-universe và độ ổn định -> correlation checks. Có thể chạy check sớm nếu muốn loại nhanh, nhưng không gọi một alpha là đạt chuẩn khi còn điều kiện chưa hoàn tất.

### Bước 6. Chẩn đoán đúng lỗi, chỉ sửa lỗi có cơ chế

| Triệu chứng | Kiểm tra đầu tiên | Hành động có thể hợp lý |
|---|---|---|
| Sharpe cao, concentration fail | Số cổ phiếu active, NaN, số giá trị phân biệt | Sửa dữ liệu hoặc loại field quá thưa; không chỉ rank thêm lần nữa |
| Sharpe tốt, fitness thấp | Return scale và turnover | Smoothing nhỏ nếu phù hợp tuổi thọ tín hiệu; không tối ưu decay vô hạn |
| Sub-universe yếu | Tín hiệu nằm ở nhóm thanh khoản/quy mô nào? | Thử universe phù hợp hoặc xem lại rủi ro; gate chỉ khi có giả thuyết |
| Self-corr cao | Thành phần chung nào mang nhiều PnL? | Bỏ/giảm thành phần đó trước khi thay anchor tiếp |
| Chỉ một năm tốt | Độ nhạy regime và sự kiện bất thường | Kiểm định khác giai đoạn hoặc dừng |
| Gate giảm turnover bất thường | Có đang giữ vị thế quá lâu/không thoát không? | Kiểm tra semantics, tuổi vị thế và coverage thực tế |

### Bước 7. Kiểm định độ bền trước khi chọn người thắng

- Xem kết quả theo năm, rolling window, drawdown, tail loss và nhóm thanh khoản/ngành.
- Kiểm tra vài tham số lân cận đã định trước; ưu tiên vùng hiệu quả ổn định hơn một điểm cực đại.
- Dùng phần dữ liệu nghiên cứu và phần xác nhận theo thời gian nếu nền tảng/quy trình cho phép; tránh chia ngẫu nhiên chuỗi thời gian. Nếu nhãn/horizon chồng lấn, cần khoảng cách phù hợp giữa các phần.
- Một giai đoạn đã được dùng để chọn công thức hoặc đã xem nhiều lần không còn là holdout sạch. Khi không có ngoài mẫu sạch, phải ghi giới hạn đó và tiếp tục forward/paper monitoring.
- Ghi tổng số phép thử, kể cả thất bại. Với quy mô nghiên cứu lớn, cân nhắc điều chỉnh multiple testing/deflated Sharpe nếu có đủ thông tin; không tự gán mức ý nghĩa từ Sharpe quan sát.
- Không coi lợi nhuận mô phỏng là lợi nhuận sau spread, market impact, borrow và chi phí thực thi nếu chưa mô hình hóa chúng.

### Bước 8. Đánh giá đóng góp cho book và quyết định

Chỉ với những ứng viên còn hợp lý, đối chiếu signal/PnL với các alpha đã submit trong tài khoản, rồi lấy check hiện tại trên BRAIN. Chấp nhận việc một công thức có ích cho book mới nhưng không còn ích cho book bão hòa, hoặc ngược lại.

[Quy tắc ưu tiên lịch sử](rules/submission-priority-long-term.md) đề xuất chọn alpha chất lượng cao và self-corr thấp trước. Đây là heuristic có lý, không phải chứng minh tối ưu điểm số; độ tương quan với một tập alpha hiện tại không đo hết ảnh hưởng lên các ứng viên tương lai.

## 8. Năm hướng nghiên cứu tiếp theo

**Tất cả hướng dưới đây là đề xuất chưa backtest trong phiên này.** “Mới” ở đây là hướng phát triển cho nghiên cứu của bạn, không khẳng định chưa ai trên BRAIN từng dùng hoặc mọi cấu trúc đều chưa có trong 1.669 hồ sơ. Trước khi chạy cần tìm biểu thức/biến thể tương đương trong nhật ký của bạn.

### 8.1. Ưu tiên 1: tách sự kiện kế toán khỏi biến động mẫu số giá

**Cơ sở:** kho dùng nhiều `abs(ts_delta(F / close, d))`. Ngay cả khi F không cập nhật, giá thay đổi vẫn tạo tín hiệu “sự kiện”. Phân rã chính xác, với P là close:

$$
\frac{F_t}{P_t}-\frac{F_{t-d}}{P_{t-d}}
=\frac{F_t-F_{t-d}}{P_t}
+F_{t-d}\left(\frac{1}{P_t}-\frac{1}{P_{t-d}}\right).
$$

Với `F = fnd6_itci`, chạy các biểu thức riêng, giữ nguyên cấu hình:

```text
rank(abs(ts_delta(fnd6_itci / close, 3)))
```

```text
rank(abs(ts_delta(fnd6_itci, 3) / close))
```

```text
rank(abs(ts_delay(fnd6_itci, 3) * (1 / close - 1 / ts_delay(close, 3))))
```

Đẳng thức đúng trước `abs`/`rank`; hai thành phần sau biến đổi phi tuyến không cộng lại thành alpha gốc.

**Kiểm tra rẻ nhất:** so thứ hạng, tỷ lệ active và PnL của ba tín hiệu. Nếu thành phần mẫu số gần như tái tạo alpha gốc còn thành phần kế toán yếu, đổi cách giải thích thành price-driven, không gọi là underreaction với tin kế toán. Nếu còn giá trị kế toán, thử hướng tăng/giảm và sự kiện mới với timestamp hợp lệ.

**Điều kiện dừng:** coverage quá thấp, chỉ thắng nhờ chung stabilizer, hoặc kết quả ngoài giai đoạn chọn mẫu không bền. Không vội thêm leverage để “cứu” một anchor chưa có bằng chứng riêng.

### 8.2. Ưu tiên 2: kiểm tra tương tác thực bằng centered ranks

**Giả thuyết:** quan hệ điều kiện giữa hai nguồn thông tin có giá trị vượt quá tổng các main effects; tích rank dương trong pattern cũ có thể đang hưởng lợi từ main effects thay vì interaction thật.

```text
ts_decay_linear(
	(rank(fnd6_ivaco / close) - 0.5)
	* (rank(open / close - 1) - 0.5),
	5
)
```

So với A, B và A+B; không so duy nhất với một baseline yếu. Centered product cho cùng dấu điểm dương và trái dấu điểm âm; cả nhóm cùng thấp cũng có thể nhận điểm dương. Vì vậy chỉ dùng nếu giả thuyết thực sự phù hợp với cấu trúc này. Nếu chỉ muốn nhóm cùng cao, product không âm hoặc điều kiện khác có thể hợp lý hơn.

**Kiểm tra bác bỏ:** interaction không cải thiện độ bền/đóng góp sau khi đã xét A và B riêng, hoặc làm concentration/turnover xấu đi. Tránh thêm đồng thời cả analyst flag chưa rõ mã hóa.

### 8.3. Ưu tiên 3: thay “revision flag” bằng thay đổi kỳ vọng đo được

**Giả thuyết:** thay đổi EPS dự báo liên tục có thể có thông tin khi được điều chỉnh theo kỳ dự báo và mức tin cậy, thay vì cộng mã forecast type.

Baseline có chủ đích để chẩn đoán, không phải công thức hứa hẹn sẵn:

```text
ts_decay_linear(rank(ts_delta(anl4_afv4_eps_mean, 22) / close), 5)
```

[Hồ sơ EPS mean](factor_profiles/anl4_afv4_eps_mean.md) cho thấy biến đổi đơn giản trước đó yếu, còn delta 5 ngày có turnover cao. Điểm mới cần kiểm định là thay đổi kỳ vọng **cùng fiscal period**, không phải chỉ kéo cửa sổ từ 5 lên 22. Nếu field chuyển kỳ dự báo hàng năm và không thể kiểm soát rollover, chưa đủ dữ liệu để kết luận về earnings revisions.

Khi có metadata phù hợp, phân biệt thay đổi consensus do analyst cập nhật với thay đổi do số analyst/thành phần mẫu. Có thể kiểm tra interaction với coverage count, nhưng [sales count](factor_profiles/sales_estimate_count_quarterly.md) đo độ phủ doanh thu, không tự động là độ tin cậy của EPS; cần số analyst khớp chỉ tiêu và kỳ dự báo nếu có.

**Điều kiện dừng:** không tách được rollover, đổi đơn vị hoặc thay thành phần analyst; không có cải thiện ngoài các phép biến đổi mức đã thử. Không gọi mọi delta của consensus là surprise.

### 8.4. Ưu tiên 4: phân biệt overnight information với intraday reversal

**Giả thuyết:** thành phần `open / close - 1` trong blend đang khai thác đảo chiều trong ngày trước, không phải thông tin tích lũy ngoài giờ giao dịch.

Hai baseline riêng để so sánh, không ghép ngay với fundamentals:

```text
ts_decay_linear(rank(open / close - 1), 5)
```

```text
ts_decay_linear(rank(open / ts_delay(close, 1) - 1), 5)
```

Thử cả hai hướng nếu chưa biết chiều, ghi trước rằng mục đích là phân loại cơ chế. Dùng giá đã điều chỉnh nhất quán và cùng Delay 1; nếu sau này nghiên cứu giao dịch tại open với Delay 0 thì phải thiết kế lại tính khả dụng của thông tin, không lấy kết quả này để suy ra.

**Kiểm tra bác bỏ:** hai baseline không có thông tin riêng hoặc hiệu quả biến mất sau chi phí. Nếu một baseline mạnh, chỉ ghép với anchor sau khi kiểm tra tương quan với reversal/buzz hiện có. Đây là thí nghiệm kiểm toán cơ chế, không tuyên bố phát hiện một family giá-volume mới.

### 8.5. Ưu tiên 5: tìm phần đóng góp còn lại sau bộ stabilizer

**Giả thuyết:** một anchor ít được dùng có thể đóng góp độc lập sau khi loại ảnh hưởng của leverage, ivaco, drlt và buzz-reversal.

Bắt đầu từ hai anchor có ngữ nghĩa rõ: [cld2](factor_profiles/fnd6_cld2.md) là Capitalized Leases - Due in 2nd Year; [fopo](factor_profiles/fnd6_fopo.md) là Funds from Operations - Other. Không nhầm “cluster nhỏ” với “alpha chưa từng submit”: kết hợp hai field này đã có đại diện trong pattern lịch sử.

Cách kiểm tra: anchor đơn -> stabilizer đơn -> blend -> blend bỏ anchor -> blend bỏ từng stabilizer. Đánh giá phần cải thiện ngoài mẫu, tương quan trọng số và PnL, không chỉ chênh lệch headline fitness.

Nếu có công cụ local và dữ liệu được phép dùng, có thể kiểm tra phần dư của signal/PnL sau hồi quy trên các thành phần chung. Hệ số chỉ được ước lượng từ dữ liệu quá khứ và đánh giá trên phần sau đó. Không residualize trên toàn mẫu rồi báo kết quả cùng mẫu như alpha mới. Chỉ triển khai vào Fast Expression khi operator thực sự được hỗ trợ và semantics khớp.

**Điều kiện dừng:** bỏ anchor gần như không làm thay đổi chất lượng, hoặc phần dư không còn tín hiệu. Khi đó có thể ghi nhận anchor không mang giá trị biên trong cấu hình này, thay vì tiếp tục cộng thành phần cho tới khi qua gate.

## 9. Gợi ý phiên đầu với ngân sách tối đa 24 mô phỏng

Không cần dùng hết ngân sách. Bảng này ưu tiên học cơ chế, không phải tối đa hóa số lần thử:

| Nhóm | Số lượt tối đa | Nội dung |
|---|---|---|
| Phân rã event-magnitude | 8 | Ba biến thể mục 8.1 và raw signed accounting change; mỗi loại thử hai hướng nếu chưa biết chiều |
| Tương tác | 4 | A, B, A+B và centered product của mục 8.2 |
| Overnight vs intraday | 4 | Hai baseline mục 8.4, mỗi loại hai hướng |
| Sửa một lỗi có chẩn đoán | 4 | Chỉ dùng cho giả thuyết còn sống; ví dụ ablation hoặc ít tham số lân cận |
| Xác nhận | 4 | Chạy đúng cấu hình đã chọn trên phần xác nhận/chế độ dữ liệu nền tảng cho phép; không chọn lại công thức từ kết quả này |

Nếu đã có baseline đúng settings, tái sử dụng kết quả thay vì chạy trùng. Các API checks không tính là mô phỏng mới trong bảng; giới hạn quota thực tế tùy tài khoản. Nếu không thể dành phần xác nhận độc lập trên BRAIN, ghi rõ và thay bằng theo dõi forward, không gọi một lần re-run cùng dữ liệu là ngoài mẫu.

Với phiên có 16 lượt khám phá đầu tiên, 8 lượt phân rã đầu tiên chủ yếu là kiểm toán, không tự động tính là cấu trúc mới so với toàn kho. Nếu áp dụng quy tắc lịch sử “ít nhất 50% novelty”, phải rà cây toán tử trước và thay các lượt trùng bằng giả thuyết chưa thử. Không vì chạy đủ 24 lượt mà xem như đã thỏa novelty.

**Quy tắc dừng:** bỏ nhánh khi lỗi cấu trúc không có cách sửa hợp lý; không đuổi theo một điểm Sharpe cực đại; khi mục tiêu là tìm một ứng viên, dừng sau khi ứng viên vượt đủ điều kiện chất lượng, độ bền và check hiện tại. Chưa có PASS thì chỉ gọi là candidate.

## 10. Checklist đánh giá và submit

### 10.1. Chỉ số phải hiểu đúng

Công thức fitness được tài liệu dự án sử dụng:

$$
\mathrm{Fitness}=\mathrm{Sharpe}\sqrt{\frac{|\mathrm{Returns}|}{\max(\mathrm{Turnover},0.125)}}.
$$

Returns/turnover phải dùng đúng định nghĩa và đơn vị của nền tảng. Không đưa 10 thay cho 0.10. Trong công thức này, khi turnover thấp hơn 12.5%, giảm thêm turnover không tự tăng fitness nếu các thành phần khác giữ nguyên; nó vẫn có thể hữu ích về chi phí hoặc độ ổn định. Fitness không phải lợi nhuận tiền mặt hay kiểm định thống kê.

Các ngưỡng Sharpe, fitness, turnover, sub-universe, concentration và correlation phụ thuộc loại alpha, settings, chương trình và chính sách hiện tại. Tài liệu này không xác nhận mọi ngưỡng BRAIN tại ngày 2026-11-18. Dùng limit/result hiển thị cho đúng alpha của bạn; không mặc định mọi check trong kho đều còn giống hiện tại.

### 10.2. Checklist bắt buộc trước khi gọi là đủ điều kiện

- [ ] Mô tả đúng ý nghĩa, đơn vị, kiểu dữ liệu và thời điểm khả dụng của từng field.
- [ ] Không có look-ahead; điều chỉnh giá và fiscal period nhất quán.
- [ ] Expression/settings/alpha ID được lưu đầy đủ; biết chính xác ngày và mẫu dữ liệu đã dùng.
- [ ] Coverage và số lượng vị thế hợp lý; concentration không chỉ tốt ở headline mà còn ổn định theo thời gian.
- [ ] Sharpe, fitness, turnover, drawdown và sub-universe đạt các yêu cầu áp dụng.
- [ ] Đã kiểm tra main effects/ablation; anchor mới có đóng góp thật.
- [ ] Không phụ thuộc một năm, một vài mã hoặc một điểm tham số duy nhất.
- [ ] Đã ghi giới hạn ngoài mẫu, số phép thử và rủi ro chi phí/thực thi.
- [ ] Đã đo tương quan với book hiện tại, không dùng book hoặc self-corr cũ để quyết định.
- [ ] Mọi check nền tảng bắt buộc đã trả về kết quả cuối cùng chấp nhận được, kể cả production correlation nếu áp dụng.
- [ ] Không còn PENDING/timeout bị hiểu nhầm thành PASS; đã xem mọi cảnh báo bổ sung.
- [ ] Đã đọc điều khoản và quyền dữ liệu/operator của tài khoản; submit là một quyết định riêng, không suy ra từ một bảng screen.

### 10.3. Khi có nhiều ứng viên

Ưu tiên ứng viên có cơ chế rõ, ổn định, đạt toàn bộ checks và thêm đóng góp khác biệt. Khi chất lượng tương đương, self-corr thấp hơn thường đáng ưu tiên để giữ lựa chọn cho các alpha sau. Không gán một công thức điểm tùy ý cho trade-off này nếu chưa kiểm định.

EXCELLENT/SPECTACULAR, các nhãn HIGH LONG-TERM VALUE và tỷ lệ Sharpe premium 1.10x là cách phân loại/quan sát trong kho. Không sử dụng chúng như chứng nhận hiệu quả đầu tư hoặc bảo đảm submit trong tài khoản hiện tại.

## 11. Ghi chép để tích lũy tri thức thay vì tích lũy công thức

Mỗi thí nghiệm nên có các trường sau, có thể ghi trong hệ thống nhật ký hiện có:

```yaml
hypothesis_id: H01
evidence_level: untested
mechanism: accounting update versus price-denominator effect
field_semantics_verified: false
expression: "rank(abs(ts_delta(fnd6_itci, 3) / close))"
settings_snapshot: null
sample_and_information_timing: null
alpha_id: null
baseline_ids: []
number_of_trials_in_family: 0
metrics: null
coverage_and_concentration: null
sub_universe_result: null
local_correlation_period_and_overlap: null
official_check_results: null
out_of_sample_status: not_tested
ablation_conclusion: null
decision: pending
next_discriminating_test: compare against price-only component
```

Đây là schema minh họa, không phải file cấu hình có thể chạy với pipeline cũ. `settings_snapshot` cần chứa đầy đủ các mục ở bước 1; không điền giá trị giả để làm bản ghi trông hoàn tất.

Sau mỗi phiên, cập nhật tri thức theo đúng loại:

- **Pattern:** hiệu quả trong điều kiện nào, bao nhiêu mẫu và phản ví dụ là gì.
- **Dead zone:** biến thể đã thử, lý do thất bại, phạm vi kết luận và điều kiện mở lại.
- **Rule:** chỉ nâng thành ràng buộc rộng khi có bằng chứng đủ và không có phản ví dụ chưa giải thích.
- **Opportunity:** giả thuyết còn mở, kiểm tra rẻ nhất và trạng thái chưa thử/đang thử/đã đóng.
- **Profile:** kết quả đúng cấu hình của field, không ghi “untested” nếu đã có thí nghiệm sau đó.

**Kết luận hành động:** bắt đầu bằng kiểm toán phép đo và tái lập một baseline; phát triển ít giả thuyết có đối chứng; chỉ thêm thành phần khi chứng minh được vai trò; kiểm tra ngoài mẫu và tương quan trước khi coi một công thức là alpha mới có ích. Tài liệu này chưa thực hiện mô phỏng hoặc submit alpha nào trên BRAIN.
