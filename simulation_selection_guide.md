# Danh sách công thức và cách chọn mô phỏng

Ngày lập: 2026-11-25. CSV: [simulation_candidates.csv](simulation_candidates.csv).

## 1. Phạm vi và giới hạn

CSV có 120 mục: toàn bộ 57 expression trong [danh mục alpha](../knowledge/alpha.md), 40 pair blend trong [factor merge](../knowledge/opportunities/factor-merge-candidates.md), 20 starter blend trong [theme blend](../knowledge/opportunities/theme-blend-candidates.md), và 3 biến thể bổ sung có biểu thức/settings cụ thể trong book. R13/R14 cũng được bổ sung số liệu từ đúng expression trong book.

Trong đó 4 mục là SKIP để lưu cảnh báo, không phải công thức khuyến nghị chạy nguyên trạng. 116 mục còn lại gồm cả đối chứng, giả thuyết và thử nghiệm có điều kiện; không phải 116 alpha mạnh hoặc 116 công thức cần chạy hết.

Không thể liệt kê hữu hạn "tất cả công thức có thể" khi cho phép tùy ý tổ hợp field, toán tử, cửa sổ và trọng số. Đây là menu có nguồn cụ thể đã đối chiếu, không phải xuất toàn bộ từng thí nghiệm trong sessions hoặc từng biến đổi trong 1.669 factor profiles. Không xuất hàng loạt batch lịch sử, pseudo-code rút gọn trong book hoặc 15 triple chỉ có tên thành phần nhưng chưa xác định đầy đủ phép biến đổi. Không lấy mã tiền tệ làm tín hiệu định lượng chỉ vì có Sharpe screen đẹp.

**Không bảo đảm Sharpe/fitness tối đa hoặc đạt chuẩn hiện tại.** Chưa chạy mô phỏng BRAIN trong phiên này. Mọi S/F/correlation trong CSV là lịch sử của nguồn, không phải kỳ vọng hoặc kết quả mới. Kho có selection bias do đã thử nhiều công thức; chạy lại cùng mẫu không phải kiểm định ngoài mẫu.

## 2. Đọc CSV và cấu hình

- `priority`: 1 chạy đại diện trước; 2 mở rộng có chọn lọc; 3 nghiên cứu/đối chứng; 4 thấp hoặc chỉ để chẩn đoán; 5 loại nguyên trạng.
- `run_policy`: RETEST là tái lập; RESEARCH là giả thuyết; CONDITIONAL cần đáp ứng cảnh báo; CONTROL chỉ để trả lời câu hỏi kiểm định; SKIP không chạy nguyên trạng.
- `evidence`: phân biệt expression lịch sử, template, đối chứng mới và PnL/theme screen. Nhãn template không chứng minh đúng expression đã có kết quả.
- `historical_sharpe`, `historical_fitness`, `historical_self_corr`: chỉ điền khi có bằng chứng cho đúng expression. Ô trống là chưa có số liệu đủ chắc, không phải 0.
- `source`, `notes`: nguồn và điều kiện cần đọc trước khi dùng.
- Mỗi dòng có settings riêng, không phải payload API hoàn chỉnh hoặc định dạng import mặc định của BRAIN. Nếu tự động hóa, ánh xạ các cột settings vào payload hiện tại của tài khoản và expression vào phần regular.

Cấu hình nghiên cứu chung: EQUITY, USA, TOP3000, Delay 1, truncation 0.08, pasteurization ON, unitHandling VERIFY, nanHandling OFF, FASTEXPR, visualization false. Neutralization/decay có ở từng dòng:

| Nhóm | Neutralization | Platform Decay |
|---|---|---:|
| Phần lớn R/N/D/B/P/T | SUBINDUSTRY | 6 |
| R06: IV smoothed zscore | MARKET | 10 |
| R17: event không leverage | MARKET | 6 |
| B03: PPE + profit flag + ITCI + intraday | SUBINDUSTRY | 8 |

Các nguồn không luôn lưu đủ settings lịch sử. Những tùy chọn không được nguồn xác nhận là mặc định nghiên cứu đề xuất, không phải tuyên bố tái lập tuyệt đối. Đặc biệt toàn bộ settings P/T là đề xuất: screen PnL/theme không có mô phỏng của expression blend. Không chuyển nguyên kết quả screen sang cột S/F.

`ts_decay_linear(..., 5)` trong expression và `decay=6` của nền tảng là hai lớp smoothing khác nhau; không bỏ một lớp khi tái lập. Không tắt VERIFY để che lỗi đơn vị; kiểm tra field, MATRIX/VECTOR và quyền operator trước khi chạy. Nếu field không hợp lệ trên tài khoản, dừng dòng đó thay vì tự thay field và giữ số liệu lịch sử.

## 3. Những công thức đáng chạy trước

| CSV ID | S lịch sử | F lịch sử | Lý do chọn | Điều kiện quan trọng |
|---|---:|---:|---|---|
| R13 | 3.02 | 3.48 | Blend acdo + intraday + ptpr + ITCI có fitness rất cao | PENDING; corr 0.6318 đã STALE sau khi sibling ACTIVE |
| R14 | 2.95 | 3.44 | Biến thể netdebt cùng họ có lịch sử ACTIVE | Corr 0.7819; đã cần premium escape; chọn đại diện với R13 |
| B03 | 2.84 | 3.21 | PPE + profit flag + ITCI + intraday | Corr 0.7943; biên premium lịch sử chỉ +0.002 Sharpe; decay 8 |
| B01 | 2.97 | 2.92 | Event ITCI + leverage + buzz có smoothing giảm turnover | Corr 0.7163; họ leverage/buzz dễ bão hòa |
| R04 | 2.64 | 2.77 | Event ITCI + leverage + drlt; baseline mạnh | Corr lịch sử 0.549 không bảo đảm book hiện tại |
| R19 | 2.63 | 2.68 | Tax event TXW + stabilizers + reversal | Họ full leverage stack bão hòa; chỉ ưu tiên nếu book thưa |
| R08 | 2.29 | 2.26 | Hai anchor và bỏ leverage/drlt/flag; lịch sử PASS 0.6181 | Đo đóng góp anchor với N23 và N24; đã có trong book gốc |
| R06 | 1.82 | 2.35 | IV call-put 270 smoothed zscore, khác nhánh fundamental | MARKET/decay 10; kiểm tra coverage và saturation IV |
| R17 | 2.10 | 2.02 | Event không leverage, MARKET; thử nhánh decorrelation | Corr discovery 0.528 chỉ là local; phải đợi check chính thức |

B02 có S=3.08 nhưng F=2.53 và turnover 27.9%, trong khi B01 có F=2.92 và turnover 18.3%. Vì vậy không ưu tiên B02 chỉ vì Sharpe cao hơn; nguồn đã đánh dấu B02 SUPERSEDED.

Nếu book còn ít alpha: bắt đầu R13, R04, R08 và R06; R13 cần xác minh flag. Sau đó thử B01 hoặc R14/B03 nếu còn khoảng trống correlation, không submit tất cả sibling cùng lúc.

Nếu book đã chứa nhiều event/leverage/value/analyst: ưu tiên đo đóng góp R08, thử R17 hoặc một nhánh IV còn trống, và một vài interaction có cơ chế. Không tiếp tục thêm full leverage stack chỉ để nâng S/F. P/T là hướng nghiên cứu sau đó, không phải nhóm có S/F xác nhận cao.

## 4. Loại công thức nên mô phỏng

### A. Tín hiệu khớp loại dữ liệu

Event magnitude chỉ dùng cho field có lịch sử hỗ trợ và cập nhật có ý nghĩa. ITCI là Investment Tax Credit, không mặc định là tồn kho. So N01/N03/N05 để biết tín hiệu đến từ cập nhật kế toán hay biến động giá mẫu số. So N07 với magnitude để kiểm tra việc xóa dấu có hợp lý.

Analyst accumulation có thể dùng `zscore(ts_sum(flag, 22))` nếu đã hiểu mã flag. Nếu đó là forecast-type code hoặc trạng thái lặp lại, tổng mã không phải số revision độc lập. Forecast liên tục như N14 cần giữ cùng fiscal period, thời điểm công bố và xử lý rollover.

IV spread có smoothing và coverage đủ rộng đáng làm baseline khác cơ chế. Không xem đổi tenor là độc lập. Buzz phải phân biệt attention level với attention nhân reversal.

### B. Blend có đóng góp biên và cơ chế khác nhau

Ghép anchor chậm với thông tin giá/attention có thể cải thiện chất lượng, nhưng cần kiểm tra baseline từng chân. Ưu tiên các raw field ít trùng với book, khác exposure/thời điểm, không chỉ tên field khác.

Hai anchor + bỏ leverage trong R08 là mẫu có bằng chứng. So R08, N23, N24 trước; chỉ mở N25-N28 khi cần chẩn đoán. Nếu N24 đã tái tạo gần hết PnL của R08 thì không gọi hai anchor là nguồn alpha mới đáng kể.

Interaction cộng/nhân có thể thử theo nhóm N09/N10/N11/N12/N17; so concentration và turnover. Centered product có cả trường hợp hai chân cùng thấp cho kết quả dương, không đồng nghĩa chỉ chọn hai chân cùng cao.

### C. Sửa một lỗi đã chẩn đoán

Volatility gate R15 chỉ nên thử kèm D02 để đo tác động thật lên sub-universe, tuổi vị thế và turnover. `trade_when` giữ trạng thái, không giống nhân một điều kiện boolean với signal.

Sales-count densifier R16 cần D03/D04/D06: số analyst có thể đang thêm size/liquidity exposure. Không chia số đếm này cho giá như earnings yield.

## 5. Loại không nên mô phỏng nguyên trạng

| Loại | Vì sao loại/giảm ưu tiên | Chỉ mở lại khi |
|---|---|---|
| T02/T03/T06: lãi suất chia giá; T14: số analyst chia giá | Không có ngữ nghĩa kinh tế được thiết kế cho tỷ số | Xây giả thuyết và phép chuẩn hóa hợp lý; ghi thành expression mới |
| Rank mã tiền tệ hoặc mã phân loại chưa hiểu | Chênh lệch số mã không đại diện lợi nhuận kinh tế | Hiểu và xử lý đúng categorical data; không dùng tổng mã tùy ý |
| `ts_zscore` fundamental2 thưa | Có trường hợp S=4.10/F=10.75 nhưng concentration 0.50 trượt limit 0.10 | Chứng minh coverage và concentration được sửa trước tối ưu S/F |
| Full stack leverage + ivaco + drlt + flag + buzz | Các ghi chép sau cho thấy correlation có thể khoảng 0.77-0.93 | Book còn trống hoặc ablation cho thấy đóng góp riêng và check mới PASS |
| Chỉ đổi flag, tenor, cửa sổ, decay hoặc đảo dấu để gọi là alpha mới | Expression khác nhưng thông tin/PnL có thể trùng | Có kiểm định đóng góp mới; đổi dấu dùng như đối chứng |
| Fundamental chậm nhân dấu momentum giá/volume | Nhiều thử nghiệm S âm và turnover khoảng 31-61% | Thay cơ chế/tần suất với đối chứng chi phí rõ ràng |
| Delta/std fundamental thưa; correlation/gating tùy ý | Có template đã thất bại; mẫu số nhỏ/NaN có thể làm tín hiệu bất ổn | Dữ liệu dày hoặc surprise có cơ sở và mẫu số an toàn |
| Tỷ số giữa field kế toán tùy ý | Không có cơ chế, có thể chỉ thêm scale hoặc lỗi đơn vị | Tỷ số có ý nghĩa kế toán và mẫu số hợp lệ |
| Standalone news12, option9, model16 hoặc RD-tax connector đã vào dead zone | Bằng chứng âm và nguy cơ saturation | Blend có cơ chế khác đúng điều kiện thất bại; thử một đại diện trước |
| Backfill dài, NaN->0 hoặc tắt unit verify để làm đẹp chỉ số | Tạo dữ liệu giả/giữ dữ liệu quá cũ hoặc che sai đơn vị | Có chẩn đoán missingness và chính sách dữ liệu minh bạch |
| Công thức chỉ đẹp tổng thể nhưng trượt concentration/sub-universe/correlation | Không đáp ứng toàn bộ bài toán submit | Sửa đúng lỗi và chạy lại check chính thức |

Dead zone không có nghĩa mọi công thức trong dataset bất khả thi. Các mục P/T liên quan được giữ ở priority 4 để nghiên cứu có điều kiện, không nên chạy hàng loạt chỉ vì screen gợi ý diversification tốt.

## 6. Tối ưu S/F với ngân sách hữu hạn

1. Chạy đại diện của 4-6 họ với config đã ghi, cùng khoảng dữ liệu. Không chọn đồng thời nhiều sibling trước khi biết correlation.
2. Với nhánh còn sống, chạy đối chứng tương ứng để xác định tín hiệu hữu ích và lỗi chính. Dành tối thiểu khoảng nửa ngân sách nghiên cứu cho cơ chế/cấu trúc mới theo kinh nghiệm novelty của kho; cặp đảo dấu và ablation không tự được tính là novelty.
3. Sau đó chỉ thay một tham số mỗi lần: platform decay 6->8 hoặc 10 nếu turnover là vấn đề; buzz 10->5 hoặc 20 trong họ R08; truncation 0.08->0.05 nếu cần kiểm soát tập trung. Đây là thí nghiệm mới, chưa có S/F và không có trong 120 dòng baseline.
4. Giữ các tham số không thử cố định. Không full-grid field x sign x window x weight x universe để chọn đúng một đỉnh in-sample. Đổi neutralization/universe là đổi bài toán, cần kết quả riêng.
5. Chọn theo S/F đồng thời với turnover, drawdown, coverage, concentration, sub-universe, chi phí và contribution/correlation, không chỉ sắp giảm dần Sharpe.
6. Xác nhận trên phần thời gian chưa dùng để chọn tham số nếu hỗ trợ; nếu không có holdout sạch, ghi rõ và theo dõi forward. Ưu tiên vùng tham số ổn định hơn một cực đại nhọn.
7. Dừng nhánh khi sai field semantics, thiếu coverage chưa sửa được, performance phụ thuộc một giai đoạn, hoặc anchor không đem đóng góp biên. Không cứu mọi nhánh bằng cùng ivaco/leverage/buzz.

Mục tiêu sàng lọc nghiên cứu: S>=2 và F>=2 nếu có thể, nhưng không loại một nguồn độc lập có S thấp hơn mà đóng góp danh mục tốt. Các ngưỡng lịch sử của [platform constraints](platform_constraints.md) gồm S>=1.25, F>=1, turnover 1%-70%, concentration<=10% và self-corr khoảng 0.70 với premium exception. Phải xác nhận quy định hiện tại; đây không phải chứng nhận submission hiện hành. Local corr/PENDING/timeout không phải PASS; production correlation cần kiểm tra riêng nếu tài khoản yêu cầu.

Mỗi mô phỏng cần lưu expression, settings thực tế, alpha ID, khoảng thời gian, S/F/T, drawdown, số vị thế, coverage, concentration, sub-universe và mọi check chính thức. Không ghi kết quả mới đè lên cột historical.

## 7. Kiểm tra tệp

CSV đã được tạo trong workspace và editor không báo lỗi. Công cụ workspace đọc được nội dung. Lệnh Python trực tiếp đã được người dùng bỏ qua, không chạy lại. Hai lần kiểm tra chỉ đọc bằng PowerShell trả về 0 bản ghi dù công cụ workspace đọc được tệp; nguyên nhân chưa xác định. Do đó chưa xác nhận được round-trip CSV bằng runtime, hay cú pháp/operator/field validity trên BRAIN. Không coi đây là kiểm tra mô phỏng thành công.
