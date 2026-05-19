---
name: transcript-to-script
description: >
  Chuyển đổi transcript YouTube (hoặc bất kỳ transcript thô nào) thành 2 file:
  (1) Script bài giảng có cấu trúc sư phạm rõ ràng, và
  (2) TTS Script tối ưu cho các công cụ text-to-speech như ElevenLabs, Murf, FPT AI Voice.
  Kích hoạt skill này bất cứ khi nào người dùng đề cập đến: transcript, chuyển đổi transcript,
  tái tạo bài giảng, viết script từ video, làm nội dung từ transcript, tạo TTS script,
  hoặc muốn chuyển nội dung nói thành văn bản có cấu trúc để quay lại video.
---

# Transcript → Script + TTS Script

Skill này thực hiện pipeline 3 bước để biến transcript thô thành 2 file output chất lượng cao.

---

## Tổng quan pipeline

```
[Transcript thô]
      ↓  Bước 1: Làm sạch & phân tích cấu trúc
[Bản đồ nội dung]
      ↓  Bước 2: Viết Script bài giảng
[script.md]
      ↓  Bước 3: Chuyển đổi sang TTS Script
[tts_script.md]
```

---

## Bước 1 — Làm sạch & Phân tích cấu trúc

### 1a. Làm sạch transcript thô

Trước khi phân tích, xử lý các vấn đề sau:
- Xóa timestamp `[00:01:23]` hoặc `-->` markers
- Xóa filler words lặp lại vô nghĩa: "ừm", "thì là", "kiểu như", "bạn biết không"
- Sửa lỗi auto-caption: tên riêng, thuật ngữ chuyên ngành, số liệu
- Ghép các câu bị tách vụn thành đoạn hoàn chỉnh theo ý

### 1b. Dịch transcript sang tiếng Việt (nếu cần)

Nếu transcript gốc không phải tiếng Việt, dịch nó sang tiếng Việt trước khi phân tích. Dùng công cụ dịch chất lượng cao để giữ nguyên ý nghĩa và ngữ điệu. Giữ nguyên những thuật ngữ chuyên ngành hoặc tên riêng hoặc giữ nguyên tiếng gốc nếu không có cách dịch phù hợp.

### 1c. Phân tích và gắn nhãn cấu trúc

Xác định và gắn nhãn từng phần theo bảng sau:

| Nhãn | Ký hiệu | Mô tả |
|------|---------|-------|
| Hook/Mở đầu | `[HOOK]` | Câu chuyện, số liệu, câu hỏi gây chú ý |
| Định nghĩa | `[DEFINE]` | Giải thích khái niệm cốt lõi |
| Ví dụ | `[EXAMPLE]` | Minh họa thực tế |
| Nội dung chính | `[MAIN]` | Luận điểm, bước, framework |
| Lặp/Lạc đề | `[REMOVE]` | Đánh dấu để loại bỏ |
| Kết luận | `[CONCLUSION]` | Tóm tắt + hành động cụ thể |

### 1d. Tạo bản đồ nội dung

Xuất ra bảng tóm tắt với các cột:
- Phần | Tiêu đề ngắn | Ý chính (1-2 câu) | Vấn đề cần xử lý

**Ghi chú khi phân tích:** Luôn kiểm tra và ghi nhận:
- Có hook không? Nếu không → cần thêm
- Có phần nào lặp ý? → gộp hoặc xóa
- Nội dung chính có ví dụ minh họa không? → nếu thiếu, gợi ý thêm
- Kết luận có call-to-action cụ thể không? → nếu không, thêm vào

---

## Bước 2 — Viết Script bài giảng

### Nguyên tắc viết Script

Script là lời *đọc để quay*, không phải lời nói. Áp dụng các nguyên tắc sau:

**Về cấu trúc:**
- Mở đầu bằng hook mạnh: câu chuyện thực tế, số liệu bất ngờ, hoặc câu hỏi chạm vào nỗi đau
- Mỗi phần có tiêu đề rõ ràng và thời lượng ước tính
- Kết luận có thử thách/hành động cụ thể người xem làm được ngay

**Về nội dung:**
- Mỗi luận điểm phải có ít nhất 1 ví dụ minh họa cụ thể
- Dùng ngôn ngữ thứ 2 ("bạn") thay vì ngôi thứ 3 để tạo kết nối
- Câu ngắn, ý rõ — không quá 25 từ/câu
- Ưu tiên ví dụ từ đời thực, gần gũi với đối tượng mục tiêu

**Về định dạng file script.md:**
```markdown
# [Tên bài giảng]

## Metadata
- Tổng thời lượng ước tính: X phút
- Đối tượng: [mô tả]
- Mục tiêu học tập: [sau khi xem, người học có thể...]

---

## [PHẦN 1 — TÊN PHẦN] (~X giây/phút)

> [Nội dung script — viết như lời thoại, dùng > để phân biệt với ghi chú]

**[Ghi chú đạo diễn: hướng dẫn cho người quay/dựng — in đậm, dùng ngoặc vuông]**

---

## [PHẦN 2 — TÊN PHẦN] (~X giây/phút)
...
```

---

## Bước 3 — Chuyển đổi sang TTS Script

### Tại sao cần bước này

Script bài giảng được tối ưu cho mắt đọc. TTS Script được tối ưu để AI voice đọc tự nhiên. Hai thứ khác nhau ở:
- Ký hiệu định dạng làm TTS đọc sai hoặc bỏ qua
- Câu văn viết cần cấu trúc lại để TTS ngắt đúng chỗ
- Chỗ nhấn mạnh và ngắt nghỉ phải được "viết" vào văn bản

### Bảng quy tắc chuyển đổi

| Vấn đề | Trong Script | Trong TTS Script |
|--------|-------------|-----------------|
| Dấu ngắt nghỉ ngắn | `,` | `...` hoặc thêm câu mới |
| Dấu ngắt nghỉ dài | `.` | `.` + dòng trống |
| Nhấn mạnh từ | `**từ**` hoặc *từ* | Viết HOA từ đó, hoặc tách thành câu riêng |
| Câu hỏi tu từ | Câu hỏi thông thường | Tách thành 2 nhịp: phát vấn + dừng |
| Danh sách gạch đầu dòng | `- item` | Viết "Thứ nhất... Thứ hai... Thứ ba..." |
| Tiêu đề phần | `## Tên phần` | Xóa hoàn toàn hoặc viết thành câu dẫn |
| Emoji / ký hiệu đặc biệt | 🎬 `*` `—` | Xóa hết |
| Số liệu | 1000 | "một nghìn" (viết chữ nếu tool không tốt) |

### Kỹ thuật điều khiển nhịp đọc

```
Ngắt ngắn (0.3-0.5s):  Dùng dấu ...
Ngắt vừa (0.5-1s):     Xuống dòng mới
Ngắt dài (1-2s):        Dòng trống giữa 2 đoạn
Nhấn mạnh:              VIẾT HOA hoặc tách thành câu riêng ngắn
Dramatic pause:         Câu cực ngắn. Đứng một mình.
```

### Ví dụ chuyển đổi

**Script gốc:**
```
Nhiều người nghe "tư duy phản biện" và nghĩ ngay đến hình ảnh một người 
hay cãi. Không phải vậy. Tư duy phản biện là khả năng đánh giá thông tin 
một cách có hệ thống — trước khi bạn tin, trước khi bạn chia sẻ.
```

**TTS Script:**
```
Nhiều người nghe "tư duy phản biện"... và nghĩ ngay đến một người hay cãi.

Không. Phải. Vậy.

Tư duy phản biện là khả năng đánh giá thông tin... một cách CÓ HỆ THỐNG.

Trước khi bạn tin.
Trước khi bạn chia sẻ.
```

### Định dạng file tts_script.md

```markdown
# TTS Script — [Tên bài giảng]

## Hướng dẫn sử dụng
- Tool khuyến nghị: [ElevenLabs / Murf / FPT AI Voice / ...]
- Giọng đọc: [Nam/Nữ, phong cách]
- Tốc độ đọc: [0.9x / 1.0x / 1.1x]
- Ghi chú: Không thay đổi dấu câu — chúng điều khiển nhịp đọc

---

[Nội dung TTS — mỗi đoạn cách nhau bằng dòng trống]

[Không có tiêu đề, không có ký hiệu, không có markdown]
```

---

## Output cuối cùng

Sau khi hoàn tất, xuất ra 2 file:

### File 1: `script.md`
- Có đầy đủ metadata (thời lượng, đối tượng, mục tiêu)
- Có ghi chú đạo diễn cho từng phần
- Dùng để: người đọc script, làm slide, review nội dung

### File 2: `tts_script.md`
- Sạch hoàn toàn — chỉ có văn bản thuần
- Nhịp đọc được điều khiển bằng dấu câu và xuống dòng
- Dùng để: paste thẳng vào tool TTS

---

## Lưu ý quan trọng

**Về bản quyền:** Nếu transcript từ video của người khác, chỉ dùng làm tham khảo cấu trúc — không sao chép nguyên văn. Script mới phải được viết lại hoàn toàn bằng ngôn ngữ của mình.

**Về độ dài:** Script thường dài hơn transcript 2-3 lần (do thêm ví dụ, mở rộng luận điểm). TTS Script thường ngắn hơn Script 10-20% (do cắt bỏ ghi chú đạo diễn và rút gọn câu).

**Về tool TTS:** Mỗi tool có quirk riêng:
- ElevenLabs: Hỗ trợ SSML tags `<break time="1s"/>` cho pause chính xác hơn
- FPT AI Voice: Không hỗ trợ SSML — dùng dấu câu thuần
- Murf: Có UI chỉnh pause trực tiếp — TTS script có thể đơn giản hơn
